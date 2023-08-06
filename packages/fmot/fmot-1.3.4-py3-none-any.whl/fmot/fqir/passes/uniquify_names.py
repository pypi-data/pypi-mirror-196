from fmot import fqir
from collections import defaultdict

def uniquify_names(graph: fqir.GraphProto):
    try:
        arith = graph.subgraphs['ARITH']
    except:
        arith = graph

    name2tensors = defaultdict(set)

    def add_tensor(x: fqir.TensorProto):
        name2tensors[x.name].add(x)

    for node in arith.nodes:
        for x in node.inputs.values():
            add_tensor(x)
        for x in node.outputs:
            add_tensor(x)
    
    for name, tensors in name2tensors.items():
        if len(tensors) > 1:
            for i, t in enumerate(tensors):
                t.name = f'{name}.{i}'
    
    return graph
            
    