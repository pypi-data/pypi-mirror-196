from fmot.fqir import registry_v1
import fmot.qat as Q

oplinks_v1 = {
    Q.nn.VVAdd:             registry_v1['vvadd'],
    Q.nn.VIAdd:             registry_v1['viadd'],
    Q.nn.VVSub:             registry_v1['vvsub'],
    Q.nn.Neg:               registry_v1['vneg'],
    Q.nn.VVMul:             registry_v1['vvmul'],
    Q.nn.VIMul:             registry_v1['vimul'],
    Q.nn.Matmul:            registry_v1['matmul'],
    Q.nn.NoShiftMM:         registry_v1['matmul'],
    Q.nn.AddMM:             registry_v1['addmm'],
    Q.nn.ReLU:              registry_v1['relu'],
    Q.nn.Transpose:         registry_v1['transpose'],
    Q.nn.FTranspose:        registry_v1['transpose'],
    Q.nn.Reshape:           registry_v1['reshape'],
    Q.nn.Quantizer:         registry_v1['quantize'],
    Q.nn.Chunk:             registry_v1['chunk'],
    Q.nn.Split:             registry_v1['split'],
    Q.nn.BareCat:           registry_v1['cat'],
    Q.nn.Stack:             registry_v1['stack'],
    Q.nn.Sum:               registry_v1['sum'],
    Q.nn.OnesLike:          registry_v1['constant_like'],
    Q.nn.Shift:             registry_v1['shift'],
    Q.nn.Requantize:        registry_v1['shift'],
    Q.nn.Gt0:               registry_v1['gt0'],
    Q.nn.FConv1d:           registry_v1['conv1d'],
    Q.nn.AvgPool1d:         registry_v1['avgpool1d'],
    Q.nn.MaxPool1d:         registry_v1['maxpool1d'],
    Q.nn.FConv2d:           registry_v1['conv2d'],
    Q.nn.Squeeze:           registry_v1['squeeze'],
    Q.nn.AdaptiveAvgPool2d: registry_v1['adaptive_avg_pool2d'],
    Q.nn.LSTM:              registry_v1['lstm']
}

lut_ops = [Q.nn.LUT, Q.nn.RSqrtPlusEps, Q.nn.PowFrac, Q.nn.BareLUT]
for op in lut_ops:
    oplinks_v1[op] =    registry_v1['lut']
