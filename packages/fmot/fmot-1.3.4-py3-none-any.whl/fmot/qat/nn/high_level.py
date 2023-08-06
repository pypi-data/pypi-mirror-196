import torch
from . import atomics
from .atomics import AtomicModule, _get_mul_constants
from torch import nn, Tensor
import torch.nn.functional as F
from ..annotated_tensors import check_for_annotations, copy_annotations, annotate, \
    copy_dim_annotations, set_dim_annotations, get_dim_annotations
from . import quantizers
from ..fake_quantization import fake_quantize
from functools import partial

class FConv1d(AtomicModule):
    def __init__(self, act_bitwidth, stride=1, padding=0, dilation=1, groups=1,
        kernel_size=1, observer=quantizers.DEFAULT_OBSERVERS['default']):
        super().__init__()
        self.stride = stride
        self.padding = padding
        self.dilation = dilation
        self.groups = groups
        self.kernel_size = kernel_size

        self.quantizer = quantizers.Quantizer(act_bitwidth, observer=observer)

    @check_for_annotations
    def forward(self, x, weight):
        y = F.conv1d(x, weight, 
            bias=None, stride=self.stride, padding=self.padding, dilation=self.dilation,
            groups=self.groups)
        y = self.quantizer(y)
        y = copy_annotations(x, y)
        y.prev_relu = False
        y.density_per_element = None
        return y

    def _get_constants(self, x, weight):
        z = self.forward(x, weight)
        constants = _get_mul_constants(x, weight, z)
        if z.quantized:
            constants['bw_out'] = z.bitwidth.bitwidth
            del constants['bw']
        constants['stride'] = self.stride
        constants['padding'] = self.padding
        constants['dilation'] = self.dilation
        constants['groups'] = self.groups
        constants['kernel_size'] = self.kernel_size
        return constants

class Conv1d(nn.Module):
    def __init__(self, in_channels, out_channels, kernel_size, act_bitwidth, 
        par_bitwidth, stride=1, padding=0, dilation=1, groups=1, bias=True, 
        padding_mode='zeros', observer=quantizers.DEFAULT_OBSERVERS['default']):

        self.in_channels = in_channels
        self.out_channels = out_channels
        if isinstance(kernel_size, tuple):
            assert len(kernel_size) == 1
            kernel_size, = kernel_size
        self.kernel_size = kernel_size
        self.stride = stride
        self.padding = padding
        self.dilation = dilation
        self.groups = groups
        self.padding_mode = padding_mode

        assert in_channels % groups == 0, 'in_channels must be divisible by groups'
        assert padding_mode == 'zeros', 'only padding_mode="zero_padding" is supported'

        super().__init__()

        self.weight = nn.Parameter(
            torch.randn(self.out_channels, self.in_channels//self.groups, 
                self.kernel_size))
        self.weight_quant = quantizers.ParameterQuantizer(par_bitwidth, 
            observer=observer)
        if bias:
            self.bias = nn.Parameter(torch.zeros(out_channels))
            self.bias_quant = quantizers.ParameterQuantizer(act_bitwidth,
                observer=observer)
            self.bias_add = atomics.VVAdd(act_bitwidth, observer=observer)
        else:
            self.register_parameter('bias', None)
            self.bias_quant = None
            self.bias_add = None

        self.requant_in = atomics.Requantize(act_bitwidth, observer)
        self.conv = FConv1d(act_bitwidth, self.stride, self.padding, self.dilation, 
            self.groups, self.kernel_size, observer)

        self.q_group = quantizers.PrecisionConstraint()
        self.q_group.recursively_add(self.requant_in)
        self.q_group.add(self.weight_quant)

    def forward(self, x):
        x = self.requant_in(x)
        weight = self.weight_quant(self.weight)
        y = self.conv(x, weight)
        if self.bias is not None:
            bias = self.bias_quant(self.bias.unsqueeze(-1))
            y = self.bias_add(y, bias)
        return y

    @classmethod
    def _from_float(cls, parent, bw_conf, interpolate,
        observer=quantizers.DEFAULT_OBSERVERS['default'], **kwargs):
        observer = partial(observer, **kwargs)

        keys = [
            'in_channels', 
            'out_channels', 
            'kernel_size',
            'stride',
            'padding',
            'dilation',
            'groups',
            'padding_mode'
        ]
        kwargs = {k: getattr(parent, k) for k in keys}
        kwargs.update(dict(
            bias=parent.bias is not None,
            act_bitwidth=bw_conf.activations,
            par_bitwidth=bw_conf.weights,
            observer=observer))

        model = cls(**kwargs)

        model.weight.data = parent.weight.data
        if model.bias is not None:
            model.bias.data = parent.bias.data
        return model

class AvgPool1d(AtomicModule):
    def __init__(self, act_bitwidth, kernel_size, stride, padding, observer,
        ceil_mode=False, count_include_pad=True):
        super().__init__()
        self.kernel_size = kernel_size
        self.stride = stride
        self.padding = padding

        assert not ceil_mode, 'AvgPool1d with ceil_mode=True not yet supported'
        assert count_include_pad, 'AvgPool1d with count_include_pad=False not yet supported'

        self.quantizer = quantizers.Quantizer(act_bitwidth, observer=observer)

    @check_for_annotations
    def forward(self, x):
        y = F.avg_pool1d(x, stride=self.stride, padding=self.padding, kernel_size=self.kernel_size,
            ceil_mode=False, count_include_pad=True)
        y = self.quantizer(y)
        y = copy_annotations(x, y)
        y.prev_relu = False
        y.density_per_element = None
        return y

    def _get_constants(self, x):
        z = self.forward(x)
        constants = {}
        if z.quantized:
            constants['bw_out'] = z.bitwidth.bitwidth
        constants['stride'] = self.stride
        constants['padding'] = self.padding
        constants['kernel_size'] = self.kernel_size
        return constants

    @classmethod
    def _from_float(cls, parent, bw_conf, interpolate,
        observer=quantizers.DEFAULT_OBSERVERS['default'], **kwargs):
        observer = partial(observer, **kwargs)

        keys = [ 
            'kernel_size',
            'stride',
            'padding',
            'ceil_mode',
            'count_include_pad'
        ]
        D = {k: getattr(parent, k) for k in keys}
        D.update(dict(
            act_bitwidth=bw_conf.activations,
            observer=observer))

        return cls(**D)

class AdaptiveAvgPool2d(AtomicModule):
    def __init__(self, output_size, bitwidth, observer=quantizers.DEFAULT_OBSERVERS['default']):
        super().__init__()
        self.output_size = output_size
        self.quantizer = quantizers.Quantizer(bitwidth, observer=observer)

    def forward(self, x):
        y = F.adaptive_avg_pool2d(x, self.output_size)
        copy_annotations(x, y)
        y = self.quantizer(y)
        y = copy_annotations(x, y)
        y.prev_relu = False
        y.density_per_element = None
        return y

    def _get_constants(self, x):
        z = self.forward(x)
        constants = {}
        if z.quantized:
            constants['bw_out'] = z.bitwidth.bitwidth
        constants['output_size'] = self.output_size
        return constants

    @classmethod
    def _from_float(cls, parent, bw_conf, interpolate,
        observer=quantizers.DEFAULT_OBSERVERS['default'], **kwargs):
        observer = partial(observer, **kwargs)

        keys = [ 
            'output_size'
        ]
        D = {k: getattr(parent, k) for k in keys}
        D.update(dict(
            bitwidth=bw_conf.activations,
            observer=observer))
        return cls(**D)

class MaxPool1d(AtomicModule):
    def __init__(self, act_bitwidth, kernel_size, stride, padding, dilation, observer,
        ceil_mode=False, return_indices=False):
        super().__init__()
        self.kernel_size = kernel_size
        self.stride = stride
        self.padding = padding
        self.dilation = dilation

        assert not ceil_mode, 'MaxPool1d with ceil_mode=True not yet supported'
        assert not return_indices, 'MaxPool1d with return_indices=True not yet supported'

        self.quantizer = quantizers.Quantizer(act_bitwidth, observer=observer)

    def forward(self, x):
        y = F.max_pool1d(x, stride=self.stride, padding=self.padding, kernel_size=self.kernel_size,
            dilation=self.dilation, ceil_mode=False, return_indices=False)
        y = self.quantizer(y)
        y = copy_annotations(x, y)
        y.prev_relu = False
        y.density_per_element = None
        return y

    def _get_constants(self, x):
        z = self.forward(x)
        constants = {}
        if z.quantized:
            constants['bw_out'] = z.bitwidth.bitwidth
        constants['stride'] = self.stride
        constants['padding'] = self.padding
        constants['kernel_size'] = self.kernel_size
        constants['dilation'] = self.dilation
        return constants

    @classmethod
    def _from_float(cls, parent, bw_conf, interpolate,
        observer=quantizers.DEFAULT_OBSERVERS['default'], **kwargs):
        observer = partial(observer, **kwargs)

        keys = [ 
            'kernel_size',
            'stride',
            'padding',
            'dilation',
            'ceil_mode',
            'return_indices'
        ]
        D = {k: getattr(parent, k) for k in keys}
        D.update(dict(
            act_bitwidth=bw_conf.activations,
            observer=observer))

        return cls(**D)

class FConv2d(AtomicModule):
    def __init__(self, act_bitwidth, stride, padding, dilation, groups, kernel_size,
        observer):
        super().__init__()
        self.stride = stride
        self.padding = padding
        self.dilation = dilation
        self.groups = groups
        self.kernel_size = kernel_size
        self.quantizer = quantizers.Quantizer(act_bitwidth, observer=observer)

    @check_for_annotations
    def forward(self, input, weight):
        y = F.conv2d(input, weight, 
            bias=None, stride=self.stride, padding=self.padding, 
            dilation=self.dilation, groups=self.groups)
        copy_annotations(input, y)
        return self.quantizer(y)

    def _get_constants(self, input, weight):
        z = self.forward(input, weight)
        constants = {}
        if z.quantized:
            constants['bw_out'] = z.bitwidth.bitwidth
        constants['stride'] = self.stride
        constants['padding'] = self.padding
        constants['dilation'] = self.dilation
        constants['groups'] = self.groups
        constants['kernel_size'] = self.kernel_size
        return constants

def to2tuple(x):
    if not isinstance(x, tuple):
        x = (x, x)
    return x

class Conv2d(nn.Module):
    def __init__(self, in_channels, out_channels, kernel_size, act_bitwidth,
        par_bitwidth, stride=1, padding=0, dilation=1, groups=1, bias=True,
        padding_mode='zeros', observer=quantizers.DEFAULT_OBSERVERS['default']):

        self.in_channels = in_channels
        self.out_channels = out_channels
        self.kernel_size = to2tuple(kernel_size)
        self.stride = to2tuple(stride)
        self.padding = to2tuple(padding)
        self.dilation = to2tuple(dilation)
        self.groups = groups
        self.padding_mode = padding_mode

        assert in_channels % groups == 0, 'in_channels must be divisible by groups'
        assert padding_mode == 'zeros', 'only padding_mode="zero_padding" is supported'

        super().__init__()

        self.weight = nn.Parameter(
            torch.randn(self.out_channels, self.in_channels//self.groups, 
                *self.kernel_size))
        self.weight_quant = quantizers.ParameterQuantizer(par_bitwidth, 
            observer=observer)

        if bias:
            self.bias = nn.Parameter(torch.zeros(out_channels))
            self.bias_quant = quantizers.ParameterQuantizer(act_bitwidth,
                observer=observer)
            self.bias_add = atomics.VVAdd(act_bitwidth, observer=observer)
        else:
            self.register_parameter('bias', None)
            self.bias_quant = None
            self.bias_add = None

        self.requant_in = atomics.Requantize(act_bitwidth, observer)
        self.conv = FConv2d(act_bitwidth, self.stride, self.padding, self.dilation, 
            self.groups, self.kernel_size, observer=observer)

        self.q_group = quantizers.PrecisionConstraint()
        self.q_group.recursively_add(self.requant_in)
        self.q_group.add(self.weight_quant)

    def forward(self, x):
        x = self.requant_in(x)
        weight = self.weight_quant(self.weight)
        y = self.conv(x, weight)
        if self.bias is not None:
            bias = self.bias_quant(self.bias.unsqueeze(-1).unsqueeze(-1))
            y = self.bias_add(y, bias)
        copy_annotations(x, y)
        return y

    @classmethod
    def _from_float(cls, parent, bw_conf, interpolate,
        observer=quantizers.DEFAULT_OBSERVERS['default'], **kwargs):
        observer = partial(observer, **kwargs)

        keys = [
            'in_channels', 
            'out_channels', 
            'kernel_size',
            'stride',
            'padding',
            'dilation',
            'groups',
            'padding_mode'
        ]
        kwargs = {k: getattr(parent, k) for k in keys}
        kwargs.update(dict(
            bias=parent.bias is not None,
            act_bitwidth=bw_conf.activations,
            par_bitwidth=bw_conf.weights,
            observer=observer))

        model = cls(**kwargs)

        model.weight.data = parent.weight.data
        if model.bias is not None:
            model.bias.data = parent.bias.data
        return model
