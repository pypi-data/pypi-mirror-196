import torch
from torch import nn
import numpy as np
from .conv1d import TemporalConv1d
from typing import List, Tuple
from torch import Tensor
from fmot.functional import cos_arctan
from . import atomics
from .composites import TuningEpsilon
from python_speech_features.base import get_filterbanks

def _get_norm(normalized):
    norm = None
    if normalized:
        norm = 'ortho'
    return norm

def get_rfft_matrix(size, normalized=False):
    weight = np.fft.rfft(np.eye(size), norm=_get_norm(normalized))
    w_real, w_imag = np.real(weight), np.imag(weight)
    return torch.tensor(w_real).float(), torch.tensor(w_imag).float()

def get_irfft_matrix(size, normalized=False):
    in_size = size//2 + 1
    w_real = np.fft.irfft(np.eye(in_size), n=size, norm=_get_norm(normalized))
    w_imag = np.fft.irfft(np.eye(in_size)*1j, n=size, norm=_get_norm(normalized))
    return torch.tensor(w_real).float(), torch.tensor(w_imag).float()

def get_mel_matrix(sr, n_dft, n_mels=128, fmin=0.0, fmax=None, **kwargs):
    mel_matrix = get_filterbanks(
        nfilt=n_mels, 
        nfft=n_dft, 
        samplerate=sr, 
        lowfreq=fmin,
        highfreq=fmax)
    return torch.tensor(mel_matrix, dtype=torch.float32)

def get_dct_matrix(n, n_out=None, dct_type=2, normalized=False):
    N = n
    if n_out is None:
        n_out = n
    K = n_out

    if K > N:
        raise ValueError(f"DCT cannot have more output features ({K}) than input features ({N})")
    matrix = None
    if dct_type == 1:
        ns = np.arange(1, N-1)
        ks = np.arange(K)
        matrix = np.zeros((N, K))
        matrix[0, :] = 1
        matrix[-1, :] = -1**ks
        matrix[1:-1, :] = 2*np.cos((np.pi*ks.reshape(1,-1)*ns.reshape(-1,1))/(N-1))
    elif dct_type == 2:
        ns = np.arange(N).reshape(-1,1)
        ks = np.arange(K).reshape(1,-1)
        matrix = 2*np.cos(np.pi*ks*(2*ns+1)/(2*N))
        if normalized:
            matrix[:,0] /= np.sqrt(4*N)
            matrix[:,1:] /= np.sqrt(2*N)
    elif dct_type == 3:
        ns = np.arange(1, N).reshape(-1,1)
        ks = np.arange(K).reshape(1,-1)
        matrix = np.zeros((N, K))
        matrix[0, :] = 1
        matrix[1:, :] = 2*np.cos(np.pi*(2*ks+1)*ns/(2*N))
        if normalized:
            matrix[0, :] /= np.sqrt(N)
            matrix[1:, :] /= np.sqrt(2*N)
    elif dct_type == 4:
        ns = np.arange(N).reshape(-1,1)
        ks = np.arange(K).reshape(1,-1)
        matrix = 2*np.cos(np.pi*(2*ks+1)*(2*ns+1)/(4*N))
        if normalized:
            matrix /= np.sqrt(2*N)
    else:
        raise ValueError(f'DCT type {dct_type} is not defined.')
    return torch.tensor(matrix).float()

class RFFT(nn.Module):
    r"""
    Real-to-complex 1D Discrete Fourier Transform.

    Returns the real and imaginary parts as two separate tensors.

    Args:
        size (int): length of input signal
        normalized (bool): whether to use a normalized DFT matrix. Default is False

    Shape:
            - Input: :math:`(*, N)` where :math:`*` can be any number of additional dimensions.
              :math:`N` must match the :attr:`size` argument.
            - Output:
                - Real Part: :math:`(*, \lfloor N/2 \rfloor + 1)`
                - Imaginary Part: :math:`(*, \lfloor N/2 \rfloor + 1)`

    .. seealso::

        - :class:`IRFFT`
    """
    def __init__(self, size, normalized=False):
        super().__init__()
        w_real, w_imag = get_rfft_matrix(size, normalized)
        self.w_real = nn.Parameter(w_real, requires_grad=False)
        self.w_imag = nn.Parameter(w_imag, requires_grad=False)

    def forward(self, x: Tensor) -> Tuple[Tensor, Tensor]:
        r"""
        Args:
            x (Tensor): Input, of shape :math:`(*, N)`

        Returns:
            - Real part, of shape :math:`(*, \lfloor N/2 \rfloor + 1)`
            - Imaginary part, of shape :math:`(*, \lfloor N/2 \rfloor + 1)`
        """
        real = torch.matmul(x, self.w_real)
        imag = torch.matmul(x, self.w_imag)
        return real, imag

class IRFFT(nn.Module):
    r"""
    Inverse of the real-to-complex 1D Discrete Fourier Transform.

    Inverse to :class:`RFFT`. Requires two input tensors for the real and imaginary
    part of the RFFT.

    Args:
        size (int): length of original real-valued input signal
        normalized (bool): whether to use a normalized DFT matrix. Default is False.

    Shape:
        - Re: :math:`(*, \lfloor N/2 \rfloor + 1)` where :math:`*` can be any number
          of additional dimensions. :math:`N` must match the :attr:`size` argument.
        - Im: :math:`(*, \lfloor N/2 \rfloor + 1)`
        - Output: :math:`(*, N)`

    .. seealso::

        - :class:`RFFT`
    """
    def __init__(self, size, normalized=False):
        super().__init__()
        w_real, w_imag = get_irfft_matrix(size, normalized)
        self.w_real = nn.Parameter(w_real, requires_grad=False)
        self.w_imag = nn.Parameter(w_imag, requires_grad=False)

    def forward(self, real: Tensor, imag: Tensor) -> Tensor:
        r"""
        Args:
            real (Tensor): Real part of the input, of shape :math:`(*, \lfloor N/2 \rfloor + 1)`
            imag (Tensor): Imaginary part of the input,
                of shape :math:`(*, \lfloor N/2 \rfloor + 1)`.

        Returns:
            - Output, of shape :math:`(*, N)`
        """
        return torch.matmul(real, self.w_real) + torch.matmul(imag, self.w_imag)

class DCT(nn.Module):
    r"""
    Discrete Cosine Transformation.

    Performs the DCT on an input by multiplying it with the DCT matrix.
    DCT Types :attr:`1`, :attr:`2`, :attr:`3`, and :attr:`4` are implemented. See
    `scipy.fftpack.dct <https://docs.scipy.org/doc/scipy/reference/generated/scipy.fftpack.dct.html>`_
    for reference about the different DCT types. Type :attr:`2` is default.

    Args:
        in_features (int): Length of input signal that is going through the DCT
        out_features (int): Number of desired output DCT features. Default is :attr:`in_features`.
            Must satisfy :math:`\text{out_features} \leq \text{in_features}`
        dct_type (int): Select between types :attr:`1`, :attr:`2`, :attr:`3`, and :attr:`4`.
            Default is :attr:`2`.
        normalized (bool): If True and :attr:`dct_type` is :attr:`2`, :attr:`3`, or :attr:`4`,
            the DCT matrix will be normalized. Has no effect for :attr:`dct_type=1`.
            Setting normalized to True is equivalent to :attr:`norm="orth"` in
            `scipy.fftpack.dct <https://docs.scipy.org/doc/scipy/reference/generated/scipy.fftpack.dct.html>`_

    Shape:
        - Input: :math:`(*, N)` where :math:`N` is :attr:`in_features`
        - Output: :math:`(*, K)` where :math:`K` is :attr:`out_features`, or :attr:`in_features` if
          :attr:`out_features` is not specified.
    """
    def __init__(self, in_features, out_features=None, dct_type=2, normalized=True):
        super().__init__()
        weight = get_dct_matrix(n=in_features, n_out=out_features, dct_type=dct_type,
            normalized=normalized)
        self.weight = nn.Parameter(weight, requires_grad=False)

    def forward(self, x):
        r"""
        Args:
            x (Tensor): Input, of shape :math:`(*, N)`
        Returns:
            - Output, of shape :math:`(*, K)` where :math:`K` is :attr:`out_features`,
                or :attr:`in_features` if :attr:`out_features` is not specified.
        """
        return torch.matmul(x, self.weight)

class MaxMin(nn.Module):
    def __init__(self):
        super().__init__()
        self.gt0 = atomics.Gt0()

    def forward(self, x, y):
        x_g = self.gt0(x - y)
        y_g = 1 - x_g
        max_els = x_g*x + y_g*y
        min_els = y_g*x + x_g*y
        return max_els, min_els

class LogEps(nn.Module):
    r"""
    Natural logarithm with a minimum floor. Minimum floor is automatically
    tuned when exposed to data. The minimum floor ensures numerical stability.

    Returns:

        .. math::

            \text{output} = \begin{cases}
                \log(x) & x > \epsilon \\
                \log(\epsilon) & x \leq \epsilon
            \end{cases}
    """
    def __init__(self):
        super().__init__()
        self.add_eps = TuningEpsilon()

    def forward(self, x):
        """
        """
        x = self.add_eps(x)
        return torch.log(x)

class Magnitude(nn.Module):
    r"""
    Computes magnitude from real and imaginary parts.

    Mathematically equivalent to

    .. math::

        \text{mag} = \sqrt{\text{Re}^2 + \text{Im}^2},

    but designed to compress the signal as minimally as possible when quantized:

    .. math::

        &a_{max} = \text{max}(|\text{Re}|, |\text{Im}|) \\
        &a_{min} = \text{min}(|\text{Re}|, |\text{Im}|) \\
        &\text{mag} = a_{max}\sqrt{1 + \frac{a_{min}}{a_{max}}^2}

    .. note::

        .. math::

            \sqrt{1 + x^2} = \cos{\arctan{x}}
    """
    def __init__(self):
        super().__init__()
        self.add_epsilon = TuningEpsilon()
        self.max_min = MaxMin()
        self.mul = atomics.VVMul()

    def forward(self, real, imag):
        """
        Args:
            real (Tensor): Real part of input
            imag (Tensor): Imaginary part of input

        Returns:
            - Magnitude
        """
        a, b = self.max_min(real.abs(), imag.abs())
        eta = b / self.add_epsilon(a)
        eta_p = cos_arctan(eta)
        return self.mul(a, eta_p)

# class STFT(nn.Module):
#     r"""
#     Short Time Fourier Transform.

#     The STFT of an input sequence takes the real-to-complex fourier transform (:class:`RFFT`)
#     of overlapping windows of the input sequence. An optional window function can be applied
#     to each window before taking the fourier transform. The output of the STFT is a complex
#     sequence whose magnitude over time represents the changing frequency content of the input
#     signal.

#     Under the hood, this STFT is implemented as a strided :class:`fmot.nn.conv1d.TemporalConv1d`.

#     .. todo::

#         - Describe how padding works
#         - Provide an equation for the STFT

#     Args:
#         n_dft (int): Number of samples in fourier transform
#         hop_length (int): Number of samples between neighboring windows, default is
#             :math:`\lfloor \text{n_dft}/4 \rfloor`.
#         normalized (bool): Whether to use a normalized FFT, default False
#         window_function (Tensor): An optional tensor of length :attr:`n_dft`. If
#             :attr:`None`, a tensor of all ones is used instead (default).

#     Shape:
#         - Input: :math:`(N, 1, L_{in})` where :math:`N` is the batch size and :math:`L_{in}`
#           is the input sequence length.
#         - Real Output: :math:`(N, C_{out}, L_{out})`
#         - Imag Output: :math:`(N, C_{out}, L_{out})`

#         .. math::

#             &C_{out} = \Big\lfloor \frac{\text{n_dft}}{2} + 1 \Big\rfloor \\
#             &L_{out} = \Big\lfloor \frac{L_{in}}{\text{hop_length}} \Big\rfloor
#     """
#     def __init__(self, n_dft, hop_length=None, normalized=False, window_function=None):
#         super().__init__()
#         self.n_dft = n_dft
#         if hop_length is None:
#             self.hop_length = n_dft//4
#         else:
#             self.hop_length = hop_length
#         w_real, w_imag = get_rfft_matrix(n_dft, normalized)
#         w_real, w_imag = w_real.t(), w_imag.t()
#         if window_function is not None:
#             assert len(window_function) == n_dft, 'Window function was not the correct length'
#             w_real *= window_function
#             w_imag *= window_function
#         self.conv = TemporalConv1d(
#             in_channels=1,
#             out_channels=(n_dft//2 + 1)*2,
#             kernel_size=n_dft,
#             stride=self.hop_length,
#             bias=False)
#         kernel = torch.cat([w_real, w_imag], 0).unsqueeze(1)
#         self.conv.conv.weight = nn.Parameter(kernel, requires_grad=False)

#     def forward(self, x: Tensor) -> Tuple[Tensor, Tensor]:
#         """
#         """
#         real, imag = self.conv(x).chunk(chunks=2, dim=1)
#         return real, imag

class MelFilterBank(nn.Module):
    r"""
    Project FFT bins into Mel-Frequency bins.

    Applies a linear transformation to project FFT bins into Mel-frequency bins.

    Args:
        sr (int): audio sampling rate (in Hz)
        n_dft (int): number of FFT frequencies
        n_mels (int): number of mel-frequencies to create
        fmin (float): lowest frequency (in Hz), default is 0
        fmax (float): maximum frequency (in Hz). If :attr:`None`, the Nyquist frequency
            :attr:`sr/2.0` is used. Default is :attr:`None`.
        **kwargs: keyword arguments to pass to
            `librosa.filters.mel <https://librosa.org/doc/latest/generated/librosa.filters.mel.html>`_
            when generating the mel transform matrix

    Shape:
        - Input: :math:`(*, C_{in})` where :math:`*` is any number of dimensions and
          :math:`C_{in} = \lfloor \text{n_dft}/2 + 1 \rfloor`
        - Output: :math:`(*, \text{n_mels})`

    .. seealso::

        - :class:`MelSpectrogram`

    .. todo::

        Compute the Mel transform matrix internally, getting rid of librosa
        dependency?
    """
    def __init__(self, sr, n_dft, n_mels=128, fmin=0.0, fmax=None, **kwargs):
        super().__init__()
        weight = get_mel_matrix(sr, n_dft, n_mels, fmin, fmax, **kwargs)
        self.weight = nn.Parameter(weight.t(), requires_grad=False)

    def forward(self, x):
        """
        """
        return torch.matmul(x, self.weight)

# class MelSpectrogram(nn.Module):
#     r"""
#     Compute a mel-scaled spectrogram from input time-series signal.

#     Combines :class:`STFT`, :class:`Magnitude`, and :class:`MelFilterBank`.

#     .. math::

#         S_{mel} = \text{Mel}(\text{mag}(\text{STFT}(x)))

#     Args:
#         sr (int): audio sampling rate (in Hz)
#         n_dft (int): Number of samples in fourier transform
#         hop_length (int): Number of samples between neighboring windows, default is
#             :math:`\lfloor \text{n_dft}/4 \rfloor`.
#         normalized (bool): Whether to use a normalized FFT, default False
#         window_function (Tensor): An optional tensor of length :attr:`n_dft`. If
#             :attr:`None`, a tensor of all ones is used instead (default).
#         n_mels (int): number of mel-frequencies to create
#         fmin (float): lowest frequency (in Hz), default is 0
#         fmax (float): maximum frequency (in Hz). If :attr:`None`, the Nyquist frequency
#             :attr:`sr/2.0` is used. Default is :attr:`None`.
#         power (float, int): power to raise STFT magnitude before projection to mel frequencies.
#             Defualt is :attr:`2.0`.
#         **kwargs: keyword arguments to pass to
#             `librosa.filters.mel <https://librosa.org/doc/latest/generated/librosa.filters.mel.html>`_
#             when generating the mel transform matrix

#     Shape:
#         - Input: :math:`(N, 1, L_{in})` where :math:`N` is the batch size and :math:`L_{in}`
#           is the input sequence length.
#         - Output: :math:`(N, \text{n_mels}, L_{out})`

#         .. math::

#             L_{out} = \Big\lfloor \frac{L_{in}}{\text{hop_length}} \Big\rfloor

#     .. seealso::

#         - :class:`STFT`
#         - :class:`MelSpectrogram`
#         - :class:`MFCC`

#     """
#     def __init__(self, sr, n_dft, hop_length=None, normalized=False, window_function=None,
#                  n_mels=128, fmin=0.0, fmax=None, power=2.0, **kwargs):
#         super().__init__()
#         self.stft = STFT(n_dft, hop_length=hop_length, normalized=normalized,
#                          window_function=window_function)
#         self.abs = Magnitude()
#         self.power = power
#         self.mel_filter = MelFilterBank(sr, n_dft, n_mels=n_mels, fmin=fmin, fmax=fmax, **kwargs)

#     def forward(self, x):
#         """Call the STFT on x"""
#         S_real, S_imag = self.stft(x)
#         S_mag = self.abs(S_real, S_imag)
#         S_pow = S_mag**self.power
#         return self.mel_filter(S_pow.transpose(1,2)).transpose(1,2)

# class MFCC(nn.Module):
#     r"""
#     Computes Mel Frequency Cepstral Coefficients.

#     Combines :class:`STFT`, :class:`Magnitude`, :class:`MelFilterBank`,
#     :class:`LogEps`, and :class:`DCT`.

#     .. math::

#         S_{mfcc} = \text{DCT}(\text{LogEps}(\text{Mel}(\text{Mag}(\text{STFT}(x)))))

#     See Input/Output shape requirements

#     Args:
#         sr (int): audio sampling rate (in Hz)
#         n_dft (int): Number of samples in fourier transform
#         n_mfccs (int): Number of cepstral coefficients to compute
#         n_mels (int): Number of mel frequencies to compute, default is :attr:`n_mfccs`
#         hop_length (int): Number of samples between neighboring windows, default is
#             :math:`\lfloor \text{n_dft}/4 \rfloor`.
#         normalized (bool): Whether to use a normalized FFT, default False
#         window_function (Tensor): An optional tensor of length :attr:`n_dft`. If
#             :attr:`None`, a tensor of all ones is used instead (default).
#         n_mels (int): number of mel-frequencies to create
#         fmin (float): lowest frequency (in Hz), default is 0
#         fmax (float): maximum frequency (in Hz). If :attr:`None`, the Nyquist frequency
#             :attr:`sr/2.0` is used. Default is :attr:`None`.
#         power (float, int): power to raise STFT magnitude before projection to mel frequencies.
#             Defualt is :attr:`2.0`.
#         log_epsilon (float): minimum input value to log, default is :math:`10^{-10}`.
#         **kwargs: keyword arguments to pass to
#             `librosa.filters.mel <https://librosa.org/doc/latest/generated/librosa.filters.mel.html>`_
#             when generating the mel transform matrix

#     Shape:
#         - Input: :math:`(N, 1, L_{in})` where :math:`N` is the batch size and :math:`L_{in}`
#           is the input sequence length.
#         - Output: :math:`(N, \text{n_mfcc}, L_{out})`

#         .. math::

#             L_{out} = \Big\lfloor \frac{L_{in}}{\text{hop_length}} \Big\rfloor

#     .. seealso::

#         - :class:`STFT`
#         - :class:`MelSpectrogram`
#         - :class:`Magnitude`
#         - :class:`LogEps`

#     """
#     def __init__(self, sr, n_dft, n_mfccs, n_mels=None, hop_length=None, normalized=False,
#         window_function=None, fmin=0.0, fmax=None, power=2.0, log_epsilon=1e-10, **kwargs):
#         super().__init__()
#         if n_mels is None:
#             n_mels = n_mfccs
#         if n_mfccs > n_mels:
#             raise ValueError('Cannot have more mfcc features than mel features.')
#         self.melspec = MelSpectrogram(
#             sr=sr,
#             n_dft=n_dft,
#             hop_length=hop_length,
#             normalized=normalized,
#             window_function=window_function,
#             n_mels=n_mels,
#             fmin=fmin,
#             fmax=fmax,
#             power=power)
#         self.log_max = LogEps(log_epsilon)
#         self.dct = DCT(in_features=n_mels, out_features=n_mfccs, normalized=True, dct_type=2)

#     def forward(self, x):
#         """
#         """
#         y = self.melspec(x).transpose(1, 2)
#         y = self.log_max(y)
#         y = self.dct(y).transpose(1, 2)
#         return y
