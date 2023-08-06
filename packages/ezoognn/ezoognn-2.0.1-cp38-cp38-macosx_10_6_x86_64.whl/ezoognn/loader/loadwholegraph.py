from pyexpat import features
import random
import sys

import dgl
import torch
import numpy as np
import networkx as nx
import quiver

from ..ezoo_graph import EzooGraph, EzooEntityPropertyType
from .. import ezoocall
from ..utils.painter import GraphPainter, PaintDataTypeEnum
from dgl.data.dgl_dataset import DGLDataset

from itertools import groupby
from operator import itemgetter
import time


class EzooDGLBuiltinDataset(DGLDataset):
    def __init__(self, name, url=None, cfg_file=None, raw_dir=None, hash_key=(), force_reload=False,
                 draw_sub=True, sub_node_count=None, train_rate=None, test_rate=None, gdi_ptr=0,
                 restore_file=None, restore_url=None, node_type='node', edge_type='edge', id_name='id',
                 label_name='label', exclude_list=""):
        # 是否绘制子图
        self.draw_sub = draw_sub
        # 子图节点数量
        self.sub_node_count = sub_node_count
        # 图结构
        self._graph = None
        # 标签类别分类
        self._num_labels = 0
        # 特征
        self._in_feat = None
        # 训练集比率
        self._train_rate = train_rate
        # self._train_rate = train_rate * 100
        # 测试集比率
        self._test_rate = test_rate
        # self._test_rate = test_rate * 100

        self.node_type = node_type
        self.edge_type = edge_type
        self.label_name = label_name
        self.id_name = id_name
        self.exclude_list = exclude_list

        self.e_graph = EzooGraph(url=url, dbname=name, cfg_file=cfg_file, gdi_ptr=gdi_ptr,
                                 restore_file=restore_file, restore_url=restore_url, schema_path="", iconf_path="").graph
        if self.e_graph is None:
            sys.exit()
        super(EzooDGLBuiltinDataset, self).__init__(name, url=url, raw_dir=raw_dir, save_dir=None, hash_key=hash_key,
                                                    force_reload=force_reload)

    def __del__(self):
        self.close_graph()

    def close_graph(self):
        if hasattr(self, 'conn'):
            self.conn.close()
        elif self.e_graph is not None:
            self.e_graph.close_graph()

    # def download(self):
    #     pass

    '''
    获取绘图工具
    '''

    def get_painter(self, notebook, nodes_limit=500, highlight_feats='label', data_type=PaintDataTypeEnum.ALL):
        painter = GraphPainter(self._graph, notebook,
                               nodes_limit=nodes_limit, highlight_feats=highlight_feats, data_type=data_type)
        return painter


class EzooWholeGraphLoader(EzooDGLBuiltinDataset):
    def __init__(self, name, url="", one_hot=False, cfg_file=None, raw_dir=None, force_reload=False,
                 draw_sub=True, sub_node_count=None,
                 train_rate=None, test_rate=None, gdi_ptr=0, restore_file=None, restore_url=None,
                 node_type='node', id_name='id', label_name='label', exclude_list="id"):
        self.one_hot = one_hot
        super(EzooWholeGraphLoader, self).__init__(name, url=url, cfg_file=cfg_file, raw_dir=raw_dir, hash_key=(), force_reload=force_reload,
                                                   draw_sub=draw_sub, sub_node_count=sub_node_count, train_rate=train_rate,
                                                   test_rate=test_rate, gdi_ptr=gdi_ptr, restore_file=restore_file, restore_url=restore_url,
                                                   node_type=node_type, id_name=id_name, label_name=label_name, exclude_list=exclude_list)
    """ thrift  call"""

    def get_data_thrift(self):
        """
                1、获取下载地址
                2、获取ezoo host、 port、dbname，并建立链接
                3、通过接口获取dbname中指定的数据（默认全部dbname中的数据），如指定start_id=》dest_id
                4、下载到本地指定位置
                """

        # 1、获取总节点数、总边数
        nodes_size = self.e_graph.get_nodes_num(self.node_type)
        nodes = self.e_graph.get_node_s_batch(
            self.name, 0, nodes_size).nodes

        # 2、获取节点的边或者说是邻居关系，用于构建二维图  关键难点在于如何获取边或者邻居关系，一维/二维， 每次获取一个节点的二维关系，就要遍历n次进行查询，肯定不行
        '''
         1、获取path路径的所有节点信息，根据direction=0表示入度，direction=1表示出度，来构建graph的U、V维度数组
         2、注意用src变量或者是用直接构建两个U、V数组，来构建起数组，并绘制成图graph
        '''
        udata = []
        vdata = []
        # 一维数组
        labels = []
        # 二维数组
        features = []
        max_feature_num = 0
        for node in nodes:
            current_node = self.e_graph.get_node_with_id(
                self.name, node.int_id)
            labels.append(int(current_node.props[self.label_name]))
            # 节点特征的构建：需要考虑对齐，对齐既可以保证数据格式正确，又可以保证二维list转numpy可以成功转换
            # DB中前两列用于保存节点id和label，feat数据列为len - 2，且编号从1开始
            node_features = []
            # for i in range(columns_num):
            for key, val in current_node.props.items():
                if key != self.label_name and key != self.id_name:
                    if self.one_hot:
                        ret_val = int(val)
                    else:
                        ret_val = float(val)
                    node_features.append(ret_val)
                    if ret_val > max_feature_num:
                        max_feature_num = ret_val
            features.append(node_features)

            # 正向
            node_neighbour = self.e_graph.query_simple_neighbour(
                self.name, node.int_id, 1, 1, 1, '')

            for k in node_neighbour.nodes[0]:
                udata.append(node.int_id)
                vdata.append(k)

        labels = np.array(labels)
        features = np.array(features)
        g = dgl.graph((torch.tensor(udata), torch.tensor(vdata)),
                      idtype=torch.int64, num_nodes=nodes_size)
        return labels, features, max_feature_num, g

    """ cpp  call"""

    def get_data_cpp(self):
        """
                1、获取下载地址
                2、获取ezoo host、 port、dbname，并建立链接
                3、通过接口获取dbname中指定的数据（默认全部dbname中的数据），如指定start_id=》dest_id
                4、下载到本地指定位置
                """

        # 获取节点的边或者说是邻居关系，用于构建二维图  关键难点在于如何获取边或者邻居关系，一维/二维， 每次获取一个节点的二维关系，就要遍历n次进行查询，肯定不行
        '''
         1、获取path路径的所有节点信息，根据direction=0表示入度，direction=1表示出度，来构建graph的U、V维度数组
         2、注意用src变量或者是用直接构建两个U、V数组，来构建起数组，并绘制成图graph
        '''
        nodes_size = self.e_graph.get_nodes_num(self.node_type)
        udata, vdata, _, _ = self.e_graph.get_adjacencylist_from_etype()
        g = dgl.graph((udata.astype(np.long), vdata.astype(np.long)),
                      idtype=torch.int64, num_nodes=nodes_size)

        '''
        # # Replace the following with 'set_graph_ndata(g)'
        # if self.one_hot:
        #     label_and_features = self.e_graph.get_node_props2int(
        #         self.node_type)
        # else:
        #     label_and_features = self.e_graph.get_node_props2float(
        #         self.node_type)

        # # Get labels and features(get rid of label and id columns).
        # label_index = self.e_graph.get_node_prop_index_from_name(
        #     self.node_type, self.label_name)
        # labels = label_and_features[:, label_index]
        # id_index = self.e_graph.get_node_prop_index_from_name(
        #     self.node_type, self.id_name)
        
        # # filter useless properties
        # ex_index_list = []
        # if self.exclude_list:
        #     ex_str_list = self.exclude_list.split(',')
        #     for ex in ex_str_list:
        #         prop_id = self.e_graph.get_node_prop_index_from_name(self.node_type, ex)
        #         if prop_id == -1:
        #             print(f"Property '{ex}' not found!")
        #         else:
        #             ex_index_list.append(prop_id)
        # ex_index_list.extend([id_index, label_index])

        # Generate a contiguous features array
        # feat_array = np.delete(label_and_features, ex_index_list, axis=1)
        # feat_list = feat_array.tolist()
        # features = np.array(feat_list)
        '''

        self.set_graph_ndata(g, self.exclude_list + ',' + self.id_name)
        labels = g.ndata['label'].numpy()
        features = g.ndata['feat'].numpy()
        max_feature_num = features.max()

        return labels, features, max_feature_num, g

    def process(self):
        if self.url != None or self.url != '':
            labels, features, column_len, g = self.get_data_cpp()
        else:
            labels, features, column_len, g = self.get_data_thrift()

        self._labels = torch.tensor(labels.astype("int64"))
        self._num_labels = len(np.unique(labels))

        # 得到特征
        if self.one_hot:
            # 创建合法二维数组矩阵，并将对应位置设置为1，同时tensor化为float32类型
            new_features = np.zeros((len(features), column_len + 1))
            for i in range(len(features)):
                feat_arr = features[i]
                for f in feat_arr:
                    if f != ezoocall.INVALID_INT:
                        new_features[i, f] = 1
            features = torch.from_numpy(new_features.astype('float32'))
        else:
            features = torch.from_numpy(features.astype('float32'))

        self.in_feat = features.shape[1]

        nodes_number = g.number_of_nodes()
        '''
        PS：dgl中的区分训练集、测试集、验证集是使用掩码来做的，也就是当前节点是否属于某个集合，以true/false来表示
        * train_mask: 训练集掩码向量，维度为 g.nodes().size()，当节点属于训练集时，相应位置为True，否则False
        * val_mask: 验证集掩码向量，维度为 g.nodes().size()，当节点属于验证集时，相应位置为True，否则False
        * test_mask: 测试集掩码向量，维度为 g.nodes().size()，当节点属于测试集时，相应位置为True，否则False
        '''
        train_n = int(self.train_rate * nodes_number)
        test_n = int(self.test_rate * nodes_number)
        train_mask = torch.zeros([nodes_number, ], dtype=torch.bool)
        train_mask[:train_n] = True
        test_mask = torch.zeros([nodes_number, ], dtype=torch.bool)
        test_mask[train_n: train_n + test_n] = True
        verify_mask = torch.zeros([nodes_number, ], dtype=torch.bool)
        verify_mask[train_n + test_n:] = True
        # train_mask = torch.zeros([nodes_number, ], dtype=torch.bool)
        # test_mask = torch.zeros([nodes_number, ], dtype=torch.bool)
        # verify_mask = torch.zeros([nodes_number, ], dtype=torch.bool)

        # for i in range(nodes_number):
        #     r = random.randint(0, 100)
        #     # 60%改了入train_mask
        #     if r > 0 and r < self._train_rate:
        #         train_mask[i] = True
        #     # 20%改了入test_mask
        #     elif r >= self.train_rate and r < (self._train_rate + self._test_rate):
        #         test_mask[i] = True
        #     else:
        #         verify_mask[i] = True

        # 最后构建所有信息，包括特征feature、标签label、权重weight、训练集掩码train_mask、测试集掩码test_mask、验证集掩码verify_mask
        g.ndata['label'] = self._labels
        g.ndata['feat'] = features
        # g.ndata['weight'] = ?
        g.ndata['train_mask'] = train_mask
        g.ndata['test_mask'] = test_mask
        g.ndata['val_mask'] = verify_mask
        self._graph = g
        # painter = self.get_painter(False, data_type=PaintDataTypeEnum.TRAIN)
        # painter.draw_graph('example.html')

    def __getitem__(self, idx):
        assert idx == 0, "This dataset has only one graph"
        return self._graph

    def __len__(self):
        return 1

    @property
    def save_name(self):
        return self.name + '_dgl_graph'

    @property
    def num_labels(self):
        return self._num_labels

    @property
    def num_classes(self):
        return self._num_labels

    @property
    def graph(self):
        return self._graph

    @property
    def train_mask(self):
        return self._train_mask

    @property
    def val_mask(self):
        return self._val_mask

    @property
    def test_mask(self):
        return self._test_mask

    @property
    def labels(self):
        return self._labels

    @property
    def features(self):
        return self._in_feat

    @property
    def train_rate(self):
        return self._train_rate

    @property
    def test_rate(self):
        return self._test_rate

    def set_graph_ndata(self, dgl_graph, exclude_list):
        exclude_list = set(exclude_list.split(','))
        node_props_dict = self.e_graph.get_all_node_prop_names_with_ntype()
        [self._set_graph_ndata(node_props_dict, ntype, exclude_list,
                               dgl_graph.ndata) for ntype in node_props_dict.keys()]

    def _set_graph_ndata(self, props_dict, n_e_type, exclude_list, dgl_grap_n_e_data):
        props = props_dict[n_e_type]
        prop_name_list = []
        for p in props:
            if p['name'] not in exclude_list:
                prop_name_list.append(p)
        props.clear()
        props = prop_name_list
        # 保证feat数据与schema中的顺序一致
        feat_name_list = []
        other_name_list = []

        for t, items in groupby(props, key=itemgetter('type')):
            items = [i['name'] for i in items]
            for i in range(len(items)):
                item = items[i]
                if item.startswith('feat'):
                    feat_name_list.append(item)
                else:
                    other_name_list.append(item)
            if other_name_list is not None and len(other_name_list) > 0:
                t = EzooEntityPropertyType(t)
                if t == EzooEntityPropertyType.Bool:
                    result = self.e_graph.get_node_props2bool(
                        n_e_type, [], other_name_list)
                elif t == EzooEntityPropertyType.Int32:
                    result = self.e_graph.get_node_props2int(
                        n_e_type, [], other_name_list)
                    result = result.astype(np.int64)
                elif t == EzooEntityPropertyType.Int64:
                    result = self.e_graph.get_node_props2long(
                        n_e_type, [], other_name_list)
                elif t == EzooEntityPropertyType.Float32:
                    result = self.e_graph.get_node_props2float(
                        n_e_type, [], other_name_list)
                elif t == EzooEntityPropertyType.Float64:
                    result = self.e_graph.get_node_props2double(
                        n_e_type, [], other_name_list)

                # 设置非feat特征数据到dgl.graph
                result = result.reshape((result.shape[1], result.shape[0]))
                for i in range(len(other_name_list)):
                    name = other_name_list[i]
                    dgl_grap_n_e_data[name] = torch.from_numpy(result[i])
                other_name_list.clear()

        # .t() :  二维向量转置
        feat_name_list = torch.from_numpy(
            self.e_graph.get_node_props2float(n_e_type, [], feat_name_list))
        dgl_grap_n_e_data['feat'] = feat_name_list

    def set_feature_cache(self, cache='cpu', gpu=-1, device_cache_size='200M', cache_policy='device_replicate'):
        '''设置节点特征的缓存和策略

        Parameters
        ----------
        cache : feature的缓存位置
            cpu : 节点特征全部加载到CPU内存
            gpu : 节点特征全部加载到GPU显存
            quiver : 每个节点被采样到的概率与该节点的连接数成正相关，将节点特征按照节点出度从大到小排序
                quiver.Feature根据用户配置的参数device_cache_size将排序后的特征进行划分存储在GPU显存以及CPU Pinned Memory中
                多GPU的默认缓存策略为device_replicate, 如果GPU之间有NVLink等高速互联, 则可设为p2p_clique_replicate
            unified : DGL0.8.0版本以后支持UnifiedTensor, 通过NVIDIA GPU的统一虚拟地址(UVM) 
                和零拷贝(Zero-Copy)访问能力, 可以从GPU直接访问CPU内存
            uva : 配合DGL dataloader的use_uva使用(use_uva为True时, 设置cache为uva)
        gpu : 使用gpu训练时的显卡编号
        device_cache_size : cache选择'quiver'时，显存中节点特征缓存区的大小，支持'数字+[K/M/G]'
        cache_policy : cache选择'quiver'时，多显卡的缓存策略，'device_replicate'/'p2p_clique_replicate'
        '''
        if gpu >= 0:
            device = torch.device('cuda:%d' % gpu)
        else:
            device = torch.device('cpu')
        
        if cache == 'uva':
            return self._graph.ndata['feat']
            
        # 获取所有节点的特征
        features = self._graph.ndata.pop('feat')

        if cache == 'cpu':
            nfeat = features
        elif cache == 'gpu':
            nfeat = features.to(device)
        elif cache == 'quiver':
            csr_topo = quiver.CSRTopo(torch.stack(self._graph.edges('uv')))
            nfeat = quiver.Feature(rank=gpu, device_list=[gpu], 
                                   device_cache_size=device_cache_size, 
                                   cache_policy=cache_policy, 
                                   csr_topo=csr_topo)
            nfeat.from_cpu_tensor(features)
        elif cache == 'unified':
            from distutils.version import LooseVersion
            assert LooseVersion(dgl.__version__) >= LooseVersion('0.8.0'), \
                f'Current DGL version ({dgl.__version__}) does not support UnifiedTensor.'
            nfeat = dgl.contrib.UnifiedTensor(features, device=device)
        else:
            raise ValueError(f'Unsupported feature storage location {cache}.')

        return nfeat       

class EzooEdgeWholeGraphLoader(EzooDGLBuiltinDataset):
    def __init__(self, name, url="", one_hot=False, cfg_file=None, raw_dir=None, force_reload=False,
                 draw_sub=True, sub_node_count=None,
                 train_rate=None, test_rate=None, gdi_ptr=0, restore_file=None, restore_url=None,
                 node_type='node', id_name='id', label_name='label'):
        self.one_hot = one_hot
        super(EzooEdgeWholeGraphLoader, self).__init__(name, url=url, cfg_file=cfg_file, raw_dir=raw_dir, hash_key=(), force_reload=force_reload,
                                                       draw_sub=draw_sub, sub_node_count=sub_node_count, train_rate=train_rate,
                                                       test_rate=test_rate, gdi_ptr=gdi_ptr, restore_file=restore_file, restore_url=restore_url,
                                                       node_type=node_type, id_name=id_name, label_name=label_name)

    """ cpp  call"""

    def get_data_cpp(self):
        nodes_size = self.e_graph.get_nodes_num(self.node_type)
        udata, vdata, _, _ = self.e_graph.get_adjacencylist_from_etype()
        g = dgl.graph((udata.astype(np.long), vdata.astype(np.long)),
                      idtype=torch.int64, num_nodes=nodes_size)

        if self.one_hot:
            label_and_features = self.e_graph.get_node_props2int(
                self.node_type)
        else:
            label_and_features = self.e_graph.get_node_props2float(
                self.node_type)
        label_and_features = np.array(label_and_features)

        # 如果是边分类模型，这块似乎讲类重新定义一个更好
        edge_size = self.e_graph.get_edges_num('edge')
        edges = [i for i in range(edge_size)]
        label_list = np.array(
            self.e_graph.get_edge_prop(edges, self.label_name))

        return label_list, g

    def process(self):
        # 目前只做支持native cpp的
        labels, g = self.get_data_cpp()
        print(type(labels))
        self._labels = torch.tensor(labels.astype("int64"))
        self._num_labels = len(np.unique(labels))

        edges_number = g.number_of_edges()
        '''
        PS：dgl中的区分训练集、测试集、验证集是使用掩码来做的，也就是当前节点是否属于某个集合，以true/false来表示
        '''
        train_n = int(self.train_rate * edges_number)
        test_n = int(self.test_rate * edges_number)
        train_mask = torch.zeros([edges_number, ], dtype=torch.bool)
        train_mask[:train_n] = True
        test_mask = torch.zeros([edges_number, ], dtype=torch.bool)
        test_mask[train_n: train_n + test_n] = True
        verify_mask = torch.zeros([edges_number, ], dtype=torch.bool)
        verify_mask[train_n + test_n:] = True

        # 构建所有信息，包括特征feature、标签label、权重weight、训练集掩码train_mask、测试集掩码test_mask、验证集掩码verify_mask
        g.edata['label'] = self._labels
        # g.ndata['weight'] = ?
        g.edata['train_mask'] = train_mask
        g.edata['test_mask'] = test_mask
        g.edata['val_mask'] = verify_mask
        self._graph = g

    def __getitem__(self, idx):
        assert idx == 0, "This dataset has only one graph"
        return self._graph

    def __len__(self):
        return 1

    @property
    def save_name(self):
        return self.name + '_dgl_graph'

    @property
    def num_labels(self):
        return self._num_labels

    @property
    def num_classes(self):
        return self._num_labels

    @property
    def graph(self):
        return self._graph

    @property
    def train_mask(self):
        return self._train_mask

    @property
    def val_mask(self):
        return self._val_mask

    @property
    def test_mask(self):
        return self._test_mask

    @property
    def labels(self):
        return self._labels

    @property
    def features(self):
        return self._in_feat

    @property
    def train_rate(self):
        return self._train_rate

    @property
    def test_rate(self):
        return self._test_rate
