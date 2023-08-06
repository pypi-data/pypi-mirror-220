""""
暂时均不考虑其他情况：
如分布式、全采样等
"""
import dgl
import numpy
import torch
from collections.abc import Mapping
from dgl.backend import pytorch as F

from dgl.dataloading.base import BlockSampler
from .. import MAXINT
import time


class EzooMultiLayerNeighborSampler(BlockSampler):

    """"
    fanouts：
    """

    def __init__(self, fanouts, replace=False, return_eids=False, e_graph=None, p=0.5, g_nodes_num=0, feats_num=0, one_hot=False, node_type='node'):
        super().__init__(len(fanouts), return_eids)

        self.fanouts = fanouts
        self.replace = replace
        self.e_graph = e_graph
        '''
        :param p 类似表示node2vec中的p、q，方向概率
        '''
        self.p = p
        self.g_nodes_num = g_nodes_num
        self.feats_num = feats_num

        self.one_hot = one_hot
        self.node_type = node_type

    def sample_frontier(self, seed_nodes, device=torch.device('cpu')):
        if self.fanouts is None:
            return
        blocks = []
        tic_sample = time.time()
        for fanout in reversed(self.fanouts):
            if fanout is None:
                fanout = MAXINT
            tic = time.time()
            # 单层采样
            if device.type == 'cpu':
                device_no = -1
            else:
                device_no = device.index
            dst_nodes, src_nodes = self.e_graph.sampling_no_weight(
                self.node_type, seed_nodes, fanout, self.replace, self.p, device_no)
            toc = time.time()
            print(f"sampling_no_weight (fan_out {fanout}) : {toc - tic}")
            # 构建图block
            g = dgl.graph((src_nodes.astype(numpy.int64),
                           dst_nodes.astype(numpy.int64)), num_nodes=self.g_nodes_num)
            # tic = time.time()
            # print(f"sample_frontier call dgl.graph() : {tic - toc}")
            block = dgl.to_block(g, seed_nodes.long())
            blocks.insert(0, block)
            seed_nodes = block.srcdata[dgl.NID]
            # toc = time.time()
            # print(f"sample_frontier call dgl.to_block() : {toc - tic}")
        print(f"sample_frontier cost : {time.time() - tic_sample}s")
        return blocks[0].srcdata[dgl.NID], blocks
    
    # 一次调用完成所有fan_out的sample
    def sample_frontier_once(self, seed_nodes, device='cpu'):
        if self.fanouts is None:
            return
        
        tic_sample = time.time()
        tic = tic_sample
        edge_num_array, dst_nodes, src_nodes = self.e_graph.sampling_no_weight_once(
            self.node_type, seed_nodes, reversed(self.fanouts), self.replace, self.p)
        toc = time.time()
        print(f"sampling_no_weight cost (all fan_out) : {toc - tic}s")
        
        # 构建图block
        blocks = []
        total_edge_num = 0
        for edge_num in edge_num_array:
            g = dgl.graph((src_nodes[total_edge_num:total_edge_num+edge_num].astype(numpy.int64),
                           dst_nodes[total_edge_num:total_edge_num+edge_num].astype(numpy.int64)), num_nodes=self.g_nodes_num)
            # tic = time.time()
            # print(f"sample_frontier call dgl.graph() : {tic - toc}")
            block = dgl.to_block(g, seed_nodes.long())
            blocks.insert(0, block)
            seed_nodes = block.srcdata[dgl.NID]
            total_edge_num += edge_num
            # toc = time.time()
            # print(f"sample_frontier call dgl.to_block() : {toc - tic}")

        print(f"sample_frontier cost : {time.time() - tic_sample}s")
        return blocks[0].srcdata[dgl.NID], blocks

    def _locate_eids_to_exclude(self, frontier_parent_eids, exclude_eids):
        """Find the edges whose IDs in parent graph appeared in exclude_eids.

        Note that both arguments are numpy arrays or numpy dicts.
        """
        if isinstance(frontier_parent_eids, Mapping):
            result = {
                k: numpy.isin(
                    frontier_parent_eids[k], exclude_eids[k]).nonzero()[0]
                for k in frontier_parent_eids.keys() if k in exclude_eids.keys()}
            return {k: F.zerocopy_from_numpy(v) for k, v in result.items()}
        else:
            result = numpy.isin(frontier_parent_eids,
                                exclude_eids).nonzero()[0]
            return F.zerocopy_from_numpy(result)

    """
    get src_nodes dst_nodes by edges
    build subgraph
    """

    def sampler_blocks_edge(self, edges, reverse_eid, exclude):
        src_nodes, dst_nodes = self.e_graph.get_src_dst_by_edges(edges)
        nodes_org_id = list(set(list(src_nodes) + list(dst_nodes)))
        # 映射边
        nodes_mapping = {}
        for index, n in enumerate(nodes_org_id):
            nodes_mapping[n] = index

        # 构建自定义子图
        sub_graph = dgl.graph(([nodes_mapping.get(i) for i in src_nodes], [
                              nodes_mapping.get(i) for i in dst_nodes]))

        # # 设置原始数据到sub_graph中
        sub_graph.edata[dgl.EID] = edges
        sub_graph.edata['etype'] = torch.tensor(
            self.e_graph.get_edge_prop(edges, 'label'))
        sub_graph.ndata[dgl.NID] = torch.tensor(
            [nodes_org_id[i].astype(numpy.int64) for i in sub_graph.nodes().numpy()])

        seed_nodes = sub_graph.ndata[dgl.NID]
        if self.fanouts is None:
            return

        # self.reverse_eid表示的是反向边的映射, 就是找到互为反向边的数据exclude_eids
        if exclude == 'reverse_id':
            exclude_eids = F.cat([edges, F.gather_row(reverse_eid, edges)], 0)
            exclude_eids = exclude_eids.numpy()
        elif exclude == 'reverse_types':
            print('todo')
        blocks = []
        for fanout in reversed(self.fanouts):
            # 兼容全采样的fanout数据, 设置c++最大值
            if fanout is None:
                fanout = MAXINT
            # 单层采样
            dst_nodes, src_nodes, sampler_edges = self.e_graph.sampling_no_weight_nodes_edges(
                self.node_type, seed_nodes, fanout, self.replace, self.p)
            # 构建图block
            g = dgl.graph((src_nodes.astype(numpy.int64), 
                dst_nodes.astype(numpy.int64)), num_nodes=self.g_nodes_num)
            g.edata[dgl.EID] = torch.tensor(sampler_edges)
            if exclude_eids is not None:
                self.remove_exclude_eids(exclude_eids, g)
            block = dgl.to_block(g, seed_nodes.long())
            blocks.insert(0, block)
            seed_nodes = block.srcdata[dgl.NID]

        return blocks[0].srcdata[dgl.NID], sub_graph, blocks

    """
    @:param src_nodes dst_nodes: 子图的节点
    @:param g: 根据子图seed_nodes采样获取到的采样子图
    """

    def remove_exclude_eids(self, exclude_eids, g):
        # remove exclude_eids
        parent_eids = g.edata[dgl.EID].numpy()
        new_edges = g.edges('all')[2].numpy()
        number_parent_mapping = {}
        for i in range(len(new_edges)):
            number_parent_mapping[parent_eids[i]] = new_edges[i]

        located_eids = self._locate_eids_to_exclude(parent_eids, exclude_eids)
        # 转换为对应子图从小到大的边的编号
        new_located_eids = []
        for i in located_eids.numpy():
            if number_parent_mapping.__contains__(i):
                new_located_eids.append(number_parent_mapping.get(i))
        new_located_eids = torch.LongTensor(new_located_eids)
        # located_eids转为g（新图）可识别的编号
        if len(located_eids) > 0:
            g.remove_edges(new_located_eids, store_ids=True)


class EzooMultiLayerFullNeighborSampler(EzooMultiLayerNeighborSampler):
    def __init__(self, n_layers, e_graph=None, p=1, g_nodes_num=None, one_hot=None, node_type=None, return_eids=False):
        super().__init__([None] * n_layers, e_graph=e_graph, p=p, g_nodes_num=g_nodes_num,
                         one_hot=one_hot, node_type=node_type, return_eids=return_eids)
