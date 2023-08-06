from .ezoo_data_graph import EzooGraphDataset, EzooExampleDatasetEnum


class RedditEzooGraphDataset(EzooGraphDataset):
    
    def __init__(self, reverse=True, raw_dir=None, force_reload=False,
                 cfg_file=None, gdi_ptr=0, restore_file='', restore_url='',
                 node_type='node', edge_type='edge',
                 name=None, split_ratio=None, data_path=None, force_download=False):
        self.reverse = reverse
        super(RedditEzooGraphDataset, self).__init__(EzooExampleDatasetEnum.REDDIT.value,
                                                     raw_dir=raw_dir,
                                                     force_reload=force_reload,
                                                     cfg_file=cfg_file,
                                                     gdi_ptr=gdi_ptr,
                                                     restore_file=restore_file,
                                                     restore_url=restore_url,
                                                     node_type=node_type,
                                                     edge_type=edge_type,
                                                     force_download=force_download)
