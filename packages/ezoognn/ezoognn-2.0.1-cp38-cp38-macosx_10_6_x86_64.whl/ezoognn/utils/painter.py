from matplotlib.pyplot import title
import torch
import random
import dgl
import copy
from pyvis.network import Network
from enum import Enum
from dgl.nn import GNNExplainer
from ..utils import str_utils
import random
import matplotlib as plt
from collections import defaultdict
from .. import MAXINT


class PaintDataTypeEnum(Enum):
    ALL = 'all'
    TRAIN = 'train'
    VAL = 'val'
    TEST = 'test'


class GraphPainter(Network):
    def __init__(self,  graph, notebook=False, height='500px', width='500px', bgcolor='white',
                 font_color='black', nodes_limit=-1, highlight_feats='', data_type=PaintDataTypeEnum.ALL):
        """
        Paint the DGL graph.

        Parameters
        ----------
        graph: the DGL graph
        notebook: draw in the jupyter notebook or not
        nodes_limit: drawn nodes' limitation
        highlight_feats: which feature in graph should be refered when coloring
        data_type: which type of data set should be painted as different colors, 
                    and other types of nodes are painted as grey.
        """

        super().__init__(height=height, width=width, notebook=notebook,
                         bgcolor=bgcolor, font_color=font_color)
        self.highlight_feats = highlight_feats
        self.graph = graph
        self.nodes_limit = nodes_limit
        self.data_type = data_type

    def prepare_data(self, graph, sg=None, nodes_limit=-1, data_type=PaintDataTypeEnum.ALL, edges_width=None):
        if sg is not None:
            sub_graph = sg
            original_ids = sub_graph.ndata[dgl.NID]
        elif nodes_limit > 0:
            shuffle_node_list = list(range(graph.number_of_nodes()))
            random.shuffle(shuffle_node_list)
            shuffle_node_list = shuffle_node_list[:nodes_limit]
            sub_graph = dgl.node_subgraph(
                graph, shuffle_node_list)
            original_ids = sub_graph.ndata[dgl.NID]
        else:
            sub_graph = graph
            original_ids = sub_graph.nodes()

        titles = [str(item) for item in original_ids.tolist()]

        if self.highlight_feats != '':
            if data_type == PaintDataTypeEnum.ALL:
                labels_array = [graph.ndata[self.highlight_feats][o_id]
                                for o_id in original_ids.tolist()]
            else:
                # When node is not in defined set, using a special color.
                labels_array = [-1 if not graph.ndata[data_type.value + '_mask'][o_id]
                                else graph.ndata[self.highlight_feats][o_id] for o_id in original_ids.tolist()]

            labels = torch.tensor(labels_array)
            colors = self.__get_color(labels)
            self.add_nodes(sub_graph.nodes().tolist(), label=titles, color=colors, title=[
                str(item) for item in labels.tolist()])
        else:

            self.add_nodes(sub_graph.nodes().tolist(),  label=titles)

        edges = sub_graph.edges()
        edges0 = edges[0].tolist()
        edges1 = edges[1].tolist()
        if edges_width is not None:
            self.add_edges([[edges0[i], edges1[i], edges_width[i]]
                           for i in range(len(edges0))])
        else:
            self.add_edges([[edges0[i], edges1[i]]
                           for i in range(len(edges0))])

    @staticmethod
    def __get_color(data):
        """
        colors nodes according labels when the labels' value are bigger than 0.
        otherwise, colors grey.
        """
        unique_data = torch.unique(data).numpy()
        colors_num = list(unique_data.shape)[0]
        cmap = plt.cm.get_cmap('plasma', colors_num)
        color_map = {}
        for i in range(colors_num):
            color_map[unique_data[i]] = plt.colors.to_hex(cmap(i))
        return ['grey' if item == -1 else color_map[item] for item in data.tolist()]

    def draw_graph(self, output_file='example.html'):
        self.prepare_data(self.graph, nodes_limit=self.nodes_limit,
                          data_type=self.data_type)
        ret = self.show(output_file)
        return ret

    def get_pred(self, model, features, explain_nodes_ids):
        """
        get the prediction values from the test set
        """
        model.eval()
        with torch.no_grad():
            logits = model(self.graph, features)
        pred = torch.argmax(logits[explain_nodes_ids], dim=1)
        return pred

    def draw_explain_graph(self, model, explain_nodes_ids, explain_node_idx, num_hops=2, output_file='explain.html'):
        """
        Set the test nodes' label as the predict values, for explaination of the pred result
        """
        features = self.graph.ndata['feat']
        pred = self.get_pred(model, features, explain_nodes_ids)
        explain_graph = copy.deepcopy(self.graph)
        explain_graph.ndata[self.highlight_feats][explain_nodes_ids] = pred

        ex_node = explain_nodes_ids[explain_node_idx]
        explainer = GNNExplainer(model, num_hops)
        _, sg, _, edge_mask = explainer.explain_node(
            ex_node, explain_graph, features)
        edge_mask = edge_mask * 4

        self.prepare_data(explain_graph, sg=sg, nodes_limit=-1,
                          edges_width=edge_mask.tolist())

        ret = self.show(output_file)
        return ret

# ===========================Heterogeneous graph===============================================================================


class HeterGraphPainter(Network):
    def __init__(self, graph, notebook=False, height='500px', width='500px', bgcolor='white',
                 font_color='black', nodes_limit=-1, highlight_feats='', data_type=PaintDataTypeEnum.ALL):
        """
        Paint the DGL graph.

        Parameters
        ----------
        graph: the DGL heterograph
        notebook: draw in the jupyter notebook or not
        nodes_limit: drawn nodes' limitation
        highlight_feats: which feature in graph should be refered when coloring
        data_type: which type of data set should be painted as different colors,
                    and other types of nodes are painted as grey.
        """
        #self.highlight_feats = highlight_feats
        self.graph = graph
        #self.nodes_limit = nodes_limit
        #self.data_type = data_type
        # self.labels={},
        self.node_type = graph.ntypes
        self.edge_type = graph.etypes
        self.nodes_limit = nodes_limit
        self.highlight_feats = highlight_feats

        super().__init__(height=height, width=width,
                         notebook=notebook, bgcolor=bgcolor, font_color=font_color)

        #self.data_type = data_type

    def get_color(self, types):
        """
        return a colormap of node/edge types (dictionary)
        """
        if types == self.node_type:
            color_scheme = 'Set3'
        elif types == self.edge_type:
            color_scheme = 'gist_rainbow'
        else:
            color_scheme = 'Accent'

        colors_num = len(types)
        cmap = plt.cm.get_cmap(color_scheme, colors_num)
        color_map = {}
        for i in range(colors_num):
            color_map[types[i]] = plt.colors.to_hex(cmap(i))

        return color_map

    def add_edges(self, edges, **kwargs):
        """
        This method serves to add multiple edges between existing nodes
        in the network instance. Adding of the edges is done based off
        of the IDs of the nodes. Order does not matter unless dealing with a
        directed graph.

        :param edges: A list of tuples, each tuple consists of source of edge,
                      edge destination and and optional width.

        :type arrowStrikethrough: list of tuples
        """
        valid_args = ["size", "value", "title",
                      "x", "y", "label", "color", "shape"]
        for k in kwargs:
            assert k in valid_args, "invalid arg '" + k + "'"

        nd = defaultdict(dict)
        for i in range(len(edges)):
            for k, v in kwargs.items():
                assert (
                    len(v) == len(edges)
                ), "keyword arg %s [length %s] does not match" \
                   "[length %s] of edges" % \
                   (
                       k, len(v), len(edges)
                )
                nd[edges[i]].update({k: v[i]})

        for edge in edges:
            # if incoming tuple contains a weight
            if len(edge) == 3:
                self.add_edge(edge[0], edge[1], width=edge[2])
            else:
                self.add_edge(edge[0], edge[1], **nd[edge])

    def draw_graph(self, output_file='example.html', show_nid=False, show_type=True, edge_color_by_type=True, data_type=PaintDataTypeEnum.ALL):
        """
        draw the DGL hetero graph, each node type has its own color

        """
        color_map_node = self.get_color(self.node_type)
        color_map_edge = self.get_color(self.edge_type)
        sub_graphs_list = []
        # 先确定一下图的大小
        if self.nodes_limit > 0:
            # pick nodes for each type based on its propotions to the total number of nodes in the graph, a total of node_limits of nodes are picked
            node_num_types = [len(self.graph.nodes(ntype=type))
                              for type in self.node_type]
            limited_node_num_types = [int(
                (node_num/self.graph.number_of_nodes())*self.nodes_limit) for node_num in node_num_types]
            for type in self.node_type:
                random_node_list = random.choices(self.graph.nodes(
                    type).tolist(), k=limited_node_num_types[self.node_type.index(type)])
                # 出边子图
                sub_graph = dgl.out_subgraph(
                    self.graph, {type: random_node_list})
                sub_graphs_list.append(sub_graph)

        # if you wanna to plot the whole graph, only if the graph is small
        else:
            sub_graph = self.graph
            sub_graphs_list.append(sub_graph)

        # each sub_graph is asscoiated with each node_type
        for sub_graph in sub_graphs_list:
            etype_tuple = sub_graph.canonical_etypes
            for etype in etype_tuple:
                edges = sub_graph.all_edges(form='uv', etype=etype)
                if len(edges[0]) != 0:

                    src_nodes_id = edges[0].tolist()

                    src_NID_list = ['NID: %s' % (id)for id in src_nodes_id]
                    src_color_list = [color_map_node[etype[0]]]*len(edges[0])
                    src_NTYPE_list = ['NTYPE: %s' % (etype[0])]*len(edges[0])

                    dst_nodes_id = edges[1].tolist()
                    dst_NID_list = ['NID: %s' % (id)for id in dst_nodes_id]
                    dst_color_list = [color_map_node[etype[2]]]*len(edges[1])
                    dst_NTYPE_list = ['NTYPE: %s' % (etype[2])]*len(edges[1])

                    edge_title_list = ['ETYPE: %s' % (etype[1])]*len(edges[1])
                    edge_color_list = [color_map_edge[etype[1]]]*len(edges[1])

                    if self.highlight_feats != '':
                        if data_type == PaintDataTypeEnum.ALL:
                            src_feature_list = [
                                sub_graph.ndata[self.highlight_feats][o_id] for o_id in src_nodes_id]
                            dst_feature_list = [
                                sub_graph.ndata[self.highlight_feats][o_id] for o_id in dst_nodes_id]
                        else:
                            self.add_nodes(
                                src_nodes_id, label=src_feature_list, title=src_NTYPE_list, color=src_color_list)
                            self.add_nodes(
                                dst_nodes_id, label=dst_feature_list, title=dst_NTYPE_list, color=dst_color_list)
                    else:

                        if (show_nid == True) and (show_type == False):
                            self.add_nodes(
                                src_nodes_id, label=src_NID_list, title=src_NTYPE_list, color=src_color_list)
                            self.add_nodes(
                                dst_nodes_id, label=dst_NID_list, title=dst_NTYPE_list, color=dst_color_list)
                        elif (show_nid == False) and (show_type == True):
                            self.add_nodes(
                                src_nodes_id, label=src_NTYPE_list, title=src_NID_list, color=src_color_list)
                            self.add_nodes(
                                dst_nodes_id, label=dst_NTYPE_list, title=dst_NID_list, color=dst_color_list)

                        elif show_nid == True and show_type == True:
                            s = [a + ' ' + b for a,
                                 b in zip(src_NID_list, src_NTYPE_list)]
                            d = [a + ' ' + b for a,
                                 b in zip(dst_NID_list, dst_NTYPE_list)]
                            self.add_nodes(src_nodes_id, label=s,
                                           color=src_color_list)
                            self.add_nodes(dst_nodes_id, label=d,
                                           color=dst_color_list)

                        elif show_nid == False and show_type == False:
                            self.add_nodes(src_nodes_id, color=src_color_list)
                            self.add_nodes(dst_nodes_id, color=dst_color_list)

                        list_edges = []
                        for i in range(len(src_nodes_id)):
                            list_edges.append(
                                (src_nodes_id[i], dst_nodes_id[i]))
                        if edge_color_by_type:
                            self.add_edges(
                                list_edges, title=edge_title_list, color=edge_color_list)

                        self.add_edges(list_edges, title=edge_title_list)

        ret = self.show(output_file)
        return ret


class EzooGraphPainter(Network):
    def __init__(self, graph, notebook=False, height='500px', width='500px', bgcolor='white',
                 font_color='black', nodes_limit=-1, highlight_feats=''):
        """
        Paint the eZoo graph.

        Parameters
        ----------
        graph: the eZoo graph
        notebook: draw in the jupyter notebook or not
        nodes_limit: drawn nodes' limitation
        highlight_feats: which feature in graph should be refered when coloring
        """

        super().__init__(height=height, width=width, notebook=notebook,
                         bgcolor=bgcolor, font_color=font_color)
        self.highlight_feats = highlight_feats
        self.graph = graph
        self.nodes_limit = nodes_limit

    @staticmethod
    def __get_colormap_from_values(data):
        """
        Get color map according to a numerical list
        """
        data = torch.tensor(data)
        unique_data = torch.unique(data).numpy()
        colors_num = list(unique_data.shape)[0]
        cmap = plt.cm.get_cmap('plasma', colors_num)
        color_map = {}
        for i in range(colors_num):
            color_map[unique_data[i]] = plt.colors.to_hex(cmap(i))
        return color_map

    @staticmethod
    def __get_colormap_from_types(data):
        """
        Get color map according to a list contains unique values
        """
        colors_num = len(data)
        cmap = plt.cm.get_cmap('plasma', colors_num)
        color_map = {}
        for i in range(colors_num):
            color_map[data[i]] = plt.colors.to_hex(cmap(i))
        return color_map

    def prepare_data(self, graph, nodes_limit=-1):
        nodes_type = graph.get_node_type_list()
        nodes_num = 0
        for node_type in nodes_type:
            nodes_num += graph.get_nodes_num(node_type)

        all_nodes_list = []
        if len(nodes_type) > 1:
            # Heterogeneous graph, colored according to nodes' type
            color_map = self.__get_colormap_from_types(nodes_type)

        for node_type in nodes_type:
            nodes_id_by_type = graph.get_node_id_batch(node_type, 0, MAXINT)
            nodes_num_by_type = len(nodes_id_by_type)
            if nodes_limit > 0 and nodes_num_by_type > nodes_limit:
                nodes_limit_by_type = int(
                    nodes_num_by_type / nodes_num * nodes_limit)
                random.shuffle(nodes_id_by_type)
                nodes_id_by_type = nodes_id_by_type[:nodes_limit_by_type]

            nodes_id_by_type = nodes_id_by_type.astype(int)
            labels = nodes_id_by_type.astype(str)
            if len(nodes_type) == 1 and self.highlight_feats != '':
                # Homogeneous graph and colored according to one feature
                highlight_feats = graph.ndata[node_type][self.highlight_feats]
                titles_array = [highlight_feats[id] for id in nodes_id_by_type]

                color_map = self.__get_colormap_from_values(titles_array)
                colors = ['grey' if item == -1 else color_map[item]
                          for item in titles_array]
                self.add_nodes(nodes_id_by_type, label=labels, color=colors, title=[
                    str(item) for item in titles_array])
            elif len(nodes_type) > 1:
                # Heterogeneous graph, colored according to nodes' type
                colors = [color_map[node_type]] * len(nodes_id_by_type)
                self.add_nodes(nodes_id_by_type, label=labels, color=colors, title=[
                               node_type] * len(nodes_id_by_type))
            else:
                self.add_nodes(nodes_id_by_type, label=labels)

            all_nodes_list.extend(nodes_id_by_type)

        src_nodes, dst_nodes, _, _, = self.graph.get_adjacencylist_from_etype()
        for i in range(len(src_nodes)):
            if src_nodes[i] in all_nodes_list and dst_nodes[i] in all_nodes_list:
                self.add_edge(int(src_nodes[i]), int(dst_nodes[i]))

    def draw_graph(self, output_file='example.html'):
        self.prepare_data(self.graph, nodes_limit=self.nodes_limit)
        ret = self.show(output_file)
        return ret
