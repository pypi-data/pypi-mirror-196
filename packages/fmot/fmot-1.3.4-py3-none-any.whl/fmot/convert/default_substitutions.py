import fmot
import torch
from ..nn.sru import SRU


DEFAULT_SUBSTITUTIONS = {
    torch.nn.modules.rnn.RNN: fmot.nn.RNN,
    torch.nn.modules.rnn.GRU: fmot.nn.GRU,
    # torch.nn.modules.rnn.LSTM: fmot.nn.LSTM,
    # torch.nn.modules.conv.Conv1d: fmot.nn.Conv1d
    fmot.nn.TemporalConv1d: fmot.nn.conv1d.FmotConv1dWrapper,
    SRU: fmot.nn.SRUSequencer
}
