import torch
from .ezoo_data_graph import GetItemGraph, EzooShapeGraphEnum, EzooHeteroGraphDataset, EzooExampleDatasetEnum


class EzooRdfGraph(GetItemGraph):
    def __init__(self, _graph=None, e_graph=None, num_classes=None, predict_category=None, name=None):
        super(EzooRdfGraph, self).__init__(e_graph=e_graph, _graph=_graph, name=name)

        self.num_classes = num_classes
        self.predict_category = predict_category


class EzooRdfGraphhDataset(EzooHeteroGraphDataset):
    
    def __init__(self, name=None, rpc_url=None, raw_dir=None, force_reload=False, cfg_file=None, gdi_ptr=0, restore_file='', restore_url='', node_exclude_list=['id'], edge_exclude_list=['id'], batch_size=0,
                 split_ratio=None, data_path=None, force_download=False):
        self.batch_size = batch_size
        super(EzooRdfGraphhDataset, self).__init__(name, rpc_url, raw_dir, force_reload, cfg_file, gdi_ptr, restore_file, restore_url, node_exclude_list, edge_exclude_list, 
                                                   force_download=force_download)

    def get_label(self, dgl_graph):
        if dgl_graph.ndata.__contains__('labels'):
            return dgl_graph.ndata['labels']
        elif dgl_graph.ndata.__contains__('label'):
            return dgl_graph.ndata['label']

    def __getitem__(self, item):
        super().__getitem__(item)
        if item is EzooShapeGraphEnum.WHOLE:
            label = self.get_label(self.dgl_graph)
            self.number_class = 0
            if label is not None:
                if type(label) == torch.tensor:
                    self.number_class = torch.unique(label).shape[0]
                elif type(label) == dict:
                    for k in label.keys():
                        # 数据集中，只有一个的类别
                        self.number_class = torch.unique(label[k]).shape[0]
                        self.predict_category = k
            
            return EzooRdfGraph(self.dgl_graph, self.e_graph, self.number_class, self.predict_category, self.db_name)
        
        return EzooRdfGraph(self.dgl_graph, self.e_graph, name=self.db_name)
    
    @property
    def num_labels(self):
        return self.number_label
    
    @property
    def graph(self):
        return self.dgl_graph

 
class AifbEzooGraphDataset(EzooRdfGraphhDataset):
    
    def __init__(self, reverse=True, raw_dir=None, force_reload=False,
                 cfg_file=None, gdi_ptr=0, restore_file='', restore_url='', batch_size=0,
                 name=None, split_ratio=None, data_path=None, force_download=False):
        self.reverse = reverse
        super(AifbEzooGraphDataset, self).__init__(EzooExampleDatasetEnum.AIFB.value,
                                                   raw_dir=raw_dir,
                                                   force_reload=force_reload,
                                                   cfg_file=cfg_file, gdi_ptr=gdi_ptr,
                                                   restore_file=restore_file, restore_url=restore_url,
                                                   batch_size=batch_size,
                                                   force_download=force_download)
        
        
class BgsEzooGraphDataset(EzooRdfGraphhDataset):
    
    def __init__(self, reverse=True, raw_dir=None, force_reload=False,
                 cfg_file=None, gdi_ptr=0, restore_file='', restore_url='', batch_size=0,
                 name=None, split_ratio=None, data_path=None, force_download=False):
        self.reverse = reverse
        super(BgsEzooGraphDataset, self).__init__(EzooExampleDatasetEnum.BGS.value,
                                                  raw_dir=raw_dir,
                                                  force_reload=force_reload,
                                                  cfg_file=cfg_file, gdi_ptr=gdi_ptr,
                                                  restore_file=restore_file, restore_url=restore_url,
                                                  batch_size=batch_size,
                                                  force_download=force_download)
        
        
class MutagEzooGraphDataset(EzooRdfGraphhDataset):
    
    def __init__(self, reverse=True, raw_dir=None, force_reload=False,
                 cfg_file=None, gdi_ptr=0, restore_file='', restore_url='', batch_size=0,
                 name=None, split_ratio=None, data_path=None, force_download=False):
        self.reverse = reverse
        super(MutagEzooGraphDataset, self).__init__(EzooExampleDatasetEnum.MUTAG.value,
                                                    raw_dir=raw_dir,
                                                    force_reload=force_reload,
                                                    cfg_file=cfg_file, gdi_ptr=gdi_ptr,
                                                    restore_file=restore_file, restore_url=restore_url,
                                                    batch_size=batch_size,
                                                    force_download=force_download)


class AmEzooGraphDataset(EzooRdfGraphhDataset):

    def __init__(self, reverse=True, raw_dir=None, force_reload=False,
                 cfg_file=None, gdi_ptr=0, restore_file='', restore_url='', batch_size=0,
                 name=None, split_ratio=None, data_path=None, force_download=False):
        self.reverse = reverse
        super(AmEzooGraphDataset, self).__init__(EzooExampleDatasetEnum.AM.value,
                                                 raw_dir=raw_dir,
                                                 force_reload=force_reload,
                                                 cfg_file=cfg_file, gdi_ptr=gdi_ptr,
                                                 restore_file=restore_file, restore_url=restore_url,
                                                 batch_size=batch_size,
                                                 force_download=force_download)

    
