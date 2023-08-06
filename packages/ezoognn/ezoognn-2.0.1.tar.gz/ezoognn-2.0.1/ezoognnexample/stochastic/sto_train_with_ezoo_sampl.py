import time
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np

import ezoognn
from ezoognn.ezoo_graph import EzooGraph
from ezoognn.loader.loadbatchgraph import EzooNodeDataLoader
from ezoognn.utils.model_loader import ModelLoader
from ezoognn.sampler.neighbor_sampler import EzooMultiLayerNeighborSampler
from ezoognn.sampler.neighbor_sampler import EzooMultiLayerFullNeighborSampler
from .sto_sage import StoSAGE
# import dgl


class StoTrainWithEzooSampl(ModelLoader):

    def __init__(self, args):
        super().__init__(args)
        self.args = args

        if self.args.gpu >= 0:
            self.device = torch.device('cuda:%d' % self.args.gpu)
        else:
            self.device = torch.device('cpu')

        # 初始化ezoodbClient  name='cora', 'ogbn-products'
        dbname = self.args.dataset
        self.e_graph = EzooGraph(url=self.args.url, dbname=dbname, cfg_file=self.args.cfg_file,
                                 restore_file=self.args.restore_file, restore_url=self.args.restore_url,
                                 gdi_ptr=self.args.gdi_ptr, cache_edge=True)
        # 获取总数量
        self.nodes_num = self.e_graph.get_nodes_num(self.args.node_type)

        # dataloader
        # 获取特征形状，属性中有一个是id，label , 获取所有需要的特征名称; v2版本，id作为属性
        self.n_classes = self.args.n_classes
        if self.args.one_hot or self.n_classes == -1:
            result = self.get_all_label_data()
            self.n_classes = len(np.unique(result))

        node_type_node_props = self.all_node_type_props[self.args.node_type]
        feat_names = [kv['name'] if kv['name'].startswith('feat') else "" for kv in node_type_node_props]
        feat_names = [name for name in feat_names if name.strip() != '']
        self.in_feats = len(feat_names)

    def get_all_label_data(self):
        ntype_prop_names = self.e_graph.get_all_node_prop_names_with_ntype()
        assert ntype_prop_names is not None and len(ntype_prop_names) > 0, 'can not get ' + self.args.node_type + '\'s props'

        self.all_node_type_props = ntype_prop_names
        if ntype_prop_names.__contains__(self.args.node_type) is False:
            raise Exception(self.args.node_type + '\'s props is None')

        prop_names = ntype_prop_names[self.args.node_type]
        for kv in prop_names:
            if self.args.label_name == kv['name']:
                t = kv['type']
                if t == 11:
                    result = self.e_graph.get_node_props2bool(self.args.node_type, [], [self.args.label_name])
                elif t == 14:
                    result = self.e_graph.get_node_props2int(self.args.node_type, [], [self.args.label_name])
                elif t == 15:
                    result = self.e_graph.get_node_props2long(self.args.node_type, [], [self.args.label_name])
                elif t == 17:
                    result = self.e_graph.get_node_props2float(self.args.node_type, [], [self.args.label_name])
                elif t == 18:
                    result = self.e_graph.get_node_props2double(self.args.node_type, [], [self.args.label_name])

        return result

    def compute_acc(self, pred, labels):
        """
        Compute the accuracy of prediction given the labels.
        """
        labels = labels.long()
        return (torch.argmax(pred, dim=1) == labels).float().sum() / len(pred)

    def load_subtensor(self, input_nodes, seeds):
        """
        Extracts features and labels for a subset of nodes
        """
        # 获取所有feat特征的名称
        node_type_prop_names = self.all_node_type_props[self.args.node_type]
        feat_names = []
        for kv in node_type_prop_names:
            if kv['name'].startswith('feat'):
                feat_names.append(kv['name'])
        features = self.e_graph.get_node_props2float(self.args.node_type, input_nodes.tolist(), feat_names)
        dst_feat = torch.from_numpy(features).float()
        # dst_feat使用UnifiedTensor, 实际使用时需要考虑device的传入
        # dst_feat = dgl.contrib.UnifiedTensor(dst_feat, device="cuda:0")

        for kv in node_type_prop_names:
            if self.args.label_name == kv['name']:
                t = kv['type']
                if t == 11:
                    result = self.e_graph.get_node_props2bool(self.args.node_type, seeds.tolist(), [self.args.label_name])
                elif t == 14:
                    result = self.e_graph.get_node_props2int(self.args.node_type, seeds.tolist(), [self.args.label_name])
                elif t == 15:
                    result = self.e_graph.get_node_props2long(self.args.node_type, seeds.tolist(), [self.args.label_name])
                elif t == 17:
                    result = self.e_graph.get_node_props2float(self.args.node_type, seeds.tolist(), [self.args.label_name])
                elif t == 18:
                    result = self.e_graph.get_node_props2double(self.args.node_type, seeds.tolist(), [self.args.label_name])
        label_tensor = torch.from_numpy(result)
        label_tensor = label_tensor.reshape((len(seeds), ))
        return dst_feat, label_tensor.long()

    def train(self):
        # # 获取train_mask val_mask test_mask
        node_type_props = self.all_node_type_props[self.args.node_type]
        mask_name_list = []
        for kv in node_type_props:
            if 'mask' in kv['name']:
                mask_name_list.append(kv['name'])
        mask_name_dict = {mask_name_list[i]: i for i in range(len(mask_name_list))}
        if mask_name_dict:
            masks = self.e_graph.get_node_props2bool(self.args.node_type, [], mask_name_list) 
            masks = torch.from_numpy(masks).t()

        # 3、根据size设置mask；训练集、验证集、测试集的mask
        if 'train_mask' in mask_name_dict:
            train_mask = masks[mask_name_dict['train_mask']]
        else:
            train_size = int(self.nodes_num / 5)
            train_mask = torch.zeros(self.nodes_num, dtype=torch.bool)
            train_mask[:train_size - 1] = True
        train_node_tensor = train_mask.nonzero().squeeze()
        # val_mask = masks[mask_name_dict['val_mask']]
        # test_mask = masks[mask_name_dict['test_mask']]

        sampler_neighbour = EzooMultiLayerNeighborSampler(fanouts=[int(fanout) for fanout in self.args.fan_out.split(
            ',')], e_graph=self.e_graph, p=1, g_nodes_num=self.nodes_num, one_hot=self.args.one_hot, node_type=self.args.node_type)

        train_loader = EzooNodeDataLoader(train_node_tensor, sampler_neighbour,
                                          self.args.label_name, device=self.device, batch_size=self.args.batch_size, num_workers=self.args.n_workers,
                                          drop_last=False, shuffle=True)

        # 模型参数
        num_hidden = self.args.n_hidden
        num_layers = self.args.n_layers
        dropout = self.args.dropout

        model = StoSAGE(self.in_feats, num_hidden, self.n_classes,
                        num_layers, F.relu, dropout)
        model = model.to(self.device)
        loss_fcn = nn.CrossEntropyLoss()
        optimizer = optim.Adam(model.parameters(), lr=self.args.lr)

        # 进行迭代
        avg = 0
        iter_tput = []
        for epoch in range(self.args.n_epochs):
            tic = time.time()

            # Loop over the dataloader to sample the computation dependency graph as a list of
            # blocks.
            tic_step = time.time()
            total_sample = 0
            total_load_subtensor = 0
            total_load = 0
            total_train = 0
            for step, (input_nodes, seeds, blocks) in enumerate(train_loader):
                tic_load_subtensor = time.time()
                total_sample += tic_load_subtensor - tic_step
                batch_inputs, batch_labels = self.load_subtensor(
                    input_nodes, seeds)
                # batch_inputs是UnifiedTensor的话，需要如下处理，不能直接to(self.device)
                # batch_idx = torch.arange(batch_inputs.shape[0]).to(self.device)
                # batch_inputs = batch_inputs[batch_idx].to(self.device)
                batch_inputs = batch_inputs.to(self.device)
                # seeds = seeds.to(self.device)
                batch_labels = batch_labels.to(self.device)

                # 如果sample_frontier中block没有to(self.device), 则在这里进行
                blocks_gpu = []
                for block in blocks:
                    block_gpu = block.to(self.device)
                    blocks_gpu.append(block_gpu)

                toc_load_subtensor = time.time()
                total_load_subtensor += toc_load_subtensor - tic_load_subtensor
                toc_load = time.time()
                total_load += toc_load - tic_step       # 记录每个step中数据加载的时间

                batch_pred = model(blocks_gpu, batch_inputs)
                loss = loss_fcn(batch_pred, batch_labels)
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

                toc_train = time.time()
                total_train += toc_train - toc_load     # 记录每个step中训练的时间
                print('Step {:05d} | On iter_sample {:06f} | On load_subtensor {:06f} | On Loader {:06f} | On Train {:06f}'.format(step,
                                                                                                           (tic_load_subtensor - tic_step),
                                                                                                           (toc_load_subtensor - tic_load_subtensor),
                                                                                                           (toc_load - tic_step),
                                                                                                           (toc_train - toc_load)))

                iter_tput.append(len(seeds) / (time.time() - tic_step))
                if step % self.args.log_every == 0:
                    acc = self.compute_acc(batch_pred, batch_labels)
                    gpu_mem_alloc = torch.cuda.max_memory_allocated(
                    ) / 1000000 if torch.cuda.is_available() else 0
                    print('Epoch {:05d} | Step {:05d} | Loss {:.4f} | Train Acc {:.4f} '
                          '| Speed (samples/sec) {:.4f} | GPU {:.1f} MB'.format(epoch, step, loss.item(), acc.item(),
                                                                                np.mean(iter_tput[3:]), gpu_mem_alloc))
                    print('Epoch {:05d} | Total Sample Time {:.6f} | Total Load_subtensor Time {:.6f} | Total Load Time {:.6f} | Total Train Time {:.6f}'.format(epoch,
                                                                                                                                      total_sample,
                                                                                                                                      total_load_subtensor,
                                                                                                                                      total_load,
                                                                                                                                      total_train))
                tic_step = time.time()
                print("="*60)
            toc = time.time()
            print('Epoch Time(s): {:.4f}'.format(toc - tic))
            print('='*60)

            if epoch >= 5:
                avg += toc - tic

        print('Avg epoch time: {}'.format(avg / (epoch - 4)))

        if self.args.save_model:
            self.save_model(model)

    def ezoo_inference(self, model, node_tensor, device):
        for l, layer in enumerate(model.layers):
            y = torch.zeros(self.nodes_num, self.args.n_hidden if l !=
                            len(model.layers) - 1 else self.n_classes)

            sampler = EzooMultiLayerFullNeighborSampler(
                1,
                e_graph=self.e_graph,
                p=1,
                g_nodes_num=self.nodes_num,
                one_hot=self.args.one_hot,
                node_type=self.args.node_type)
            dataloader = EzooNodeDataLoader(
                node_tensor,
                sampler,
                self.args.label_name,
                device=device,
                batch_size=self.args.batch_size,
                num_workers=self.args.n_workers,
                drop_last=False,
                shuffle=True)

            for input_nodes, output_nodes, blocks in dataloader:
                block = blocks[0]

                block = block.int().to(device)
                if l == 0:
                    input_features, _ = self.load_subtensor(
                        input_nodes, len(input_nodes))
                else:
                    input_features = x[input_nodes]
                h = input_features.to(device)
                h = layer(block, h)
                if l != len(model.layers) - 1:
                    h = model.activation(h)
                    h = model.dropout(h)

                y[output_nodes] = h.cpu()

            x = y
        return y

    def inference(self, node=None):
        model = StoSAGE(self.in_feats, self.args.n_hidden, self.n_classes,
                        self.args.n_layers, F.relu, self.args.dropout)
        if not self.load_model(model):
            print('Model loading failed!')
            return

        if node is not None:
            node_tensor = self.e_graph.query_simple_neighbour(
                node, 1, len(model.layers) * 2 + 1).astype(np.long)
            if node not in node_tensor:
                node_tensor = np.append(node_tensor, node)
        else:
            node_tensor = (self.e_graph.get_node_id_batch(
                self.args.node_type, 0, self.nodes_num)).astype(np.long)

        device = torch.device('cpu') if self.args.gpu < 0 else torch.device(
            'cuda:%d' % self.args.gpu)
        model = model.to(device)

        model.eval()
        with torch.no_grad():
            result = self.ezoo_inference(model, node_tensor, device)
            if node is not None:
                return torch.argmax(result, dim=1)[node]
            else:
                return torch.argmax(result, dim=1)
