import torch
from torch import nn, Tensor
from .sequencer import Sequencer
from .atomics import Identity
from .super_structures import SuperStructure
from .fft import RFFT, IRFFT
from typing import *
import sys
sys.setrecursionlimit(10000)

class Cat(nn.Module):
    """Utility; exists so that STFTBUffCell can be a SuperStructure
    """
    def __init__(self, dim):
        super().__init__()
        self.dim = dim

    def forward(self, x: List[Tensor]) -> Tensor:
        return torch.cat(x, self.dim)

class _STFTBuffCell(SuperStructure):
    """Handles the data orchestration inside of STFT Buffer (with arb. kernel size)"""
    def __init__(self):
        super().__init__()
        self.cat = Cat(-1)

    @torch.jit.export
    def forward(self, x_t: Tensor, state: List[Tensor]) -> Tuple[Tensor, List[Tensor]]:
        y_t = self.cat(state + [x_t])
        state = state[1:] + [x_t]
        return y_t, state

class STFTBuffer(Sequencer):
    """Manages the internal buffer of an STFT and concatenates inputs with past inputs
    to fill the window-size.
    
    window_size must be an integer multiple of hop_size."""
    def __init__(self, window_size: int, hop_size: int):
        k = window_size / hop_size
        assert k % 1 == 0, 'window_size must be an integer multiple of hop_size'
        k = int(k)

        super().__init__(state_shapes=[[hop_size]]*(k-1), batch_dim=0, seq_dim=1)
        self.cell = _STFTBuffCell()
    
    @torch.jit.export
    def step(self, x_t: Tensor, state: List[Tensor]) -> Tuple[Tensor, List[Tensor]]:
        return self.cell(x_t, state)

class WindowMul(nn.Module):
    def __init__(self, window):
        super().__init__()
        self.window = nn.Parameter(window, requires_grad=False)

    def forward(self, x):
        return x * self.window
    
class ConstantMul(nn.Module):
    def __init__(self, cnst: float):
        super().__init__()
        self.cnst = cnst

    def forward(self, x):
        return self.cnst * x

class ZeroCatter(nn.Module):
    def __init__(self, n):
        super().__init__()
        self.zeros = nn.Parameter(torch.zeros(n), requires_grad=False)
    
    def forward(self, x):
        return torch.cat([x, self.zeros], -1)

class STFT(SuperStructure):
    def __init__(self, n_fft: int, hop_size: int, n_stages: int, window_size: int=None,
        window_fn: Tensor=None, base_rfft=False):
        super().__init__()
        self.n_fft = n_fft
        self.hop_size = hop_size
        if window_size is None:
            window_size = n_fft
        self.window_size = window_size
        self.n_stages = n_stages
        
        if window_fn is not None:
            self.window_mul = WindowMul(window_fn)
        else:
            self.window_mul = None
        
        if window_size < n_fft:
            self.catter = ZeroCatter(n_fft - window_size)
        elif window_size > n_fft:
            raise ValueError('window_size cannot exceed n_fft')
        else:
            self.catter = None
        
        self.buffer = STFTBuffer(window_size, hop_size)
        self.rfft = RFFT(n_fft, n_stages, base_rfft=base_rfft)

    def forward(self, x):

        # concatenate with previous frames
        x_stack, __ = self.buffer(x)

        # optionally apply window_fn:
        if self.window_mul is not None:
            x_stack = self.window_mul(x_stack)

        # optionally pad with zeros:
        if self.catter is not None:
            x_stack = self.catter(x_stack)

        # apply the RFFT
        re_out, im_out = self.rfft(x_stack)
        return re_out, im_out

@torch.no_grad()
def check_50pct_cola(window: Tensor) -> Tuple[bool, Union[float, Tensor]]:
    """Checks a window-function for the COLA (Constant Overlap Add)
    condition for 50% overlap. 
    
    If COLA is satisfied, returns (True, c), where c is a scalar float
    given by the 50%-overlap-sum of the window function.

    If COLA is not satisfied, returns (False, woverlap), where woverlap
    is a tensor given by the 50%-overlap-sum of the window function.
    """

    N = len(window)
    assert N % 2 == 0, 'Window function must be even-lengthed'

    w_left = window[:N//2]
    w_right = window[N//2:]

    woverlap = w_left + w_right

    assert torch.all(woverlap != 0), \
        "Window function does not satisfy the NOLA (nonzero overlap add) constraint"

    c = woverlap[0]

    if torch.all((woverlap - c).abs()/torch.max(woverlap) < 1e-6):
        return True, c.item()
    else:
        return False, woverlap
    
class SynthesisWindow(nn.Module):
    """Convert an analysis window into a synthesis window,
    assuming 50% overlap.
    """
    def __init__(self, analysis_window: torch.Tensor):
        super().__init__()
        wa, wb = analysis_window.chunk(2, 0)
        den = wa**2 + wb**2
        assert torch.all(den > 0), 'Window function must satisfy the COLA constraint'
        den = torch.cat([den, den])
        self.window = nn.Parameter(analysis_window / den, requires_grad=False)

    def forward(self, x):
        return self.window * x
    
class _OverlapAdd50pct(Sequencer):
    def __init__(self, hop_size: int):
        super().__init__([[hop_size]], 0, 1)
    
    @torch.jit.export
    def step(self, x: Tensor, state: List[Tensor]) -> Tuple[Tensor, List[Tensor]]:
        x_curr, x_next = torch.chunk(x, 2, -1)
        s_curr, = state
        x = x_curr + s_curr
        return x, [x_next]
        
class OverlapAdd50Pct(nn.Module):
    """50% Overlap-Add Decoding. Takes overlapping waveforms and performs
    overlap-add, multiplying by a constant/time-varying factor if a window-function
    is used.
    """
    def __init__(self, hop_size: int, window: Tensor=None):
        super().__init__()
        if window is not None:
            self.synthesis_window = SynthesisWindow(window)

        else:
            self.synthesis_window = ConstantMul(0.5)
        self.ola = _OverlapAdd50pct(hop_size)

    def forward(self, x):
        x = self.synthesis_window(x)
        y, __ = self.ola(x)
        return y