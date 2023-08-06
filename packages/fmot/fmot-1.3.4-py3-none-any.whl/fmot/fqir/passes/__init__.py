from .batchdim_removal import remove_batchdim
from .dimtag_removal import remove_named_dims
from .kernelize_lstm import kernelize_lstm
from .kernelize_temporal_unfold import kernelize_temporal_unfold
from .uniquify_names import uniquify_names


PASS_ORDER = [
    kernelize_lstm,
    uniquify_names,
    kernelize_temporal_unfold
]

def run_passes(graph):
    for p in PASS_ORDER:
        p(graph)
