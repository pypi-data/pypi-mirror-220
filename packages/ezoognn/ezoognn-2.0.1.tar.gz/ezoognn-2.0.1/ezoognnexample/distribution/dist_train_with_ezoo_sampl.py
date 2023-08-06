# -*- coding: utf-8 -*-
# @Time    : 2022/7/25 3:03 PM
# @Author  : lch
# @Email   : iltie165@163.com
# @File    : dist_train_with_ezoo_sampl.py
import dgl
import torch as th
from .dist_sage import SAGE
from .dist_train_base import DistTrainBase


class DistTrainSageWithEzoo(DistTrainBase):
    def __init__(self, args):
        super().__init__(args)

    def one_step(self, data_loader):
        with self.model.join():
            batch = 0
            for step, (input_nodes, seeds, blocks) in enumerate(data_loader):
                # Load the input features as well as output labels
                batch_inputs = self.g.ndata['feat'][input_nodes]
                batch_labels = self.g.ndata[self.args.label_name][seeds]

                # Compute loss and prediction
                batch_pred = self.model(blocks, batch_inputs)
                loss = self.loss_fcn(batch_pred, batch_labels)
                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()
                batch += 1
            return loss

    def get_trainer_for_graph(self):
        import torch.nn as nn
        import torch.optim as optim
        num_hidden = self.args.n_hidden
        num_labels = len(th.unique(self.g.ndata[self.args.label_name][0:self.g.number_of_nodes()]))
        num_layers = self.args.n_layers
        lr = self.args.lr
        model = SAGE(self.g.ndata['feat'].shape[1], num_hidden, num_labels, num_layers)
        loss_fcn = nn.CrossEntropyLoss()
        optimizer = optim.Adam(model.parameters(), lr=lr)

        return model, loss_fcn, optimizer

