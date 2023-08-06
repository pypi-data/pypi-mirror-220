import dgl


def are_graph_identical(g1, g2):
    ret = True

    if not isinstance(g1, dgl.DGLGraph) or not isinstance(g2, dgl.DGLGraph):
        print("The graphs' types are different.")
        ret = False

    if set(g1.ntypes) != set(g2.ntypes) or set(g1.etypes) != set(g2.etypes):
        print('The node types or edge types do not match.')
        ret = False

    if g1.num_nodes() != g2.num_nodes() or g1.num_edges() != g2.num_edges():
        print('The total nodes or edges number do not match.')
        ret = False

    # check each node type
    for ntype in g1.ntypes:
        if g1.number_of_nodes(ntype) != g2.number_of_nodes(ntype):
            print('The node number of the type', ntype, 'are different.')
            ret = False
        # compare node ids for each type
        if set(g1.nodes(ntype).tolist()) != set(g2.nodes(ntype).tolist()):
            print('The node ids of type', ntype, 'are different.')
            ret = False

    # check each edge type
    for etype in g1.etypes:
        if g1.number_of_edges(etype) != g2.number_of_edges(etype):
            print('The edge number of the type', etype, 'are different.')
            ret = False
        # compare source and destination node ids for each edge type
        if set(g1.edges(form='uv', etype=etype)[0].tolist()) != set(g2.edges(form='uv', etype=etype)[0].tolist()):
            print('The start node ids of edge type', etype, 'are different.')
            ret = False
        if set(g1.edges(form='uv', etype=etype)[1].tolist()) != set(g2.edges(form='uv', etype=etype)[1].tolist()):
            print('The end node ids of edge type', etype, 'are different.')
            ret = False

    return ret
