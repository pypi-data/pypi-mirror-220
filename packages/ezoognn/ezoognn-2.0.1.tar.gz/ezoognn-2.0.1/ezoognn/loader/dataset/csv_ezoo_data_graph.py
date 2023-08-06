import os
import abc
import csv
import dgl
import torch
import numpy
import pandas
import pkgutil
from pathlib import Path
from jinja2 import Template
from itertools import zip_longest
from ezoognn.loader.dataset.ezoo_data_graph import EzooShapeGraphEnum, EzooExampleDatasetEnum, EzooGraphDataset, EzooHeteroGraphDataset

file_current_dir = Path(__file__).resolve().parent


def replace(x, old, new=None, strip=False) -> str:
    if not new:
        new = ''
    if isinstance(old, str):
        x = x.replace(old, new)
    if isinstance(old, list):
        for _old, _new in zip_longest(old, new, fillvalue='_'):
            if _new == None:
                _new = ''
            x = x.replace(_old, _new)

    if strip:
        x = x.strip()
    return x

def str2filename(url):
    return replace(url, ['S:', '.', '<', '>', '/', '\\', '|', ':', '*', '?', '://'])


class EzooDataset(object):
    def __init__(self):
        self.node_mask_dict = {}
        self.edge_mask_dict = {}
        self.jinja_path = os.sep + 'loader' + os.sep + 'dataset' + os.sep + 'jinja_py' + os.sep
        super(EzooDataset, self).__init__()

    def torch_type_2_cpp_type(self, torch_type):
        if torch_type == torch.int:
            return 'int32'
        elif torch_type == torch.int8:
            return 'int32'
        elif torch_type == torch.int16:
            return 'int32'
        elif torch_type == torch.int32:
            return 'int32'
        elif torch_type == torch.uint8:
            return 'int32'
        elif torch_type == torch.int64:
            return 'int64'
        elif torch_type == torch.bool:
            return 'bool'
        elif torch_type == torch.float:
            return 'float32'
        elif torch_type == torch.float16:
            return 'float32'
        elif torch_type == torch.float32:
            return 'float32'
        elif torch_type == torch.float64:
            return 'float64'
        elif torch_type == torch.double:
            return 'float64'
        else:
            return 'string'

    def build_mask_file(self, k, mask_tensor, number_nodes_tensor, node=True):
        arr = []
        if mask_tensor is not None and \
                mask_tensor.dtype == torch.bool and \
                mask_tensor.shape[0] == \
                number_nodes_tensor.shape[0]:
            mask_tensor = mask_tensor.int()
            for prop in numpy.ndenumerate(mask_tensor):
                location = prop[0]
                index = location[0]
                value = prop[1]
                arr.append(value)
        else:
            mask_nodes_tensor = torch.zeros((number_nodes_tensor.shape[0], 1)).int()
            for i in mask_nodes_tensor.numpy():
                mask_nodes_tensor[i.min()] = 1

            for prop in numpy.ndenumerate(mask_tensor):
                location = prop[0]
                index = location[0]
                value = prop[1]
                arr.append(value)
        if node:
            self.node_mask_dict[k] = arr
        else:
            self.edge_mask_dict[k] = arr

    def write_mask_csv(self):
        if self.node_mask_dict.__len__() > 0:
            node_headers = [header for header in self.node_mask_dict.keys()]
            node_frames = [frame for frame in self.node_mask_dict.values()]
            node_frames = numpy.array(node_frames).T
            node_frames = pandas.DataFrame(node_frames)
            node_frames.to_csv(self.path + 'node_mask.csv', mode='w', header=node_headers)

        if self.edge_mask_dict.__len__() > 0:
            edge_headers = [header for header in self.edge_mask_dict.keys()]
            edge_frames = [frame for frame in self.edge_mask_dict.values()]
            edge_frames = numpy.array(edge_frames).T
            edge_frames = pandas.DataFrame(edge_frames)
            edge_frames.to_csv(self.path + 'edge_mask.csv', mode='w', header=edge_headers)

    def __getitem__(self, item):
        return self.path


'''
点同构图，这一类是点同构图
'''


class EzooPublicDataset(EzooDataset):
    def __init__(self, name=None, path=None, dgl_graph=None, cache=False):
        super(EzooPublicDataset, self).__init__()
        self.dgl_graph = dgl_graph
        self.name = name
        self.cache = cache

        if path is None:
            path = "." + os.sep
        self.path = path + name + os.sep
        if not os.path.exists(self.path):
            os.makedirs(self.path)

        number_nodes_tensor = self.dgl_graph.nodes()

        ndata_dataview = self.dgl_graph.ndata
        ndata_dic = []
        for k in ndata_dataview:
            ndata_dic.append(k)
            if 'mask' in k or 'train' in k or 'test' in k or 'valid' in k or 'val' in k:
                ndata_dataview[k] = self._get_mask(ndata_dataview[k], number_nodes_tensor=number_nodes_tensor)
            else:
                ndata_dataview[k] = ndata_dataview[k]

        self.ndata_dic = ndata_dic

        edata_dataview = self.dgl_graph.edata
        edata_dic = []
        # edgeids
        # edge size
        src, dst, edges = self.dgl_graph.edges('all')
        self.dgl_graph.edata['edgeIds'] = edges
        for k in edata_dataview:
            if 'mask' in k or 'train' in k or 'test' in k or 'valid' in k or 'val' in k:
                # 不再设置到数据库中
                self.build_mask_file('edge###' + k, edata_dataview[k], edges)
            else:
                edata_dic.append(k)
        self.edata_dic = edata_dic

        # pandas写mask为csv文件
        self.write_mask_csv()

        self.node_index = 0
        self.edge_index = 3
        self.schema_json = self.build_conf_json()

        self._build_ezoo_file()

    def _get_mask(self, mask_tensor, number_nodes_tensor):
        # dgl的数据集，使用的是true、false的数据类型表示mask；ogb的数据类型则是数值类型，直接表示节点或者位置；这里判断用于兼容citation数据集
        if mask_tensor is not None and mask_tensor.dtype == torch.bool and mask_tensor.shape[0] == number_nodes_tensor.shape[0]:
            return mask_tensor
        mask_nodes_tensor = torch.zeros((number_nodes_tensor.shape[0], 1)).bool()
        for i in mask_tensor.numpy():
            mask_nodes_tensor[i.min()] = True
        return mask_nodes_tensor

    def _build_ezoo_file(self):
        self.build_schema_conf()
        self.build_import_conf()
        self.build_node_csv()
        self.build_edge_csv()

    def __getitem__(self, idx):
        return self.path

    def build_node_csv(self):
        f_nodes = open(self.path + self.name + '-node.csv', 'w', newline='', encoding='utf-8')
        f_nodes_write = csv.writer(f_nodes)

        # nodes_size
        nodes = self.dgl_graph.nodes()
        nodes_size = nodes.shape[0]
        # nodes 特征属性等信息
        _row_array = torch.empty([nodes_size, 0])
        for tag in self.ndata_dic:
            tag_tensor = self.dgl_graph.ndata[tag]
            dim = len(tag_tensor.shape)
            if dim == 1:
                tag_tensor = torch.reshape(tag_tensor, (tag_tensor.shape[0], 1))
            _row_array = torch.hstack((_row_array, tag_tensor))
        # node's ids
        _row_array = torch.hstack((nodes.reshape([nodes_size, 1]).int(), _row_array)).numpy()

        # 数据类型转换，并写数据到csv
        line_row = []
        row_size = _row_array.shape[1] - 1
        for prop in numpy.ndenumerate(_row_array):
            location = prop[0]
            i = location[0]
            y = location[1]
            value = prop[1]

            if y <= -1:
                line_row.append(int(value))
            else:
                line_row.append(value)

            if y == row_size:
                f_nodes_write.writerow(line_row)
                line_row = []
            if i % 10000 == 0 and i != 0:
                print('build ', self.name, ' node :', i)
                # break
        f_nodes.close()

    def build_edge_csv(self):
        f_edges = open(self.path + self.name + '-edge.csv', 'w', newline='', encoding='utf-8')
        f_edges_write = csv.writer(f_edges)

        # edge size
        src, dst, edges = self.dgl_graph.edges('all')

        edges_size = edges.shape[0]
        # edge 特征属性等信息
        _row_array = torch.empty([edges_size, 0]).int()

        for tag in self.edata_dic:
            tag_tensor = self.dgl_graph.edata[tag]
            # 兼容一维数组
            if len(tag_tensor.shape) == 1:
                tag_tensor = torch.reshape(tag_tensor, (tag_tensor.shape[0], 1))
            _row_array = torch.hstack((_row_array, tag_tensor))

        # edge's索引id
        _row_array = torch.hstack((edges.reshape([edges_size, 1]), _row_array))

        if len(dst.shape) <= 1:
            dst = torch.reshape(dst, (dst.shape[0], 1))
        _row_array = torch.hstack((dst.int(), _row_array))
        if len(src.shape) <= 1:
            src = torch.reshape(src, (src.shape[0], 1))
        _row_array = torch.hstack((src.int(), _row_array)).numpy()

        # 数据类型转换，并写数据到csv
        for i in range(len(_row_array)):
            prop = _row_array[i]
            f_edges_write.writerow(prop)
            if i % 1000 == 0 and i != 0:
                print('xxx build ', self.name, ' node :', i)
                # break
        f_edges.close()

    def build_conf_json(self):
        schema_json = {}
        if self.cache:
            schema_json['cache_level'] = 1
        if self.name is not None or self.name != '':
            schema_json['db_name'] = self.name

        # graph's node info
        self.node_index = 0
        node_json = []
        for tag in self.ndata_dic:
            tag_tensor = self.dgl_graph.ndata[tag]
            prop_type = self.torch_type_2_cpp_type(tag_tensor.dtype)
            if len(tag_tensor.shape) <=1 :
                dim = 1
            else:
                dim = tag_tensor.shape[1]
            if dim <= 1:
                self.node_index = self.node_index + 1

                j_unit = {'name': tag, 'column': self.node_index, 'type': prop_type}
                node_json.append(j_unit)
            else:
                for i in range(dim):
                    self.node_index = self.node_index + 1

                    j_unit = {'name': tag + str(i), 'column': self.node_index, 'type': prop_type}
                    node_json.append(j_unit)

        # last_prop_no_tag用于严格模式下，json格式最后一个','的判断
        l_node_json = node_json.__len__()
        if l_node_json > 0:
            last_node_json = node_json.pop(l_node_json - 1)
            last_node_json['last_prop_no_tag'] = 0
            node_json.append(last_node_json)
            # last_prop_no_tag用于严格模式下，json格式最后一个','的判断
        schema_json['node_json'] = node_json

        # graph's edge info
        self.edge_index = 2
        edge_json = []
        for tag in self.edata_dic:
            tag_tensor = self.dgl_graph.edata[tag]
            prop_type = self.torch_type_2_cpp_type(tag_tensor.dtype)
            dim = len(tag_tensor.shape)
            if dim <= 1:
                self.edge_index = self.edge_index + 1

                j_unit = {'name': tag, 'column': self.edge_index, 'type': prop_type}
                edge_json.append(j_unit)
            else:
                for i in range(dim):
                    self.edge_index = self.edge_index + 1

                    j_unit = {'name': tag + str(i), 'column': self.edge_index, 'type': prop_type}
                    edge_json.append(j_unit)

        # last_prop_no_tag用于严格模式下，json格式最后一个','的判断
        l_edge_schema = edge_json.__len__()
        if l_edge_schema > 0:
            last_edge_schema = edge_json.pop(l_edge_schema - 1)
            last_edge_schema['last_prop_no_tag'] = 0
            edge_json.append(last_edge_schema)
            # last_prop_no_tag用于严格模式下，json格式最后一个','的判断
        schema_json['edge_json'] = edge_json
        return schema_json

    def build_schema_conf(self):
        schema_content = Template(str(pkgutil.get_data('ezoognn', self.jinja_path + 'homogeneous_graph_schema.jinja-py'), 'utf-8'))\
            .render(SESSION_NAME='schema', schema_json=self.schema_json)
        with open(self.path + 'schema.txt', 'w', newline='', encoding='utf-8') as schema_write:
            schema_write.write(schema_content)

    def build_import_conf(self):
        import_conf_content = Template(str(pkgutil.get_data('ezoognn', self.jinja_path + 'homogeneous_graph_import.jinja-py'), 'utf-8'))\
            .render(SESSION_NAME='import_conf', import_conf_json=self.schema_json)
        with open(self.path + 'import_conf.txt', 'w', newline='', encoding='utf-8') as import_conf_write:
            import_conf_write.write(import_conf_content)


'''
点异构图，这一类是点异构图，边没有超过一个的属性特征
'''


class EzooHeterogeneousPublicDataset(EzooDataset):
    def __init__(self, name=None, path=None, dgl_graph=None, nlabels={}, nsplit_idx={}, cache=False, extend_ndata_dic=None):
        super(EzooHeterogeneousPublicDataset, self).__init__()
        self.dgl_graph = dgl_graph
        self.name = name
        self.cache = cache
        if extend_ndata_dic is not None:
            self.extend_ndata_dic = extend_ndata_dic

        if path is None:
            path = "." + os.sep
        self.path = path + name + os.sep
        if not os.path.exists(self.path):
            os.makedirs(self.path)

        ndata_dic = {}
        _nodes = self.dgl_graph.ndata._nodes
        for type_id in self.dgl_graph.ndata._ntid:
            type = self.dgl_graph.ndata._ntype[type_id]
            # 将不同点类型标签设置到
            if nlabels.__contains__(type):
                n_label = {'label': nlabels[type]}
                self.dgl_graph._set_n_repr(type_id, _nodes, n_label)
            # 将不同点 mask标签设置到点的属性中去，但是由于每个mask可能获取的都是部分数据，所以需要将mask的长度补齐
            number_nodes_tensor = self.dgl_graph.nodes(type)
            for _key in nsplit_idx:
                _mask_dict = nsplit_idx[_key]
                if _mask_dict is None or len(_mask_dict) <= 0:
                    continue
                for mask_name in _mask_dict.keys():
                    if type != mask_name:
                        continue
                    _mask = _mask_dict[mask_name]
                    self._get_mask(_mask, number_nodes_tensor, type_id, _nodes, _key)

            props = self.dgl_graph._get_n_repr(type_id, _nodes)
            # 生成mask相关的文件数据，然后下一次遍历，删除
            for prop in list(props.keys()):
                if 'mask' in prop or 'train' in prop or 'test' in prop or 'valid' in prop or 'val' in prop:
                    mask_tensor = props[prop]
                    self.build_mask_file('node###'+str2filename(type)+'###'+prop, mask_tensor, number_nodes_tensor)
                    del props[prop]
            ndata_dic[type] = props
        self.ndata_dic = ndata_dic

        edata_dic = {}
        _edges = self.dgl_graph.edata._edges
        for type_id in self.dgl_graph.edata._etid:
            type = self.dgl_graph.edata._etype[type_id]
            _, _, edges_id = self.dgl_graph.edges(form='all', etype=type)
            edgeId = edges_id.reshape([edges_id.shape[0], 1]).int()
            self.dgl_graph._set_e_repr(type_id, _edges, {'edgeIds': edgeId})
            props = self.dgl_graph._get_e_repr(type_id, _edges)
            # 处理如果单个属性含有多列数据的话，使用索引号拆分成一列一列的
            new_props = {}
            for prop in list(props.keys()):
                v = props[prop]
                if 'mask' in prop or 'train' in prop or 'test' in prop or 'valid' in prop or 'val' in prop:
                    mask_tensor = v
                    self.build_mask_file('node###'+str2filename(str(type))+'###'+prop, mask_tensor, number_nodes_tensor, node=False)
                    del props[prop]
                if len(v.shape) >= 2 and v.shape[1] >= 2:
                    vv = torch.transpose(v, dim0=1, dim1=0)
                    col_num = v.shape[1]
                    for ii in range(col_num):
                        new_props[prop + '_' + str(ii)] = vv[ii]
                else:
                    new_props[prop] = v
            edata_dic[type] = new_props
        self.edata_dic = edata_dic

        self.write_mask_csv()

        self.schema_json = self.build_conf_json()
        self._build_ezoo_file()

    def _get_mask(self, mask_tensor, number_nodes_tensor, type_id, _nodes, mask_name):
        mask_nodes_tensor = torch.zeros((number_nodes_tensor.shape[0], 1)).bool()
        for i in mask_tensor.numpy():
            mask_nodes_tensor[i.min()] = True
        _mask = {mask_name: mask_nodes_tensor}
        self.dgl_graph._set_n_repr(type_id, _nodes, _mask)

    def _build_ezoo_file(self):
        self.build_schema_conf()
        self.build_import_conf()
        self.build_node_csv()
        self.build_edge_csv()

    def __getitem__(self, idx):
        return self.path

    def build_node_csv(self):
        for ntype in self.ndata_dic:
            node_file_name = str2filename(ntype)
            f_nodes = open(self.path + self.name + '-' + node_file_name + '-node.csv', 'w', newline='', encoding='utf-8')
            f_nodes_write = csv.writer(f_nodes)
            # nodes id
            nodes = self.dgl_graph.nodes(ntype)
            nodes_size = nodes.shape[0]
            # nodes 特征属性等信息
            _row_array = torch.empty([nodes_size, 0])

            props = self.ndata_dic[ntype]
            for prop in props:
                tag_tensor = props[prop]
                dim = len(tag_tensor.shape)
                if dim == 1:
                    tag_tensor = torch.reshape(tag_tensor, (tag_tensor.shape[0], 1))
                _row_array = torch.hstack((_row_array, tag_tensor))
            # node's ids
            _row_array = torch.hstack((nodes.reshape([nodes_size, 1]).int(), _row_array)).numpy()

            if hasattr(self, 'extend_ndata_dic'):
                if self.extend_ndata_dic is not None and self.extend_ndata_dic.__contains__(ntype):
                    current_extend_type_dict = self.extend_ndata_dic[ntype]
                    for k in current_extend_type_dict.keys():
                        values = current_extend_type_dict[k].reshape([nodes_size, 1])
                        _row_array = numpy.hstack((_row_array, values))

            # 数据类型转换，并写数据到csv
            line_row = []
            row_size = _row_array.shape[1] - 1
            for prop in numpy.ndenumerate(_row_array):
                location = prop[0]
                i = location[0]
                y = location[1]
                value = prop[1]
                # 因为这里没有想好应该是怎么去处理哪些列用作int类型，所以暂取-1，也就是全部都用浮点型
                if y <= -1:
                    line_row.append(int(value))
                else:
                    line_row.append(value)
                if y == row_size:
                    f_nodes_write.writerow(line_row)
                    line_row = []
                if i % 10000 == 0 and i != 0:
                    print('build heterogeneous graph : ', self.name, ' type :', ntype, ' node :', location)
                    # break
            f_nodes.close()

    def build_edge_csv(self):
        for etype in self.edata_dic:
            etype_name = str2filename(str(etype))
            f_edges = open(self.path + self.name + '-' + etype_name + '-edge.csv', 'w', newline='', encoding='utf-8')
            f_edges_write = csv.writer(f_edges)

            # 边中，只有前两个是固定的，其他属性都可以根据遍历来做
            # edge size  三元组的 1 位置 是对应的关系数据
            src, dst, edges_id = self.dgl_graph.edges(form='all', etype=etype)
            edges_size = edges_id.shape[0]
            # edge 特征属性等信息
            _row_array = torch.empty([edges_size, 0])

            # edges_number
            edges_number = edges_id.reshape([edges_size, 1]).int()
            if len(edges_number.shape) <= 1:
                edges_number = torch.reshape(edges_number, (edges_number.shape[0], 1))
            _row_array = torch.hstack((edges_number.int(), _row_array))

            weight_edge_dict = self.edata_dic[etype]
            for prop in weight_edge_dict.keys():
                weight_edges = weight_edge_dict[prop]
                if len(weight_edges.shape) <= 1:
                    weight_edges = torch.reshape(weight_edges, (weight_edges.shape[0], 1))
                _row_array = torch.hstack((weight_edges.int(), _row_array))

            if len(dst.shape) <= 1:
                dst = torch.reshape(dst, (dst.shape[0], 1))
            _row_array = torch.hstack((dst.int(), _row_array))
            if len(src.shape) <= 1:
                src = torch.reshape(src, (src.shape[0], 1))
            _row_array = torch.hstack((src.int(), _row_array)).numpy()
            # 数据类型转换，并写数据到csv
            line_row = []
            row_size = _row_array.shape[1] - 1
            for prop in numpy.ndenumerate(_row_array):
                location = prop[0]
                i = location[0]
                y = location[1]
                value = prop[1]
                # 因为这里没有想好应该是怎么去处理哪些列用作int类型，所以暂取-1，也就是全部都用浮点型
                if y <= 1:
                    line_row.append(int(value))
                else:
                    line_row.append(value)

                if y == row_size:
                    f_edges_write.writerow(line_row)
                    line_row = []
                if i % 10000 == 0 and i != 0:
                    print('build ', self.name, ' node :', i)
                    # break
            f_edges.close()

    def build_conf_json(self):
        schema_json = {}
        if self.cache:
            schema_json['cache_level'] = 1
        if self.name is not None or self.name != '':
            schema_json['db_name'] = self.name

        # graph's node info
        node_schema = []
        for ntype in self.ndata_dic:
            values = self.ndata_dic[ntype]
            props = []
            # node_ids
            node_index = 0

            node_tensor = self.dgl_graph.nodes(ntype)
            id_type = self.torch_type_2_cpp_type(node_tensor.dtype)
            props.append({'name': 'id', 'type': id_type, 'column': node_index})
            for k in values:
                v_tensor = values[k]
                prop_type = self.torch_type_2_cpp_type(v_tensor.dtype)
                len_shape = len(v_tensor.shape)
                # 如果是二维数组，需一个一个的将属性设置进去
                if len_shape >= 2:
                    size = v_tensor.shape[1]
                    if size > 1:
                        [props.append({'name': k+str(i), 'type': prop_type, 'column': node_index + 1 + i}) for i in range(size)]
                        node_index = node_index + size
                    else:
                        node_index = node_index + 1
                        [props.append({'name': k, 'type': prop_type, 'column': node_index}) for i in range(size)]
                else:
                    node_index = node_index + 1
                    props.append({'name': k, 'type': prop_type, 'column': node_index})

            if hasattr(self, 'extend_ndata_dic'):
                if self.extend_ndata_dic is not None and self.extend_ndata_dic.__contains__(ntype):
                    current_extend_type_dict = self.extend_ndata_dic[ntype]
                    for k in current_extend_type_dict.keys():
                        node_index = node_index + 1
                        props.append({'name': k, 'type': 'string', 'column': node_index})



            # last_prop_no_tag用于严格模式下，json格式最后一个','的判断
            l_props = props.__len__()
            last_prop = props.pop(l_props - 1)
            last_prop['last_prop_no_tag'] = 0
            props.append(last_prop)
            # last_prop_no_tag用于严格模式下，json格式最后一个','的判断
            node_file_name = str2filename(ntype)
            node_schema.append({'path': self.name + '-' + node_file_name + '-node.csv', 'name': ntype, 'props': props})

        # last_prop_no_tag用于严格模式下，json格式最后一个','的判断
        l_node_schema = node_schema.__len__()
        last_node_schema = node_schema.pop(l_node_schema - 1)
        last_node_schema['last_prop_no_tag'] = 0
        node_schema.append(last_node_schema)
        # last_prop_no_tag用于严格模式下，json格式最后一个','的判断
        schema_json['node_schema'] = node_schema

        # graph's edge info
        edge_schema = []
        for etype in self.edata_dic:
            edge_file_name = str2filename(str(etype))
            edge_json = {'path': self.name + '-' + edge_file_name + '-edge.csv', 'name': edge_file_name, 'start_node': etype[0], 'end_node': etype[2]}
            props = []
            indexes = []
            edge_index = 1

            # 边的属性：这是边的权重处理；reltype是边的属性，可以看做权重，也可以看做一个属性，对应这个边类型的编号
            edge_props = self.edata_dic[etype]
            for name in edge_props.keys():
                prop_type = self.torch_type_2_cpp_type(edge_props[name].dtype)
                edge_index = edge_index + 1
                props.append({'name': name, 'type': prop_type, 'column': edge_index})

            # 设置边的(索引)名称，对应的就是edge_number
            edge_index = edge_index + 1
            edge_name = etype[1]
            edge_json['edge_type'] = etype[0] + ' ' + edge_name + ' ' + etype[2]
            props.append({'name': edge_name + '_id', 'type': prop_type, 'column': edge_index})
            # 边索引
            indexes.append({'name': edge_name + '_id', 'type': prop_type, 'column': edge_index})

            # last_prop_no_tag用于严格模式下，json格式最后一个','的判断
            l_props = props.__len__()
            last_prop = props.pop(l_props - 1)
            last_prop['last_prop_no_tag'] = 0
            props.append(last_prop)
            # last_prop_no_tag用于严格模式下，json格式最后一个','的判断
            edge_json['props'] = props

            # last_prop_no_tag用于严格模式下，json格式最后一个','的判断
            l_indexes = indexes.__len__()
            last_indexes = indexes.pop(l_indexes - 1)
            last_indexes['last_prop_no_tag'] = 0
            indexes.append(last_indexes)
            # last_prop_no_tag用于严格模式下，json格式最后一个','的判断
            edge_json['indexes'] = indexes
            edge_schema.append(edge_json)

        # last_prop_no_tag用于严格模式下，json格式最后一个','的判断
        l_edge_schema = edge_schema.__len__()
        last_edge_schema = edge_schema.pop(l_edge_schema - 1)
        last_edge_schema['last_prop_no_tag'] = 0
        edge_schema.append(last_edge_schema)
        # last_prop_no_tag用于严格模式下，json格式最后一个','的判断
        schema_json['edge_schema'] = edge_schema
        return schema_json

    def build_schema_conf(self):
        schema_content = Template(str(pkgutil.get_data('ezoognn', self.jinja_path + 'heterogeneous_graph_schema.jinja-py'), 'utf-8'))\
            .render(SESSION_NAME='schema', schema_json=self.schema_json)
        with open(self.path + 'schema.txt', 'w', newline='', encoding='utf-8') as schema_write:
            schema_write.write(schema_content)

    def build_import_conf(self):
        import_conf_content = Template(str(pkgutil.get_data('ezoognn', self.jinja_path + 'heterogeneous_graph_import.jinja-py'), 'utf-8'))\
            .render(SESSION_NAME='import_conf', import_conf_json=self.schema_json)
        with open(self.path + 'import_conf.txt', 'w', newline='', encoding='utf-8') as import_conf_write:
            import_conf_write.write(import_conf_content)


'''
@:param path: 表示生成ezoodb元文件生成的路径地址
@:param mem_cache: 表示在ezoo中有个cache_level，是否对字段数据进行缓存到内存中去
'''

class CsvEzooGraphDataset(EzooGraphDataset):

    def __init__(self, path=None, data_path=None, cache=False, cfg_file=None,
                 name=None, split_ratio=None):
        assert cfg_file is not None or cfg_file != '', 'cfg_file is None !!!'

        self.ezoo_graph_list = []
        dataset = dgl.data.CSVDataset(data_path)
        name = dataset.name
        # 这里的graphs是个list，也就是它支持graph图组的构建
        if dataset.graphs.__len__() <= 0:
            return

        for i in range(dataset.graphs.__len__()):
            dgl_graph = dataset.graphs[i]
            assert dgl_graph is not None, 'dgl_graph is None !!!'

            if i == 0:
                temp_name = name
            else:
                temp_name = name + '_' + str(i)

            if dgl_graph.is_homogeneous:
                ezoo_path = EzooPublicDataset(name=temp_name, path=path, dgl_graph=dgl_graph, cache=cache)[0]
                self.ezoo_graph_list.append(EzooGraphDataset(name=temp_name,
                                                             cfg_file=cfg_file,
                                                             schema_path=ezoo_path + '/schema.txt',
                                                             iconf_path=ezoo_path + '/import_conf.txt'))
            else:
                ezoo_path = EzooHeterogeneousPublicDataset(name=temp_name, path=path, dgl_graph=dgl_graph, cache=cache)[0]
                self.ezoo_graph_list.append(EzooHeteroGraphDataset(name=temp_name,
                                                                   cfg_file=cfg_file,
                                                                   schema_path=ezoo_path + '/schema.txt',
                                                                   iconf_path=ezoo_path + '/import_conf.txt'))

    def __getitem__(self, item):
        assert self.ezoo_graph_list is not None and len(self.ezoo_graph_list) > 0, 'self.ezoo_graph_list is None !!!'
        # 获取第一个
        return self.ezoo_graph_list[0][item]


    
