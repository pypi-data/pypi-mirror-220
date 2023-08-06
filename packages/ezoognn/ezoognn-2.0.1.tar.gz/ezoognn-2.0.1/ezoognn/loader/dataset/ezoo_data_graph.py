import os
import sys

import dgl
import abc
import errno

import pandas
import torch
import numpy
from enum import Enum
import pandas as pd
import numpy as np
from operator import itemgetter
from dgl.data import download, extract_archive
from ezoognn import get_ezoo_home
from ezoognn.utils.graph_store import GraphStore
from ezoognn.ezoo_graph import EzooEntityPropertyType
from ezoognn.utils.properties_utils import Properties
from ezoognn.utils.painter import GraphPainter, HeterGraphPainter, PaintDataTypeEnum
import quiver


class EzooShapeGraphEnum(Enum):
    WHOLE = 'whole'
    FRAME = 'frame'


class EzooExampleDatasetEnum(Enum):
    OGBN_PRODUCTS = 'ogbn-products'

    OGBN_PROTEINS = 'ogbn-proteins'

    # graph  PS : no algorithm model implementation
    OGBN_DDI = 'ogbn-ddi'
    OGBN_MAG = 'ogbn-mag'
    # knowledge PS : no algorithm model implementation
    WN18 = 'wn18'
    FB15K_237 = 'FB15k-237'
    FB15K = 'FB15k'
    # citation
    CORA = 'cora'
    CORA_V2 = 'cora_v2'
    CITESEER = 'citeseer'
    PUBMED = 'pubmed'
    # rdf
    AIFB = 'aifb'
    BGS = 'bgs'
    MUTAG = 'mutag'
    AM = 'am'
    # reddit
    REDDIT = 'reddit'
    # small graph
    EDGE_PROPERTY = 'edge_property'
    # gowalla(heterogenous)
    GOWALLA = 'gowalla'
    AMAZONBOOK = 'amazon-book'

    # gas(hetergenous, edge_mask)
    POL = 'pol'
    GOS = 'gos'

    # ml-1m
    ML1M = 'ml-1m'

    # NowPlayingRs
    NOWPLAYINGRS = 'nowplaying-rs'

    # LastFM4KGCN
    LASTFM4KGCN_0 = 'LastFM4KGCN_0'
    LASTFM4KGCN_1 = 'LastFM4KGCN_1'


class EzooDataset(abc.ABC):
    def __init__(self, name, raw_dir=None, save_dir=None, force_reload=False, cfg_file=None,
                 force_download=False):
        self._name = name
        self._download_url = self._get_download_url(
            'gnn-data/') + '{}.zip'.format(name)
        print('download url from ezoo oss : ', self._download_url)
        self._force_reload = force_reload
        self._force_download = force_download
        if force_download:
            self._force_reload = True

        self._cfg_file = cfg_file

        # if no dir is provided, the default download dir is used.
        if raw_dir is None:
            self._raw_dir = self.get_download_dir()
        else:
            self._raw_dir = raw_dir

        if save_dir is None:
            self._save_dir = self._raw_dir
        else:
            self._save_dir = save_dir

        self._load()

    def download(self):
        r""" Automatically download data and extract it.
        """
        zip_file_path = os.path.join(str(self.raw_dir), self.name + '.zip')
        download(self.url, path=zip_file_path)
        self.rm_folder(self.raw_path)
        extract_archive(zip_file_path, self.raw_path, overwrite=True)

    def _get_download_url(self, file_url):
        """Get eZoo online url for download."""
        dgl_repo_url = 'https://ezoo-public.oss-cn-beijing.aliyuncs.com/'
        repo_url = os.environ.get('EZOO_REPO', dgl_repo_url)
        if repo_url[-1] != '/':
            repo_url = repo_url + '/'
        return repo_url + file_url

    def get_download_dir(self):
        dirname = os.environ.get(
            'EZOO_DOWNLOAD_DIR', get_ezoo_home(self._cfg_file))
        if dirname is not None and isinstance(dirname, str):
            if not os.path.exists(dirname):
                os.makedirs(dirname)
        return dirname

    def load(self):
        if self.url is not None:
            zip_file_path = os.path.join(str(self.raw_dir), self.name + '.zip')
            download(self.url, path=zip_file_path)
            # 先判断是否存在，如果存在，则删除
            self.rm_folder(self.raw_path)
            extract_archive(zip_file_path, self.raw_path)

    def rm_folder(self, path):
        if os.path.exists(path) is False:
            return
        if os.path.isdir(path):
            for f in os.listdir(path):
                self.rm_folder(os.path.join(path, f))
            if os.path.exists(path):
                os.rmdir(path)
                print('delete folder ', path)
        else:
            if os.path.isfile(path):
                os.remove(path)
                print('delete file ', path)

    def prepare_conf_paths(self):
        row_path = self.raw_path + '/' + self.name

        self.schema_path = row_path + '/schema.txt'
        self.iconf_path = row_path + '/import_conf.txt'

    def _download(self):
        r"""Download dataset by calling ``self.download()`` if the dataset does not exists under ``self.raw_path``.
            By default ``self.raw_path = os.path.join(self.raw_dir, self.name)``
            One can overwrite ``raw_path()`` function to change the path.
        """
        if os.path.exists(self.raw_path) and not self._force_download:  # pragma: no cover
            return

        self.makedirs(self.raw_dir)
        self.download()

    def makedirs(self, path):
        try:
            os.makedirs(os.path.expanduser(os.path.normpath(path)))
        except OSError as e:
            if e.errno != errno.EEXIST and os.path.isdir(path):
                raise e

    def _load(self):
        load_flag = not self._force_reload

        if load_flag:
            try:
                self.load()
            except KeyboardInterrupt:
                raise
            except:
                load_flag = False

        if not load_flag:
            self._download()

        # 无论如何，都要设置schame_path、iconf_path，这样，无论如何，都会对ezoodb库中进行删除一遍，然后重建
        self.prepare_conf_paths()

    @property
    def url(self):
        r"""Get url to download the raw dataset.
        """
        return self._download_url

    @property
    def name(self):
        r"""Name of the dataset.
        """
        return self._name

    @property
    def raw_dir(self):
        r"""Raw file directory contains the input data folder.
        """
        return self._raw_dir

    @property
    def raw_path(self):
        r"""Directory contains the input data files.
            By default raw_path = os.path.join(self.raw_dir, self.name)
        """
        return os.path.join(str(self.raw_dir), self.name)

    def __len__(self):
        return 1

    @abc.abstractmethod
    def __getitem__(self, idx):
        r"""Gets the data object at index.
        """
        pass


'''
加载ezoo数据库
'''


class EzooLoaderDataset(EzooDataset, abc.ABC):
    def __init__(self, name, rpc_url, raw_dir=None, force_reload=False, cfg_file=None,
                 schema_path='', iconf_path='', gdi_ptr=0, restore_file=None, restore_url=None,
                 cache_edge=True, cache_node=True, train_rate=0.6, force_download=False, dataset_name='',
                 feat_mapping={'node': {}, 'edge': {}}):
        assert cfg_file is not None and cfg_file != '', 'cfg_file is None, Please set the configuration file ! '
        self.cfg_file = cfg_file
        self.db_name = name
        self.cache_edge = cache_edge
        self.cache_node = cache_node
        self.train_rate = train_rate
        self.feat_mapping = feat_mapping

        # 从枚举获取字符串
        self.schema_path = schema_path
        self.iconf_path = iconf_path

        # 如果使用rpc_url从远端获取数据，则不需要下载csv并load数据库的操作
        if force_download:
            force_reload = True
        if force_reload:
            super().__init__(name, raw_dir=raw_dir, force_reload=force_reload,
                             cfg_file=cfg_file, force_download=force_download)
            GraphStore(rpc_url, cfg_file).remove_graph(name)

        self.dateset_name = dataset_name

        # 此处需要添加 schema_path=self.schema_path, iconf_path=self.iconf_path 参数，用于在cpp端判断是否需要force_reload也就是重新导入数据
        self.e_graph = GraphStore(rpc_url, cfg_file).get_graph(
            name, gdi_ptr=gdi_ptr, restore_file=restore_file, restore_url=restore_url, schema_path=self.schema_path, iconf_path=self.iconf_path, cache_edge=cache_edge, cache_node=cache_node)
        if self.e_graph is None and \
                self.schema_path != '' and \
                self.iconf_path != '':
            self.e_graph = GraphStore(rpc_url, cfg_file).get_graph(
                name, gdi_ptr=gdi_ptr, restore_file=restore_file, restore_url=restore_url, schema_path=self.schema_path,
                iconf_path=self.iconf_path,
                cache_edge=cache_edge, cache_node=cache_node)
        # 如果无法获得e_graph客户端，则从远端下载开源数据集，并load到ezoodb中
        if self.e_graph is None:
            try:
                print('ezoodb的配置路径：', self.iconf_path,
                      '  ', self.schema_path, ' ', cfg_file)
                super().__init__(name, raw_dir=raw_dir, force_reload=force_reload, cfg_file=cfg_file)
            except Exception as e:
                print('can not get ', name, ' from ezoo oss !!!')
                sys.exit(1)
            else:
                self.e_graph = GraphStore(rpc_url, cfg_file).get_graph(
                    name, gdi_ptr=gdi_ptr, restore_file=restore_file, restore_url=restore_url, schema_path=self.schema_path, iconf_path=self.iconf_path,
                    cache_edge=cache_edge, cache_node=cache_node)
                if self.e_graph is None:
                    print('can not init ', name, ' database !!!')
                    sys.exit(1)

        self.dgl_graph = self.get_graph_frame()

    @abc.abstractmethod
    def get_graph_frame(self) -> dgl.DGLGraph:
        pass

    @abc.abstractmethod
    def get_idx_split(self):
        pass

    '''
    如果没有mask，则根据train_rate自动设置训练集、测试集、验证集的mask数据
    '''

    def set_custom_mask(self, dgl_graph_data, _split_dict, nodes_number):
        if _split_dict.__contains__('train_mask') is not True \
                or _split_dict.__contains__('test_mask') is not True:
            # 获取点的数量，或者边的数量。通过传入的dgl_graph_data来区分不同的边/点数量
            train_n = int(self.train_rate * nodes_number)
            test_n = int((1 - self.train_rate)/2 * nodes_number)
            train_mask = torch.zeros([nodes_number, ], dtype=torch.bool)
            train_mask[:train_n] = True
            _split_dict['train_mask'] = train_mask
            dgl_graph_data['train_mask'] = train_mask

            test_mask = torch.zeros([nodes_number, ], dtype=torch.bool)
            test_mask[train_n: train_n + test_n] = True
            _split_dict['test_mask'] = test_mask
            dgl_graph_data['test_mask'] = test_mask

            valid_mask = torch.zeros([nodes_number, ], dtype=torch.bool)
            valid_mask[train_n + test_n:] = True
            _split_dict['valid_mask'] = valid_mask
            dgl_graph_data['val_mask'] = valid_mask
            dgl_graph_data['valid_mask'] = valid_mask

    '''
    ndata/edata中最基本的构建单元
    @:param props
    @:param ne_exclude_list
    @:param ne_dict
    @:param e_graph_nedata_func
    @:param netype
    '''

    def set_data_unit(self, props, ne_exclude_list, ne_dict, e_graph_nedata_func, netype, n_or_e='node'):
        props = [p for p in props if p['name'] not in ne_exclude_list]
        mul_feat_name_list = []

        # 默認使用feat，如果存在需要特別聚合的，則使用feat_mapping獲取對應類型處理
        if self.feat_mapping is not None \
                and self.feat_mapping.__contains__(n_or_e) \
                and self.feat_mapping[n_or_e].__contains__(netype):
            feat_name_dict = self.feat_mapping[n_or_e][netype]
            for k in feat_name_dict.keys():
                feat_prop_names = feat_name_dict[k]
                feat_name_list = [p['name']
                                  for p in props if p['name'] in feat_prop_names]
                if len(feat_name_list) > 0:
                    ne_dict[k] = torch.from_numpy(
                        e_graph_nedata_func[:netype][k:feat_name_list])
                mul_feat_name_list.extend(feat_name_list)
        else:
            feat_name_list = [p['name']
                              for p in props if p['name'].startswith('feat')]
            if len(feat_name_list) > 0:
                ne_dict['feat'] = torch.from_numpy(
                    e_graph_nedata_func[:netype]['feat':feat_name_list])
            mul_feat_name_list.extend(feat_name_list)

        if mul_feat_name_list is not None:
            props = [p for p in props if p['name'] not in mul_feat_name_list]
            for kv in props:
                ne_dict[kv['name']] = torch.from_numpy(
                    e_graph_nedata_func[:netype][kv['name']])

    '''
    mask节点，从文件中获取
    '''

    def set_dgl_graph_mask(self):
        dataset_path = os.path.join(get_ezoo_home(
            self.cfg_file), self.db_name, self.dateset_name)
        if os.path.exists(dataset_path) is False:
            print('Fail to set dgl graph mask, the dataset does not exist.')
            return

        for root, ds, fs in os.walk(dataset_path):
            if fs is None or len(fs) <= 0:
                continue
            internal_idx = None
            for f in fs:
                if f.endswith('node_mask.csv') or f.endswith('edge_mask.csv'):
                    mask_path = os.path.join(root, f)
                    print('Loading mask from the file', mask_path)
                    data_frame = pandas.read_csv(mask_path, low_memory=False)
                    for header in data_frame.columns:
                        if '###' not in header:
                            continue
                        _mask = torch.from_numpy(
                            data_frame[header].values).type(torch.bool)
                        # mask_list 长度==3 表示异构图，索引0表示边/点，索引1表示类型，索引2表示哪种mask; 长度==2 表示异构图，索引0表示边/点，索引1表示哪种mask
                        header_list = header.split('###')

                        if len(header_list) == 3:
                            ne_type = header_list[1]
                            prop_name = header_list[2]

                            if f.endswith('node_mask.csv'):
                                if internal_idx is None:
                                    num_nodes = self.dgl_graph.number_of_nodes(
                                        ne_type)
                                    internal_idx = self.e_graph.get_node_id_by_outter_index(
                                        ne_type, 'id', list(range(num_nodes)))
                                _mask = _mask[torch.tensor(
                                    internal_idx.astype(np.int64))]
                                self.dgl_graph.nodes[ne_type].data[prop_name] = _mask
                            else:
                                # 边: 在dgl中的边是三元组
                                if ne_type is not None and ne_type != '':
                                    ne_type_3 = ne_type\
                                        .replace('(', '')\
                                        .replace(')', '')\
                                        .replace('\'', '')\
                                        .replace(' ', '').split(',')
                                    if len(ne_type_3) == 3:
                                        self.dgl_graph.edges[ne_type_3[1]
                                                             ].data[prop_name] = _mask
                        elif len(header_list) == 2:
                            prop_name = header_list[1]
                            if f.endswith('node_mask.csv'):
                                if internal_idx is None:
                                    num_nodes = self.dgl_graph.num_nodes()
                                    internal_idx = self.e_graph.get_node_id_by_outter_index(
                                        self.node_type, 'id', list(range(num_nodes)))
                                _mask = _mask[torch.tensor(
                                    internal_idx.astype(np.int64))]
                                self.dgl_graph.ndata[prop_name] = _mask
                            else:
                                self.dgl_graph.edata[prop_name] = _mask
                        else:
                            return

    def store_dgl_graph(self):
        download_dir = os.path.join(get_ezoo_home(
            self.cfg_file), self.db_name, self.dateset_name)
        dgl.save_graphs(os.path.join(
            download_dir, 'dgl_graph.bin'), self.dgl_graph)


'''
基类：_getitem_
'''


class GetItemGraph(object):
    def __init__(self, e_graph=None, _graph=None, name=None):
        self.e_graph = e_graph
        self.dgl_graph = _graph
        self.graph = _graph
        # 数组对象：按顺序存储dgl.graph、ezoognn.graph
        self.obj_graph_list = [self.dgl_graph, self.e_graph]
        self.name = name

    def __getitem__(self, item):
        assert(len(self.obj_graph_list) >= item)
        return self.obj_graph_list[item]


class EzooGetItemGraph(GetItemGraph):
    def __init__(self, e_graph=None, _graph=None, idx_split=None, num_classes=None, name=None):
        super(EzooGetItemGraph, self).__init__(
            e_graph=e_graph, _graph=_graph, name=name)

        self.idx_split = idx_split
        self.num_labels = num_classes
        self.num_classes = num_classes


'''
同构图
XXX_exclude_list: 如果存在 '*' 则表示所有的点/边都不加载
'''


class EzooGraphDataset(EzooLoaderDataset):
    def __init__(self, name=EzooExampleDatasetEnum.CORA_V2.value, rpc_url=None, raw_dir=None, force_reload=False,
                 cfg_file=None, gdi_ptr=0, restore_file='', restore_url='',
                 node_type='node', edge_type='edge', node_exclude_list=[], edge_exclude_list=[], cache_edge=True, cache_node=True, train_rate=0.6,
                 schema_path='', iconf_path='', force_download=False, dataset_name='', feat_mapping={'node': {}, 'edge': {}}):
        self.node_type = node_type
        self.edge_type = edge_type
        self.node_exclude_list = node_exclude_list
        self.edge_exclude_list = edge_exclude_list
        super(EzooGraphDataset, self).__init__(name,
                                               rpc_url=rpc_url,
                                               raw_dir=raw_dir,
                                               force_reload=force_reload,
                                               cfg_file=cfg_file,
                                               gdi_ptr=gdi_ptr,
                                               restore_file=restore_file,
                                               restore_url=restore_url,
                                               cache_edge=cache_edge,
                                               cache_node=cache_node,
                                               train_rate=train_rate,
                                               schema_path=schema_path,
                                               iconf_path=iconf_path,
                                               force_download=force_download,
                                               dataset_name=dataset_name,
                                               feat_mapping=feat_mapping)

    def get_graph_frame(self):
        nodes_size = self.e_graph.get_nodes_num(self.node_type)
        udata, vdata, _, _ = self.e_graph.get_adjacencylist_from_etype(
            self.edge_type)
        dgl_graph = dgl.graph((udata.astype(numpy.int64), vdata.astype(numpy.int64)),
                              idtype=torch.int64, num_nodes=nodes_size)
        return dgl_graph

    def set_ne_data_unit(self, dgl_graph, ne_exclude_list, _ne_data='node'):
        # 判断设置 边 ，还是设置 点
        if _ne_data != 'node':
            e_graph_nedata = self.e_graph.edata
            dgl_graph_nedata_fun = dgl_graph.edata
            props_dict = self.e_graph.get_all_edge_prop_names_with_etype()
        else:
            e_graph_nedata = self.e_graph.ndata
            dgl_graph_nedata_fun = dgl_graph.ndata
            props_dict = self.e_graph.get_all_node_prop_names_with_ntype()

        for netype in props_dict.keys():
            props = props_dict[netype]
            self.set_data_unit(props, ne_exclude_list,
                               dgl_graph_nedata_fun,
                               e_graph_nedata_func=e_graph_nedata,
                               netype=netype)

    def set_graph_ndata(self, dgl_graph, exclude_list=['id']):
        self.set_ne_data_unit(
            dgl_graph, ne_exclude_list=exclude_list, _ne_data='node')

    def set_graph_edata(self, dgl_graph, exclude_list=['id']):
        self.set_ne_data_unit(
            dgl_graph, ne_exclude_list=exclude_list, _ne_data='edge')

    def get_idx_split_unit(self, dgl_graph_number_ne, dgl_graph_data):
        _split_dict = {}
        for _data_key in dgl_graph_data:
            if 'mask' in _data_key or 'train' in _data_key or 'test' in _data_key or 'val' in _data_key or 'valid' in _data_key:
                _split_dict[_data_key] = dgl_graph_data[_data_key]
        self.set_custom_mask(dgl_graph_data, _split_dict,
                             dgl_graph_number_ne)

        return _split_dict

    '''
    同构图中，获取idx掩码的切割
    '''

    def get_idx_split(self):
        _idx_split_dict = {}
        _idx_split_dict['node_mask'] = self.get_idx_split_unit(
            dgl_graph_number_ne=self.dgl_graph.number_of_nodes(), dgl_graph_data=self.dgl_graph.ndata)
        _idx_split_dict['edge_mask'] = self.get_idx_split_unit(
            dgl_graph_number_ne=self.dgl_graph.number_of_edges(), dgl_graph_data=self.dgl_graph.edata)
        return _idx_split_dict

    def get_label(self, dgl_graph):
        return dgl_graph.ndata['label'] if dgl_graph.ndata.__contains__('label') else None

    '''
    获取绘图工具
    '''

    def get_painter(self, notebook, nodes_limit=500, highlight_feats='', data_type=PaintDataTypeEnum.ALL):
        # 同构图
        return GraphPainter(self.dgl_graph, notebook, nodes_limit=nodes_limit, highlight_feats=highlight_feats, data_type=data_type)

    '''
    frame框架下，仅仅设置label与mask到图中
    '''

    def simple_frame_exclude_props_list(self, prop_name_list, set_graph_Xdata):
        exclude_list = [[kv['name'] for kv in prop_name_list[n_type]
                         if kv['name'].__contains__('mask') is False
                         and kv['name'].__contains__('train') is False
                         and kv['name'].__contains__('test') is False
                         and kv['name'].__contains__('valid') is False
                         and kv['name'].__contains__('val') is False
                         and kv['name'].__contains__('label') is False] for n_type in prop_name_list]
        for exclude in exclude_list:
            set_graph_Xdata(self.dgl_graph, exclude_list=exclude)

    def __getitem__(self, item):
        # 返回e_graph、dgl.graph
        if item is EzooShapeGraphEnum.WHOLE:
            # 需保证feat数据于schema中的顺序一致
            if self.node_exclude_list is not None and '*' not in self.node_exclude_list:
                self.set_graph_ndata(
                    self.dgl_graph, exclude_list=self.node_exclude_list)
            if self.edge_exclude_list is not None and '*' not in self.edge_exclude_list:
                self.set_graph_edata(
                    self.dgl_graph, exclude_list=self.edge_exclude_list)
            label = self.get_label(self.dgl_graph)
            self.number_class = 0
            if label is not None:
                self.number_class = torch.unique(label).shape[0]

            # Set mask
            self.set_dgl_graph_mask()
            self.idx_split = self.get_idx_split()
            return EzooGetItemGraph(self.e_graph, self.dgl_graph, self.idx_split, self.number_class, self.db_name)
        else:
            self.simple_frame_exclude_props_list(
                self.e_graph.get_all_node_prop_names_with_ntype(), self.set_graph_ndata)
            self.simple_frame_exclude_props_list(
                self.e_graph.get_all_edge_prop_names_with_etype(), self.set_graph_edata)

            # Set mask
            self.set_dgl_graph_mask()
            self.idx_split = self.get_idx_split()
            return EzooGetItemGraph(self.e_graph, self.dgl_graph, self.idx_split, name=self.db_name)

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
            return self.dgl_graph.ndata['feat']

        # 获取所有节点的特征
        features = self.dgl_graph.ndata.pop('feat')

        if cache == 'cpu':
            nfeat = features
        elif cache == 'gpu':
            nfeat = features.to(device)
        elif cache == 'quiver':
            csr_topo = quiver.CSRTopo(torch.stack(self.dgl_graph.edges('uv')))
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


'''
异构图 getitem
'''


class EzooHeteroGetItemGraph(GetItemGraph):
    def __init__(self, e_graph=None, _graph=None, idx_split=None, label_dict=None, name=None):
        super(EzooHeteroGetItemGraph, self).__init__(
            e_graph=e_graph, _graph=_graph, name=name)
        self.idx_split = idx_split
        self.label_dict = label_dict


'''
异构图
XXX_exclude_list: 如果存在 '*' 则表示所有的点/边都不加载
'''


class EzooHeteroGraphDataset(EzooLoaderDataset):
    def __init__(self, name="ogbn-mag", rpc_url=None, raw_dir=None, force_reload=False, cfg_file=None, gdi_ptr=0, restore_file='', restore_url='', train_rate=0.6,
                 node_exclude_list=[], edge_exclude_list=[], schema_path='', iconf_path='', force_download=False, dataset_name='', feat_mapping={'node': {}, 'edge': {}}):
        self.node_exclude_list = node_exclude_list
        self.edge_exclude_list = edge_exclude_list
        # 映射边类型与udata、vdata的类型区别，以区分
        self.etype_dict_mapping = {}
        self.read_edge_feat = True
        super(EzooHeteroGraphDataset, self).__init__(name,
                                                     rpc_url=rpc_url,
                                                     raw_dir=raw_dir,
                                                     force_reload=force_reload,
                                                     cfg_file=cfg_file,
                                                     gdi_ptr=gdi_ptr,
                                                     restore_file=restore_file,
                                                     restore_url=restore_url,
                                                     cache_edge=True,
                                                     cache_node=True,
                                                     train_rate=train_rate,
                                                     schema_path=schema_path,
                                                     iconf_path=iconf_path,
                                                     force_download=force_download,
                                                     dataset_name=dataset_name,
                                                     feat_mapping=feat_mapping)

    '''
    1、获取异构图框架数据，并构建dgl.heterograph
    '''

    def get_graph_frame(self):
        num_nodes_dict = {}
        node_type_list = self.e_graph.get_node_type_list()
        for node_type in node_type_list:
            n_size = self.e_graph.get_nodes_num(node_type)
            num_nodes_dict[node_type] = n_size

        heter_graph_data = {}
        edge_type_list = self.e_graph.get_edge_type_list()
        type_map = self.e_graph.get_node_typeid_string_map()

        for edge_type in edge_type_list:
            src_ids, dst_ids, src_types, dst_types = self.e_graph.get_adjacencylist_from_etype(
                edge_type)

            if len(src_ids) == 0 or len(dst_ids) == 0:
                continue

            adj_data_df = pd.DataFrame(
                {'src_types': src_types, 'dst_types': dst_types, 'src_ids': src_ids, 'dst_ids': dst_ids})
            grouped = adj_data_df.groupby(['src_types', 'dst_types'])

            src_dst_type_dict = {}
            for key, group in grouped:
                triple = (type_map[key[0]], edge_type, type_map[key[1]])
                src_dst_type_dict[key] = triple

                heter_graph_data[triple] = (torch.tensor(
                    group['src_ids'].values.astype(numpy.int64)), torch.tensor(group['dst_ids'].values.astype(numpy.int64)))

            self.etype_dict_mapping[edge_type] = {
                'src_types': src_types, 'dst_types': dst_types, 'src_dst_type_dict': src_dst_type_dict}

        return dgl.heterograph(heter_graph_data, num_nodes_dict=num_nodes_dict)

    def set_heter_ne_data_unit(self, dgl_graph, ne_exclude_list, _ne_data='node'):
        if _ne_data != 'node':
            _tid = dgl_graph.edata._etid
            netype_dict = self.e_graph.get_all_edge_prop_names_with_etype()
            e_graph_nedata = self.e_graph.edata
            _set_ne_repr = dgl_graph._set_e_repr
            _nodes_or_edges = dgl_graph.edata._edges
            dgl_graph_netype = dgl_graph.etypes
        else:
            e_graph_nedata = self.e_graph.ndata
            _set_ne_repr = dgl_graph._set_n_repr
            _nodes_or_edges = dgl_graph.ndata._nodes
            dgl_graph_netype = dgl_graph.ntypes
            _tid = dgl_graph.ndata._ntid
            netype_dict = self.e_graph.get_all_node_prop_names_with_ntype()

        for type_id in _tid:
            netype = dgl_graph_netype[type_id]

            ne_dict = {}

            props = netype_dict[netype]
            props.sort(key=itemgetter('type'))

            self.set_data_unit(props, ne_exclude_list,
                                ne_dict,
                                e_graph_nedata_func=e_graph_nedata,
                                netype=netype, n_or_e=_ne_data)
            try:
                # 存在边有多种类型的情况，边对应两侧节点，有多种不同情况
                if _ne_data != 'node':
                    uv_edge_type = self.etype_dict_mapping[netype]

                    src_types = 'src_types'
                    dst_types = 'dst_types'
                    src_dst_type_dict = uv_edge_type['src_dst_type_dict']
                    ne_dict[src_types] = uv_edge_type[src_types]
                    ne_dict[dst_types] = uv_edge_type[dst_types]

                    '''
                    pandas只支持一维数组，但是还是要分组，同一边，但是不同类型的U、V起點終點
                    PS：一般情況下，一種類型中只有一份特徵屬性
                    '''
                    feat = 'feat'
                    if self.feat_mapping is not None \
                            and len(self.feat_mapping['edge']) > 0 \
                            and self.feat_mapping['edge'][netype]:
                        feat = [
                            k for k in self.feat_mapping['edge'][netype]][0]

                    feat_col_df = None
                    if ne_dict.__contains__(feat):
                        feat_tensor = ne_dict.pop(feat).T.numpy()
                        feat_col_df = pd.DataFrame(feat_tensor.reshape(-1, len(feat_tensor)), columns=[
                                                    feat + str(i) for i in range(feat_tensor.shape[0])])
                    adj_data_df = pd.DataFrame(ne_dict)
                    if feat_col_df is not None and len(feat_col_df) > 0:
                        adj_data_df = pd.concat(
                            [adj_data_df, feat_col_df], axis=1)

                    grouped = adj_data_df.groupby([src_types, dst_types])
                    for key, group in grouped:
                        triple = dgl_graph.canonical_etypes[type_id]
                        if src_dst_type_dict.__contains__(key) and src_dst_type_dict[key] == triple:
                            group_ne_dict = {}
                            columns = group.columns.values.tolist()

                            if feat_col_df is not None and len(feat_col_df) > 0:
                                group_ne_dict[feat] = torch.from_numpy(group.values.T[[col for col in range(
                                    len(columns)) if feat in columns[col]]].T).float()

                            for index_col in range(len(columns)):
                                col = columns[index_col]
                                # 跳过srctypes、dsttypes，然后形成dict形式，重新调用_set_ne_repr
                                if col == dst_types or col == src_types or feat in col:
                                    continue
                                group_ne_dict[col] = torch.from_numpy(
                                    group.values.T[index_col])
                            _set_ne_repr(
                                type_id, _nodes_or_edges, group_ne_dict)
                            break
                else:
                    _set_ne_repr(type_id, _nodes_or_edges, ne_dict)
            except Exception as e:
                print(ne_dict, '--- error ---', e)

    '''
    2、获取ndata数据
    '''

    def set_heter_graph_ndata(self, dgl_graph, exclude_list=['id']):
        self.set_heter_ne_data_unit(dgl_graph, exclude_list, _ne_data='node')

    '''
    3、获取edata数据
    '''

    def set_heter_graph_edata(self, dgl_graph, exclude_list=['id', 'label']):
        self.set_heter_ne_data_unit(dgl_graph, exclude_list, _ne_data='edge')

    '''
    异构图获取idx的掩码
    '''

    def get_idx_split_unit(self, dgl_graph_data_tid, dgl_graph_data_ne, dgl_graph_type, dgl_graph_get_ne_repr):
        _split_dict = {}
        for type_id in dgl_graph_data_tid:
            type = dgl_graph_type[type_id]
            _frame_dict = dgl_graph_get_ne_repr(type_id, dgl_graph_data_ne)
            for t_name in _frame_dict.keys():
                if 'mask' in t_name or 'train' in t_name or 'test' in t_name or 'val' in t_name or 'valid' in t_name:
                    if _split_dict.__contains__(t_name):
                        _split_dict[t_name][type] = _frame_dict[t_name].nonzero(
                        ).squeeze()
                    else:
                        _split_dict[t_name] = {
                            type: _frame_dict[t_name].nonzero().squeeze()}
        return _split_dict

    '''
    done：根据具体数据集，返回相应的边或者点的ids
    '''

    def get_idx_split(self):
        _idx_split_dict = {}
        _idx_split_dict['node_mask'] = self.get_idx_split_unit(
            self.dgl_graph.ndata._ntid, self.dgl_graph.ndata._nodes, self.dgl_graph.ndata._ntype, self.dgl_graph._get_n_repr)
        _idx_split_dict['edge_mask'] = self.get_idx_split_unit(
            self.dgl_graph.edata._etid, self.dgl_graph.edata._edges, self.dgl_graph.edata._etype, self.dgl_graph._get_e_repr)

        return _idx_split_dict

    def get_label_list(self):
        all_label_dict = {}
        nlabel = self.dgl_graph.ndata['label']
        elabel = self.dgl_graph.edata['label']
        all_label_dict['nlabel'] = nlabel
        all_label_dict['elabel'] = elabel
        return all_label_dict

    def __getitem__(self, item):
        # 返回e_graph、dgl.graph
        if item is EzooShapeGraphEnum.WHOLE:
            if self.node_exclude_list is not None and '*' not in self.node_exclude_list:
                self.set_heter_graph_ndata(
                    self.dgl_graph, exclude_list=self.node_exclude_list)
            if self.read_edge_feat and self.edge_exclude_list is not None and '*' not in self.edge_exclude_list:
                self.set_heter_graph_edata(
                    self.dgl_graph, exclude_list=self.edge_exclude_list)
            label_dict = self.get_label_list()

            # Set mask
            self.set_dgl_graph_mask()
            self.idx_split = self.get_idx_split()
            return EzooHeteroGetItemGraph(self.e_graph, self.dgl_graph, self.idx_split, label_dict)
        else:
            # Set mask
            self.set_dgl_graph_mask()
            self.idx_split = self.get_idx_split()
            return EzooHeteroGetItemGraph(self.e_graph, self.dgl_graph)

    def get_painter(self, notebook, nodes_limit=10, highlight_feats='', data_type=PaintDataTypeEnum.ALL):
        return HeterGraphPainter(self.dgl_graph, notebook, nodes_limit=nodes_limit, data_type=data_type)
