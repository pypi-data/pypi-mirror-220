import os
import json
import torch
from ezoognn import get_ezoo_home
from .ezoo_data_graph import GetItemGraph, EzooShapeGraphEnum, EzooHeteroGraphDataset


class IeeeFraudDetectionEzooGetItemGraph(GetItemGraph):
    def __init__(self, e_graph, _graph=None, train_mask=None, test_mask=None, labels=None, id_to_node={},
                 name=None, split_ratio=None, data_path=None):
        super(IeeeFraudDetectionEzooGetItemGraph, self).__init__(
            e_graph=e_graph, _graph=_graph, name=name)

        self.train_mask = train_mask
        self.test_mask = test_mask
        self.labels = labels

        self.num_labels = torch.unique(labels).int().numpy().max() + 1
        self.num_classes = torch.unique(labels).int().numpy().max() + 1
        self.id_to_node = id_to_node


class IeeeFraudDetectionEzooGraphDataset(EzooHeteroGraphDataset):

    def __init__(self, name='ieee-fraud-detection', reverse=True, raw_dir=None, force_reload=False,
                 cfg_file=None, gdi_ptr=0, restore_file='', restore_url='', force_download=False):
        self.reverse = reverse
        super(IeeeFraudDetectionEzooGraphDataset, self).__init__(name=name,
                                                                 raw_dir=raw_dir,
                                                                 force_reload=force_reload,
                                                                 cfg_file=cfg_file,
                                                                 gdi_ptr=gdi_ptr,
                                                                 restore_file=restore_file,
                                                                 restore_url=restore_url,
                                                                 node_exclude_list=[
                                                                     'id'],
                                                                 edge_exclude_list=[
                                                                     'edgeIds', 'numbers', 'id'],
                                                                 force_download=force_download)

    def get_idx_split(self):
        _nodes = self.dgl_graph.ndata._nodes
        train_mask = None
        test_mask = None
        for type_id in self.dgl_graph.ndata._ntid:
            type = self.dgl_graph.ndata._ntype[type_id]
            if type != 'target':
                continue
            node_frame_dict = self.dgl_graph._get_n_repr(type_id, _nodes)
            if node_frame_dict.__contains__('train_mask'):
                train_mask = node_frame_dict['train_mask'].float()
            if node_frame_dict.__contains__('test_mask'):
                test_mask = node_frame_dict['test_mask'].float()
            break
        return train_mask, test_mask

    def get_label_list(self):
        return self.dgl_graph.nodes['target'].data['labels']

    '''
    
    '''

    def get_id_to_node(self):
        id_to_node_dict = {}
        for nt in self.dgl_graph.ntypes:
            ndata_dict = self.dgl_graph.nodes[nt].data
            if nt == 'target':
                continue
            if ndata_dict.__contains__('source_' + nt):
                old_id_list_dict = self.e_graph.get_node_props(
                    nt, [k for k in ndata_dict.keys()])
                if len(old_id_list_dict) == 0:
                    continue
                tensor_node_id = ndata_dict['source_' + nt].numpy().tolist()
                old_id_list = old_id_list_dict['source_' + nt]
                kv_dict = dict(zip(old_id_list, tensor_node_id))
                id_to_node_dict[nt] = kv_dict
        return id_to_node_dict

    def __getitem__(self, item):
        # 返回e_graph、dgl.graph
        if item is EzooShapeGraphEnum.WHOLE:
            # Save the time, there is no useful feature should be read from edges
            self.read_edge_feat = False
            super().__getitem__(item)
            labels = self.get_label_list()
            id_to_node = self.get_id_to_node()
            return IeeeFraudDetectionEzooGetItemGraph(self.e_graph, self.dgl_graph, self.idx_split[0], self.idx_split[1], labels, id_to_node, self.db_name)
        else:
            return self.dgl_graph, self.e_graph
