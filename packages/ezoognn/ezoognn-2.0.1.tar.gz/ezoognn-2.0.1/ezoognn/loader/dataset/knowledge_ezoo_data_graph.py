from .ezoo_data_graph import EzooGraphDataset, EzooExampleDatasetEnum


class Wn18EzooGraphDataset(EzooGraphDataset):

    def __init__(self, reverse=True, raw_dir=None, force_reload=False,
                 cfg_file=None, gdi_ptr=0, restore_file='', restore_url='',
                 node_type='node',
                 name=None, split_ratio=None, data_path=None, force_download=False):
        self.reverse = reverse
        super(Wn18EzooGraphDataset, self).__init__(EzooExampleDatasetEnum.WN18.value,
                                                    raw_dir=raw_dir,
                                                    force_reload=force_reload,
                                                   cfg_file=cfg_file, gdi_ptr=gdi_ptr,
                                                   restore_file=restore_file, restore_url=restore_url,
                                                   node_type=node_type,
                                                   force_download=force_download)


class FB15KEzooGraphDataset(EzooGraphDataset):
    
    def __init__(self, reverse=True, raw_dir=None, force_reload=False,
                 cfg_file=None, gdi_ptr=0, restore_file='', restore_url='',
                 node_type='node',
                 name=None, split_ratio=None, data_path=None, force_download=False):
        self.reverse = reverse
        super(FB15KEzooGraphDataset, self).__init__(EzooExampleDatasetEnum.FB15K.value,
                                                    raw_dir=raw_dir,
                                                    force_reload=force_reload,
                                                    cfg_file=cfg_file, gdi_ptr=gdi_ptr,
                                                    restore_file=restore_file, restore_url=restore_url,
                                                    node_type=node_type,
                                                    force_download=force_download)
    

class FB15K237EzooGraphDataset(EzooGraphDataset):
    
    def __init__(self, reverse=True, raw_dir=None, force_reload=False,
                 cfg_file=None, gdi_ptr=0, restore_file='', restore_url='',
                 node_type='node',
                 name=None, split_ratio=None, data_path=None, force_download=False):
        self.reverse = reverse
        super(FB15K237EzooGraphDataset, self).__init__(EzooExampleDatasetEnum.FB15K_237.value,
                                                    raw_dir=raw_dir,
                                                    force_reload=force_reload,
                                                       cfg_file=cfg_file, gdi_ptr=gdi_ptr,
                                                       restore_file=restore_file, restore_url=restore_url,
                                                       node_type=node_type,
                                                       force_download=force_download)
    
    



