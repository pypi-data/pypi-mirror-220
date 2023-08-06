import dgl
import time
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np
from sklearn import metrics
import dgl.nn.pytorch as dglnn

from ezoognn.ezoo_graph import EzooGraph
from ..loadingwholegraph.model_basic import EdgeLoadingWholeGraph
from ezoognn.loader.loadbatchgraph import EzooEdgeDataLoader
from ezoognn.sampler.neighbor_sampler import EzooMultiLayerNeighborSampler, EzooMultiLayerFullNeighborSampler

class TwoLayerGCN(nn.Module):
    def __init__(self, in_dim, hid_dim, out_dim):
        """两层的GCN模型"""
        super().__init__()
        self.conv1 = dglnn.GraphConv(in_dim, hid_dim, allow_zero_in_degree=True)
        self.conv2 = dglnn.GraphConv(hid_dim, out_dim, allow_zero_in_degree=True)

    def forward(self, blocks, x):
        x = F.relu(self.conv1(blocks[0], x))
        x = F.relu(self.conv2(blocks[1], x))
        return x


class Predictor(nn.Module):
    """边预测模块，将边两端节点表示拼接，然后接一个线性变换，得到最后的分类表示输出"""

    def __init__(self, in_dim, num_classes):
        super().__init__()
        self.W = nn.Linear(2 * in_dim, num_classes)

    def apply_edges(self, edges):
        data = torch.cat([edges.src['x'], edges.dst['x']], dim=-1)
        return {'score': self.W(data)}

    def forward(self, edge_subgraph, x):
        with edge_subgraph.local_scope():
            edge_subgraph.ndata['x'] = x
            edge_subgraph.apply_edges(self.apply_edges)
            return edge_subgraph.edata['score']


class MyModel(nn.Module):
    """主模型：结构比较清晰"""

    def __init__(self, emb_dim, hid_dim, out_dim, num_classes, num_nodes):
        super().__init__()
        self.node_emb = nn.Embedding(num_nodes, emb_dim)
        self.gcn = TwoLayerGCN(emb_dim, hid_dim, out_dim)
        self.predictor = Predictor(out_dim, num_classes)

    def forward(self, edge_subgraph, blocks, input_nodes):
        x = self.node_emb(input_nodes)
        x = self.gcn(blocks, x)
        return self.predictor(edge_subgraph, x)


'''
ezoo 边采样
'''
class StoTrainWithEzooSamplEdges():

    def __init__(self, args):
        self.args = args

    def train(self):
        if self.args.gpu >= 0:
            device = torch.device('cuda:%d' % self.args.gpu)
        else:
            device = torch.device('cpu')

        # 1、初始化ezoodbClient  name='wn18'
        dbname = self.args.dataset
        e_graph = EzooGraph(url=self.args.url, dbname=dbname, cfg_file=self.args.cfg_file,
                            restore_file=self.args.restore_file, restore_url=self.args.restore_url, gdi_ptr=self.args.gdi_ptr)
        # 2、获取总数量，随机获取指定node的节点，截取部分内容，比如十分之一作为train_mask，百分之一作为val_mask，剩余的为test_mask
        nodes_num = e_graph.get_nodes_num(self.args.node_type)
        n_edges = e_graph.get_edges_num(self.args.edge_type)

        train_size = 60575
        val_size = 5000
        edges_tensor = torch.LongTensor([i for i in range(n_edges)])
        # 3、根据size设置mask；训练集、验证集、测试集的mask
        train_eid = edges_tensor[:train_size]
        val_eid = edges_tensor[train_size: (train_size + val_size)]
        # 获取边的lable标签 todo
        labels = np.asarray(e_graph.get_edge_prop(val_eid, 'label'))
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # Create sampler
        sampler_neighbour = EzooMultiLayerNeighborSampler(fanouts=[int(fanout) for fanout in self.args.fan_out.split(
            ',')], e_graph=e_graph, p=1, g_nodes_num=nodes_num, one_hot=self.args.one_hot,
                                                          node_type=self.args.node_type)
        train_loader = EzooEdgeDataLoader(
            train_eid, sampler_neighbour,
            exclude='reverse_id',  # 去除反向边，否则模型可能知道存在边的联系，导致模型“作弊”
            # For each edge with ID e in dataset, the reverse edge is e ± |E|/2.
            reverse_eids=torch.cat([torch.arange(n_edges // 2, n_edges), torch.arange(0, n_edges // 2)]),
            device=device,
            shuffle=True,
            batch_size=self.args.batch_size,
            drop_last=False,
            num_workers=self.args.n_workers)

        model = MyModel(64, self.args.n_hidden, self.args.n_hidden, 36, nodes_num)
        model = model.to(device)
        loss_fcn = nn.CrossEntropyLoss()  # 交叉熵损失
        optimizer = optim.Adam(model.parameters(), lr=self.args.lr)

        def predict(model, valid_eid, device, n_edges, args):
            # Create sampler（全采样）
            sampler = EzooMultiLayerFullNeighborSampler(2, e_graph=e_graph, p=1, g_nodes_num=nodes_num, one_hot=self.args.one_hot, node_type=self.args.node_type)
            dataloader = EzooEdgeDataLoader(
                valid_eid, sampler, exclude='reverse_id',
                # For each edge with ID e in dataset, the reverse edge is e ± |E|/2.
                reverse_eids=torch.cat([torch.arange(n_edges // 2, n_edges), torch.arange(0, n_edges // 2)]),
                batch_size=args.batch_size,
                shuffle=False,
                drop_last=False,
                num_workers=args.n_workers)

            valid_preds = []
            model.eval()
            with torch.no_grad():
                for input_nodes, edges_subgraph, blocks in dataloader:
                    edges_subgraph = edges_subgraph.to(device)
                    blocks = [block.int().to(device) for block in blocks]
                    pred = model(edges_subgraph, blocks, input_nodes)
                    pred = pred.cpu().argmax(-1).numpy().tolist()
                    valid_preds.extend(pred)
            return valid_preds

        best_val_acc = 0  # 记录验证集上的最好效果
        patience = 0  # For early stopping
        # Training loop
        for epoch in range(self.args.n_epochs):
            # Loop over the dataloader to sample the computation dependency graph as a list of
            # blocks.
            start_time = time.time()
            all_loss = []
            trn_label, trn_pred = [], []
            n_batches = train_loader.__len__()

            for step, (input_nodes, edges_subgraph, blocks) in enumerate(train_loader):
                edges_subgraph = edges_subgraph.to(device)
                blocks = [block.to(device) for block in blocks]

                # Compute loss and prediction
                edge_preds = model(edges_subgraph, blocks, input_nodes)
                etypes = edges_subgraph.edata['etype']

                loss = loss_fcn(edge_preds, etypes)  # or labels[edges_subgraph.edata['_ID']]
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

                all_loss.append(loss.item())
                trn_label.extend(etypes.cpu().numpy().tolist())
                trn_pred.extend(edge_preds.argmax(-1).detach().cpu().numpy().tolist())

                if (step + 1) % (n_batches // 10) == 0:
                    cur_acc = metrics.accuracy_score(trn_label, trn_pred)
                    print('Epoch {:2d} | Step {:04d}/{} | Loss {:.4f} | Avg Loss {:.4f} | Acc {:.4f} | Time {:.2f}s'.format(
                        epoch + 1, step, n_batches, loss.item(), np.mean(all_loss), cur_acc, time.time() - start_time))

            ## 验证集预测
            val_preds = predict(model, val_eid, device, n_edges, args=self.args)

            val_acc = metrics.accuracy_score(labels, val_preds)

            if val_acc > best_val_acc:
                best_val_acc = val_acc
                patience = 0
                torch.save(model.state_dict(), "edge_cls_best_model.bin")
            else:
                patience += 1
            print('Cur Val Acc {:.4f}, Best Val Acc {:.4f}, Time {:.2f}s'.format(
                val_acc, best_val_acc, time.time() - start_time))

            ## earlystopping，如果验证集效果连续三次以上都没上升，直接停止训练
            if patience > 100:
                break


'''
dgl的全图采样，使用ezoo构建全图
'''
class DglStoTrainWithEzooSamplEdges(EdgeLoadingWholeGraph):
    
    
    def __init__(self, args):
        super().__init__(args)

    def train(self):
        args = self.args
        # load wordnet data 需要torch==1.9.1
        n_classes = self.n_classes  ## 关系数量，也就是边分类的分类数
        g = self.g
        ## 训练集、验证集、测试集
        train_edge_mask = g.edata['train_mask']
        val_edge_mask = g.edata['val_mask']
        test_edge_mask = g.edata['test_mask']

        # Pack data
        data = train_edge_mask, val_edge_mask, test_edge_mask, n_classes, g
        print('\n', g)
        g.to_canonical_etype
        edges = g.edges()
        nodes = g.nodes()
        n_edges = g.num_edges()  # 图中边的数量
        labels = g.edata['label']  # 图中所有边的标签
        train_mask = g.edata['train_mask']
        test_mask = g.edata['test_mask']
        val_mask = g.edata['val_mask']
        labels = g.edata['label']

        train_edge_mask, val_edge_mask, test_edge_mask, n_classes, g = data
        print('\n', train_edge_mask.sum(), val_edge_mask.sum(), test_edge_mask.sum())

        ## train, valid, test 边的id列表
        train_eid = torch.LongTensor(np.nonzero(train_edge_mask)).squeeze()
        val_eid = torch.LongTensor(np.nonzero(val_edge_mask)).squeeze()
        test_eid = torch.LongTensor(np.nonzero(test_edge_mask)).squeeze()
        print(train_eid.shape, val_eid.shape, test_eid.shape)

        # Create sampler
        sampler = dgl.dataloading.MultiLayerNeighborSampler(
            [int(fanout) for fanout in args.fan_out.split(',')])
        dataloader = dgl.dataloading.EdgeDataLoader(
            g, train_eid, sampler,
            exclude='reverse_id',  # 去除反向边，否则模型可能知道存在边的联系，导致模型“作弊”
            # For each edge with ID e in dataset, the reverse edge is e ± |E|/2.
            reverse_eids=torch.cat([torch.arange(n_edges // 2, n_edges), torch.arange(0, n_edges // 2)]),
            batch_size=args.batch_size,
            shuffle=True,
            drop_last=False,
            num_workers=args.n_workers)

        ## For debug

        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print("device: {}".format(device))

        model = MyModel(64, args.n_hidden, args.n_hidden, n_classes, g.num_nodes())
        model = model.to(device)
        loss_fcn = nn.CrossEntropyLoss()  # 交叉熵损失
        optimizer = optim.Adam(model.parameters(), lr=args.lr)

        def predict(model, g, valid_eid, device):
            # Create sampler（全采样）
            sampler = dgl.dataloading.MultiLayerFullNeighborSampler(2)
            dataloader = dgl.dataloading.EdgeDataLoader(
                g, valid_eid, sampler, exclude='reverse_id',
                # For each edge with ID e in dataset, the reverse edge is e ± |E|/2.
                reverse_eids=torch.cat([torch.arange(n_edges // 2, n_edges), torch.arange(0, n_edges // 2)]),
                batch_size=args.batch_size,
                shuffle=False,
                drop_last=False,
                num_workers=args.n_workers)

            valid_preds = []
            model.eval()
            with torch.no_grad():
                for input_nodes, edges_subgraph, blocks in dataloader:
                    edges_subgraph = edges_subgraph.to(device)
                    blocks = [block.int().to(device) for block in blocks]
                    pred = model(edges_subgraph, blocks, input_nodes)
                    pred = pred.cpu().argmax(-1).numpy().tolist()
                    valid_preds.extend(pred)
            return valid_preds

        best_val_acc = 0  # 记录验证集上的最好效果
        patience = 0  # For early stopping

        # Training loop
        for epoch in range(args.n_epochs):
            # Loop over the dataloader to sample the computation dependency graph as a list of
            # blocks.
            start_time = time.time()
            all_loss = []
            trn_label, trn_pred = [], []
            n_batches = len(dataloader)

            for step, (input_nodes, edges_subgraph, blocks) in enumerate(dataloader):
                edges_subgraph = edges_subgraph.to(device)
                blocks = [block.to(device) for block in blocks]

                # Compute loss and prediction
                edge_preds = model(edges_subgraph, blocks, input_nodes)
                loss = loss_fcn(edge_preds, edges_subgraph.edata['label'])  # or labels[edges_subgraph.edata['_ID']]
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

                all_loss.append(loss.item())
                trn_label.extend(edges_subgraph.edata['label'].cpu().numpy().tolist())
                trn_pred.extend(edge_preds.argmax(-1).detach().cpu().numpy().tolist())

                if (step + 1) % (n_batches // 10) == 0:
                    cur_acc = metrics.accuracy_score(trn_label, trn_pred)
                    print('Epoch {:2d} | Step {:04d}/{} | Loss {:.4f} | Avg Loss {:.4f} | Acc {:.4f} | Time {:.2f}s'.format(
                        epoch + 1, step, n_batches, loss.item(), np.mean(all_loss), cur_acc, time.time() - start_time))

            ## 验证集预测
            val_preds = predict(model, g, val_eid, device)
            val_acc = metrics.accuracy_score(labels[val_eid], val_preds)

            if val_acc > best_val_acc:
                best_val_acc = val_acc
                patience = 0
                torch.save(model.state_dict(), "edge_cls_best_model.bin")
            else:
                patience += 1
            print('Cur Val Acc {:.4f}, Best Val Acc {:.4f}, Time {:.2f}s'.format(
                val_acc, best_val_acc, time.time() - start_time))

            ## earlystopping，如果验证集效果连续三次以上都没上升，直接停止训练
            if patience > 100:
                break