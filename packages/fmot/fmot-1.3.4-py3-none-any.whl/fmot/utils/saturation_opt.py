"""
A tool used to insert FixedRangeObservers into a model with saturating 
nonlinearities. Saturating nonlinearities such as sigmoid and tanh are insensitive 
to inputs with magnitudes greater than 8 and 4, respectively. 
"""
import fmot
import torch
import networkx as nx
from collections import defaultdict
import functools

__all__ = ['insert_fixed_range_observers']

# All atomic modules that we want to trace into nx.DiGraph
ATOMICS = [
    fmot.qat.nn.VVAdd,
    fmot.qat.nn.VIAdd,
    fmot.qat.nn.VVSub,
    fmot.qat.nn.Neg,
    fmot.qat.nn.VVMul,
    fmot.qat.nn.VIMul,
    fmot.qat.nn.Matmul,
    fmot.qat.nn.AddMM,
    fmot.qat.nn.ReLU,
    fmot.qat.nn.Transpose,
    fmot.qat.nn.FTranspose,
    fmot.qat.nn.Reshape,
    fmot.qat.nn.Chunk,
    fmot.qat.nn.BareCat,
    fmot.qat.nn.Stack,
    fmot.qat.nn.Sum,
    fmot.qat.nn.OnesLike,
    fmot.qat.nn.Shift,
    fmot.qat.nn.Requantize,
    fmot.qat.nn.Gt0,
    fmot.qat.nn.LUT,
    fmot.qat.nn.RSqrtPlusEps,
    fmot.qat.nn.PowFrac,
    fmot.qat.nn.BareLUT
]

# All atomic modules that pass a fixed domain to their predecessors.
# No multiply or LUT atomics.
FR_ATOMICS = [
    fmot.qat.nn.VVAdd,
    fmot.qat.nn.VIAdd,
    fmot.qat.nn.VVSub,
    fmot.qat.nn.Neg,
    fmot.qat.nn.ReLU,
    fmot.qat.nn.Transpose,
    fmot.qat.nn.FTranspose,
    fmot.qat.nn.Reshape,
    fmot.qat.nn.Chunk,
    fmot.qat.nn.BareCat,
    fmot.qat.nn.Stack,
    fmot.qat.nn.Shift,
    fmot.qat.nn.Requantize,
    fmot.qat.nn.Gt0
]

def hook_layer(module, graph):
    """
    A hook function that adds a node and edges to a 
    networkx digraph during tracing. Modifies graph in-place.

    Args:
        module (torch.nn.Module): layer to add to graph during tracing
        graph (nx.DiGraph): directed acyclic graph

    Returns:
        - RemoveableHandle
    """

    module._called = False
    def hook_fn(module, inputs, outputs):
        if module._called:
            return outputs
        else:
            module._called = True

        graph.add_node(module)
        if isinstance(inputs, torch.Tensor):
            inputs = (inputs,)
        for i in inputs:
            if hasattr(i, 'node'):
                graph.add_edge(i.node, module)
        if isinstance(outputs, torch.Tensor):
            outputs.node = module
            return outputs
        else:
            for o in outputs:
                o.node = module
            return outputs
    return module.register_forward_hook(hook_fn)

def trace_graph(model, x):
    """
    Trace an nx.DiGraph with input x. Graph is not guaranteed to be perfect
    (i.e. not good enough to use as a program), but will be good enough
    to recursively backtrack to apply fixed-range observers to the model.

    Args:
        model (torch.nn.Module): Converted pytorch model
        x (torch.Tensor, tuple(torch.Tensor)): tracing input(s) to the model

    Returns:
        - Graph (nx.DiGraph). Nodes are atomic modules, and directed edges denote
            data dependencies
    """
    G = nx.DiGraph()
    handles = []
    for module in model.modules():
        if type(module) in ATOMICS:
            handles.append(hook_layer(module, G))
    if isinstance(x, tuple):
        __ = model(*x)
    else:
        __ = model(x)
    for h in handles:
        h.remove()
    return G

def get_vvmul_preds(graph, node, recurse=True):
    parents = list(graph.predecessors(node))
    if len(parents) != 2:
        return []

    lut_parents = [p for p in parents if isinstance(p, fmot.qat.nn.LUT)]
    nonlut_parents = [p for p in parents if p not in lut_parents]
    if len(lut_parents) != 1:
        return []

    lut_parent = lut_parents[0]
    nonlut_parent = nonlut_parents[0]
    if lut_parent.function not in [torch.sigmoid, torch.tanh]:
        return []

    preds = [nonlut_parent]
    if recurse:
        preds += get_fixed_range_preds(graph, nonlut_parent, recurse=True,
            use_vvmul=True)
    return preds


def get_fixed_range_preds(graph, node, recurse=True, use_vvmul=False):
    """
    Returns a list of predecessors for a given node in the graph. If 
    :attr:`recurse=True`, will recursively add predecessors of predecessors,
    but only recursing through layers in :attr:`FR_ATOMICS` (the set of nodes
    that passes fixed domains to parents).

    Args:
        graph (nx.DiGraph): DiGraph representation of the model (i.e. from
            :attr:`trace_graph()`)
        node (torch.nn.Module): The node, whose predecessors we want
        recurse (bool): Whether to recurse, default is :attr:`True`
    Returns:
        - Predecessors (list[torch.nn.Module]): A list of all the predecessor
            nodes
    """
    assert node in graph.nodes
    preds = []
    for n in graph.predecessors(node):
        preds.append(n)
        if recurse:
            if type(n) in FR_ATOMICS:
                preds += get_fixed_range_preds(graph, n, recurse=True)
            elif isinstance(n, fmot.qat.nn.VVMul) and use_vvmul:
                preds += get_vvmul_preds(graph, n, recurse=True)
    return preds

def build_limits_dict(graph, use_vvmul=False):
    """
    For each LUT layer, recursively backtrack to find candidate limits for
    predecessor nodes in the graph. Each predecessor node will have one or more
    candidate limits (more than one if it is predecessor to more than one LUT).

    Args:
        graph (nx.DiGraph): A directed acyclic graph, output by :attr:`trace_graph()`
    Returns:
        A dictionary, connecting predecessor nodes to a list of candidate limits.
    """
    candidates = defaultdict(list)
    for node in graph.nodes:
        if isinstance(node, fmot.qat.nn.LUT):
            limits = node.limits
            preds = get_fixed_range_preds(graph, node, recurse=True,
                use_vvmul=use_vvmul)
            for p in preds:
                candidates[p].append(limits)
    return candidates

def arbitrate_limits(candidates):
    """
    Finds largest limits among all candidates. If all candidates are 
    (None, None), will return (None, None)

    Args:
        candidates (list[tuple]): List of (min, max) limit candidates
    Returns:
        limits, a (min, max) tuple. 
    """
    l0, l1 = (None, None)
    for (c0, c1) in candidates:
        if l0 is None:
            l0 = c0
        elif c0 < l0:
            l0 = c0
        
        if l1 is None:
            l1 = c1
        elif c1 > l1:
            l1 = c1
    return (l0, l1)

def rsetattr(obj, attr, val):
    pre, _, post = attr.rpartition('.')
    return setattr(rgetattr(obj, pre) if pre else obj, post, val)

def rgetattr(obj, attr, *args):
    if attr == '':
        return obj
    def _getattr(obj, attr):
        return getattr(obj, attr, *args)
    return functools.reduce(_getattr, [obj] + attr.split('.'))

def apply_fixed_ranges(limits_dict, scaling=1., verbose=False):
    """
    Apply :attr:`FixedRangeWrappedObserver` layers to all of the predecessor layers.

    For each :attr:`layer: [candidate_limits]` pair in the limits dictionary,
    arbitrate to find an optimal limits tuple. This limits tuple is used to apply
    a :attr:`FixedRangeWrappedObserver` to the layer's quantizer/observer.

    The observers are updated in-place, so this function has no returned value.

    Args:
        limits_dict (dict): A dictionary of :attr:`layer: limits[]` pairs, as
            output from :attr:`build_limits_dict()`
        scaling (float): A scaling factor to increase headroom above the saturating
            range. Should be >= 1, default is :attr:`1`.
        verbose (bool): If :attr:`True`, will print out details each time an
            observer is wrapped.
    """
    for layer, candidates in limits_dict.items():
        limits = arbitrate_limits(candidates)
        if limits != (None, None):
            # rescale limits
            l0, l1 = limits
            if l0 is not None:
                l0 *= scaling
            if l1 is not None:
                l1 *= scaling
            limits = (l0, l1)
            # replace observers with fixed-range
            for name, module in layer.named_modules():
                if isinstance(module, fmot.qat.nn.ObserverBase):
                    new_obs = fmot.qat.nn.FixedRangeWrappedObserver(
                        limits, module, hard_maximum=False)
                    rsetattr(layer, name, new_obs)
                    if verbose:
                        print(f'Applied limits {limits} to {layer}')

def insert_fixed_range_observers(model, x, scaling=1, in_place=True, 
    verbose=False, use_vvmul=True):
    """
    Recurse backwards from each saturating nonlinearity to apply fixed-range
    observers to predecessor layers. This restricts dynamic range prior to 
    saturating nonlinearities like sigmoid and tanh, to make the most of 
    dynamic range once the model is quantized.

    Args:
        model (torch.nn.Module): Converted pytorch model
        x (torch.Tensor or tuple(torch.Tensor)): Input(s) to the model, for tracing
            purposes
        scaling (float): Optional scaling factor for dynamic ranges. Should be 
            >= 1. Default is 1.
        in_place (bool): Whether to modify the model in-place or to modify a replica.
            Default is False.
        verbose (bool): Print out details about the insertion of 
            :attr:`FixedRangeWrappedObserver` layers.
        use_vvmul (bool): If True, passes fixed range through VVMUL if one of the
            operands is the output of a sigmoid or tanh nonlinearity. Default True.
    """
    if not in_place:
        raise NotImplementedError('non-in-place conversion not yet implemented')
    graph = trace_graph(model, x)
    limits = build_limits_dict(graph, use_vvmul=use_vvmul)
    apply_fixed_ranges(limits, scaling=scaling, verbose=verbose)






