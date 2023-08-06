import torch
from fmot.nn import FFT
import fmot
import sys
sys.setrecursionlimit(10000)

def test_fft():
    model = FFT(512, 3, dft_parallelism=2,
        twiddle_parallelism=2)
    cmodel = fmot.ConvertedModel(model)
    cmodel.quantize([torch.randn(8, 512) for _ in range(4)])
    graph = cmodel.trace()
    assert True