import torch.nn.functional as F

import dgl
import torch
import time

from .model_basic import LoadingWholeGraph
from .gcn import GCN


class TrainGCN(LoadingWholeGraph):

    def __init__(self, args):
        super().__init__(args)

    def train(self):
        """the logic for testing gcn is very similar for dgl and ezoo"""
        if self.args.self_loop:
            self.g = dgl.remove_self_loop(self.g)
            self.g = dgl.add_self_loop(self.g)
        n_edges = self.g.number_of_edges()

        # normalization
        degs = self.g.in_degrees().float()
        norm = torch.pow(degs, -0.5)
        norm[torch.isinf(norm)] = 0
        self.g.ndata['norm'] = norm.unsqueeze(1)

        # create GCN model
        model = GCN(self.g,
                    self.in_feats,
                    self.args.n_hidden,
                    self.n_classes,
                    self.args.n_layers,
                    F.relu,
                    self.args.dropout)

        if self.cuda:
            model.cuda()
        loss_fcn = torch.nn.CrossEntropyLoss()

        # use optimizer
        optimizer = torch.optim.Adam(model.parameters(),
                                     lr=self.args.lr,
                                     weight_decay=self.args.weight_decay)

        # initialize graph
        dur = []
        acc_dict = []
        loss_dict = []
        for epoch in range(self.args.n_epochs):
            model.train()
            t0 = time.time()
            logits = model(self.features)
            loss = loss_fcn(logits[self.train_mask],
                            self.labels[self.train_mask])
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            dur.append(time.time() - t0)
            acc = self.evaluate(model, self.val_mask,
                                self.features, self.labels)
            loss_dict.append(loss.item())
            acc_dict.append(acc)
            self.print_info(epoch, dur, loss, acc, n_edges)

        acc = self.evaluate(model, self.test_mask, self.features, self.labels)
        print("Test accuracy {:.2%}".format(acc))
        end = time.time()
        print('all duration time is ', (end - self.start))
        self.show_loss_acc(loss_dict, acc_dict)

        if self.args.save_model:
            self.save_model(model)

    def inference(self, node=None):
        model = GCN(self.g,
                    self.in_feats,
                    self.args.n_hidden,
                    self.n_classes,
                    self.args.n_layers,
                    F.relu,
                    self.args.dropout)
        if node is not None:
            return super().inference(model)[node]
        else:
            return super().inference(model)
