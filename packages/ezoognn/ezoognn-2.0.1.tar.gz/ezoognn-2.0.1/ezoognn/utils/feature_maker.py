from hashlib import algorithms_available

from .graph_store import GraphStore
from ..ezoocall import HandlerGenerateType
from ..ezoocall import SearchDirectionType
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler, LabelEncoder
from ..ezoo_graph import EzooEntityPropertyType
from .. import MAXINT

import numpy as np
import pandas as pd
from torchtext.data.utils import get_tokenizer
from torchtext.vocab import build_vocab_from_iterator
from torchtext.data import numericalize_tokens_from_iterator
import torch
from ezoognn.utils.data_utils import padding
from collections import defaultdict

class FeatureMaker():
    def __init__(self, *args, **kwargs):
        """
        Feature transformer, generate the new feature based on the features from origin graph.
        The possible operations includes:
        ----------
        1. Add features.
        2. Transform: user defined function operations, np.log10 etc.
                      value copy
                      min-max scale
                      standard scale
                      digitize(bins)
                      dummies(one hot)
                      node degree computation
                      graph mining node score
        Parameters
        ----------
        url: The GDB thrift url from which getting the DB's data, default value None
        cfg_file: The configuration directory, default value None
        """
        self.g_store = GraphStore(*args, **kwargs)

    def list_graph(self, is_activate=True):
        self.g_store.get_graph()

    def clear_graph_store(self):
        self.g_store.reset()

    def load_graph(self, db_name, restore_file='', restore_url='', schema_path='', init_type=HandlerGenerateType.Load):
        return self.g_store.get_graph(g_name=db_name, restore_file=restore_file, restore_url=restore_url, schema_path=schema_path,
                                      init_type=init_type)

    def copy_graph(self, dst_db_name, src_db_name):
        return self.graph_projection(dst_db_name, src_db_name)

    def graph_projection(self, dst_db_name, src_db_name='', restore_file='', restore_url='', schema_path='', del_props={}, add_props={}, directly_use_return=False):
        if directly_use_return:
            cache_node = cache_edge = True
        else:
            cache_node = cache_edge = False
        return self.g_store.get_graph(g_name=dst_db_name, init_type=HandlerGenerateType.Projection, src_db=src_db_name, restore_file=restore_file,
                                      restore_url=restore_url, schema_path=schema_path, del_props=del_props, add_props=add_props, cache_node=cache_node,
                                      cache_edge=cache_edge)

    def transform_func(self, func,
                       src_gname,
                       ntype,
                       src_column_names,
                       dst_gname,
                       dst_column_names=None,
                       dst_column_types=None,
                       **kwargs):
        '''
        Transform a source graph's column values to the target graph's column.
        '''
        src_graph = self.g_store.get_graph(g_name=src_gname)
        dst_graph = self.g_store.get_graph(g_name=dst_gname)

        out_cols = []
        for index, src_column in enumerate(src_column_names):
            if isinstance(src_column, list):
                input_param = [src_graph.ndata[ntype][column]
                               for column in src_column]
            else:
                input_param = src_graph.ndata[ntype][src_column]

            res = func(input_param, **kwargs)

            if len(res.shape) > 1:
                res_col_num = res.shape[1]
                cols = []

                for idx in range(res_col_num):
                    # 需要根据dst_column_names[0]来动态生成字段，因为ezoo不支持矩阵存储
                    if len(dst_column_names[0]) == 1:
                        prefix = dst_column_names[0][0]
                        col_name = '{}_{}'.format(prefix, idx)
                        dst_graph.add_node_property(
                            ntype, col_name, EzooEntityPropertyType.Float32.value, 0.0, '0')
                        dst_graph.ndata[ntype][col_name] = res[:, idx]
                        cols.append(col_name)
                    else:
                        dst_graph.ndata[ntype][dst_column_names[index]
                                               [idx]] = res[:, idx]
                        cols.append(dst_column_names[index][idx])

                out_cols.append(cols)
            else:
                dst_column = src_column if dst_column_names is None else dst_column_names[index]
                dst_column = dst_column[0] if isinstance(
                    dst_column, list) else dst_column
                if dst_column_types is not None:
                    dst_graph.remove_node_property(ntype, dst_column)
                    dst_column_type = dst_column_types[0] if len(dst_column_types) == 1 else dst_column_types[index]
                    dst_graph.add_node_property(
                        ntype, dst_column, dst_column_type, 0.0, '0')
                dst_graph.ndata[ntype][dst_column] = res


        # return output cols for loop call func
        return out_cols

    def node_value_copy(self, src_gname, ntype, src_column_names, dst_gname, dst_column_names=None):
        def func(data):
            return data
        self.transform_func(func, src_gname, ntype, src_column_names,
                            dst_gname, dst_column_names=dst_column_names)

    def __scaler_operate(self, scaler, src_gname, ntype, src_column_names, dst_gname, dst_column_names=None):
        def func(data, scaler):
            src_val = np.reshape(data, (-1, 1))
            return scaler.fit_transform(src_val).squeeze()

        self.transform_func(func, src_gname, ntype, src_column_names,
                            dst_gname, dst_column_names=dst_column_names, scaler=scaler)

    def min_max_scaler(self, src_gname, ntype, src_column_names, dst_gname, dst_column_names=None):
        scaler = MinMaxScaler()
        self.__scaler_operate(scaler, src_gname, ntype,
                              src_column_names, dst_gname, dst_column_names)

    def text_encoder(self, src_gname, ntype, src_column_names, dst_gname):
        """
        将文本类型的特征转换位数值类型，并返回对应字典
        :param src_gname: 图名称
        :param ntype: 节点类型
        :param src_column_names: 节点字段名称
        :param dst_gname: 新字典写入的图名称
        :return: 返回字典和生成的特征长度
        """
        src_graph = self.g_store.get_graph(src_gname)
        dst_graph = self.g_store.get_graph(dst_gname)
        textset = {}
        tokenizer = get_tokenizer(None)

        textlist = []
        item_texts = {}
        for src_column_name in src_column_names:
            item_texts[src_column_name] = src_graph.ndata[ntype][src_column_name]

        for i in range(len(src_graph.ndata[ntype][src_column_names[0]])):
            for key in item_texts.keys():
                l = tokenizer(item_texts[key][i].lower())
                textlist.append(l)
        for key, field in item_texts.items():
            vocab2 = build_vocab_from_iterator(
                textlist, specials=["<unk>", "<pad>"]
            )
            textset[key] = (
                textlist,
                vocab2,
                vocab2.get_stoi()["<pad>"],
                True,
            )

        node_ids = src_graph.ndata[ntype]['id']

        newfield_len = defaultdict(int)
        for field_name, field in textset.items():
            textlist, vocab, pad_var, batch_first = field

            examples = [textlist[i] for i in node_ids]
            ids_iter = numericalize_tokens_from_iterator(vocab, examples)

            maxsize = max([len(textlist[i]) for i in node_ids])
            ids = next(ids_iter)
            x = torch.asarray([num for num in ids])
            lengths = torch.tensor([len(x)])
            tokens = padding(x, maxsize, pad_var)

            for ids in ids_iter:
                x = torch.asarray([num for num in ids])
                l = torch.tensor([len(x)])
                y = padding(x, maxsize, pad_var)
                tokens = torch.vstack((tokens, y))
                lengths = torch.cat((lengths, l))

            new_columns_name = [f"{field_name}{i}" for i in range(tokens.size()[1])]
            features = pd.DataFrame(tokens.numpy(), columns=new_columns_name)
            for new_column in new_columns_name:
                print(
                    f'==== generate new columns {ntype}:{new_column} in the graph {dst_gname} ====')
                dst_graph.add_node_property(
                    ntype, new_column, EzooEntityPropertyType.Int32.value, 1, '0')
                dst_graph.ndata[ntype][new_column] = features[new_column]
                newfield_len[field_name] += 1

        return textset, newfield_len

    def standard_scaler(self, src_gname, ntype, src_column_names, dst_gname, dst_column_names=None):
        scaler = StandardScaler()
        self.__scaler_operate(scaler, src_gname, ntype,
                              src_column_names, dst_gname, dst_column_names)

    def digitize(self, bins, src_gname, ntype, src_column_names, dst_gname, dst_column_names=None):
        def func(data, bins):
            return np.digitize(data, bins)
        self.transform_func(func, src_gname, ntype, src_column_names,
                            dst_gname, dst_column_names=dst_column_names, bins=bins)

    def dummies(self, src_gname, ntype, src_column_names, dst_gname):
        '''
        Get dummies of src_columns_names columns, save the result to the dst_gname graph.
        New columns should be created in the target graph.
        '''
        src_graph = self.g_store.get_graph(g_name=src_gname)
        features = None
        for src_column in src_column_names:
            features = np.column_stack(
                (features, src_graph.ndata[ntype][src_column])) if features is not None else src_graph.ndata[ntype][src_column]
        features = pd.DataFrame(
            features, columns=src_column_names)
        features = pd.get_dummies(features, columns=src_column_names)

        dst_graph = self.g_store.get_graph(g_name=dst_gname)
        new_columns_name = features.columns.values.tolist()
        for new_column in new_columns_name:
            print(
                f'==== generate new columns {ntype}:{new_column} in the graph {dst_gname} ====')
            dst_graph.add_node_property(
                ntype, new_column, EzooEntityPropertyType.Int32.value, 1, '0')
            dst_graph.ndata[ntype][new_column] = features[new_column]

    def set_degree_prop(self, src_gname, dst_gname, dir, dst_ntype, dst_column_name):
        '''
        Set the node's degree to the dst_ntype:dst_column_name property of the graph named dst_gname.
        The dst_column_name should be created in advance.
        The parameter dir should be type of ezoocall.SearchDirectionType, 0 stands for the directionn in, 
        1 for out and 2 for in_out.
        '''
        src_graph = self.g_store.get_graph(g_name=src_gname)
        dst_graph = self.g_store.get_graph(g_name=dst_gname)
        dst_graph.ndata[dst_ntype][dst_column_name] = src_graph.get_inout_degree(
            dir.value, MAXINT)

    def set_mining_score_prop(self, src_gname, alg_name, dst_gname, dst_ntype, dst_column_name, **kwargs):
        '''
        Set the algorithm result on source graph to the dst_ntype:dst_column_name property of the graph named dst_gname.
        The dst_column_name should be created in advance.
        alg_name is type of string, can be: 'pagerank', 'wcc', 'scc', 'louvain', 'lpa', 'k-core'
        '''
        if alg_name not in {'pagerank', 'wcc', 'scc', 'louvain', 'lpa', 'k-core'}:
            return f'Algorithm {alg_name} is not be supported!'
        src_graph = self.g_store.get_graph(g_name=src_gname)
        score = getattr(self, '_' + alg_name)(src_graph, **kwargs)
        dst_graph = self.g_store.get_graph(g_name=dst_gname)
        dst_graph.ndata[dst_ntype][dst_column_name] = score

    def _pagerank(self, graph, damping_factor=0.85, epoch_limit=100, max_convergence_error=0.001, vertex_init_value=1,
                  bidirection=False, edge_type='', weight_pro_name=''):
        return graph.pagerank(damping_factor, epoch_limit, max_convergence_error,
                              vertex_init_value, bidirection, edge_type, weight_pro_name)

    def _wcc(self, graph):
        # Only return the community's number the nodes belong to
        return graph.wcc()[0]

    def _scc(self, graph):
        # Only return the community's number the nodes belong to
        return graph.scc()[0]

    def _louvain(self, graph, edge_type='', prop_name='', max_iter=10, max_levels=10, thread_num=1):
        return graph.louvain(edge_type, prop_name, max_iter, max_levels, thread_num)[0]

    def _lpa(self, graph, epoch_limit=100):
        return graph.lpa(epoch_limit)

    def _k_core(self, graph, k_max=5):
        return graph.k_core(k_max)

    def call_balance_udf(self, src_gname, **kwargs):
        from .feature_custom import call_udf_transform
        src_graph = self.g_store.get_graph(g_name=src_gname)
        return call_udf_transform(src_graph, **kwargs)

    def data_selection(self, gname, dataset_name, ntypes, is_udf=False, **kwargs):
        import os
        import shutil
        from ezoognn import get_ezoo_home
        import pandas as pd

        def build_dataset_dir():
            graph_home = "{}/{}".format(get_ezoo_home(
                self.g_store.cfg_file), gname)
            if not os.path.exists(graph_home):
                os.mkdir(graph_home)

            dataset_path = "{}/{}".format(graph_home, dataset_name)
            if os.path.exists(dataset_path):
                shutil.rmtree(dataset_path)
            os.mkdir(dataset_path)

            return dataset_path

        dataset_path = build_dataset_dir()
        graph = self.g_store.get_graph(g_name=gname)
        node_entity = graph.ndata[ntypes]

        if is_udf:
            from feature_custom import call_udf_transform
            train_mask, val_mask, test_mask = call_udf_transform(
                node_entity, **kwargs)
        else:
            op = kwargs['op']
            del kwargs['op']
            train_mask, val_mask, test_mask = op.split_tvt(
                node_entity, **kwargs)

        data = {"n###{}###train_mask".format(ntypes): train_mask,
                "n###{}###val_mask".format(ntypes): val_mask,
                "n###{}###test_mask".format(ntypes): test_mask}

        pd.DataFrame(data).to_csv(
            "{}/node_mask.csv".format(dataset_path), index=False)

        # return count of t, v, t
        return train_mask.sum(), val_mask.sum(), test_mask.sum()

    def data_sampling(self, graph, is_udf=False, **kwargs):
        graph = self.g_store.get_graph(g_name=graph)

        if is_udf:
            from feature_custom import call_udf_transform
            call_udf_transform(graph, **kwargs)
        else:
            op = kwargs['op']
            del kwargs['op']
            op.balance(graph, **kwargs)
