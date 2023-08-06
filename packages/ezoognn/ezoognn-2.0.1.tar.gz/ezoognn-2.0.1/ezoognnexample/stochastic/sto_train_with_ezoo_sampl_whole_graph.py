# 代码说明
# 参考：https://github.com/NVIDIA/apex/issues/304 和 https://zhuanlan.zhihu.com/p/80695364
# 实现GPU不同stream之间的overlap，但未达到预期效果
# 分析原因：1）blocks没有pin_memory；2）blocks在to(device)时，有synchronize动作
# 留待以后再进一步研究分析

import time
import math
import dgl
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from ..loadingwholegraph.model_basic import LoadingWholeGraph
from .sto_sage import StoSAGE
from ezoognn.loader.loadbatchgraph import EzooNodeDataLoader
from ezoognn.loader.dataprefetcher import DataPrefetcher
from ezoognn.sampler.neighbor_sampler import EzooMultiLayerNeighborSampler


class StoTrainWithEzooSamplWholeGraph(LoadingWholeGraph):

    def __init__(self, args):
        super().__init__(args)
        self.args = args

        if self.args.gpu >= 0:
            self.device = torch.device('cuda:%d' % self.args.gpu)
        else:
            self.device = torch.device('cpu')

        self.train_stream = torch.cuda.Stream()

    def compute_acc(self, pred, labels):
        """
        Compute the accuracy of prediction given the labels.
        """
        labels = labels.long()
        return (torch.argmax(pred, dim=1) == labels).float().sum() / len(pred)

    def evaluate(self, model, val_nid, device):
        """
        Evaluate the model on the validation set specified by ``val_nid``.
        g : The entire graph.
        inputs : The features of all the nodes.
        labels : The labels of all the nodes.
        val_nid : the node Ids for validation.
        device : The GPU device to evaluate on.
        """
        model.eval()
        with torch.no_grad():
            pred = model.inference(self.g, self.features,
                                   device, self.args.batch_size, self.args.n_workers)
        model.train()
        return self.compute_acc(pred[val_nid], self.labels[val_nid].to(pred.device))

    def load_subtensor(self, nfeat, labels, seeds, input_nodes, device):
        """
        Extracts features and labels for a subset of nodes
        """
        batch_inputs = nfeat[input_nodes].to(device)
        batch_labels = labels[seeds].to(device)
        return batch_inputs, batch_labels

    def train(self):
        device = torch.device('cpu')
        if self.args.gpu < 0:
            self.cuda = False
            print("use cpu")
        elif self.args.use_uva:
            device = torch.device('cuda:%d' % self.args.gpu)
            torch.cuda.set_device(self.args.gpu)
            self.features = self.features.pin_memory()
            self.labels = self.labels.pin_memory()
            print("use cuda:", self.args.gpu, " | uva:", self.args.use_uva)
        else:
            device = torch.device('cuda:%d' % self.args.gpu)
            self.cuda = True
            torch.cuda.set_device(self.args.gpu)
            self.features = self.features.cuda()
            self.labels = self.labels.cuda()
            self.train_mask = self.train_mask.cuda()
            self.val_mask = self.val_mask.cuda()
            self.test_mask = self.test_mask.cuda()
            print("use cuda:", self.args.gpu, " | uva:", self.args.use_uva)

        train_nid = self.train_mask.nonzero().squeeze()
        val_nid = self.val_mask.nonzero().squeeze()
        test_nid = self.test_mask.nonzero().squeeze()
        # processing
        # self.g = dgl.remove_self_loop(self.g)
        self.n_nodes = self.data.e_graph.get_nodes_num(self.args.node_type)
        self.n_edges = self.g.number_of_edges()
        # comment the following 2 lines, because self.g has been loaded on device in class LoadingWholeGraph
        # if self.cuda:
        #     self.g = self.g.to(self.args.gpu)

        # Create PyTorch DataLoader for constructing blocks
        # sampler = dgl.dataloading.MultiLayerNeighborSampler(
        #     [int(fanout) for fanout in self.args.fan_out.split(',')])
        # dataloader = dgl.dataloading.NodeDataLoader(
        #     self.g,
        #     train_nid,
        #     sampler,
        #     device=device,
        #     batch_size=self.args.batch_size,
        #     shuffle=True,
        #     drop_last=False,
        #     num_workers=self.args.n_workers,
        #     use_uva=self.args.use_uva)

        # Create ezoo sampler & dataloader
        sampler = EzooMultiLayerNeighborSampler(fanouts=[int(fanout) for fanout in self.args.fan_out.split(',')],
                                                e_graph=self.data.e_graph,
                                                p=1,
                                                g_nodes_num=self.n_nodes,
                                                one_hot=self.args.one_hot,
                                                node_type=self.args.node_type)

        dataloader = EzooNodeDataLoader(train_nid,
                                        sampler,
                                        self.args.label_name,
                                        device=self.device,
                                        batch_size=self.args.batch_size,
                                        num_workers=self.args.n_workers,
                                        drop_last=False,
                                        shuffle=True,
                                        pin_memory=False)

        model = StoSAGE(self.in_feats, self.args.n_hidden, self.n_classes,
                        self.args.n_layers, F.relu, self.args.dropout)
        model = model.to(device)

        optimizer = torch.optim.Adam(model.parameters(), lr=self.args.lr)
        loss_fcn = nn.CrossEntropyLoss()

        # Training loop
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

            # ========================================
            prefetcher = DataPrefetcher(dataloader, self.features, self.labels, self.device)
            seed_nodes, batch_inputs, batch_labels, blocks = prefetcher.next()
            iter_id = 0
            num_iters = math.ceil(len(train_nid) / self.args.batch_size)
            while batch_inputs is not None:
                iter_id += 1
                if iter_id > num_iters:
                    break

                if self.args.prof >= 0 and iter_id == self.args.prof:
                    print("Profiling begun at iteration {}".format(iter_id))
                    torch.cuda.cudart().cudaProfilerStart()

                if self.args.prof >= 0: torch.cuda.nvtx.range_push("Body of iteration {}".format(iter_id))

                tic_blocks = time.time()
                blocks = [block.int().to(device=self.device, non_blocking=True) for block in blocks]
                tic_train = time.time()

                # Compute loss and prediction
                with torch.cuda.stream(self.train_stream):
                    # print(f"current stream : {torch.cuda.current_stream()}")
                    if self.args.prof >= 0: torch.cuda.nvtx.range_push("forward")
                    for i in range(100):
                        batch_pred = model(blocks, batch_inputs)
                    if self.args.prof >= 0: torch.cuda.nvtx.range_pop()

                    loss = loss_fcn(batch_pred, batch_labels)
                    optimizer.zero_grad()

                    if self.args.prof >= 0: torch.cuda.nvtx.range_push("backward")
                    loss.backward()
                    if self.args.prof >= 0: torch.cuda.nvtx.range_pop()

                    if self.args.prof >= 0: torch.cuda.nvtx.range_push("optimizer.step()")
                    optimizer.step()
                    if self.args.prof >= 0: torch.cuda.nvtx.range_pop()

                torch.cuda.synchronize()  # Wait for the events to be recorded!
                toc_train = time.time()

                print(f"default stream : {torch.cuda.current_stream()}")
                print('Step {:05d} | On blocks {:06f} | On Train {:06f} | On Iter {:06f}'.format(
                      iter_id,
                      tic_train - tic_blocks,
                      toc_train - tic_train,
                      toc_train - tic_step))

                iter_tput.append(len(seed_nodes) / (toc_train - tic_step))
                if iter_id % self.args.log_every == 0:
                    acc = self.compute_acc(batch_pred, batch_labels)
                    gpu_mem_alloc = torch.cuda.max_memory_allocated() / 1000000 if torch.cuda.is_available() else 0
                    print('Epoch {:05d} | Step {:05d} | Loss {:.4f} | Train Acc {:.4f} | Speed (samples/sec) {:.4f} '
                          '| GPU {:.1f} MB'.
                          format(epoch, iter_id, loss.item(), acc.item(), np.mean(iter_tput[3:]),
                                 gpu_mem_alloc))
                tic_step = time.time()

                if self.args.prof >= 0: torch.cuda.nvtx.range_push("prefetcher.next()")
                seed_nodes, batch_inputs, batch_labels, blocks = prefetcher.next()
                if self.args.prof >= 0: torch.cuda.nvtx.range_pop()

                # Pop range "Body of iteration {}".format(i)
                if self.args.prof >= 0: torch.cuda.nvtx.range_pop()

                if self.args.prof >= 0 and iter_id == self.args.prof + 10:
                    print("Profiling ended at iteration {}".format(iter_id))
                    torch.cuda.cudart().cudaProfilerStop()
                    quit()
            # ========================================

            # for step, (input_nodes, seeds, blocks) in enumerate(dataloader):
            #     tic_load_subtensor = time.time()
            #     total_sample += tic_load_subtensor - tic_step
            #     # Load the input features as well as output labels
            #     batch_inputs, batch_labels = self.load_subtensor(self.features, self.labels,
            #                                                      seeds, input_nodes, device)
            #     blocks = [block.int().to(device) for block in blocks]
            #
            #     toc_load_subtensor = time.time()
            #     total_load_subtensor += toc_load_subtensor - tic_load_subtensor
            #     toc_load = time.time()
            #     total_load += toc_load - tic_step  # 记录每个step中数据加载的时间
            #
            #     # Compute loss and prediction
            #     batch_pred = model(blocks, batch_inputs)
            #     loss = loss_fcn(batch_pred, batch_labels)
            #     optimizer.zero_grad()
            #     loss.backward()
            #     optimizer.step()
            #
            #     toc_train = time.time()
            #     total_train += toc_train - toc_load  # 记录每个step中训练的时间
            #     print(
            #         'Step {:05d} | On iter_sample {:06f} | On load_subtensor {:06f} | On Loader {:06f} | On Train {:06f}'.format(
            #             step,
            #             (tic_load_subtensor - tic_step),
            #             (toc_load_subtensor - tic_load_subtensor),
            #             (toc_load - tic_step),
            #             (toc_train - toc_load)))
            #
            #     iter_tput.append(len(seeds) / (time.time() - tic_step))
            #     if step % self.args.log_every == 0:
            #         acc = self.compute_acc(batch_pred, batch_labels)
            #         gpu_mem_alloc = torch.cuda.max_memory_allocated(
            #         ) / 1000000 if torch.cuda.is_available() else 0
            #         print(
            #             'Epoch {:05d} | Step {:05d} | Loss {:.4f} | Train Acc {:.4f} | Speed (samples/sec) {:.4f} | GPU {:.1f} MB'.format(
            #                 epoch, step, loss.item(), acc.item(), np.mean(iter_tput[3:]), gpu_mem_alloc))
            #         print(
            #             'Epoch {:05d} | Total Sample Time {:.6f} | Total Load_subtensor Time {:.6f} | Total Load Time {:.6f} | Total Train Time {:.6f}'.format(
            #                 epoch,
            #                 total_sample,
            #                 total_load_subtensor,
            #                 total_load,
            #                 total_train))
            #     tic_step = time.time()
            torch.cuda.synchronize()
            toc = time.time()
            print('Epoch Time(s): {:.4f}'.format(toc - tic))
            print('=' * 60)

            if epoch >= 5:
                avg += toc - tic
            if epoch % self.args.eval_every == 0 and epoch != 0:
                eval_acc = self.evaluate(model, val_nid, device)
                print('Eval Acc {:.4f}'.format(eval_acc))
                test_acc = self.evaluate(model, test_nid, device)
                print('Test Acc: {:.4f}'.format(test_acc))

        print('Avg epoch time: {}'.format(avg / (epoch - 4)))

        if self.args.save_model:
            self.save_model(model)

    def inference(self, node=None):
        model = StoSAGE(self.in_feats, self.args.n_hidden, self.n_classes,
                        self.args.n_layers, F.relu, self.args.dropout)
        if not self.load_model(model):
            print('Model loading failed!')
            return

        device = torch.device('cpu') if self.args.gpu < 0 else torch.device(
            'cuda:%d' % self.args.gpu)
        model = model.to(device)

        model.eval()
        with torch.no_grad():
            result = model.inference(self.g, self.features,
                                     device, self.args.batch_size, self.args.n_workers)
            if node is not None:
                return torch.argmax(result, dim=1)[node]
            else:
                return torch.argmax(result, dim=1)
