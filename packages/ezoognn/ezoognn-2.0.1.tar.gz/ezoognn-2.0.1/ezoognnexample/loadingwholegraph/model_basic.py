from ezoognn import get_ezoo_home
from ezoognn.utils.model_loader import ModelLoader
from ezoognn.loader.loadwholegraph import EzooWholeGraphLoader, EzooEdgeWholeGraphLoader
from ezoognn.loader.dataset.ezoo_data_graph import EzooGraphDataset, EzooShapeGraphEnum
from dgl.data import CoraGraphDataset
import numpy as np
import torch
import time
import matplotlib.pyplot as plt

import sys
if sys.platform.startswith('linux'):
    import matplotlib
    matplotlib.use('Agg')


class ModelBasicOp(ModelLoader):
    def __init__(self, args, loader_type):
        # if you are using DGL cora dataset ( we can add a list of DGL dataset later, for now just use cora)
        self.args = args
        self.start = time.time()
        if self.args.dataset == 'cora' and self.args.gnn_type[:3] == 'dgl':
            self.data = CoraGraphDataset()
        # if you using EZOO to load dataset
        elif self.args.gnn_type[:4] == 'ezoo':
            if loader_type == "edge":
                self.data = EzooEdgeWholeGraphLoader(
                    name=self.args.dataset, url=self.args.url, cfg_file=self.args.cfg_file, one_hot=self.args.one_hot, train_rate=0.2, test_rate=0.1,
                    gdi_ptr=self.args.gdi_ptr, restore_file=self.args.restore_file, restore_url=self.args.restore_url,
                    node_type=self.args.node_type, id_name=self.args.id_name, label_name=self.args.label_name)
            else:
                # self.data = EzooWholeGraphLoader(
                #     name=self.args.dataset, url=self.args.url, cfg_file=self.args.cfg_file, one_hot=self.args.one_hot, train_rate=0.2, test_rate=0.1,
                #     gdi_ptr=self.args.gdi_ptr, restore_file=self.args.restore_file, restore_url=self.args.restore_url,
                #     node_type=self.args.node_type, id_name=self.args.id_name, label_name=self.args.label_name, exclude_list=self.args.exclude_list)
                self.data = EzooGraphDataset(name=self.args.dataset, cfg_file=self.args.cfg_file, train_rate=0.2,
                                             gdi_ptr=self.args.gdi_ptr, restore_file=self.args.restore_file, restore_url=self.args.restore_url,
                                             node_type=self.args.node_type, node_exclude_list=self.args.node_exclude_list,
                                             edge_exclude_list=self.args.edge_exclude_list)[EzooShapeGraphEnum.WHOLE]
        else:
            raise ValueError('Unknown dataset: {}'.format(self.args.dataset))

        if self.args.gpu < 0:
            self.cuda = False
            device = torch.device('cpu')
        else:
            self.cuda = True
            device = torch.device('cuda:%d' % self.args.gpu)

        if self.cuda and not self.args.use_uva:
            self.g = self.data[0].to(device)
        else:
            self.g = self.data[0]

        loader_end = time.time()
        print('loader dataset duration time is : ',
              (loader_end - self.start), self.data)

        super().__init__(args)

    @staticmethod
    def print_info(epoch, dur, loss, acc, n_edges):
        print("Epoch {:05d} | Time(s) {:.4f} | Loss {:.4f} | Accuracy {:.4f} | "
              "ETputs(KTEPS) {:.2f}".format(epoch, dur[-1], loss.item(),
                                            acc, n_edges / np.mean(dur) / 1000))

    @staticmethod
    def show_loss_acc(loss_dict, acc):
        plt.plot(loss_dict, label='loss for every epoch', color='r')
        plt.plot(acc, label='acc for every epoch', color='g')
        plt.legend()
        plt.show()

    @staticmethod
    def evaluate(model, mask, features, labels):
        # mask can be train, test, or val mask
        model.eval()
        with torch.no_grad():
            logits = model(features)
            logits = logits[mask]
            labels = labels[mask]
            _, indices = torch.max(logits, dim=1)
            correct = torch.sum(indices == labels)
            return correct.item() * 1.0 / len(labels)

    def inference(self, model):
        if not self.load_model(model):
            print('Model loading failed!')
            return

        if self.cuda:
            model.cuda()

        model.eval()
        with torch.no_grad():
            logits = model(self.features)
            return torch.argmax(logits, dim=1)


class LoadingWholeGraph(ModelBasicOp):
    """train and test all sorts of gnn model"""

    def __init__(self, args):
        super().__init__(args, 'node')

        self.features = self.g.ndata['feat']
        self.labels = self.g.ndata['label']
        self.train_mask = self.g.ndata['train_mask']
        self.val_mask = self.g.ndata['val_mask']
        self.test_mask = self.g.ndata['test_mask']
        self.in_feats = self.features.shape[1]
        # num_labels is deprecated and replaced by num_classes
        self.n_classes = self.data.num_classes
        self.n_edges = self.data.dgl_graph.number_of_edges()
        print("""----Data statistics------'
          #Edges %d
          #Classes %d
          #Train samples %d
          #Val samples %d
          #Test samples %d""" %
              (self.n_edges, self.n_classes,
               self.train_mask.int().sum().item(),
               self.val_mask.int().sum().item(),
               self.test_mask.int().sum().item()))


class EdgeLoadingWholeGraph(ModelBasicOp):
    """train and test all sorts of gnn model"""

    def __init__(self, args):
        super().__init__(args, 'edge')

        self.labels = self.g.edata['label']
        self.train_mask = self.g.edata['train_mask']
        self.val_mask = self.g.edata['val_mask']
        self.test_mask = self.g.edata['test_mask']
        # num_labels is deprecated and replaced by num_classes
        self.n_classes = self.data.num_classes
        self.n_edges = self.data.dgl_graph.number_of_edges()
        print("""----Data statistics------'
          #Edges %d
          #Classes %d
          #Train samples %d
          #Val samples %d
          #Test samples %d""" %
              (self.n_edges, self.n_classes,
               self.train_mask.int().sum().item(),
               self.val_mask.int().sum().item(),
               self.test_mask.int().sum().item()))
