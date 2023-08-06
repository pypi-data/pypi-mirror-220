import torch as th
from .ezoo_data_graph import GetItemGraph, EzooShapeGraphEnum, EzooGraphDataset, EzooExampleDatasetEnum


class LastFM4KGCNEzooGraph(GetItemGraph):
    def __init__(self, e_graph=None, _graph=None, name=None, n_edges=None, train_idx=None, val_idx=None, test_idx=None):
        super(LastFM4KGCNEzooGraph, self).__init__(e_graph=e_graph, _graph=_graph, name=name)

        self.n_edges = n_edges
        self.train_idx = train_idx
        self.val_idx = val_idx
        self.test_idx = test_idx

'''
gos：Gossip Cop是国外一个专门报道娱乐新闻和澄清传言绯闻的网站 他们的报道最公正 消息十分可靠.
pol：PolitiFact 数据集：对于新闻报道，提供了原始内容、事实核查结果和全面的事实核查报告。平台根据内容将它们分类为不同的主题和话题
可用于新闻真实性检测的数据集
边采样相关数据集
'''


class LastFM4KGcnEzooGraphhDataset(EzooGraphDataset):

    def __init__(self, name=None, rpc_url=None, raw_dir=None, force_reload=False, cfg_file=None, gdi_ptr=0, restore_file='', restore_url='', node_exclude_list=['_ID'], edge_exclude_list=['id'], batch_size=0,
                 split_ratio=None, data_path=None, force_download=False):
        self.batch_size = batch_size
        super(LastFM4KGcnEzooGraphhDataset, self).__init__(name, rpc_url, raw_dir, force_reload, cfg_file, gdi_ptr, restore_file, restore_url, node_exclude_list=node_exclude_list, edge_exclude_list=edge_exclude_list,
                                                           force_download=force_download)

    def get_split(self):
        n_edges = self.dgl_graph.num_edges()
        random_int = th.randperm(n_edges)
        train_idx = random_int[:int(n_edges*0.6)]
        val_idx = random_int[int(n_edges*0.6):int(n_edges*0.8)]
        test_idx = random_int[int(n_edges*0.6):int(n_edges*0.8)]
        return n_edges, train_idx, val_idx, test_idx

    def __getitem__(self, item):
        n_edges, train_idx, val_idx, test_idx = self.get_split()
        super().__getitem__(item)
        return LastFM4KGCNEzooGraph(self.e_graph, self._graph, self.db_name, n_edges=n_edges, train_idx=train_idx, val_idx=val_idx, test_idx=test_idx)

    @property
    def num_labels(self):
        return self.number_label

    @property
    def graph(self):
        return self.dgl_graph


class LastFM4KGCN_0EzooGraphhDataset(LastFM4KGcnEzooGraphhDataset):

    def __init__(self, reverse=True, raw_dir=None, force_reload=False,
                 cfg_file=None, gdi_ptr=0, restore_file='', restore_url='', batch_size=0,
                 name=None, split_ratio=None, data_path=None, force_download=False):
        self.reverse = reverse
        super(LastFM4KGCN_0EzooGraphhDataset, self).__init__(EzooExampleDatasetEnum.LASTFM4KGCN_0.value,
                                                             raw_dir=raw_dir,
                                                             force_reload=force_reload,
                                                             cfg_file=cfg_file, gdi_ptr=gdi_ptr,
                                                             restore_file=restore_file, restore_url=restore_url,
                                                             batch_size=batch_size,
                                                             force_download=force_download)


class LastFM4KGCN_1EzooGraphhDataset(LastFM4KGcnEzooGraphhDataset):

    def __init__(self, reverse=True, raw_dir=None, force_reload=False,
                 cfg_file=None, gdi_ptr=0, restore_file='', restore_url='', batch_size=0,
                 name=None, split_ratio=None, data_path=None, force_download=False):
        self.reverse = reverse
        super(LastFM4KGCN_1EzooGraphhDataset, self).__init__(EzooExampleDatasetEnum.LASTFM4KGCN_1.value,
                                                             raw_dir=raw_dir,
                                                             force_reload=force_reload,
                                                             cfg_file=cfg_file, gdi_ptr=gdi_ptr,
                                                             restore_file=restore_file, restore_url=restore_url,
                                                             batch_size=batch_size,
                                                             force_download=force_download)
        
        

    
