import os
import pickle
from ezoognn import get_ezoo_home
from .ezoo_data_graph import GetItemGraph, EzooShapeGraphEnum, EzooHeteroGraphDataset, EzooExampleDatasetEnum


class EzooMl1mGraph(GetItemGraph):
    def __init__(self, e_graph=None, _graph=None, name=None, _dataset=None):
        super(EzooMl1mGraph, self).__init__(e_graph=e_graph, _graph=_graph, name=name)
        if _dataset is not None:
            self._dataset = _dataset
        self.num_classes = 2

'''
gos：Gossip Cop是国外一个专门报道娱乐新闻和澄清传言绯闻的网站 他们的报道最公正 消息十分可靠.
pol：PolitiFact 数据集：对于新闻报道，提供了原始内容、事实核查结果和全面的事实核查报告。平台根据内容将它们分类为不同的主题和话题
可用于新闻真实性检测的数据集
边采样相关数据集
'''


class Ml1mEzooGraphhDataset(EzooHeteroGraphDataset):
    
    def __init__(self, name=EzooExampleDatasetEnum.ML1M.value, rpc_url=None, raw_dir=None, force_reload=False, cfg_file=None, gdi_ptr=0, restore_file='', restore_url='', node_exclude_list=['id'], edge_exclude_list=['id', 'edgeIds', 'watched-by_id', 'watched_id'], batch_size=0,
                 split_ratio=None, data_path=None, force_download=False):
        feat_mapping = {'node': {'movie': {'genre': ['genre0', 'genre1', 'genre2', 'genre3',
                                                     'genre4', 'genre5', 'genre6', 'genre7',
                                                     'genre8', 'genre9', 'genre10', 'genre11',
                                                     'genre12', 'genre13', 'genre14', 'genre15',
                                                     'genre16', 'genre17']}}, 'edge': {}}
        self.batch_size = batch_size
        super(Ml1mEzooGraphhDataset, self).__init__(name, rpc_url, raw_dir, force_reload, cfg_file, gdi_ptr, restore_file, restore_url, node_exclude_list, edge_exclude_list,
                                                   force_download=force_download, feat_mapping=feat_mapping)

    def get_label(self, dgl_graph):
        if dgl_graph.ndata.__contains__('labels'):
            return dgl_graph.ndata['labels']
        elif dgl_graph.ndata.__contains__('label'):
            return dgl_graph.ndata['label']

    def __getitem__(self, item):
        super().__getitem__(item)
        if item is EzooShapeGraphEnum.WHOLE:
            _dataset = self.get_mapping_dataset()
            return EzooMl1mGraph(self.e_graph, self.dgl_graph, self.db_name, _dataset)
        
        return EzooMl1mGraph(self.e_graph, self.dgl_graph, name=self.db_name)

    def get_mapping_dataset(self):
        dataset_path = get_ezoo_home(self.cfg_file) + os.sep + self.db_name + os.sep + self.db_name
        if os.path.exists(dataset_path) is False:
            return
        data_info_path = os.path.join(dataset_path, "data.pkl")
        with open(data_info_path, "rb") as f:
            _dataset = pickle.load(f)

        return _dataset