from ezoognnexample.fullgraph.gcn.gcn import GCN
from ezoognn.nni.nni_params_handler import MetricsReporter
from ezoognn.loader.dataset.citation_ezoo_data_graph import *
from ezoognn.loader.dataset.ezoo_data_graph import EzooShapeGraphEnum
from dgl.data import CoraGraphDataset, CiteseerGraphDataset, PubmedGraphDataset
import dgl
import torch.nn.functional as F
import torch
import numpy as np
import time
import argparse
#from gcn_mp import GCN
#from gcn_spmv import GCN


def evaluate(model, graph, features, labels, mask):
    model.eval()
    with torch.no_grad():
        logits = model(graph, features)
        logits = logits[mask]
        labels = labels[mask]
        _, indices = torch.max(logits, dim=1)
        correct = torch.sum(indices == labels)
        return correct.item() * 1.0 / len(labels)


def main(args):
    if args.ezoo_fullgraph is not None and args.ezoo_fullgraph:
        # load and preprocess dataset
        if args.dataset == 'cora':
            ezooGraph = CoraEzooGraphDatasetV2(cfg_file=args.cfg_file)
        elif args.dataset == 'citeseer':
            ezooGraph = CiteseerEzooGraphDataset(cfg_file=args.cfg_file)
        elif args.dataset == 'pubmed':
            ezooGraph = PubmedEzooGraphDataset(cfg_file=args.cfg_file)
        else:
            raise ValueError('Unknown dataset: {}'.format(args.dataset))
        data = ezooGraph[EzooShapeGraphEnum.WHOLE]
    else:
        # load and preprocess dataset
        if args.dataset == 'cora':
            data = CoraGraphDataset()
        elif args.dataset == 'citeseer':
            data = CiteseerGraphDataset()
        elif args.dataset == 'pubmed':
            data = PubmedGraphDataset()
        else:
            raise ValueError('Unknown dataset: {}'.format(args.dataset))

    g = data[0]
    if args.gpu < 0:
        cuda = False
    else:
        cuda = True
        g = g.int().to(args.gpu)

    features = g.ndata['feat']
    labels = g.ndata['label']
    train_mask = g.ndata['train_mask']
    val_mask = g.ndata['val_mask']
    test_mask = g.ndata['test_mask']
    in_feats = features.shape[1]
    n_classes = data.num_labels
    n_edges = data.graph.number_of_edges()
    print("""----Data statistics------'
      #Edges %d
      #Classes %d
      #Train samples %d
      #Val samples %d
      #Test samples %d""" %
          (n_edges, n_classes,
              train_mask.int().sum().item(),
              val_mask.int().sum().item(),
              test_mask.int().sum().item()))

    # add self loop
    if args.self_loop:
        g = dgl.remove_self_loop(g)
        g = dgl.add_self_loop(g)
    n_edges = g.number_of_edges()

    # normalization
    degs = g.in_degrees().float()
    norm = torch.pow(degs, -0.5)
    norm[torch.isinf(norm)] = 0
    if cuda:
        norm = norm.cuda()
    g.ndata['norm'] = norm.unsqueeze(1)

    # create GCN model
    model = GCN(in_feats,
                args.n_hidden,
                n_classes,
                args.n_layers,
                F.relu,
                args.dropout)

    if cuda:
        model.cuda()
    loss_fcn = torch.nn.CrossEntropyLoss()

    # use optimizer
    optimizer = torch.optim.Adam(model.parameters(),
                                 lr=args.lr,
                                 weight_decay=args.weight_decay)

    # initialize graph
    dur = []
    for epoch in range(args.n_epochs):
        model.train()
        if epoch >= 3:
            t0 = time.time()
        # forward
        logits = model(g, features)
        loss = loss_fcn(logits[train_mask], labels[train_mask])

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if epoch >= 3:
            dur.append(time.time() - t0)

        acc = evaluate(model, g, features, labels, val_mask)
        MetricsReporter.report_intermediate_result(acc)
        print("Epoch {:05d} | Time(s) {:.4f} | Loss {:.4f} | Accuracy {:.4f} | "
              "ETputs(KTEPS) {:.2f}". format(epoch, np.mean(dur), loss.item(),
                                             acc, n_edges / np.mean(dur) / 1000))

    print()
    acc = evaluate(model, g, features, labels, test_mask)
    MetricsReporter.report_final_result(acc)
    print("Test accuracy {:.2%}".format(acc))
    return acc

    # test_idx = test_mask.nonzero().squeeze()
    # painter = ezooGraph.get_painter(notebook=True, nodes_limit=-1,
    #                                 highlight_feats='label')
    # painter.draw_explain_graph(model, test_idx, 2, output_file='explain.html')


if __name__ == '__main__':
    import os
    current_dir = os.path.dirname(os.path.abspath(__file__))

    parser = argparse.ArgumentParser(description='GCN')
    parser.add_argument("--dataset", type=str, default="cora",
                        help="Dataset name ('cora', 'citeseer', 'pubmed').")
    parser.add_argument("--dropout", type=float, default=0.5,
                        help="dropout probability")
    parser.add_argument("--gpu", type=int, default=-1,
                        help="gpu")
    parser.add_argument("--lr", type=float, default=1e-2,
                        help="learning rate")
    parser.add_argument("--n-epochs", type=int, default=200,
                        help="number of training epochs")
    parser.add_argument("--n-hidden", type=int, default=16,
                        help="number of hidden gcn units")
    parser.add_argument("--n-layers", type=int, default=1,
                        help="number of hidden gcn layers")
    parser.add_argument("--weight-decay", type=float, default=5e-4,
                        help="Weight for L2 loss")
    parser.add_argument("--self-loop", action='store_true',
                        help="graph self-loop (default=False)")
    parser.add_argument("-cfg", "--cfg-file", type=str, default=os.path.join(current_dir, '../../../../../resources/conf/ezoodb.conf'),
                        help="ezoo cfg config")
    parser.add_argument("-nni-yaml", "--nni-yaml", type=str, default='',
                        help="nni_yaml")
    parser.add_argument("--ezoo-fullgraph", type=bool, default=True,
                        help="ezoo full graph")
    parser.add_argument("--use-cache", type=bool, default=False,
                        help="Use cache in ezoo loader or not")
    parser.set_defaults(self_loop=False)
    args = parser.parse_args()
    print(args)

    MetricsReporter.update_report_params(args)

    main(args)
