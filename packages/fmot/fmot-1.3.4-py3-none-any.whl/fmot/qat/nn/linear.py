import math
from functools import partial

import torch
from torch import nn

from . import atomics, quantizers
from .density_matmul import AddMM, Matmul
from ..annotated_tensors import set_dim_annotations

class Linear(torch.nn.Module):
    def __init__(self, in_features, out_features, act_bitwidth, par_bitwidth,
        bias=True, observer=quantizers.DEFAULT_OBSERVERS['default']):
        super().__init__()

        self.q_group = quantizers.PrecisionConstraint()

        self.in_features = in_features
        self.out_features = out_features
        self.requant_in = atomics.Requantize(act_bitwidth, observer)
        self.q_group.recursively_add(self.requant_in)
        self.weight = nn.Parameter(torch.Tensor(out_features, in_features))
        self.weight_quant = quantizers.ParameterQuantizer(par_bitwidth,
            observer=quantizers.DEFAULT_OBSERVERS['param'])
        self.q_group.add(self.weight_quant)
        self.weight_transpose = atomics.Transpose()
        if bias:
            self.bias = nn.Parameter(torch.Tensor(out_features))
            set_dim_annotations(['F'], self.bias)
            self.multiplier = AddMM(act_bitwidth, observer=observer)
            self.bias_quant = quantizers.ParameterQuantizer(act_bitwidth,
                observer=quantizers.DEFAULT_OBSERVERS['param'])
        else:
            self.register_parameter('bias', None)
            self.multiplier = Matmul(act_bitwidth, observer=observer)
        self.reset_parameters()

    def reset_parameters(self):
        nn.init.kaiming_uniform_(self.weight, a=math.sqrt(5))
        if self.bias is not None:
            fan_in, _ = nn.init._calculate_fan_in_and_fan_out(self.weight)
            bound = 1 / math.sqrt(fan_in)
            nn.init.uniform_(self.bias, -bound, bound)

    def forward(self, x):
        x = self.requant_in(x)
        set_dim_annotations(['F', 'F'], self.weight)
        weight = self.weight_quant(self.weight)
        weight = self.weight_transpose(weight)
        set_dim_annotations(['F', 'F'], weight)
        if self.bias is not None:
            bias = self.bias_quant(self.bias)
            set_dim_annotations(['F'], bias)
            return self.multiplier(bias, x, weight)
        else:
            return self.multiplier(x, weight)

    def __repr__(self):
        return 'QuantLinear(in_features={}, out_features={}, bias={}, act_bw={}, par_bw={})'.format(
            self.in_features, self.out_features, self.bias is not None,
            self.multiplier.quantizer.bitwidth, self.weight_quant.bitwidth
        )

    @classmethod
    def _from_float(cls, parent, bw_conf, interpolate,
        observer=quantizers.DEFAULT_OBSERVERS['default'], **kwargs):
        observer = partial(observer, **kwargs)
        model = cls(
                in_features=parent.in_features,
                out_features=parent.out_features,
                act_bitwidth=bw_conf.activations,
                par_bitwidth=bw_conf.weights,
                bias = parent.bias is not None,
                observer = observer
            )
        model.weight.data = parent.weight.data
        if model.bias is not None:
            model.bias.data = parent.bias.data
        return model
