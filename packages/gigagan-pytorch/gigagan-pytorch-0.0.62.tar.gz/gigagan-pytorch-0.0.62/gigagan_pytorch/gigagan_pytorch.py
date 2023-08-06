from collections import namedtuple
from pathlib import Path
from math import log2, sqrt
from functools import partial

import torch
import torch.nn.functional as F
from torch.optim import Adam
from torch import nn, einsum, Tensor
from torch.autograd import grad as torch_grad
from torch.utils.data import DataLoader

from beartype import beartype
from beartype.typing import List, Optional, Tuple, Dict, Union, Iterable

from einops import rearrange, pack, unpack, repeat, reduce
from einops.layers.torch import Rearrange, Reduce

from ema_pytorch import EMA

from gigagan_pytorch.version import __version__
from gigagan_pytorch.open_clip import OpenClipAdapter

from tqdm import tqdm

# helpers

def exists(val):
    return val is not None

def default(*vals):
    for val in vals:
        if exists(val):
            return val
    return None

def is_power_of_two(n):
    return log2(n).is_integer()

def safe_unshift(arr):
    if len(arr) == 0:
        return None
    return arr.pop(0)

def divisible_by(numer, denom):
    return (numer % denom) == 0

def is_unique(arr):
    return len(set(arr)) == len(arr)

def cycle(dl):
    while True:
        for data in dl:
            yield data

# activation functions

def leaky_relu(neg_slope = 0.1):
    return nn.LeakyReLU(neg_slope)

def conv2d_3x3(dim_in, dim_out):
    return nn.Conv2d(dim_in, dim_out, 3, padding = 1)

# tensor helpers

def log(t, eps = 1e-20):
    return t.clamp(min = eps).log()

def gradient_penalty(
    images,
    outputs,
    grad_output_weights = None,
    weight = 10
):
    if not isinstance(outputs, (list, tuple)):
        outputs = [outputs]

    if not exists(grad_output_weights):
        grad_output_weights = (1,) * len(outputs)

    gradients, *_ = torch_grad(
        outputs = outputs,
        inputs = images,
        grad_outputs = [(torch.ones_like(output) * weight) for output, weight in zip(outputs, grad_output_weights)],
        create_graph = True,
        retain_graph = True,
        only_inputs = True
    )

    gradients = rearrange(gradients, 'b ... -> b (...)')
    return weight * ((gradients.norm(2, dim = 1) - 1) ** 2).mean()

# hinge gan losses

def generator_hinge_loss(fake):
    return fake.mean()

def discriminator_hinge_loss(real, fake):
    return (F.relu(1 + real) + F.relu(1 - fake)).mean()

# auxiliary losses

def aux_matching_loss(real, fake):
    return log(1 + real.exp()) + log(1 + fake.exp())

@beartype
def aux_clip_loss(
    clip: OpenClipAdapter,
    images: Tensor,
    texts: Optional[List[str]] = None,
    text_embeds: Optional[Tensor] = None
):
    assert exists(texts) ^ exists(text_embeds)

    if exists(texts):
        text_embeds = clip.embed_texts(texts)

    return clip.contrastive_loss(images = images, text_embeds = text_embeds)

# rmsnorm (newer papers show mean-centering in layernorm not necessary)

class ChannelRMSNorm(nn.Module):
    def __init__(self, dim):
        super().__init__()
        self.scale = dim ** 0.5
        self.gamma = nn.Parameter(torch.ones(dim, 1, 1))

    def forward(self, x):
        normed = F.normalize(x, dim = 1)
        return normed * self.scale * self.gamma

class RMSNorm(nn.Module):
    def __init__(self, dim):
        super().__init__()
        self.scale = dim ** 0.5
        self.gamma = nn.Parameter(torch.ones(dim))

    def forward(self, x):
        normed = F.normalize(x, dim = -1)
        return normed * self.scale * self.gamma

# down and upsample

class Upsample(nn.Module):
    def __init__(self, dim):
        super().__init__()
        conv = nn.Conv2d(dim, dim * 4, 1)

        self.net = nn.Sequential(
            conv,
            nn.SiLU(),
            nn.PixelShuffle(2)
        )

        self.init_conv_(conv)

    def init_conv_(self, conv):
        o, i, h, w = conv.weight.shape
        conv_weight = torch.empty(o // 4, i, h, w)
        nn.init.kaiming_uniform_(conv_weight)
        conv_weight = repeat(conv_weight, 'o ... -> (o 4) ...')

        conv.weight.data.copy_(conv_weight)
        nn.init.zeros_(conv.bias.data)

    def forward(self, x):
        return self.net(x)

def Downsample(dim):
    return nn.Sequential(
        Rearrange('b c (h s1) (w s2) -> b (c s1 s2) h w', s1 = 2, s2 = 2),
        nn.Conv2d(dim * 4, dim, 1)
    )

# skip layer excitation

def SqueezeExcite(dim, dim_out, reduction = 4, dim_min = 32):
    dim_hidden = max(dim_out // reduction, dim_min)

    return nn.Sequential(
        Reduce('b c h w -> b c', 'mean'),
        nn.Linear(dim, dim_hidden),
        nn.SiLU(),
        nn.Linear(dim_hidden, dim_out),
        nn.Sigmoid(),
        Rearrange('b c -> b c 1 1')
    )

# adaptive conv
# the main novelty of the paper - they propose to learn a softmax weighted sum of N convolutional kernels, depending on the text embedding

def get_same_padding(size, kernel, dilation, stride):
    return ((size - 1) * (stride - 1) + dilation * (kernel - 1)) // 2

class AdaptiveConv2DMod(nn.Module):
    def __init__(
        self,
        dim,
        dim_out,
        kernel,
        *,
        demod = True,
        stride = 1,
        dilation = 1,
        eps = 1e-8,
        num_conv_kernels = 1 # set this to be greater than 1 for adaptive
    ):
        super().__init__()
        self.eps = eps

        self.dim_out = dim_out

        self.kernel = kernel
        self.stride = stride
        self.dilation = dilation
        self.adaptive = num_conv_kernels > 1

        self.weights = nn.Parameter(torch.randn((num_conv_kernels, dim_out, dim, kernel, kernel)))

        self.demod = demod

        nn.init.kaiming_normal_(self.weights, a = 0, mode = 'fan_in', nonlinearity = 'leaky_relu')

    def forward(
        self,
        fmap,
        mod: Optional[Tensor] = None,
        kernel_mod: Optional[Tensor] = None
    ):
        """
        notation

        b - batch
        n - convs
        o - output
        i - input
        k - kernel
        """

        b, h = fmap.shape[0], fmap.shape[-2]

        weights = self.weights

        if self.adaptive:
            weights = repeat(weights, '... -> b ...', b = b)

            # determine an adaptive weight and 'select' the kernel to use with softmax

            assert exists(kernel_mod)

            kernel_attn = kernel_mod.softmax(dim = -1)
            kernel_attn = rearrange(kernel_attn, 'b n -> b n 1 1 1 1')

            weights = reduce(weights * kernel_attn, 'b n ... -> b ...', 'sum')

        # do the modulation, demodulation, as done in stylegan2

        mod = rearrange(mod, 'b i -> b 1 i 1 1')

        weights = weights * (mod + 1)

        if self.demod:
            inv_norm = reduce(weights ** 2, 'b o i k1 k2 -> b o 1 1 1', 'sum').clamp(min = self.eps).rsqrt()
            weights = weights * inv_norm

        fmap = rearrange(fmap, 'b c h w -> 1 (b c) h w')

        weights = rearrange(weights, 'b o ... -> (b o) ...')

        padding = get_same_padding(h, self.kernel, self.dilation, self.stride)
        fmap = F.conv2d(fmap, weights, padding = padding, groups = b)

        return rearrange(fmap, '1 (b o) ... -> b o ...', b = b)

# attention
# they use an attention with a better Lipchitz constant - l2 distance similarity instead of dot product - also shared query / key space - shown in vitgan to be more stable
# not sure what they did about token attention to self, so masking out, as done in some other papers using shared query / key space

class SelfAttention(nn.Module):
    def __init__(
        self,
        dim,
        dim_head = 64,
        heads = 8,
        dot_product = False
    ):
        super().__init__()
        self.heads = heads
        self.scale = dim_head ** -0.5
        dim_inner = dim_head * heads

        self.dot_product = dot_product

        self.norm = ChannelRMSNorm(dim)

        self.to_q = nn.Conv2d(dim, dim_inner, 1, bias = False)
        self.to_k = nn.Conv2d(dim, dim_inner, 1, bias = False) if dot_product else None
        self.to_v = nn.Conv2d(dim, dim_inner, 1, bias = False)

        self.null_kv = nn.Parameter(torch.randn(2, heads, dim_head))

        self.to_out = nn.Conv2d(dim_inner, dim, 1, bias = False)

    def forward(self, fmap):
        """
        einstein notation

        b - batch
        h - heads
        x - height
        y - width
        d - dimension
        i - source seq (attend from)
        j - target seq (attend to)
        """
        batch = fmap.shape[0]

        fmap = self.norm(fmap)

        x, y = fmap.shape[-2:]

        h = self.heads

        q, v = self.to_q(fmap), self.to_v(fmap)

        k = self.to_k(fmap) if exists(self.to_k) else q

        q, k, v = map(lambda t: rearrange(t, 'b (h d) x y -> (b h) (x y) d', h = self.heads), (q, k, v))

        # add a null key / value, so network can choose to pay attention to nothing

        nk, nv = map(lambda t: repeat(t, 'h d -> (b h) 1 d', b = batch), self.null_kv)

        k = torch.cat((nk, k), dim = -2)
        v = torch.cat((nv, v), dim = -2)

        # l2 distance or dot product

        if self.dot_product:
            sim = einsum('b i d, b j d -> b i j', q, k)
        else:
            # using pytorch cdist leads to nans in lightweight gan training framework, at least
            q_squared = (q * q).sum(dim = -1)
            k_squared = (k * k).sum(dim = -1)
            l2dist_squared = rearrange(q_squared, 'b i -> b i 1') + rearrange(k_squared, 'b j -> b 1 j') - 2 * einsum('b i d, b j d -> b i j', q, k) # hope i'm mathing right
            sim = -l2dist_squared

        # scale

        sim = sim * self.scale

        # attention

        attn = sim.softmax(dim = -1)

        out = einsum('b i j, b j d -> b i d', attn, v)

        out = rearrange(out, '(b h) (x y) d -> b (h d) x y', x = x, y = y, h = h)

        return self.to_out(out)

class CrossAttention(nn.Module):
    def __init__(
        self,
        dim,
        dim_context,
        dim_head = 64,
        heads = 8
    ):
        super().__init__()
        self.heads = heads
        self.scale = dim_head ** -0.5
        dim_inner = dim_head * heads
        kv_input_dim = default(dim_context, dim)

        self.norm = ChannelRMSNorm(dim)
        self.norm_context = RMSNorm(kv_input_dim)

        self.to_q = nn.Conv2d(dim, dim_inner, 1, bias = False)
        self.to_kv = nn.Linear(kv_input_dim, dim_inner * 2, bias = False)
        self.to_out = nn.Conv2d(dim_inner, dim, 1, bias = False)

    def forward(self, fmap, context, mask = None):
        """
        einstein notation

        b - batch
        h - heads
        x - height
        y - width
        d - dimension
        i - source seq (attend from)
        j - target seq (attend to)
        """

        fmap = self.norm(fmap)
        context = self.norm_context(context)

        x, y = fmap.shape[-2:]

        h = self.heads

        q, k, v = (self.to_q(fmap), *self.to_kv(context).chunk(2, dim = -1))

        k, v = map(lambda t: rearrange(t, 'b n (h d) -> (b h) n d', h = h), (k, v))

        q = rearrange(q, 'b (h d) x y -> (b h) (x y) d', h = self.heads)

        sim = einsum('b i d, b j d -> b i j', q, k) * self.scale

        if exists(mask):
            mask = repeat(mask, 'b j -> (b h) 1 j', h = self.heads)
            sim = sim.masked_fill(~mask, -torch.finfo(sim.dtype).max)

        attn = sim.softmax(dim = -1)

        out = einsum('b i j, b j d -> b i d', attn, v)

        out = rearrange(out, '(b h) (x y) d -> b (h d) x y', x = x, y = y, h = h)

        return self.to_out(out)

# classic transformer attention, stick with l2 distance

class TextAttention(nn.Module):
    def __init__(
        self,
        dim,
        dim_head = 64,
        heads = 8
    ):
        super().__init__()
        self.heads = heads
        self.scale = dim_head ** -0.5
        dim_inner = dim_head * heads

        self.norm = RMSNorm(dim)
        self.to_qkv = nn.Linear(dim, dim_inner * 3, bias = False)

        self.null_kv = nn.Parameter(torch.randn(2, heads, dim_head))

        self.to_out = nn.Linear(dim_inner, dim, bias = False)

    def forward(self, encodings, mask = None):
        """
        einstein notation

        b - batch
        h - heads
        x - height
        y - width
        d - dimension
        i - source seq (attend from)
        j - target seq (attend to)
        """
        batch = encodings.shape[0]

        encodings = self.norm(encodings)

        h = self.heads

        q, k, v = self.to_qkv(encodings).chunk(3, dim = -1)
        q, k, v = map(lambda t: rearrange(t, 'b n (h d) -> (b h) n d', h = self.heads), (q, k, v))

        # add a null key / value, so network can choose to pay attention to nothing

        nk, nv = map(lambda t: repeat(t, 'h d -> (b h) 1 d', b = batch), self.null_kv)

        k = torch.cat((nk, k), dim = -2)
        v = torch.cat((nv, v), dim = -2)

        sim = einsum('b i d, b j d -> b i j', q, k) * self.scale

        # key padding mask

        if exists(mask):
            mask = F.pad(mask, (1, 0), value = True)
            mask = repeat(mask, 'b n -> (b h) 1 n', h = h)
            sim = sim.masked_fill(~mask, -torch.finfo(sim.dtype).max)

        # attention

        attn = sim.softmax(dim = -1)
        out = einsum('b i j, b j d -> b i d', attn, v)

        out = rearrange(out, '(b h) n d -> b n (h d)', h = h)

        return self.to_out(out)

# feedforward

def FeedForward(
    dim,
    mult = 4,
    channel_first = False
):
    dim_hidden = int(dim * mult)
    norm_klass = ChannelRMSNorm if channel_first else RMSNorm
    proj = partial(nn.Conv2d, kernel_size = 1) if channel_first else nn.Linear

    return nn.Sequential(
        norm_klass(dim),
        proj(dim, dim_hidden),
        nn.GELU(),
        proj(dim_hidden, dim)
    )

# different types of transformer blocks or transformers (multiple blocks)

class SelfAttentionBlock(nn.Module):
    def __init__(
        self,
        dim,
        dim_head = 64,
        heads = 8,
        ff_mult = 4,
        dot_product = False
    ):
        super().__init__()
        self.attn = SelfAttention(dim = dim, dim_head = dim_head, heads = heads, dot_product = dot_product)
        self.ff = FeedForward(dim = dim, mult = ff_mult, channel_first = True)

    def forward(self, x):
        x = self.attn(x) + x
        x = self.ff(x) + x
        return x

class CrossAttentionBlock(nn.Module):
    def __init__(
        self,
        dim,
        dim_context,
        dim_head = 64,
        heads = 8,
        ff_mult = 4
    ):
        super().__init__()
        self.attn = CrossAttention(dim = dim, dim_context = dim_context, dim_head = dim_head, heads = heads)
        self.ff = FeedForward(dim = dim, mult = ff_mult, channel_first = True)

    def forward(self, x, context, mask = None):
        x = self.attn(x, context = context, mask = mask) + x
        x = self.ff(x) + x
        return x

class Transformer(nn.Module):
    def __init__(
        self,
        dim,
        depth,
        dim_head = 64,
        heads = 8,
        ff_mult = 4
    ):
        super().__init__()
        self.layers = nn.ModuleList([])
        for _ in range(depth):
            self.layers.append(nn.ModuleList([
                TextAttention(dim = dim, dim_head = dim_head, heads = heads),
                FeedForward(dim = dim, mult = ff_mult)
            ]))

        self.norm = RMSNorm(dim)

    def forward(self, x, mask = None):
        for attn, ff in self.layers:
            x = attn(x, mask = mask) + x
            x = ff(x) + x

        return self.norm(x)

# text encoder

class TextEncoder(nn.Module):
    @beartype
    def __init__(
        self,
        *,
        dim,
        depth,
        clip: Optional[OpenClipAdapter] = None,
        dim_head = 64,
        heads = 8,
    ):
        super().__init__()
        self.dim = dim

        if not exists(clip):
            clip = OpenClipAdapter()

        self.clip = clip
        self.learned_global_token = nn.Parameter(torch.randn(dim))

        self.project_in = nn.Linear(clip.dim_latent, dim) if clip.dim_latent != dim else nn.Identity()

        self.transformer = Transformer(
            dim = dim,
            depth = depth,
            dim_head = dim_head,
            heads = heads
        )

    @beartype
    def forward(
        self,
        texts: Optional[List[str]] = None,
        text_encodings: Optional[Tensor] = None
    ):
        assert exists(texts) ^ exists(text_encodings)

        if not exists(text_encodings):
            with torch.no_grad():
                self.clip.eval()
                _, text_encodings = self.clip.embed_texts(texts)

        mask = (text_encodings != 0.).any(dim = -1)

        text_encodings = self.project_in(text_encodings)

        mask_with_global = F.pad(mask, (1, 0), value = True)

        batch = text_encodings.shape[0]
        global_tokens = repeat(self.learned_global_token, 'd -> b d', b = batch)

        text_encodings, ps = pack([global_tokens, text_encodings], 'b * d')

        text_encodings = self.transformer(text_encodings, mask = mask_with_global)

        global_tokens, text_encodings = unpack(text_encodings, ps, 'b * d')

        return global_tokens, text_encodings, mask

# style mapping network

class EqualLinear(nn.Module):
    def __init__(
        self,
        dim,
        dim_out,
        lr_mul = 1,
        bias = True
    ):
        super().__init__()
        self.weight = nn.Parameter(torch.randn(dim_out, dim))
        if bias:
            self.bias = nn.Parameter(torch.zeros(dim_out))

        self.lr_mul = lr_mul

    def forward(self, input):
        return F.linear(input, self.weight * self.lr_mul, bias=self.bias * self.lr_mul)

class StyleNetwork(nn.Module):
    def __init__(
        self,
        dim,
        depth,
        lr_mul = 0.1,
        dim_text_latent = 0
    ):
        super().__init__()
        self.dim = dim
        self.dim_text_latent = dim_text_latent

        layers = []
        for i in range(depth):
            is_first = i == 0
            dim_in = (dim + dim_text_latent) if is_first else dim

            layers.extend([EqualLinear(dim_in, dim, lr_mul), leaky_relu()])

        self.net = nn.Sequential(*layers)

    def forward(
        self,
        x,
        text_latent = None
    ):
        x = F.normalize(x, dim = 1)

        if self.dim_text_latent > 0:
            assert exists(text_latent)
            x = torch.cat((x, text_latent), dim = -1)

        return self.net(x)

# generator

class BaseGenerator(nn.Module):
    pass

class Generator(BaseGenerator):
    @beartype
    def __init__(
        self,
        *,
        dim,
        image_size,
        dim_max = 2048,
        capacity = 16,
        channels = 3,
        style_network: Optional[Union[StyleNetwork, Dict]] = None,
        style_network_dim = None,
        text_encoder: Optional[Union[TextEncoder, Dict]] = None,
        dim_latent = 512,
        self_attn_resolutions: Tuple[int, ...] = (32, 16),
        self_attn_dim_head = 64,
        self_attn_heads = 8,
        self_attn_dot_product = True,
        self_ff_mult = 4,
        cross_attn_resolutions: Tuple[int, ...] = (32, 16),
        cross_attn_dim_head = 64,
        cross_attn_heads = 8,
        cross_ff_mult = 4,
        num_conv_kernels = 2,  # the number of adaptive conv kernels
        num_skip_layers_excite = 0,
        unconditional = False
    ):
        super().__init__()
        self.dim = dim
        self.channels = channels

        if isinstance(style_network, dict):
            style_network = StyleNetwork(**style_network)

        self.style_network = style_network

        assert exists(style_network) ^ exists(style_network_dim), 'style_network_dim must be given to the generator if StyleNetwork not passed in as style_network'

        if not exists(style_network_dim):
            style_network_dim = style_network.dim

        self.style_network_dim = style_network_dim

        if isinstance(text_encoder, dict):
            text_encoder = TextEncoder(**text_encoder)

        self.text_encoder = text_encoder

        self.unconditional = unconditional

        assert not (unconditional and exists(text_encoder))
        assert not (unconditional and exists(style_network) and style_network.dim_text_latent > 0)
        assert unconditional or (exists(text_encoder) and text_encoder.dim == style_network.dim_text_latent), 'the `dim_text_latent` on your StyleNetwork must be equal to the `dim` set for the TextEncoder'

        assert is_power_of_two(image_size)
        num_layers = int(log2(image_size) - 1)
        self.num_layers = num_layers

        # generator requires convolutions conditioned by the style vector
        # and also has N convolutional kernels adaptively selected (one of the only novelties of the paper)

        is_adaptive = num_conv_kernels > 1
        dim_kernel_mod = num_conv_kernels if is_adaptive else 0

        style_embed_split_dims = []

        adaptive_conv = partial(AdaptiveConv2DMod, kernel = 3, num_conv_kernels = num_conv_kernels)

        # initial 4x4 block and conv

        self.init_block = nn.Parameter(torch.randn(dim_latent, 4, 4))
        self.init_conv = adaptive_conv(dim_latent, dim_latent)

        style_embed_split_dims.extend([
            dim_latent,
            dim_kernel_mod
        ])

        # main network

        num_layers = int(log2(image_size) - 1)
        self.num_layers = num_layers

        resolutions = image_size / ((2 ** torch.arange(num_layers)))
        resolutions = resolutions.long().tolist()

        dim_layers = (2 ** (torch.arange(num_layers) + 1)) * capacity
        dim_layers.clamp_(max = dim_max)

        dim_layers = torch.flip(dim_layers, (0,))
        dim_layers = F.pad(dim_layers, (1, 0), value = dim_latent)

        dim_layers = dim_layers.tolist()
        dim_layers[-1]
        dim_pairs = list(zip(dim_layers[:-1], dim_layers[1:]))

        self.num_skip_layers_excite = num_skip_layers_excite

        self.layers = nn.ModuleList([])

        # go through layers and construct all parameters

        for ind, ((dim_in, dim_out), resolution) in enumerate(zip(dim_pairs, resolutions)):
            is_last = (ind + 1) == len(dim_pairs)
            should_upsample = not is_last
            should_skip_layer_excite = num_skip_layers_excite > 0 and (ind + num_skip_layers_excite) < len(dim_pairs)

            has_self_attn = resolution in self_attn_resolutions
            has_cross_attn = resolution in cross_attn_resolutions and not unconditional

            skip_squeeze_excite = None
            if should_skip_layer_excite:
                dim_skip_in, _ = dim_pairs[ind + num_skip_layers_excite]
                skip_squeeze_excite = SqueezeExcite(dim_in, dim_skip_in)

            resnet_block = nn.ModuleList([
                adaptive_conv(dim_in, dim_out),
                leaky_relu(),
                adaptive_conv(dim_out, dim_out),
                leaky_relu()
            ])

            to_rgb = adaptive_conv(dim_out, channels)

            self_attn = cross_attn = rgb_upsample = upsample = None

            if should_upsample:
                upsample = Upsample(dim_out)
                rgb_upsample = Upsample(channels)

            if has_self_attn:
                self_attn = SelfAttentionBlock(dim_out, dot_product = self_attn_dot_product)

            if has_cross_attn:
                cross_attn = CrossAttentionBlock(dim_out, dim_context = text_encoder.dim)

            style_embed_split_dims.extend([
                dim_in,             # for first conv in resnet block
                dim_kernel_mod,     # first conv kernel selection
                dim_out,            # second conv in resnet block
                dim_kernel_mod,     # second conv kernel selection
                dim_out,            # to RGB conv
                dim_kernel_mod,     # RGB conv kernel selection
            ])

            self.layers.append(nn.ModuleList([
                skip_squeeze_excite,
                resnet_block,
                to_rgb,
                self_attn,
                cross_attn,
                upsample,
                rgb_upsample
            ]))

        # determine the projection of the style embedding to convolutional modulation weights (+ adaptive kernel selection weights) for all layers

        self.style_to_conv_modulations = nn.Linear(style_network_dim, sum(style_embed_split_dims))
        self.style_embed_split_dims = style_embed_split_dims

        self.apply(self.init_)

    def init_(self, m):
        if type(m) in {nn.Conv2d, nn.Linear}:
            nn.init.kaiming_normal_(m.weight, a = 0, mode = 'fan_in', nonlinearity = 'leaky_relu')

    @property
    def device(self):
        return next(self.parameters()).device

    @beartype
    def forward(
        self,
        styles = None,
        noise = None,
        texts: Optional[List[str]] = None,
        global_text_tokens = None,
        fine_text_tokens = None,
        text_mask = None,
        batch_size = 1,
        return_all_rgbs = False
    ):
        # take care of text encodings
        # which requires global text tokens to adaptively select the kernels from the main contribution in the paper
        # and fine text tokens to attend to using cross attention

        if not self.unconditional:
            if exists(texts):
                assert exists(self.text_encoder)
                global_text_tokens, fine_text_tokens, text_mask = self.text_encoder(texts)
            else:
                assert all([*map(exists, (global_text_tokens, fine_text_tokens, text_mask))]), 'raw text or text embeddings were not passed in for conditional training'
        else:
            assert not any([*map(exists, (texts, global_text_tokens, fine_text_tokens))])

        # determine styles

        if not exists(styles):
            assert exists(self.style_network)

            if not exists(noise):
                noise = torch.randn((batch_size, self.style_network_dim), device = self.device)

            styles = self.style_network(noise, global_text_tokens)

        # project styles to conv modulations

        conv_mods = self.style_to_conv_modulations(styles)
        conv_mods = conv_mods.split(self.style_embed_split_dims, dim = -1)
        conv_mods = iter(conv_mods)

        # prepare initial block

        batch_size = styles.shape[0]

        x = repeat(self.init_block, 'c h w -> b c h w', b = batch_size)
        x = self.init_conv(x, mod = next(conv_mods), kernel_mod = next(conv_mods))

        rgb = torch.zeros((batch_size, self.channels, 4, 4), device = self.device, dtype = x.dtype)

        # skip layer squeeze excitations

        excitations = [None] * self.num_skip_layers_excite

        # all the rgb's of each layer of the generator is to be saved for multi-resolution input discrimination

        rgbs = []

        # main network

        for squeeze_excite, (resnet_conv1, act1, resnet_conv2, act2), to_rgb_conv, self_attn, cross_attn, upsample, upsample_rgb in self.layers:

            if exists(squeeze_excite):
                skip_excite = squeeze_excite(x)
                excitations.append(skip_excite)

            excite = safe_unshift(excitations)
            if exists(excite):
                x = x * excite

            x = resnet_conv1(x, mod = next(conv_mods), kernel_mod = next(conv_mods))
            x = act1(x)
            x = resnet_conv2(x, mod = next(conv_mods), kernel_mod = next(conv_mods))
            x = act2(x)

            if exists(self_attn):
                x = self_attn(x)

            if exists(cross_attn):
                x = cross_attn(x, context = fine_text_tokens, mask = text_mask)

            layer_rgb = to_rgb_conv(x, mod = next(conv_mods), kernel_mod = next(conv_mods))

            rgb = rgb + layer_rgb

            rgbs.append(rgb)

            if exists(upsample):
                x = upsample(x)

            if exists(upsample_rgb):
                rgb = upsample_rgb(rgb)

        if return_all_rgbs:
            return rgb, rgbs

        return rgb

# discriminator

@beartype
class SimpleDecoder(nn.Module):
    def __init__(
        self,
        dim,
        *,
        dims: Tuple[int, ...],
        patch_dim: int = 1,
        frac_patches: float = 1.
    ):
        super().__init__()
        assert 0 < frac_patches <= 1.

        self.patch_dim = patch_dim
        self.frac_patches = frac_patches

        dims = [dim, *dims]

        layers = [conv2d_3x3(dim, dim)]

        for dim_in, dim_out in zip(dims[:-1], dims[1:]):
            layers.append(nn.Sequential(
                Upsample(dim_in),
                conv2d_3x3(dim_in, dim_out * 2),
                nn.GLU(dim = 1)
            ))

        self.net = nn.Sequential(*layers)

    @property
    def device(self):
        return next(self.parameters()).device

    def forward(
        self,
        fmap,
        orig_image
    ):
        if self.frac_patches < 1.:
            batch, patch_dim = fmap.shape[0], self.patch_dim
            fmap_size, img_size = fmap.shape[-1], orig_image.shape[-1]

            assert divisible_by(fmap_size, patch_dim), f'feature map dimensions are {fmap_size}, but the patch dim was designated to be {patch_dim}'
            assert divisible_by(img_size, patch_dim), f'image size is {img_size} but the patch dim was specified to be {patch_dim}'

            fmap, orig_image = map(lambda t: rearrange(t, 'b c (p1 h) (p2 w) -> b (p1 p2) c h w', p1 = patch_dim, p2 = patch_dim), (fmap, orig_image))

            total_patches = patch_dim ** 2
            num_patches_recon = max(int(self.frac_patches * total_patches), 1)

            batch_arange = torch.arange(batch, device = self.device)[..., None]
            batch_randperm = torch.randn((batch, total_patches)).sort(dim = -1).indices
            patch_indices = batch_randperm[..., :num_patches_recon]

            fmap, orig_image = map(lambda t: t[batch_arange, patch_indices], (fmap, orig_image))
            fmap, orig_image = map(lambda t: rearrange(t, 'b p ... -> (b p) ...'), (fmap, orig_image))

        recon = self.net(fmap)
        return F.mse_loss(recon, orig_image)

class RandomFixedProjection(nn.Module):
    def __init__(
        self,
        dim,
        dim_out,
        channel_first = True
    ):
        super().__init__()
        weights = torch.randn(dim, dim_out)
        nn.init.kaiming_normal_(weights, mode = 'fan_out', nonlinearity = 'linear')

        self.channel_first = channel_first
        self.register_buffer('fixed_weights', weights)

    def forward(self, x):
        if not self.channel_first:
            return x @ self.fixed_weights

        return einsum('b c ..., c d -> b d ...', x, self.fixed_weights)

class VisionAidedDiscriminator(nn.Module):
    """ the vision-aided gan loss """
    def __init__(
        self,
        *,
        clip: OpenClipAdapter,
        depth = 2,
        dim_head = 64,
        heads = 8,
        layer_indices = (-1, -2, -3),
        conv_dim = None,
        text_dim = None,
        unconditional = False,
        num_conv_kernels = 2
    ):
        super().__init__()
        self.clip = clip
        dim = clip._dim_image_latent

        self.unconditional = unconditional
        text_dim = default(text_dim, dim)
        conv_dim = default(conv_dim, dim)

        self.layer_discriminators = nn.ModuleList([])
        self.layer_indices = layer_indices

        conv_klass = partial(AdaptiveConv2DMod, kernel = 3, num_conv_kernels = num_conv_kernels) if not unconditional else conv2d_3x3

        for _ in layer_indices:
            self.layer_discriminators.append(nn.ModuleList([
                RandomFixedProjection(dim, conv_dim),
                conv_klass(conv_dim, conv_dim),
                nn.Linear(text_dim, conv_dim) if not unconditional else None,
                nn.Linear(text_dim, num_conv_kernels) if not unconditional else None,
                nn.Sequential(
                    conv2d_3x3(conv_dim, 1),
                    Rearrange('b 1 ... -> b ...')
                )
            ]))

    def parameters(self):
        return [
            *self.network.parameters(),
            *self.to_pred.parameters()
        ]

    def forward(
        self,
        images,
        text_embeds = None
    ):
        with torch.no_grad():
            self.clip.eval()
            _, image_encodings = self.clip.embed_images(images)
            image_encodings = image_encodings.detach()

        logits = []
        for layer_index, (rand_proj, conv, to_conv_mod, to_conv_kernel_mod, to_logits) in zip(self.layer_indices, self.layer_discriminators):
            image_encoding = image_encodings[layer_index]

            cls_token, rest_tokens = image_encoding[:, :1], image_encoding[:, 1:]
            height_width = int(sqrt(rest_tokens.shape[-2])) # assume square

            img_fmap = rearrange(rest_tokens, 'b (h w) d -> b d h w', h = height_width)

            img_fmap = img_fmap + rearrange(cls_token, 'b 1 d -> b d 1 1 ') # pool the cls token into the rest of the tokens
            img_fmap = rand_proj(img_fmap)

            if self.unconditional:
                img_fmap = conv(img_fmap)
            else:
                assert exists(text_embeds)

                img_fmap = conv(
                    img_fmap,
                    mod = to_conv_mod(text_embeds),
                    kernel_mod = to_conv_kernel_mod(text_embeds)
                )

            layer_logits = to_logits(img_fmap)

            logits.append(layer_logits)

        return logits

class Predictor(nn.Module):
    def __init__(
        self,
        dim,
        depth = 4,
        num_conv_kernels = 2,
        unconditional = False
    ):
        super().__init__()
        self.unconditional = unconditional
        self.residual_fn = nn.Conv2d(dim, dim, 1)
        self.layers = nn.ModuleList([])

        klass = nn.Conv2d if unconditional else partial(AdaptiveConv2DMod, num_conv_kernels = num_conv_kernels)

        for ind in range(depth):
            self.layers.append(klass(dim, dim, 1))

        self.to_logits = nn.Conv2d(dim, 1, 1)

    def forward(
        self,
        x,
        mod = None,
        kernel_mod = None
    ):
        residual = self.residual_fn(x)

        for layer in self.layers:
            kwargs = dict()
            if not self.unconditional:
                kwargs = dict(mod = mod, kernel_mod = kernel_mod)

            x = layer(x, **kwargs)

        x = x + residual
        return self.to_logits(x)

class Discriminator(nn.Module):
    @beartype
    def __init__(
        self,
        *,
        dim,
        image_size,
        capacity = 16,
        dim_max = 2048,
        channels = 3,
        attn_resolutions: Tuple[int, ...] = (32, 16),
        attn_dim_head = 64,
        attn_heads = 8,
        self_attn_dot_product = False,
        ff_mult = 4,
        text_encoder: Optional[Union[TextEncoder, Dict]] = None,
        text_dim = None,
        multiscale_input_resolutions: Tuple[int, ...] = (64, 32, 16, 8),
        multiscale_output_resolutions: Tuple[int, ...] = (32, 16, 8, 4),
        aux_recon_resolutions: Tuple[int, ...] = (8,),
        aux_recon_patch_dims: Tuple[int, ...] = (2,),
        aux_recon_frac_patches: Tuple[float, ...] = (0.25,),
        aux_recon_frac_batch_scales: Tuple[float, ...] = (0.25,),
        resize_mode = 'bilinear',
        num_conv_kernels = 2,
        num_skip_layers_excite = 0,
        unconditional = False,
        scale_invariant_training = True
    ):
        super().__init__()
        self.unconditional = unconditional
        assert not (unconditional and exists(text_encoder))

        assert is_power_of_two(image_size)
        assert all([*map(is_power_of_two, attn_resolutions)])

        assert is_unique(multiscale_input_resolutions)
        assert all([*map(is_power_of_two, multiscale_input_resolutions)])
        assert all([*map(lambda t: t >= 4, multiscale_input_resolutions)])
        assert all([*map(lambda t: t < image_size, multiscale_input_resolutions)])

        self.multiscale_input_resolutions = multiscale_input_resolutions

        assert is_unique(multiscale_output_resolutions)
        assert all([*map(is_power_of_two, multiscale_output_resolutions)])
        assert all([*map(lambda t: t >= 4, multiscale_output_resolutions)])
        assert all([*map(lambda t: t < image_size, multiscale_output_resolutions)])

        if len(multiscale_input_resolutions) > 0 and len(multiscale_output_resolutions) > 0:
            assert max(multiscale_input_resolutions) > max(multiscale_output_resolutions)
            assert min(multiscale_input_resolutions) > min(multiscale_output_resolutions)

        self.multiscale_output_resolutions = multiscale_output_resolutions

        assert all([*map(is_power_of_two, aux_recon_resolutions)])
        assert all([*map(lambda t: 0 < t <= 1., aux_recon_frac_batch_scales)])
        assert len(aux_recon_resolutions) == len(aux_recon_patch_dims) == len(aux_recon_frac_patches) == len(aux_recon_frac_batch_scales)

        self.aux_recon_resolutions_to_patches = {resolution: (patch_dim, frac_patches) for resolution, patch_dim, frac_patches in zip(aux_recon_resolutions, aux_recon_patch_dims, aux_recon_frac_patches)}
        self.aux_recon_frac_batch_scales = aux_recon_frac_batch_scales

        self.resize_mode = resize_mode

        num_layers = int(log2(image_size) - 1)
        self.num_layers = num_layers
        self.image_size = image_size

        resolutions = image_size / ((2 ** torch.arange(num_layers)))
        resolutions = resolutions.long().tolist()

        dim_layers = (2 ** (torch.arange(num_layers) + 1)) * capacity
        dim_layers = F.pad(dim_layers, (1, 0), value = channels)
        dim_layers.clamp_(max = dim_max)

        dim_layers = dim_layers.tolist()
        dim_last = dim_layers[-1]
        dim_pairs = list(zip(dim_layers[:-1], dim_layers[1:]))

        self.num_skip_layers_excite = num_skip_layers_excite

        self.residual_scale = 2 ** -0.5
        self.layers = nn.ModuleList([])

        upsample_dims = []
        predictor_dims = []
        dim_kernel_attn = (num_conv_kernels if num_conv_kernels > 1 else 0)

        for ind, ((dim_in, dim_out), resolution) in enumerate(zip(dim_pairs, resolutions)):
            is_first = ind == 0
            is_last = (ind + 1) == len(dim_pairs)
            should_downsample = not is_last
            should_skip_layer_excite = not is_first and num_skip_layers_excite > 0 and (ind + num_skip_layers_excite) < len(dim_pairs)

            has_attn = resolution in attn_resolutions
            has_multiscale_input = resolution in multiscale_input_resolutions
            has_multiscale_output = resolution in multiscale_output_resolutions

            has_aux_recon_decoder = resolution in aux_recon_resolutions
            upsample_dims.insert(0, dim_in)

            skip_squeeze_excite = None
            if should_skip_layer_excite:
                dim_skip_in, _ = dim_pairs[ind + num_skip_layers_excite]
                skip_squeeze_excite = SqueezeExcite(dim_in, dim_skip_in)

            # multi-scale rgb input to feature dimension

            from_rgb = None
            if has_multiscale_input and scale_invariant_training:
                from_rgb = nn.Conv2d(channels, dim_in, 7, padding = 3)

            # dim in + channels for the main features

            dim_in = dim_in + (channels if has_multiscale_input else 0)

            # residual convolution

            residual_conv = nn.Conv2d(dim_in, dim_out, 1, stride = (2 if should_downsample else 1))

            # main resnet block

            resnet_block = nn.Sequential(
                conv2d_3x3(dim_in, dim_out),
                leaky_relu(),
                conv2d_3x3(dim_out, dim_out),
                leaky_relu()
            )

            # multi-scale output

            multiscale_output_predictor = None

            if has_multiscale_output:
                multiscale_output_predictor = Predictor(dim_out, num_conv_kernels = num_conv_kernels, unconditional = unconditional)
                predictor_dims.extend([dim_out, dim_kernel_attn])

            aux_recon_decoder = None

            if has_aux_recon_decoder:
                patch_dim, frac_patches = self.aux_recon_resolutions_to_patches[resolution]

                aux_recon_decoder = SimpleDecoder(
                    dim_out,
                    dims = tuple(upsample_dims),
                    patch_dim = patch_dim,
                    frac_patches = frac_patches
                )

            self.layers.append(nn.ModuleList([
                skip_squeeze_excite,
                from_rgb,
                resnet_block,
                residual_conv,
                SelfAttentionBlock(dim_out, heads = attn_heads, dim_head = attn_dim_head, ff_mult = ff_mult, dot_product = self_attn_dot_product) if has_attn else None,
                multiscale_output_predictor,
                aux_recon_decoder,
                Downsample(dim_out) if should_downsample else None,
            ]))

        self.to_logits = nn.Sequential(
            conv2d_3x3(dim_last, dim_last),
            leaky_relu(),
            Rearrange('b c h w -> b (c h w)'),
            nn.Linear(dim_last * (4 ** 2), 1),
            Rearrange('b 1 -> b')
        )

        # take care of text conditioning in the multiscale predictor branches

        assert unconditional or (exists(text_dim) ^ exists(text_encoder))

        if not unconditional:
            if isinstance(text_encoder, dict):
                text_encoder = TextEncoder(**text_encoder)

            self.text_dim = default(text_dim, text_encoder.dim)

            self.predictor_dims = predictor_dims
            self.text_to_conv_conditioning = nn.Linear(self.text_dim, sum(predictor_dims)) if exists(self.text_dim) else None

        self.text_encoder = text_encoder

        self.apply(self.init_)

    def init_(self, m):
        if type(m) in {nn.Conv2d, nn.Linear}:
            nn.init.kaiming_normal_(m.weight, a = 0, mode = 'fan_in', nonlinearity = 'leaky_relu')

    def resize_image_to(self, images, resolution):
        return F.interpolate(images, resolution, mode = self.resize_mode)

    @property
    def device(self):
        return next(self.parameters()).device

    @beartype
    def forward(
        self,
        images,
        rgbs: Optional[List[Tensor]] = None,  # multi-resolution inputs (rgbs) from the generator
        texts: Optional[List[str]] = None,
        text_embeds = None,
        real_images = None,                   # if this were passed in, the network will automatically append the real to the presumably generated images passed in as the first argument, and generate all intermediate resolutions through resizing and concat appropriately
        return_all_aux_loss = False,          # this would return auxiliary reconstruction loss for both fake and real
        return_multiscale_outputs = True      # can force it not to return multi-scale logits
    ):
        if not self.unconditional:
            assert exists(texts) ^ exists(text_embeds)

            if exists(texts):
                assert exists(self.text_encoder)
                text_embeds, *_ = self.text_encoder(texts)

            assert exists(text_embeds), 'raw text or text embeddings were not passed into discriminator for conditional training'

            conv_mods = self.text_to_conv_conditioning(text_embeds).split(self.predictor_dims, dim = -1)
            conv_mods = iter(conv_mods)

        else:
            assert not any([*map(exists, (texts, text_embeds))])

        x = images

        assert x.shape[-2:] == (self.image_size, self.image_size)

        # if real images are passed in, assume `images` are generated, and take care of all the multi-resolution input. this can also be done externally, in which case `real_images` will not be populated

        has_real_images = exists(real_images)

        if has_real_images:
            split_batch_size = (x.shape[0], real_images.shape[0])
            x = torch.cat((x, real_images), dim = 0)

        batch = x.shape[0]

        aux_recon_target = real_images if has_real_images else x

        assert not (has_real_images and not exists(rgbs)) 

        if has_real_images:
            rgbs = [torch.cat((rgb, self.resize_image_to(real_images, rgb.shape[-1])), dim = 0) for rgb in rgbs]

        # index the rgbs by resolution

        rgbs_index = {t.shape[-1]: t for t in rgbs} if exists(rgbs) else {}

        # hold multiscale outputs

        multiscale_outputs = []

        # hold auxiliary recon losses

        aux_recon_losses = []
        iter_aux_recon_frac = iter(self.aux_recon_frac_batch_scales)

        # excitations

        excitations = [None] * (self.num_skip_layers_excite + 1) # +1 since first image in pixel space is not excited

        for squeeze_excite, from_rgb, block, residual_fn, attn, predictor, recon_decoder, downsample in self.layers:
            resolution = x.shape[-1]

            if exists(squeeze_excite):
                skip_excite = squeeze_excite(x)
                excitations.append(skip_excite)

            excite = safe_unshift(excitations)

            if exists(excite):
                excite = repeat(excite, 'b ... -> (s b) ...', s = x.shape[0] // excite.shape[0])
                x = x * excite

            if resolution in self.multiscale_input_resolutions:
                images_to_concat = rgbs_index.get(resolution, None)

                # if no rgbs passed in, assume all real images, and just resize, though realistically you would concat fake and real images together using helper function `create_real_fake_rgbs` function

                if not exists(images_to_concat):
                    images_to_concat = self.resize_image_to(images, resolution)

                images_to_concat = repeat(images_to_concat, 'b ... -> (s b) ...', s = x.shape[0] // images_to_concat.shape[0])

                # concat the rgb (or real images reshaped)

                x = torch.cat((images_to_concat, x), dim = 1)

                # concat the rgb, projected into the feature dimension space

                if exists(from_rgb):
                    multi_scale_x = from_rgb(images_to_concat)
                    multi_scale_x = torch.cat((images_to_concat, multi_scale_x), dim = 1)
                    x = torch.cat((x, multi_scale_x), dim = 0)

            residual = residual_fn(x)
            x = block(x)

            if exists(attn):
                x = attn(x)

            if exists(predictor) and return_multiscale_outputs:
                pred_kwargs = dict()
                if not self.unconditional:
                    pred_kwargs = dict(mod = next(conv_mods), kernel_mod = next(conv_mods))

                multiscale_outputs.append(predictor(x, **pred_kwargs))

            if exists(downsample):
                x = downsample(x)

            x = x + residual
            x = x * self.residual_scale

            if exists(recon_decoder) and (return_all_aux_loss or has_real_images):

                if return_all_aux_loss:
                    recon_output = x

                elif has_real_images:
                    recon_output = rearrange(x, '(s b) ... -> s b ...', b = batch)
                    _, recon_output = recon_output.split(split_batch_size, dim = 1)
                    recon_output = rearrange(recon_output, 's b ... -> (s b) ...')

                aux_recon_target = repeat(aux_recon_target, 'b ... -> (s b) ...', s = recon_output.shape[0] // aux_recon_target.shape[0])

                # only reconstruct a fraction of images across batch and scale
                # for efficiency

                batch_scale = aux_recon_target.shape[0]
                batch_scale_frac = next(iter_aux_recon_frac)

                if batch_scale_frac < 1.:
                    num_batch_scale = max(int(batch_scale_frac * batch_scale), 1)
                    rand_indices = torch.randn((batch_scale,), device = self.device).sort(dim = -1).indices
                    rand_indices = rand_indices[:num_batch_scale]

                    recon_output = recon_output[rand_indices]
                    aux_recon_target = aux_recon_target[rand_indices]

                aux_recon_loss = recon_decoder(recon_output, aux_recon_target)
                aux_recon_losses.append(aux_recon_loss)

        logits = self.to_logits(x)   
        logits = rearrange(logits, '(s b) ... -> s b ...', b = batch)

        if not has_real_images:
            return logits, multiscale_outputs, aux_recon_losses

        # if real images are present, break up the outputs into (fake, real) tuples

        split_logits = logits.split(split_batch_size, dim = 1)

        split_multiscale_outputs = []

        for multiscale_output in multiscale_outputs:
            multiscale_output = rearrange(multiscale_output, '(s b) ... -> s b ...', b = batch)
            multiscale_output = multiscale_output.split(split_batch_size, dim = 1)
            split_multiscale_outputs.append(multiscale_output)

        return split_logits, split_multiscale_outputs, aux_recon_losses

# gan

TrainDiscrLosses = namedtuple('TrainDiscrLosses', [
    'divergence',
    'multiscale_divergence',
    'gradient_penalty',
    'aux_reconstruction'
])

TrainGenLosses = namedtuple('TrainGenLosses', [
    'divergence',
    'multiscale_divergence'
])

class GigaGAN(nn.Module):
    @beartype
    def __init__(
        self,
        *,
        generator: Union[BaseGenerator, Dict],
        discriminator: Union[Discriminator, Dict],
        text_encoder: Optional[Union[TextEncoder, Dict]] = None,
        learning_rate = 1e-4,
        betas = (0.9, 0.99),
        discr_aux_recon_loss_weight = 0.25,
        multiscale_divergence_loss_weight = 1.,
        apply_gradient_penalty_every = 16,
        train_upsampler = False,
        upsampler_replace_rgb_with_input_lowres_image = False,
        log_steps_every = 20,
        create_ema_generator_at_init = True
    ):
        super().__init__()

        self.train_upsampler = train_upsampler

        self.upsampler_replace_rgb_with_input_lowres_image= upsampler_replace_rgb_with_input_lowres_image
        self.apply_gradient_penalty_every = apply_gradient_penalty_every

        if train_upsampler:
            from gigagan_pytorch.unet_upsampler import UnetUpsampler
            generator_klass = UnetUpsampler
        else:
            generator_klass = Generator

        if isinstance(generator, dict):
            generator = generator_klass(**generator)

        if isinstance(discriminator, dict):
            discriminator = Discriminator(**discriminator)

        assert isinstance(generator, generator_klass)

        self.G = generator
        self.D = discriminator

        # text encoder

        if exists(text_encoder):
            if isinstance(text_encoder, dict):
                text_encoder = TextEncoder(**text_encoder)

        self.text_encoder = text_encoder

        assert generator.unconditional == discriminator.unconditional

        self.unconditional = generator.unconditional

        # optimizers

        self.G_opt = Adam(self.G.parameters(), lr = learning_rate, betas = betas)
        self.D_opt = Adam(self.D.parameters(), lr = learning_rate, betas = betas)

        # loss related

        self.discr_aux_recon_loss_weight = discr_aux_recon_loss_weight
        self.multiscale_divergence_loss_weight = multiscale_divergence_loss_weight

        # ema

        self.has_ema_generator = False

        if create_ema_generator_at_init:
            self.create_ema_generator()

        # steps

        self.log_steps_every = log_steps_every

        self.register_buffer('steps', torch.ones(1, dtype = torch.long))

    def save(self, path, overwrite = True):
        path = Path(path)
        path.parents[0].mkdir(parents = True, exist_ok =True)

        assert overwrite or not path.exists()

        pkg = dict(
            G = self.G.state_dict(),
            D = self.D.state_dict(),
            G_opt = self.G_opt.state_dict(),
            D_opt = self.D_opt.state_dict(),
            steps = self.steps.item(),
            version = __version__
        )

        if self.has_ema_generator:
            pkg['G_ema'] = self.G_ema.state_dict()

        torch.save(pkg, str(path))

    def load(self, path, strict = False):
        path = Path(path)
        assert path.exists()

        pkg = torch.load(str(path))

        if 'version' in pkg and pkg['version'] != __version__:
            print(f"trying to load from version {pkg['version']}")

        self.G.load_state_dict(pkg['G'], strict = strict)
        self.D.load_state_dict(pkg['D'], strict = strict)

        if self.has_ema_generator:
            self.G_ema.load_state_dict(pkg['G_ema'])

        if 'steps' in pkg:
            self.steps.copy_(torch.tensor([pkg['steps']]))

        if 'G_opt'not in pkg or 'D_opt' not in pkg:
            return

        try:
            self.G_opt.load_state_dict(pkg['G_opt'])
            self.D_opt.load_state_dict(pkg['D_opt'])
        except Exception as e:
            self.print(f'unable to load optimizers {e.msg}- optimizer states will be reset')
            pass

    @property
    def device(self):
        return self.steps.device

    def create_ema_generator(
        self,
        update_every = 10,
        update_after_step = 100,
        decay = 0.995
    ):
        assert not self.has_ema_generator, 'EMA generator has already been created'

        self.has_ema_generator = True
        self.G_ema = EMA(self.G, update_every = update_every, update_after_step = update_after_step, beta = decay)

    def print(self, msg):
        print(msg)

    @beartype
    def train_discriminator_step(
        self,
        dl_iter: Iterable,
        grad_accum_every = 1,
        apply_gradient_penalty = False
    ):
        total_divergence = 0.
        total_gp_loss = 0.
        total_aux_loss = 0.
        total_multiscale_divergence = 0.

        self.D_opt.zero_grad()

        for _ in range(grad_accum_every):

            if self.unconditional:
                real_images = next(dl_iter)
            else:
                result = next(dl_iter)
                assert isinstance(result, tuple), 'dataset should return a tuple of two items for text conditioned training, (images: Tensor, texts: List[str])'
                real_images, texts = result

            # requires grad for real images, for gradient penalty

            real_images = real_images.to(self.device)
            real_images.requires_grad_()

            batch_size = real_images.shape[0]

            # for discriminator training, fit upsampler and image synthesis logic under same function

            if self.train_upsampler:
                size = self.G.input_image_size
                lowres_real_images = F.interpolate(real_images, (size, size))

                G_kwargs = dict(
                    lowres_image = lowres_real_images,
                    replace_rgb_with_input_lowres_image = self.upsampler_replace_rgb_with_input_lowres_image
                )
            else:
                G_kwargs = dict(batch_size = batch_size)

            # add texts for conditioning if needed

            maybe_text_kwargs = dict()

            if not self.unconditional:
                maybe_text_kwargs['texts'] = texts

            # generator

            with torch.no_grad():
                images, rgbs = self.G(
                    **G_kwargs,
                    **maybe_text_kwargs,
                    return_all_rgbs = True
                )

            # detach output of generator, as training discriminator only

            images.detach_()

            for rgb in rgbs:
                rgb.detach_()

            # main divergence loss

            (fake_logits, real_logits), multiscale_logits, aux_recon_losses = self.D(
                images,
                rgbs,
                real_images = real_images,
                **maybe_text_kwargs,
            )

            divergence = discriminator_hinge_loss(real_logits, fake_logits)
            total_divergence = total_divergence + (divergence / grad_accum_every)

            # handle multi-scale divergence

            multiscale_divergence = 0.

            multiscale_real_logits = []

            if self.multiscale_divergence_loss_weight > 0.:

                for multiscale_fake, multiscale_real in multiscale_logits:
                    multiscale_loss = discriminator_hinge_loss(multiscale_fake, multiscale_real)
                    multiscale_divergence = multiscale_divergence + multiscale_loss
                    multiscale_real_logits.append(multiscale_real)

                total_multiscale_divergence += multiscale_divergence / grad_accum_every

            # figure out gradient penalty if needed

            gp_loss = 0.

            if apply_gradient_penalty:
                gp_loss = gradient_penalty(
                    real_images,
                    outputs = [real_logits, *multiscale_real_logits],
                    grad_output_weights = [1., *(self.multiscale_divergence_loss_weight,) * len(multiscale_real_logits)]
                )

                total_gp_loss += gp_loss / grad_accum_every

            # sum up losses

            total_loss = divergence + gp_loss

            if self.multiscale_divergence_loss_weight > 0.:
                total_loss = total_loss + multiscale_divergence * self.multiscale_divergence_loss_weight

            if self.discr_aux_recon_loss_weight > 0.:
                aux_loss = sum(aux_recon_losses)

                total_aux_loss += aux_loss / grad_accum_every

                total_loss = total_loss + aux_loss * self.discr_aux_recon_loss_weight

            # backwards

            (total_loss / grad_accum_every).backward()

        self.D_opt.step()

        return TrainDiscrLosses(total_divergence, total_multiscale_divergence, total_gp_loss, total_aux_loss)

    def train_generator_step(
        self,
        batch_size = None,
        dl_iter: Optional[Iterable] = None,
        grad_accum_every = 1
    ):
        total_divergence = 0.
        total_multiscale_divergence = 0.

        self.D_opt.zero_grad()
        self.G_opt.zero_grad()

        for _ in range(grad_accum_every):

            # what to pass into the generator
            # depends on whether training upsampler or not

            maybe_text_kwargs = dict()

            if self.train_upsampler or not self.unconditional:
                assert exists(dl_iter)

                if self.unconditional:
                    real_images = next(dl_iter)
                else:
                    result = next(dl_iter)
                    assert isinstance(result, tuple), 'dataset should return a tuple of two items for text conditioned training, (images: Tensor, texts: List[str])'
                    real_images, texts = result

                    maybe_text_kwargs['texts'] = texts

                real_images = real_images.to(self.device)

            # if training upsample generator, need to downsample real images

            if self.train_upsampler:
                size = self.G.input_image_size
                lowres_real_images = F.interpolate(real_images, (size, size))

                G_kwargs = dict(
                    lowres_image = lowres_real_images,
                    replace_rgb_with_input_lowres_image = self.upsampler_replace_rgb_with_input_lowres_image
                )
            else:
                assert exists(batch_size)

                G_kwargs = dict(batch_size = batch_size)

            # generator

            image, rgbs = self.G(
                **G_kwargs,
                **maybe_text_kwargs,
                return_all_rgbs = True
            )

            # discriminator

            logits, multiscale_logits, _ = self.D(
                image,
                rgbs,
                **maybe_text_kwargs
            )

            # hinge loss

            divergence = generator_hinge_loss(logits)

            total_divergence += divergence

            total_loss = divergence

            if self.multiscale_divergence_loss_weight > 0.:
                multiscale_divergence = 0.

                for multiscale_logit in multiscale_logits:
                    multiscale_divergence = multiscale_divergence + generator_hinge_loss(multiscale_logit)

                total_multiscale_divergence += multiscale_divergence

                total_loss = total_loss + multiscale_divergence * self.multiscale_divergence_loss_weight

            (total_loss / grad_accum_every).backward()

        self.G_opt.step()

        # update exponentially moving averaged generator

        if self.has_ema_generator:
            self.G_ema.update()

        return TrainGenLosses(total_divergence, total_multiscale_divergence)

    @beartype
    def forward(
        self,
        *,
        steps,
        dataloader: DataLoader,
        grad_accum_every = 1
    ):
        batch_size = dataloader.batch_size
        dl_iter = cycle(dataloader)

        last_gp_loss = 0.

        for _ in tqdm(range(steps), initial = self.steps.item()):
            steps = self.steps.item()
            is_first_step = steps == 1

            apply_gradient_penalty = self.apply_gradient_penalty_every > 0 and divisible_by(steps, self.apply_gradient_penalty_every)

            d_loss, multiscale_d_loss, gp_loss, recon_loss = self.train_discriminator_step(dl_iter, grad_accum_every = grad_accum_every, apply_gradient_penalty = apply_gradient_penalty)
            g_loss, multiscale_g_loss = self.train_generator_step(dl_iter = dl_iter, batch_size = batch_size, grad_accum_every = grad_accum_every)

            if exists(gp_loss):
                last_gp_loss = gp_loss

            if is_first_step or divisible_by(steps, self.log_steps_every):
                self.print(f' G: {g_loss:.2f} | MSG: {multiscale_g_loss:.2f} | D: {d_loss:.2f} | MSD: {multiscale_d_loss:.2f} | GP: {last_gp_loss:.2f} | SSL: {recon_loss:.2f}')

            self.steps += 1

        self.print(f'complete {steps} training steps')
