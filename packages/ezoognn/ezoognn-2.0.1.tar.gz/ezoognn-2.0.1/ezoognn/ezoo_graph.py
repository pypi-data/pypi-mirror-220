import torch
import numpy as np
from itertools import groupby
from operator import itemgetter
from . import ezoocall
from . import rpc_client
from .ezoocall import HandlerGenerateType
from .utils.painter import EzooGraphPainter


class entity_data(object):
    def __init__(self, node_or_edge, graph):
        self.node_or_edge = node_or_edge
        self.graph = graph

    @staticmethod
    def translate_data_type(prop_type):
        t = EzooEntityPropertyType(prop_type)
        if t == EzooEntityPropertyType.Bool:
            result = 'Bool'
        elif t == EzooEntityPropertyType.Int32:
            result = 'Int32'
        elif t == EzooEntityPropertyType.Int64:
            result = 'Int64'
        elif t == EzooEntityPropertyType.Float32:
            result = 'Float32'
        elif t == EzooEntityPropertyType.Float64:
            result = 'Float64'
        elif t == EzooEntityPropertyType.String:
            result = 'String'
        else:
            result = 'Unknown'
        return result

    def get_num(self):
        res = {}
        if 'node' == self.node_or_edge:
            get_num_func = self.graph.get_nodes_num
            entity_type_and_props = self.graph.get_all_node_prop_names_with_ntype()
        else:
            get_num_func = self.graph.get_edges_num
            entity_type_and_props = self.graph.get_all_edge_prop_names_with_etype()

        total = 0
        for _type in entity_type_and_props:
            num = get_num_func(_type)
            res[_type] = num
            total = total + num

        res['total'] = total
        return res

    def describe(self):
        sep = '\n'
        info = []
        if 'node' == self.node_or_edge:
            info.append('------ node type and properties ------')
            entity_type_and_props = self.graph.get_all_node_prop_names_with_ntype()
            get_num_func = self.graph.get_nodes_num
        else:
            info.append('------ edge type and properties ------')
            entity_type_and_props = self.graph.get_all_edge_prop_names_with_etype()
            get_num_func = self.graph.get_edges_num

        for _type in entity_type_and_props:
            info.append('entity_type ' + _type + ':')
            info.append('number: ' + str(get_num_func(_type)))
            props = entity_type_and_props[_type]
            prop_info = []
            for prop in props:
                prop_info.append(
                    {'name': prop['name'], 'type': self.translate_data_type(prop['type'])})
            info.append(str(prop_info))

        return sep.join(info)


class edata_props():
    def __init__(self, edge_type, graph=None, string_to_int=False):
        self.edge_type = edge_type
        self.graph = graph
        self.string_to_int = string_to_int

    def get_values_according_type(self, etype, prop_type, prop_name_list):
        graph = self.graph
        t = EzooEntityPropertyType(prop_type)
        if t == EzooEntityPropertyType.Bool:
            result = np.array(graph.get_edge_props2bool(
                etype, prop_name_list))
        elif t == EzooEntityPropertyType.Int32 or (self.string_to_int and t == EzooEntityPropertyType.String):
            result = graph.get_edge_props2int(
                etype, prop_name_list)
            result = result.astype(np.int64)
        elif t == EzooEntityPropertyType.Int64:
            result = graph.get_edge_props2long(
                etype, prop_name_list)
        elif t == EzooEntityPropertyType.Float32:
            result = graph.get_edge_props2float(
                etype, prop_name_list)
        elif t == EzooEntityPropertyType.Float64:
            result = graph.get_edge_props2double(
                etype, prop_name_list)
        elif t == EzooEntityPropertyType.String:
            result = graph.get_edge_props2string(
                etype, prop_name_list)
        return result

    def set_values_according_type(self, etype, prop_type, prop_name, prop_values):
        graph = self.graph
        t = EzooEntityPropertyType(prop_type)
        if t == EzooEntityPropertyType.Bool:
            graph.update_all_edges_bool_property(
                etype, prop_name, prop_values)
        elif t == EzooEntityPropertyType.Int32 or (self.string_to_int and t == EzooEntityPropertyType.String):
            graph.update_all_edges_int_property(
                etype, prop_name, prop_values)
        elif t == EzooEntityPropertyType.Int64:
            graph.update_all_edges_int_property(
                etype, prop_name, prop_values.astype(np.int32))
        elif t == EzooEntityPropertyType.Float32:
            graph.update_all_edges_float_property(
                etype, prop_name, prop_values)
        elif t == EzooEntityPropertyType.Float64:
            graph.update_all_edges_double_property(
                etype, prop_name, prop_values)
        elif t == EzooEntityPropertyType.String:
            graph.update_all_edges_string_property(
                etype, prop_name, prop_values)

    def get_oneprop_data_by_type(self, key):
        prop_type = self.graph.get_edge_prop_type_from_name(
            self.edge_type, key)

        result = self.get_values_according_type(
            self.edge_type, prop_type, [key])
        # 极端场景下，比如边/点只有一个元素的情况下，如果使用numpy.squeeze()删除一维度的形状，则会造成错误，所以这里需要额外判断只有一个元素的情况
        if result.size == 1:
            return result.reshape((1, ))
        return np.squeeze(result)

    def get_prop_data_by_type(self, exclude_list=[]):
        nedata_dict = {}
        props_dict = self.graph.get_all_edge_prop_names_with_etype()

        props = props_dict[self.edge_type]
        props.sort(key=itemgetter('type'))
        props = [p for p in props if p['name'] not in exclude_list]

        bool_props_arr, int_props_arr, long_props_arr, float_props_arr, features_arr, double_props_arr, string_props_arr = self.graph.get_edge_all_props_with_type_diff(
            self.edge_type, exclude_list)
        # bool_props_arr = np.array(bool_props_arr)

        feat_name_list = [p['name']
                          for p in props if p['name'].startswith('feat')]
        if len(features_arr) > 0:
            nedata_dict['feat'] = torch.from_numpy(features_arr)

        props = [p for p in props if p['name'] not in feat_name_list]

        for key, value in groupby(props, key=itemgetter('type')):
            key = EzooEntityPropertyType(key)
            names = [x['name'] for x in value]
            if key == EzooEntityPropertyType.Bool:
                bool_props_arr = bool_props_arr.transpose()
                # bool_tensor = torch.from_numpy(bool_props_arr)
                for i in range(len(names)):
                    name = names[i]
                    nedata_dict[name] = bool_props_arr[i]
            elif key == EzooEntityPropertyType.Int32:
                int_props_arr = int_props_arr.transpose()
                # int_tensor = torch.from_numpy(int_props_arr)
                for i in range(len(names)):
                    name = names[i]
                    # 兼容一开始的数据库格式....
                    if name in 'labels':
                        nedata_dict[name] = int_props_arr[i].long()
                    else:
                        nedata_dict[name] = int_props_arr[i]
            elif key == EzooEntityPropertyType.Int64:
                long_props_arr = long_props_arr.transpose()
                # long_tensor = torch.from_numpy(long_props_arr)
                for i in range(len(names)):
                    name = names[i]
                    nedata_dict[name] = long_props_arr[i]
            elif key == EzooEntityPropertyType.Float32:
                float_props_arr = float_props_arr.transpose()
                # float_tensor = torch.from_numpy(float_props_arr)
                for i in range(len(names)):
                    name = names[i]
                    nedata_dict[name] = float_props_arr[i]
            elif key == EzooEntityPropertyType.Float64:
                double_props_arr = double_props_arr.transpose()
                # double_tensor = torch.from_numpy(double_props_arr)
                for i in range(len(names)):
                    name = names[i]
                    nedata_dict[name] = double_props_arr[i]
            else:
                string_props_arr = string_props_arr.transpose()
                # string_int_tensor = torch.from_numpy(string_props_arr)
                for i in range(len(names)):
                    name = names[i]
                    nedata_dict[name] = string_props_arr[i]
        return nedata_dict

    def __getitem__(self, key):
        # 单独字符串属性名称，则将该属性获取返回，也可以判断
        if isinstance(key, str):
            return self.get_oneprop_data_by_type(key)
        elif isinstance(key, (list, set, tuple)):
            result = []
            for i in key:
                result.append(self.get_oneprop_data_by_type(i))
            return result
        elif isinstance(key, slice):
            if key.stop is None:
                exclude_list = []
                if isinstance(key.step, (list, set, tuple)):
                    exclude_list = key.step
                # 表示获取全部的, key.step表示exclude_list的值
                return self.get_prop_data_by_type(exclude_list)
            else:
                # 表示获取综合起来作为一个字段返回的数据
                prop_type = self.graph.get_edge_prop_type_from_name(
                    self.edge_type, key.stop[0])

                result = self.get_values_according_type(
                    self.edge_type, prop_type, key.stop)
                return np.squeeze(result)
        else:
            print('could not analysis form !!!', TypeError(key))

    def __setitem__(self, key, value):
        # key's format should be "edge_type:prop_name"
        # value should be a numpy array
        etype = self.edge_type
        column_name = key
        prop_type = self.graph.get_edge_prop_type_from_name(
            etype, column_name)

        self.set_values_according_type(etype, prop_type, column_name, value)

    def get_edges_num(self):
        return self.graph.get_edges_num(self.edge_type)


class edata(entity_data):
    def __init__(self, graph):
        super().__init__('edge', graph)

    def __getitem__(self, key):
        # The first dimension is string, defines the node type
        if isinstance(key, str):
            return edata_props(key, graph=self.graph)
        else:
            assert isinstance(
                key, slice), 'The first dimension should be string or slice'
            # The special data retriving, getting int type to represent the string for GNN, e.g.
            return edata_props(key.stop, graph=self.graph, string_to_int=True)


'''
三种格式：
    1 单独一个字符串，表示获取该类型的对应属性值，如: ['train_mask']
    2 数组形式，表示批量获取数组元素指定的属性名对应的值，如: ['feat1', 'feat2', 'feat3']
    3 切片形式，分为两种
        (1) 数值类型，表示获取所有的属性值，仅一种传值，如: [:]/[0:]/[::['zzz', 'xxx']]/[0::['zzz', 'xxx']]
        (2) start=str end=[str, str]形式，表示，end的切片形式是组成一种名字叫做start=str的形式，如: ('feat': ['feat1', 'feat2', 'feat3'])
'''


class ndata_props():
    def __init__(self, node_type, graph=None, string_to_int=False):
        self.node_type = node_type
        self.graph = graph
        self.string_to_int = string_to_int

    def get_values_according_type(self, ntype, prop_type, prop_name_list):
        graph = self.graph
        t = EzooEntityPropertyType(prop_type)
        if t == EzooEntityPropertyType.Bool:
            result = graph.get_node_props2bool(
                ntype, [], prop_name_list)
            result = result.astype(np.uint8)
        elif t == EzooEntityPropertyType.Int32 or (self.string_to_int and t == EzooEntityPropertyType.String):
            result = graph.get_node_props2int(
                ntype, [], prop_name_list)
            result = result.astype(np.int64)
        elif t in [EzooEntityPropertyType.Int64, EzooEntityPropertyType.Timestamp]:
            result = graph.get_node_props2long(
                ntype, [], prop_name_list)
        elif t == EzooEntityPropertyType.Float32:
            result = graph.get_node_props2float(
                ntype, [], prop_name_list)
        elif t == EzooEntityPropertyType.Float64:
            result = graph.get_node_props2double(
                ntype, [], prop_name_list)
        elif t == EzooEntityPropertyType.String:
            result = graph.get_node_props2string(
                ntype, [], prop_name_list)

        return result

    def set_values_according_type(self, ntype, prop_type, prop_name, prop_values):
        graph = self.graph
        t = EzooEntityPropertyType(prop_type)
        if t == EzooEntityPropertyType.Bool:
            graph.update_all_nodes_bool_property(
                ntype, prop_name, prop_values)
        elif t == EzooEntityPropertyType.Int32 or (self.string_to_int and t == EzooEntityPropertyType.String):
            graph.update_all_nodes_int_property(
                ntype, prop_name, prop_values)
        elif t == EzooEntityPropertyType.Int64:
            graph.update_all_nodes_int_property(
                ntype, prop_name, prop_values.astype(np.int32))
        elif t == EzooEntityPropertyType.Float32:
            graph.update_all_nodes_float_property(
                ntype, prop_name, prop_values)
        elif t == EzooEntityPropertyType.Float64:
            graph.update_all_nodes_double_property(
                ntype, prop_name, prop_values)
        elif t == EzooEntityPropertyType.String:
            graph.update_all_nodes_string_property(
                ntype, prop_name, prop_values)

    def get_oneprop_data_by_type(self, key):
        prop_type = self.graph.get_node_prop_type_from_name(
            self.node_type, key)

        result = self.get_values_according_type(
            self.node_type, prop_type, [key])

        if result.size == 1:
            return result.reshape((1, ))
        return np.squeeze(result)

    def get_prop_data_by_type(self, exclude_list=[]):
        nedata_dict = {}
        props_dict = self.graph.get_all_node_prop_names_with_ntype()

        props = props_dict[self.node_type]
        props.sort(key=itemgetter('type'))
        props = [p for p in props if p['name'] not in exclude_list]

        bool_props_arr, int_props_arr, long_props_arr, float_props_arr, features_arr, double_props_arr, string_props_arr = self.graph.get_node_all_props_with_type_diff(
            self.node_type, exclude_list)

        feat_name_list = [p['name']
                          for p in props if p['name'].startswith('feat')]
        if len(features_arr) > 0:
            nedata_dict['feat'] = torch.from_numpy(features_arr)

        props = [p for p in props if p['name'] not in feat_name_list]

        for key, value in groupby(props, key=itemgetter('type')):
            key = EzooEntityPropertyType(key)
            names = [x['name'] for x in value]
            if key == EzooEntityPropertyType.Bool:
                bool_props_arr = bool_props_arr.transpose()
                # bool_tensor = torch.from_numpy(bool_props_arr)
                for i in range(len(names)):
                    name = names[i]
                    nedata_dict[name] = bool_props_arr[i]
            elif key == EzooEntityPropertyType.Int32:
                int_props_arr = int_props_arr.transpose()
                # int_tensor = torch.from_numpy(int_props_arr)
                for i in range(len(names)):
                    name = names[i]
                    # 兼容一开始的数据库格式....
                    if name == 'labels' or name == 'label':
                        nedata_dict[name] = int_props_arr[i].astype('int64')
                    else:
                        nedata_dict[name] = int_props_arr[i]
            elif key == EzooEntityPropertyType.Int64:
                long_props_arr = long_props_arr.transpose()
                # long_tensor = torch.from_numpy(long_props_arr)
                for i in range(len(names)):
                    name = names[i]
                    nedata_dict[name] = long_props_arr[i]
            elif key == EzooEntityPropertyType.Float32:
                float_props_arr = float_props_arr.transpose()
                # float_tensor = torch.from_numpy(float_props_arr)
                for i in range(len(names)):
                    name = names[i]
                    nedata_dict[name] = float_props_arr[i]
            elif key == EzooEntityPropertyType.Float64:
                double_props_arr = double_props_arr.transpose()
                # double_tensor = torch.from_numpy(double_props_arr)
                for i in range(len(names)):
                    name = names[i]
                    nedata_dict[name] = double_props_arr[i]
            else:
                string_props_arr = string_props_arr.transpose()
                # string_int_tensor = torch.from_numpy(string_props_arr)
                for i in range(len(names)):
                    name = names[i]
                    nedata_dict[name] = string_props_arr[i]
        return nedata_dict

    def __getitem__(self, key):
        # 单独字符串属性名称，则将该属性获取返回，也可以判断
        if isinstance(key, str):
            return self.get_oneprop_data_by_type(key)
        elif isinstance(key, (list, set, tuple)):
            result = []
            for i in key:
                result.append(self.get_oneprop_data_by_type(i))
            return result
        elif isinstance(key, slice):
            if key.stop is None:
                exclude_list = []
                if isinstance(key.step, (list, set, tuple)):
                    exclude_list = key.step
                # 表示获取全部的, key.step表示exclude_list的值. example: ndata['node'][:None:]
                return self.get_prop_data_by_type(exclude_list)
            elif isinstance(key.stop, (list, tuple)):
                # 表示获取综合起来作为一个字段返回的数据
                prop_type = self.graph.get_node_prop_type_from_name(
                    self.node_type, key.stop[0])

                result = self.get_values_according_type(
                    self.node_type, prop_type, key.stop)
                return np.squeeze(result)
            else:
                print('could not analysis form !!!', TypeError(key))
        else:
            print('could not analysis form !!!', TypeError(key))

    def __setitem__(self, key, value):
        ntype = self.node_type
        column_name = key

        prop_type = self.graph.get_node_prop_type_from_name(
            ntype, column_name)
        self.set_values_according_type(ntype, prop_type, column_name, value)

    def get_nodes_num(self):
        return self.graph.get_nodes_num(self.node_type)


class ndata(entity_data):
    def __init__(self, graph):
        super().__init__('node', graph)

    def __getitem__(self, key):
        # The first dimension is string, defines the node type
        if isinstance(key, str):
            return ndata_props(key, graph=self.graph)
        else:
            assert isinstance(
                key, slice), 'The first dimension should be string or slice'
            # The special data retriving, getting int type to represent the string for GNN, e.g.
            return ndata_props(key.stop, graph=self.graph, string_to_int=True)


class EzooGraph(object):
    def __init__(self, url='', dbname='', cfg_file='', schema_path='', iconf_path='', gdi_ptr=0, restore_file='',
                 restore_url='', cache_edge=True, cache_node=True, init_type=HandlerGenerateType.Load, src_db='',
                 del_props={}, add_props={}):
        if url != None and url != '':
            self.init_rpc_client(url, dbname)
        else:
            self.init_native_client(
                dbname=dbname, cfg_file=cfg_file, schema_path=schema_path, iconf_path=iconf_path,
                restore_file=restore_file, restore_url=restore_url, gdi_ptr=gdi_ptr,
                cache_edge=cache_edge, cache_node=cache_node, init_type=init_type, src_db=src_db,
                del_props=del_props, add_props=add_props)
        self.ndata = ndata(self.client)
        self.edata = edata(self.client)

    def init_rpc_client(self, url, dbname):
        self.client = rpc_client.RpcClient(url, dbname)

    def init_native_client(self, dbname, cfg_file, schema_path, iconf_path, gdi_ptr, restore_file, restore_url,
                           cache_edge, cache_node, init_type, src_db, del_props, add_props):
        self.client = ezoocall.graph_handler(dbname, cfg_file, restore_file, restore_url,
                                             schema_path, iconf_path, gdi_ptr, cache_edge, cache_node, init_type,
                                             src_db, del_props, add_props)

    @property
    def graph(self):
        return self.client

    def __getattr__(self, attr):
        return getattr(self.client, attr)

    def describe(self):
        sep = '\n'
        graph_info = []
        graph_info.append('====== graph informations ======')
        graph_info.append(self.ndata.describe())
        graph_info.append(self.edata.describe())
        return sep.join(graph_info)

    def paint(self, notebook=False, node_limit=100, highlight_feats='', output_file='example.html'):
        painter = EzooGraphPainter(
            self, notebook=notebook, nodes_limit=node_limit, highlight_feats=highlight_feats)
        return painter.draw_graph(output_file=output_file)


EzooEntityPropertyType = ezoocall.EzooEntityPropertyType
