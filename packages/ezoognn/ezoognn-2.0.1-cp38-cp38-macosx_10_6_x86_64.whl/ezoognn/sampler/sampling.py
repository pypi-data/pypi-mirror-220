import torch
import numpy as np

'''
node2vec采样
'''
def node2vec_random_walk(g, e_graph, nodes, p, q, walk_length, prob=None, return_eids=False):
    if prob is None:
        prob_list = np.array([])
    else:
        prob_list = g.edata[prob].numpy()

    nids, eids = e_graph.sampling_Node2vec(nodes, p, q, walk_length, prob_list)
    nids = torch.from_numpy(nids.astype(np.int64))
    if eids is None:
        return nids
    eids = torch.from_numpy(eids.astype(np.int64))

    return (nids, eids) if return_eids else nids