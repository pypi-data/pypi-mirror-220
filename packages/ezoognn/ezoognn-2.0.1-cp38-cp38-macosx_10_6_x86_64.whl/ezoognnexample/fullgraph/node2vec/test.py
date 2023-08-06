import dgl
import torch
from dgl import backend as F

g1 = dgl.heterograph({
    ('user', 'follow', 'user'): ([0, 1, 2], [1, 2, 0])
})
g2 = dgl.heterograph({
    ('user', 'follow', 'user'): ([0, 1, 1, 2, 3], [1, 2, 3, 0, 0])
})
g2.edata['p'] = torch.tensor([3, 0, 3, 3, 3], dtype=torch.float32)

ntypes = torch.zeros((5,), dtype=torch.int64)

traces, eids = dgl.sampling.node2vec_random_walk(g1, [0, 1, 2, 0, 1, 2], 1, 1, 4, return_eids=True)

def check_random_walk(g, metapath, traces, ntypes, prob=None, trace_eids=None):
    traces = F.asnumpy(traces)
    ntypes = F.asnumpy(ntypes)
    for j in range(traces.shape[1] - 1):
        assert ntypes[j] == g.get_ntype_id(g.to_canonical_etype(metapath[j])[0])
        assert ntypes[j + 1] == g.get_ntype_id(g.to_canonical_etype(metapath[j])[2])

    for i in range(traces.shape[0]):
        for j in range(traces.shape[1] - 1):
            between = g.has_edge_between(traces[i, j], traces[i, j + 1], etype=metapath[j])
            assert between
            if prob is not None and prob in g.edges[metapath[j]].data:
                p = F.asnumpy(g.edges[metapath[j]].data['p'])
                eids = g.edge_ids(traces[i, j], traces[i, j+1], etype=metapath[j])
                assert p[eids] != 0
            if trace_eids is not None:
                u, v = g.find_edges(trace_eids[i, j], etype=metapath[j])
                assert (u == traces[i, j]) and (v == traces[i, j + 1])

check_random_walk(g1, ['follow'] * 4, traces, ntypes, trace_eids=eids)

traces, eids = dgl.sampling.node2vec_random_walk(
    g2, [0, 1, 2, 3, 0, 1, 2, 3], 1, 1, 4, prob='p', return_eids=True)
check_random_walk(g2, ['follow'] * 4, traces, ntypes, 'p', trace_eids=eids)


a = torch.arange(3*5).reshape(3,5).view(-1)
b = torch.nonzero(a==10).squeeze()
print(b) # tensor(10)

sdfsd = torch.empty((2705, 128))
weights = torch.rand(10, 3)
weights[0, :].zero_()
embedding_matrix = weights
input = torch.tensor([[0,2,0,5,9,4]])
xxx = torch.nn.functional.embedding(input, embedding_matrix, padding_idx=0)
yyyy = xxx.numpy()
print(xxx)
