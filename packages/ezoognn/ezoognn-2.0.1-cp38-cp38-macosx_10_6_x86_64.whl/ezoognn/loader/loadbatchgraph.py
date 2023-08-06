"""
ezoodb：采样的生成器，用于异步回调的迭代
EzooSamplerNodeDataLoader：节点采样
EzooSamplerEdgeDataLoader：边采样
EzooSamplerNeighborDataLoader：邻居采样
"""
from torch.utils.data import DataLoader


class EzooNodeDataLoaderIter:
    def __init__(self, node_dataloader, kwargs):
        self.kwargs = kwargs
        self.device = node_dataloader.device
        self.node_dataloader = node_dataloader
        self.iter_ = iter(node_dataloader.dataloader)

    def __next__(self):
        # input_nodes, output_nodes, blocks
        seed_nodes = next(self.iter_)
        input_nodes, blocks = self.kwargs['block_sampler'].sample_frontier(seed_nodes, self.device)
        return input_nodes, seed_nodes, blocks


class EzooNodeDataLoader:
    def __init__(self, nids, block_sampler, label_name, device='cpu', **kwargs):
        self.nids = nids
        self.block_sampler = block_sampler
        self.label_name = label_name
        # collator_kwargs = {}
        dataloader_kwargs = {}
        for k, v in kwargs.items():
            dataloader_kwargs[k] = v
            # if k in self.collator_arglist:
            #     collator_kwargs[k] = v
            # else:

        # if isinstance(g, dgl.distributed.DistGraph):
        #     # todo: 分布式
        #     self.is_distributed = True
        # else:

        self.is_distributed = False
        self.dataloader = DataLoader(nids, **dataloader_kwargs)
        # 多线程处理
        # if dataloader_kwargs.get('num_workers', 0) > 0:
        #     g.create_formats_()
        self.device = device

    def __iter__(self):
        """Return the iterator of the data loader."""
        if self.is_distributed:
            # todo: Directly use the iterator of DistDataLoader, which doesn't copy features anyway.
            return iter(self.dataloader)
        else:
            args = {'block_sampler': self.block_sampler,
                    'label_name': self.label_name}
            return EzooNodeDataLoaderIter(self, args)

    def __len__(self):
        """Return the number of batches of the data loader."""
        return len(self.dataloader)


class EzooEdgeDataLoaderIter:
    def __init__(self, edge_dataloader, kwargs):
        self.device = edge_dataloader.device
        self.edge_dataloader = edge_dataloader
        self.kwargs = kwargs
        self.iter_ = iter(edge_dataloader.dataloader)

    def __next__(self):
        result_ = next(self.iter_)
        input_nodes, sub_graph, blocks = self.kwargs['block_sampler'].sampler_blocks_edge(result_, self.kwargs['reverse_eids'], self.kwargs['exclude'])
        return input_nodes, sub_graph, blocks


class EzooEdgeDataLoader:
    def __init__(self, eids, block_sampler, exclude, reverse_eids, device='cpu', **kwargs):
        self.eids = eids
        self.block_sampler = block_sampler
        self.exclude = exclude
        self.reverse_eids = reverse_eids

        dataloader_kwargs = {}
        for k, v in kwargs.items():
            dataloader_kwargs[k] = v
            # if k in self.collator_arglist:
            #     collator_kwargs[k] = v
            # else:
            #     dataloader_kwargs[k] = v
        # 负采样常常在训练当中用
        self.dataloader = DataLoader(eids, **dataloader_kwargs)
        self.device = device

    def __iter__(self):
        """Return the iterator of the data loader."""
        args = {'block_sampler': self.block_sampler,
                'reverse_eids': self.reverse_eids,
                'exclude': self.exclude
                }
        return EzooEdgeDataLoaderIter(self, args)

    def __next__(self):
        """Return the number of batches of the data loader."""
        return len(self.dataloader)

    def __len__(self):
        return len(self.dataloader)


class EzooSamplerNeighborDataLoader:
    def __init__(self):
        pass

    def __iter__(self):
        pass

    def __next__(self):
        pass
