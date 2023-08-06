import torch as th
import torch.nn as nn
import dgl.nn as dglnn
import torch.nn.functional as F




class RelGraphEmbed(nn.Module):
    r"""Embedding layer for featureless heterograph.

    Parameters
    ----------
    g : DGLGraph
        Input graph.
    embed_size : int
        The length of each embedding vector
    exclude : list[str]
        The list of node-types to exclude (e.g., because they have natural features)
    """

    def __init__(self, g, embed_size, exclude=list()):

        super(RelGraphEmbed, self).__init__()
        self.g = g
        self.embed_size = embed_size

        # create learnable embeddings for all nodes, except those with a node-type in the "exclude" list
        self.embeds = nn.ParameterDict()
        for ntype in g.ntypes:
            if ntype in exclude:
                continue
            embed = nn.Parameter(th.Tensor(g.number_of_nodes(ntype), self.embed_size))
            self.embeds[ntype] = embed

        self.reset_parameters()

    def reset_parameters(self):
        for emb in self.embeds.values():
            nn.init.xavier_uniform_(emb)

    def forward(self, block=None):
        return self.embeds


class RelGraphConvLayer(nn.Module):
    r"""Relational graph convolution layer.

    Parameters
    ----------
    in_feat : int
        Input feature size.
    out_feat : int
        Output feature size.
    ntypes : list[str]
        Node type names
    rel_names : list[str]
        Relation names.
    weight : bool, optional
        True if a linear layer is applied after message passing. Default: True
    bias : bool, optional
        True if bias is added. Default: True
    activation : callable, optional
        Activation function. Default: None
    self_loop : bool, optional
        True to include self loop message. Default: False
    dropout : float, optional
        Dropout rate. Default: 0.0
    """

    def __init__(self,
                 in_feat,
                 out_feat,
                 ntypes,
                 rel_names,
                 *,
                 weight=True,
                 bias=True,
                 activation=None,
                 self_loop=False,
                 dropout=0.0):
        super(RelGraphConvLayer, self).__init__()
        self.in_feat = in_feat
        self.out_feat = out_feat
        self.ntypes = ntypes
        self.rel_names = rel_names
        self.bias = bias
        self.activation = activation
        self.self_loop = self_loop

        self.conv = dglnn.HeteroGraphConv({
            rel: dglnn.GraphConv(in_feat, out_feat, norm='right', weight=False, bias=False)
            for rel in rel_names
        })

        self.use_weight = weight
        if self.use_weight:
            self.weight = nn.ModuleDict({
                rel_name: nn.Linear(in_feat, out_feat, bias=False)
                for rel_name in self.rel_names
            })

        # weight for self loop
        if self.self_loop:
            self.loop_weights = nn.ModuleDict({
                ntype: nn.Linear(in_feat, out_feat, bias=bias)
                for ntype in self.ntypes
            })

        self.dropout = nn.Dropout(dropout)

        self.reset_parameters()

    def reset_parameters(self):
        if self.use_weight:
            for layer in self.weight.values():
                layer.reset_parameters()

        if self.self_loop:
            for layer in self.loop_weights.values():
                layer.reset_parameters()

    def forward(self, g, inputs):
        """Forward computation

        Parameters
        ----------
        g : DGLHeteroGraph
            Input graph.
        inputs : dict[str, torch.Tensor]
            Node feature for each node type.

        Returns
        -------
        dict[str, torch.Tensor]
            New node features for each node type.
        """
        g = g.local_var()
        if self.use_weight:
            wdict = {rel_name: {'weight': self.weight[rel_name].weight.T}
                     for rel_name in self.rel_names}
        else:
            wdict = {}

        if g.is_block:
            inputs_dst = {k: v[:g.number_of_dst_nodes(k)] for k, v in inputs.items()}
        else:
            inputs_dst = inputs

        hs = self.conv(g, inputs, mod_kwargs=wdict)

        def _apply(ntype, h):
            if self.self_loop:
                h = h + self.loop_weights[ntype](inputs_dst[ntype])
            if self.activation:
                h = self.activation(h)
            return self.dropout(h)

        return {ntype: _apply(ntype, h) for ntype, h in hs.items()}


class EntityClassify(nn.Module):
    r"""
    R-GCN node classification model

    Parameters
    ----------
    g : DGLGraph
        The heterogenous graph used for message passing
    in_dim : int
        Input feature size.
    h_dim : int
        Hidden dimension size.
    out_dim : int
        Output dimension size.
    num_hidden_layers : int, optional
        Number of RelGraphConvLayers. Default: 1
    dropout : float, optional
        Dropout rate. Default: 0.0
    use_self_loop : bool, optional
        True to include self loop message in RelGraphConvLayers. Default: True
    """

    def __init__(self,
                 g, in_dim,
                 h_dim, out_dim,
                 num_hidden_layers=1,
                 dropout=0,
                 use_self_loop=True):
        super(EntityClassify, self).__init__()
        self.g = g
        self.in_dim = in_dim
        self.h_dim = h_dim
        self.out_dim = out_dim
        self.rel_names = list(set(g.etypes))
        self.rel_names.sort()
        self.num_hidden_layers = num_hidden_layers
        self.dropout = dropout
        self.use_self_loop = use_self_loop

        self.layers = nn.ModuleList()
        # i2h
        self.layers.append(RelGraphConvLayer(
            self.in_dim, self.h_dim, g.ntypes, self.rel_names,
            activation=F.relu, self_loop=self.use_self_loop,
            dropout=self.dropout))
        # h2h
        for _ in range(self.num_hidden_layers):
            self.layers.append(RelGraphConvLayer(
                self.h_dim, self.h_dim, g.ntypes, self.rel_names,
                activation=F.relu, self_loop=self.use_self_loop,
                dropout=self.dropout))
        # h2o
        self.layers.append(RelGraphConvLayer(
            self.h_dim, self.out_dim, g.ntypes, self.rel_names,
            activation=None,
            self_loop=self.use_self_loop))

    def reset_parameters(self):
        for layer in self.layers:
            layer.reset_parameters()

    def forward(self, h, blocks):
        for layer, block in zip(self.layers, blocks):
            h = layer(block, h)
        return h


class Logger(object):
    r"""
    This class was taken directly from the PyG implementation and can be found
    here: https://github.com/snap-stanford/ogb/blob/master/examples/nodeproppred/mag/logger.py

    This was done to ensure that performance was measured in precisely the same way
    """

    def __init__(self, runs, info=None):
        self.info = info
        self.results = [[] for _ in range(runs)]

    def add_result(self, run, result):
        assert len(result) == 3
        assert run >= 0 and run < len(self.results)
        self.results[run].append(result)

    def print_statistics(self, run=None):
        if run is not None:
            result = 100 * th.tensor(self.results[run])
            argmax = result[:, 1].argmax().item()
            print(f'Run {run + 1:02d}:')
            print(f'Highest Train: {result[:, 0].max():.2f}')
            print(f'Highest Valid: {result[:, 1].max():.2f}')
            print(f'  Final Train: {result[argmax, 0]:.2f}')
            print(f'   Final Test: {result[argmax, 2]:.2f}')
        else:
            result = 100 * th.tensor(self.results)

            best_results = []
            for r in result:
                train1 = r[:, 0].max().item()
                valid = r[:, 1].max().item()
                train2 = r[r[:, 1].argmax(), 0].item()
                test = r[r[:, 1].argmax(), 2].item()
                best_results.append((train1, valid, train2, test))

            best_result = th.tensor(best_results)

            print(f'All runs:')
            r = best_result[:, 0]
            print(f'Highest Train: {r.mean():.2f} ± {r.std():.2f}')
            r = best_result[:, 1]
            print(f'Highest Valid: {r.mean():.2f} ± {r.std():.2f}')
            r = best_result[:, 2]
            print(f'  Final Train: {r.mean():.2f} ± {r.std():.2f}')
            r = best_result[:, 3]
            print(f'   Final Test: {r.mean():.2f} ± {r.std():.2f}')





