import time
import dgl
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from ..loadingwholegraph.model_basic import LoadingWholeGraph
from .sto_sage import StoSAGE


class StoTrainWithDglSampl(LoadingWholeGraph):

    def __init__(self, args):
        super().__init__(args)

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
        else:
            device = torch.device('cuda:%d' % self.args.gpu)
            self.cuda = True
            torch.cuda.set_device(self.args.gpu)
            self.features = self.features.cuda()
            self.labels = self.labels.cuda()
            self.train_mask = self.train_mask.cuda()
            self.val_mask = self.val_mask.cuda()
            self.test_mask = self.test_mask.cuda()
            print("use cuda:", self.args.gpu)

        print("DGL dataloader use_uva =", self.args.use_uva)

        train_nid = self.train_mask.nonzero().squeeze()
        val_nid = self.val_mask.nonzero().squeeze()
        test_nid = self.test_mask.nonzero().squeeze()
        # processing
        # self.g = dgl.remove_self_loop(self.g)
        self.n_edges = self.g.number_of_edges()
        # comment the following 2 lines, because self.g has been loaded on device in class LoadingWholeGraph
        # if self.cuda:
        #     self.g = self.g.to(self.args.gpu)

        # Create PyTorch DataLoader for constructing blocks
        sampler = dgl.dataloading.MultiLayerNeighborSampler(
            [int(fanout) for fanout in self.args.fan_out.split(',')])
        dataloader = dgl.dataloading.NodeDataLoader(
            self.g,
            train_nid,
            sampler,
            device=device,
            batch_size=self.args.batch_size,
            shuffle=True,
            drop_last=False,
            num_workers=self.args.n_workers,
            use_uva=self.args.use_uva)

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
            for step, (input_nodes, seeds, blocks) in enumerate(dataloader):
                tic_load_subtensor = time.time()
                total_sample += tic_load_subtensor - tic_step
                # Load the input features as well as output labels
                batch_inputs, batch_labels = self.load_subtensor(self.features, self.labels,
                                                                 seeds, input_nodes, device)
                blocks = [block.int().to(device) for block in blocks]
                
                toc_load_subtensor = time.time()
                total_load_subtensor += toc_load_subtensor - tic_load_subtensor
                toc_load = time.time()
                total_load += toc_load - tic_step       # 记录每个step中数据加载的时间
                
                # Compute loss and prediction
                batch_pred = model(blocks, batch_inputs)
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
                    print('Epoch {:05d} | Step {:05d} | Loss {:.4f} | Train Acc {:.4f} | Speed (samples/sec) {:.4f} | GPU {:.1f} MB'.format(
                        epoch, step, loss.item(), acc.item(), np.mean(iter_tput[3:]), gpu_mem_alloc))
                    print('Epoch {:05d} | Total Sample Time {:.6f} | Total Load_subtensor Time {:.6f} | Total Load Time {:.6f} | Total Train Time {:.6f}'.format(epoch,
                                                                                                                                      total_sample,
                                                                                                                                      total_load_subtensor,
                                                                                                                                      total_load,
                                                                                                                                      total_train))
                tic_step = time.time()
            toc = time.time()
            print('Epoch Time(s): {:.4f}'.format(toc - tic))
            print('='*60)
            
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
