from .ezoo_data_graph import GetItemGraph, EzooGraphDataset, EzooExampleDatasetEnum


class EzooCitationGraphDataset(EzooGraphDataset):

    def __init__(self, name=None, rpc_url=None, raw_dir=None, force_reload=False, cfg_file=None, gdi_ptr=0, restore_file='', restore_url='', node_type='node', edge_type='edge', node_exclude_list=['id'], edge_exclude_list=['id'], force_download=False):
        super(EzooCitationGraphDataset, self).__init__(name, rpc_url, raw_dir, force_reload, cfg_file, gdi_ptr, restore_file, restore_url, node_type, edge_type, node_exclude_list, edge_exclude_list, cache_edge=True, cache_node=True,
                                                       force_download=force_download)

    def get_label(self, dgl_graph):
        return dgl_graph.ndata['label'] if dgl_graph.ndata.__contains__('label') else None

    @property
    def num_labels(self):
        return self.number_label

    @property
    def graph(self):
        return self.dgl_graph


class CoraEzooGraphDatasetV2(EzooCitationGraphDataset):

    def __init__(self, reverse=True, raw_dir=None, force_reload=False,
                 cfg_file=None, gdi_ptr=0, restore_file='', restore_url='',
                 node_type='node', edge_type='edge',
                 name=None, split_ratio=None, data_path=None, force_download=False):
        self.reverse = reverse
        super(CoraEzooGraphDatasetV2, self).__init__(EzooExampleDatasetEnum.CORA_V2.value,
                                                     raw_dir=raw_dir,
                                                     force_reload=force_reload,
                                                     cfg_file=cfg_file, gdi_ptr=gdi_ptr,
                                                     restore_file=restore_file, restore_url=restore_url,
                                                     node_type=node_type, edge_type=edge_type,
                                                     force_download=force_download)


class CiteseerEzooGraphDataset(EzooCitationGraphDataset):

    def __init__(self, reverse=True, raw_dir=None, force_reload=False,
                 cfg_file=None, gdi_ptr=0, restore_file='', restore_url='',
                 node_type='node', edge_type='edge',
                 name=None, split_ratio=None, data_path=None, force_download=False):
        self.reverse = reverse
        super(CiteseerEzooGraphDataset, self).__init__(EzooExampleDatasetEnum.CITESEER.value,
                                                       raw_dir=raw_dir,
                                                       force_reload=force_reload,
                                                       cfg_file=cfg_file, gdi_ptr=gdi_ptr,
                                                       restore_file=restore_file, restore_url=restore_url,
                                                       node_type=node_type, edge_type=edge_type,
                                                       force_download=force_download)


class PubmedEzooGraphDataset(EzooCitationGraphDataset):

    def __init__(self, reverse=True, raw_dir=None, force_reload=False,
                 cfg_file=None, gdi_ptr=0, restore_file='', restore_url='',
                 node_type='node', edge_type='edge',
                 name=None, split_ratio=None, data_path=None, force_download=False):
        self.reverse = reverse
        super(PubmedEzooGraphDataset, self).__init__(EzooExampleDatasetEnum.PUBMED.value,
                                                     raw_dir=raw_dir,
                                                     force_reload=force_reload,
                                                     cfg_file=cfg_file, gdi_ptr=gdi_ptr,
                                                     restore_file=restore_file, restore_url=restore_url,
                                                     node_type=node_type, edge_type=edge_type,
                                                     force_download=force_download)
