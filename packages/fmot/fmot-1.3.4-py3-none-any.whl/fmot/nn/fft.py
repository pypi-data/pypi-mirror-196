import torch
from torch import nn
from fmot.nn import SuperStructure
import numpy as np
from typing import *

__all__ = ['FFT', 'RFFT', 'IRFFT']

def get_fft_matrices(n_fft, dtype=torch.float32):
    mat = np.fft.fft(np.eye(n_fft))
    m_real = torch.tensor(mat.real, dtype=dtype)
    m_imag = torch.tensor(mat.imag, dtype=dtype)
    return m_real, m_imag

def get_complex_twiddle(n_fft, dtype=torch.float32):
    w = np.exp(-2j * np.pi / n_fft)
    w = np.power(w, np.arange(n_fft//2))
    return torch.tensor(w.real, dtype=dtype), torch.tensor(w.imag, dtype=dtype)

def get_rfft_reverse_matrix(n_fft, dtype=torch.float32):
    n = n_fft // 2 + 1
    mat = torch.zeros((n_fft - n, n), dtype=dtype)
    for k in range(n_fft - n):
        mat[k, n - k - 1 - ((n_fft+1)%2)] = 1
    return mat

def _get_mod_seq(order):
    mset = [0]
    for ord in range(order):
        ord = 2**ord

        new_mset = []
        for x in mset:
            new_mset.append(x)
            new_mset.append(x + ord)
        mset = new_mset

    return mset

def get_fft_permutation_matrix(N, order, dtype=torch.float32):
    m = np.zeros((N, N))
    perm_set = _get_mod_seq(order)
    base = 2**order

    k = 0
    for p in perm_set:
        for j in range(N//base):
            m[j*base+p, k] = 1
            k += 1
    
    return torch.tensor(m, dtype=dtype)

class DFT(nn.Module):
    """Applies NxN DFT to real signal, returning
    real and imaginary parts as separate tensors.
    """
    def __init__(self, n_fft: int):
        super().__init__()
        self.n_fft = n_fft
        fft_real, fft_imag = get_fft_matrices(n_fft, dtype=torch.float32)
        self.fft_real = nn.Parameter(fft_real, requires_grad=False)
        self.fft_imag = nn.Parameter(fft_imag, requires_grad=False)

    def forward(self, x):
        y_real = torch.matmul(x, self.fft_real.T)
        y_imag = torch.matmul(x, self.fft_imag.T)
        return y_real, y_imag

class DFTFromRFFT(nn.Module):
    def __init__(self, n_fft: int):
        super().__init__()
        self.n_fft = n_fft
        self.n = n_fft//2 + 1
        fft_real, fft_imag = get_fft_matrices(n_fft, dtype=torch.float32)
        rfft_real = fft_real[:self.n]
        rfft_imag = fft_imag[:self.n]
        self.rfft_real = nn.Parameter(rfft_real, requires_grad=False)
        self.rfft_imag = nn.Parameter(rfft_imag, requires_grad=False)
        self.rev = nn.Parameter(get_rfft_reverse_matrix(n_fft), requires_grad=False)
    
    def forward(self, x):
        fwd_real = torch.matmul(x, self.rfft_real.T)
        fwd_imag = torch.matmul(x, self.rfft_imag.T)

        rev_real = torch.matmul(fwd_real, self.rev.T)
        rev_imag = torch.matmul(fwd_imag, self.rev.T)

        y_real = torch.cat([fwd_real, rev_real], dim=-1)
        y_imag = torch.cat([fwd_imag, -rev_imag], dim=-1)
        return y_real, y_imag

class FFTwiddle(nn.Module):
    def __init__(self, n_fft: int):
        super().__init__()
        self.n_fft = n_fft
        twid_real, twid_imag = get_complex_twiddle(n_fft)
        self.twid_real = nn.Parameter(twid_real, requires_grad=False)
        self.twid_imag = nn.Parameter(twid_imag, requires_grad=False)

    def forward(self, even_real, even_imag, odd_real, odd_imag):
        todd_real = self.twid_real * odd_real - self.twid_imag * odd_imag
        todd_imag = self.twid_real * odd_imag + self.twid_imag * odd_real

        upper_real = even_real + todd_real
        upper_imag = even_imag + todd_imag
        lower_real = even_real - todd_real
        lower_imag = even_imag - todd_imag

        real = torch.cat([upper_real, lower_real], dim=-1)
        imag = torch.cat([upper_imag, lower_imag], dim=-1)

        return real, imag

    def extra_repr(self) -> str:
        return f'n_fft={self.n_fft}'


class FFTPermuter(nn.Module):
    def __init__(self, n_fft, n_stages):
        super().__init__()
        self.n_fft = n_fft
        self.n_stages = n_stages
        self.n_chunks = 2**n_stages
            
        self.perm = nn.Parameter(get_fft_permutation_matrix(n_fft, n_stages),
                requires_grad=False)

    def forward(self, x):
        y = torch.matmul(x, self.perm)
        return torch.chunk(y, self.n_chunks, dim=-1)

class FFT(SuperStructure):
    def __init__(self, n_fft, n_stages, dft_parallelism=1, twiddle_parallelism=1,
        base_rfft=False):
        super().__init__()

        if base_rfft:
            dft_class = DFTFromRFFT
        else:
            dft_class = DFT

        self.n_fft = n_fft
        self.n_stages = n_stages
        assert n_fft / 2**n_stages % 1 == 0, f'Cannot decompose {n_fft} with {n_stages} power-of-2 stages'

        dft_parallelism = min(2**n_stages, dft_parallelism)
        assert dft_parallelism <= 2**n_stages
        self.dft_parallelism = dft_parallelism
        self.twiddle_parallelism = twiddle_parallelism

        self.dfts = nn.ModuleList()
        for _ in range(dft_parallelism):
            self.dfts.append(dft_class(n_fft//2**n_stages))

        if n_stages > 0:
            self.permuter = FFTPermuter(n_fft, n_stages)
            self.twiddle_stages = nn.ModuleList()

            stage_size = n_fft//2**(n_stages-1)
            num_calls = n_fft//stage_size
            for _ in range(n_stages):
                twiddle_list = nn.ModuleList()
                for j in range(min(num_calls, twiddle_parallelism)):
                    twiddle_list.append(FFTwiddle(stage_size))
                self.twiddle_stages.append(twiddle_list)
                # self.twiddle_stages.append(FFTwiddle(stage_size))
                stage_size = stage_size * 2
                num_calls = num_calls//2

        else:
            self.permuter = None
            self.twiddle_stages = None

        # quantization configs
        self.observe: bool = False
        self.quantize: bool = False

    @torch.jit.ignore
    def forward(self, x):

        # Fallback to fast implementation of FFT if 
        # not in quantization or observation mode
        if not (self.observe or self.quantize or hasattr(x, 'dimensions')):
            y = torch.fft.fft(x, dim=-1, n=self.n_fft)
            real, imag = y.real, y.imag
            return real, imag

        if self.permuter is None:
            return self.dfts[0](x)

        else:
            perms = self.permuter(x)

            sub_dfts = [[],[],[],[]] # stores even_real, even_imag, odd_real, odd_imag sets

            for j, (x_even, x_odd) in enumerate(zip(perms[::2], perms[1::2])):

                ev_r, ev_i = self.dfts[2*j % self.dft_parallelism](x_even)
                od_r, od_i = self.dfts[(2*j+1) % self.dft_parallelism](x_odd)

                sub_dfts[0].append(ev_r)
                sub_dfts[1].append(ev_i)
                sub_dfts[2].append(od_r)
                sub_dfts[3].append(od_i)

            for twiddle_list in self.twiddle_stages:
                new_sub_dfts = [[],[],[],[]]
                for i, (ev_r, ev_i, od_r, od_i) in enumerate(zip(*sub_dfts)):
                    twiddler = twiddle_list[i%len(twiddle_list)]
                    real, imag = twiddler(ev_r, ev_i, od_r, od_i)
                    if i % 2 == 0:
                        new_sub_dfts[0].append(real)
                        new_sub_dfts[1].append(imag)
                    else:
                        new_sub_dfts[2].append(real)
                        new_sub_dfts[3].append(imag)
                sub_dfts = new_sub_dfts
            
            real, imag = sub_dfts[0][0], sub_dfts[1][0]
            return real, imag
                
    def extra_repr(self) -> str:
        f'n_fft: {self.n_fft} n_stages: {self.n_stages}'


class _RFFTDecomp(nn.Module):
    def __init__(self, n_fft, n_stages, dft_parallelism=1, twiddle_parallelism=1,
        base_rfft=False):
        super().__init__()
        self.n_fft = n_fft
        self.n_stages = n_stages
        self.dft_parallelism = dft_parallelism
        self.twiddle_parallelism = twiddle_parallelism

        self.fft = FFT(n_fft, n_stages, dft_parallelism, twiddle_parallelism,
            base_rfft=base_rfft)
        self._split0 = int(np.floor(n_fft/2 + 1))
        self._split1 = n_fft - self._split0

    def forward(self, x):
        yre, yim = self.fft(x)
        yre, __ = torch.split(yre, [self._split0, self._split1], -1)
        yim, __ = torch.split(yim, [self._split0, self._split1], -1)
        return yre, yim

class _RFFTDirect(nn.Module):
    def __init__(self, n_fft):
        super().__init__()
        self.n_fft = n_fft
        m_real, m_imag = get_fft_matrices(n_fft, dtype=torch.float32)
        n_rfft = int(np.floor(n_fft/2 + 1))
        m_real = m_real[:n_rfft]
        m_imag = m_imag[:n_rfft]

        self.rfft_real = nn.Parameter(m_real, requires_grad=False)
        self.rfft_imag = nn.Parameter(m_imag, requires_grad=False)

    def forward(self, x):
        re = torch.matmul(x, self.rfft_real.T)
        im = torch.matmul(x, self.rfft_imag.T)
        return re, im

class RFFT(nn.Module):
    def __init__(self, n_fft, n_stages, dft_parallelism=1, twiddle_parallelism=1,
        base_rfft=False):
        super().__init__()
        if n_stages == 0:
            self.rfft = _RFFTDirect(n_fft)
        else:
            self.rfft = _RFFTDecomp(n_fft, n_stages, dft_parallelism, twiddle_parallelism,
                base_rfft)
        
    def forward(self, x):
        return self.rfft(x)

def get_irfft_matrices(n_fft: int, dtype=torch.float32):
    n = n_fft // 2 + 1
    m_real = np.fft.irfft(np.eye(n))
    m_imag = np.fft.irfft(1j*np.eye(n))
    m_real = torch.tensor(m_real, dtype=dtype)
    m_imag = torch.tensor(m_imag, dtype=dtype)
    return m_real, m_imag

class _IRFFTDirect(nn.Module):
    def __init__(self, n_fft):
        super().__init__()
        self.n_fft = n_fft
        m_real, m_imag = get_irfft_matrices(n_fft, dtype=torch.float32)

        self.irfft_real = nn.Parameter(m_real.T, requires_grad=False)
        self.irfft_imag = nn.Parameter(m_imag.T, requires_grad=False)

    def forward(self, re, im):
        return torch.matmul(re, self.irfft_real.T) + torch.matmul(im, self.irfft_imag.T)

class IRFFT(nn.Module):
    """
    Placeholder for efficient implementation -- for now,
    just calls the pytorch irfft
    """
    def __init__(self, n_fft):
        super().__init__()
        self.n_fft = n_fft

        self.irfft = _IRFFTDirect(n_fft)

    def forward(self, re, im):
        return self.irfft(re, im)