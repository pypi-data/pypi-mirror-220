import time
import dgl
import torch
import torch.nn.functional as F
from ezoognnexample.loadingwholegraph.model_basic import LoadingWholeGraph
from ezoognnexample.fullgraph.graphsage.sage import *


class TrainSAGE(LoadingWholeGraph):

    def __init__(self, args):
        super().__init__(args)

    def train(self):
        if self.args.gpu < 0:
            self.cuda = False
        else:
            self.cuda = True
            torch.cuda.set_device(self.args.gpu)
            self.features = self.features.cuda()
            self.labels = self.labels.cuda()
            self.train_mask = self.train_mask.cuda()
            self.val_mask = self.val_mask.cuda()
            self.test_mask = self.test_mask.cuda()
            print("use cuda:", self.args.gpu)
        train_nid = self.train_mask.nonzero().squeeze()
        val_nid = self.val_mask.nonzero().squeeze()
        test_nid = self.test_mask.nonzero().squeeze()
        # processing
        self.g = dgl.remove_self_loop(self.g)
        self.n_edges = self.g.number_of_edges()
        if self.cuda:
            self.g = self.g.int().to(self.args.gpu)

        model = GraphSAGE(self.g,
                          self.in_feats,
                          self.args.n_hidden,
                          self.n_classes,
                          self.args.n_layers,
                          F.relu,
                          self.args.dropout,
                          self.args.aggregator_type)
        if self.cuda:
            model.cuda()
        optimizer = torch.optim.Adam(
            model.parameters(), lr=self.args.lr, weight_decay=self.args.weight_decay)

        dur = []
        acc_dict = []
        loss_dict = []
        for epoch in range(self.args.n_epochs):
            model.train()
            t0 = time.time()
            logits = model(self.features)
            loss = F.cross_entropy(logits[train_nid], self.labels[train_nid])

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            dur.append(time.time() - t0)

            acc = self.evaluate(model, val_nid, self.features, self.labels)
            loss_dict.append(loss.item())
            acc_dict.append(acc)
            self.print_info(epoch, dur, loss, acc, self.n_edges)

        acc = self.evaluate(model, test_nid, self.features, self.labels)
        print("Test accuracy {:.2%}".format(acc))
        end = time.time()
        print('all duration time is ', (end - self.start))
        self.show_loss_acc(loss_dict, acc_dict)

        if self.args.save_model:
            self.save_model(model)
        return acc
    def inference(self, node=None):
        model = GraphSAGE(self.g,
                          self.in_feats,
                          self.args.n_hidden,
                          self.n_classes,
                          self.args.n_layers,
                          F.relu,
                          self.args.dropout,
                          self.args.aggregator_type)
        if node is not None:
            return super().inference(model)[node]
        else:
            return super().inference(model)
