from .ezoo_data_graph import EzooGraphDataset, EzooExampleDatasetEnum, EzooHeteroGraphDataset

 
class OgbnEzooHeteroGraphDataset(EzooHeteroGraphDataset):
    
    def __init__(self, name=EzooExampleDatasetEnum.OGBN_MAG.value, reverse=True, raw_dir=None, force_reload=False,
                 cfg_file=None, gdi_ptr=0, restore_file='', restore_url='',
                 split_ratio=None, data_path=None, force_download=False):
        self.reverse = reverse
        super(OgbnEzooHeteroGraphDataset, self).__init__(name,
                                                         rpc_url=None,
                                                         raw_dir=raw_dir,
                                                         force_reload=force_reload,
                                                         cfg_file=cfg_file, gdi_ptr=gdi_ptr,
                                                         restore_file=restore_file, restore_url=restore_url,
                                                         force_download=force_download)


class OgbnEzooGraphDataset(EzooGraphDataset):

    def __init__(self, name=EzooExampleDatasetEnum.OGBN_PRODUCTS.value, reverse=True, raw_dir=None, force_reload=False,
                 cfg_file=None, gdi_ptr=0, restore_file='', restore_url='',
                 node_type='node',
                 split_ratio=None, data_path=None, force_download=False):
        self.reverse = reverse
        super(OgbnEzooGraphDataset, self).__init__(name,
                                                   rpc_url=None,
                                                   raw_dir=raw_dir,
                                                   force_reload=force_reload,
                                                   cfg_file=cfg_file, gdi_ptr=gdi_ptr,
                                                   restore_file=restore_file, restore_url=restore_url,
                                                   node_type=node_type, cache_node=True, cache_edge=True,
                                                   edge_exclude_list=['*'],
                                                   force_download=force_download)
        

class OgblEzooGraphDataset(EzooGraphDataset):
    
    def __init__(self, name=EzooExampleDatasetEnum.OGBN_DDI.value, reverse=True, raw_dir=None, force_reload=False,
                 cfg_file=None, gdi_ptr=0, restore_file='', restore_url='',
                 node_type='node',
                 split_ratio=None, data_path=None, force_download=False):
        self.reverse = reverse
        super(OgblEzooGraphDataset, self).__init__(name,
                                                   raw_dir=raw_dir,
                                                   force_reload=force_reload,
                                                   cfg_file=cfg_file, gdi_ptr=gdi_ptr,
                                                   restore_file=restore_file, restore_url=restore_url,
                                                   node_type=node_type,
                                                   force_download=force_download)
        
        
class OgbgEzooGraphDataset(EzooGraphDataset):
    
    def __init__(self, name='', reverse=True, raw_dir=None, force_reload=False,
                 cfg_file=None, gdi_ptr=0, restore_file='', restore_url='',
                 node_type='node',
                 split_ratio=None, data_path=None, force_download=False):
        self.reverse = reverse
        super(OgbgEzooGraphDataset, self).__init__(name,
                                                   raw_dir=raw_dir,
                                                   force_reload=force_reload,
                                                   cfg_file=cfg_file, gdi_ptr=gdi_ptr,
                                                   restore_file=restore_file, restore_url=restore_url,
                                                   node_type=node_type,
                                                   force_download=force_download)



