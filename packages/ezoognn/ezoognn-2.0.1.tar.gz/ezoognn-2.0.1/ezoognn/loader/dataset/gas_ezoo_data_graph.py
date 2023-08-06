import torch
from .ezoo_data_graph import GetItemGraph, EzooShapeGraphEnum, EzooHeteroGraphDataset, EzooExampleDatasetEnum


class EzooGasGraph(GetItemGraph):
    def __init__(self, e_graph=None, _graph=None, name=None):
        super(EzooGasGraph, self).__init__(e_graph=e_graph, _graph=_graph, name=name)

        self.num_classes = 2

'''
gos：Gossip Cop是国外一个专门报道娱乐新闻和澄清传言绯闻的网站 他们的报道最公正 消息十分可靠.
pol：PolitiFact 数据集：对于新闻报道，提供了原始内容、事实核查结果和全面的事实核查报告。平台根据内容将它们分类为不同的主题和话题
可用于新闻真实性检测的数据集
边采样相关数据集
'''


class EzooGasGraphhDataset(EzooHeteroGraphDataset):
    
    def __init__(self, name=None, rpc_url=None, raw_dir=None, force_reload=False, cfg_file=None, gdi_ptr=0, restore_file='', restore_url='', node_exclude_list=['id', '_ID'], edge_exclude_list=['id', 'forward_id', 'forward_id'], batch_size=0,
                 split_ratio=None, data_path=None, force_download=False):
        self.batch_size = batch_size
        super(EzooGasGraphhDataset, self).__init__(name, rpc_url, raw_dir, force_reload, cfg_file, gdi_ptr, restore_file, restore_url, node_exclude_list, edge_exclude_list,
                                                   force_download=force_download)

    def get_label(self, dgl_graph):
        if dgl_graph.ndata.__contains__('labels'):
            return dgl_graph.ndata['labels']
        elif dgl_graph.ndata.__contains__('label'):
            return dgl_graph.ndata['label']

    def __getitem__(self, item):
        super().__getitem__(item)
        return EzooGasGraph(self.e_graph, self.dgl_graph, self.db_name)


    @property
    def num_labels(self):
        return self.number_label

    @property
    def graph(self):
        return self.dgl_graph


class PolEzooGraphDataset(EzooGasGraphhDataset):
    
    def __init__(self, reverse=True, raw_dir=None, force_reload=False,
                 cfg_file=None, gdi_ptr=0, restore_file='', restore_url='', batch_size=0,
                 name=None, split_ratio=None, data_path=None, force_download=False):
        self.reverse = reverse
        super(PolEzooGraphDataset, self).__init__(EzooExampleDatasetEnum.POL.value,
                                                   raw_dir=raw_dir,
                                                   force_reload=force_reload,
                                                   cfg_file=cfg_file, gdi_ptr=gdi_ptr,
                                                   restore_file=restore_file, restore_url=restore_url,
                                                   batch_size=batch_size,
                                                   force_download=force_download)
        
        
class GosEzooGraphDataset(EzooGasGraphhDataset):
    
    def __init__(self, reverse=True, raw_dir=None, force_reload=False,
                 cfg_file=None, gdi_ptr=0, restore_file='', restore_url='', batch_size=0,
                 name=None, split_ratio=None, data_path=None, force_download=False):
        self.reverse = reverse
        super(GosEzooGraphDataset, self).__init__(EzooExampleDatasetEnum.GOS.value,
                                                  raw_dir=raw_dir,
                                                  force_reload=force_reload,
                                                  cfg_file=cfg_file, gdi_ptr=gdi_ptr,
                                                  restore_file=restore_file, restore_url=restore_url,
                                                  batch_size=batch_size,
                                                  force_download=force_download)
        
        

    
