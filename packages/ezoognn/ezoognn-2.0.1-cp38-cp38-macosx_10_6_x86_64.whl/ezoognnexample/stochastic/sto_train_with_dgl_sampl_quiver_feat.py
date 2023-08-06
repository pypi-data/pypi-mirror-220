# Reaches around 0.7866 ± 0.0041 test accuracy.

import dgl
import torch as th
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import dgl.nn.pytorch as dglnn
import time
import argparse
from tqdm import tqdm
from ogb.nodeproppred import DglNodePropPredDataset
from ezoognn.loader.loadwholegraph import EzooWholeGraphLoader

import quiver

class SAGE(nn.Module):
    def __init__(self, in_feats, n_hidden, n_classes, n_layers, activation, dropout):
        super().__init__()
        self.init(in_feats, n_hidden, n_classes, n_layers, activation, dropout)

    def init(self, in_feats, n_hidden, n_classes, n_layers, activation, dropout):
        self.n_layers = n_layers
        self.n_hidden = n_hidden
        self.n_classes = n_classes
        self.layers = nn.ModuleList()
        if n_layers > 1:
            self.layers.append(dglnn.SAGEConv(in_feats, n_hidden, 'mean'))
            for i in range(1, n_layers - 1):
                self.layers.append(dglnn.SAGEConv(n_hidden, n_hidden, 'mean'))
            self.layers.append(dglnn.SAGEConv(n_hidden, n_classes, 'mean'))
        else:
            self.layers.append(dglnn.SAGEConv(in_feats, n_classes, 'mean'))
        self.dropout = nn.Dropout(dropout)
        self.activation = activation

    def forward(self, blocks, x):
        h = x
        for l, (layer, block) in enumerate(zip(self.layers, blocks)):
            h = layer(block, h)
            if l != len(self.layers) - 1:
                h = self.activation(h)
                h = self.dropout(h)
        return h

    def inference(self, g, x, device, batch_size, num_workers):
        """
        Inference with the GraphSAGE model on full neighbors (i.e. without neighbor sampling).
        g : the entire graph.
        x : the input of entire node set.
        The inference code is written in a fashion that it could handle any number of nodes and
        layers.
        """
        # During inference with sampling, multi-layer blocks are very inefficient because
        # lots of computations in the first few layers are repeated.
        # Therefore, we compute the representation of all nodes layer by layer.  The nodes
        # on each layer are of course splitted in batches.
        # TODO: can we standardize this?
        for l, layer in enumerate(self.layers):
            y = th.zeros(g.num_nodes(), self.n_hidden if l != len(
                self.layers) - 1 else self.n_classes)

            sampler = dgl.dataloading.MultiLayerFullNeighborSampler(1)
            dataloader = dgl.dataloading.NodeDataLoader(
                g,
                th.arange(g.num_nodes(), device=g.device),
                sampler,
                device=device if num_workers == 0 else None,
                batch_size=batch_size*4,                                # args.batch_size
                shuffle=False,
                drop_last=False,
                num_workers=0 if args.sample_gpu else num_workers)      # args.n_workers

            for input_nodes, output_nodes, blocks in tqdm(dataloader):
                block = blocks[0].int().to(device)

                h = x[input_nodes].to(device)
                h_dst = h[:block.num_dst_nodes()]
                h = layer(block, (h, h_dst))
                if l != len(self.layers) - 1:
                    h = self.activation(h)
                    h = self.dropout(h)

                y[output_nodes] = h.cpu()

            x = y
        return y


def compute_acc(pred, labels):
    """
    Compute the accuracy of prediction given the labels.
    """
    return (th.argmax(pred, dim=1) == labels).float().sum() / len(pred)


def evaluate(model, g, nfeat, labels, val_nid, test_nid, device, args):
    """
    Evaluate the model on the validation set specified by ``val_mask``.
    g : The entire graph.
    inputs : The features of all the nodes.
    labels : The labels of all the nodes.
    val_mask : A 0-1 mask indicating which nodes do we actually compute the accuracy for.
    device : The GPU device to evaluate on.
    """
    model.eval()
    with th.no_grad():
        pred = model.inference(g, nfeat, device, args.batch_size, args.n_workers).to(device)
    model.train()
    return compute_acc(pred[val_nid], labels[val_nid]), compute_acc(pred[test_nid], labels[test_nid])


def load_subtensor(nfeat, labels, seeds, input_nodes, device):
    """
    Extracts features and labels for a set of nodes.
    """
    batch_inputs = nfeat[input_nodes].to(device)
    batch_labels = labels[seeds].to(device)
    return batch_inputs, batch_labels

# Entry point

def run(args, device, data):
    # Unpack data
    train_nid, val_nid, test_nid, in_feats, labels, n_classes, nfeat, g = data

    if args.sample_gpu:
        train_nid = train_nid.to(device)
        # copy only the csc to the GPU
        g = g.formats(['csc'])
        g = g.to(device)

    # Create PyTorch DataLoader for constructing blocks
    sampler = dgl.dataloading.MultiLayerNeighborSampler(
        [int(fanout) for fanout in args.fan_out.split(',')])
    dataloader = dgl.dataloading.NodeDataLoader(
        g,
        train_nid,
        sampler,
        device=device,
        batch_size=args.batch_size,
        shuffle=True,
        drop_last=True,
        num_workers=0 if args.sample_gpu else args.n_workers,
        persistent_workers=not args.sample_gpu)

    # Define model and optimizer
    model = SAGE(in_feats, args.n_hidden, n_classes,
                 args.n_layers, F.relu, args.dropout)
    model = model.to(device)
    loss_fcn = nn.CrossEntropyLoss()
    optimizer = optim.Adam(
        model.parameters(), lr=args.lr)         # weight_decay=args.wd

    # Training loop
    best_val_acc = final_test_acc = 0
    for epoch in range(args.n_epochs):
        tic = time.time()

        model.train()
        pbar = tqdm(total=train_nid.size(0))
        pbar.set_description(f'Epoch {epoch:02d}')
        total_loss = total_correct = 0
        # Loop over the dataloader to sample the computation dependency graph as a list of
        # blocks.
        for input_nodes, seeds, blocks in dataloader:

            # copy block to gpu
            blocks = [blk.int().to(device) for blk in blocks]

            # Load the input features as well as output labels
            batch_inputs, batch_labels = load_subtensor(
                nfeat, labels, seeds, input_nodes, device)

            # Compute loss and prediction
            batch_pred = model(blocks, batch_inputs)
            loss = loss_fcn(batch_pred, batch_labels)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            total_loss += loss.item()
            total_correct += batch_pred.argmax(dim=-1).eq(batch_labels).sum().item()
            pbar.update(args.batch_size)

        pbar.close()

        loss = total_loss / len(dataloader)
        approx_acc = total_correct / (len(dataloader) * args.batch_size)
        print(f'Epoch {epoch:02d}, Loss: {loss:.4f}, Approx. Train: {approx_acc:.4f}, Epoch Time: {time.time() - tic:.4f}')

        if epoch >= 5:
            val_acc, test_acc = evaluate(model, g, nfeat, labels, val_nid, test_nid, device, args)
            print(f'Val: {val_acc:.4f}, Test: {test_acc:.4f}')

            if val_acc > best_val_acc:
                best_val_acc = val_acc
                final_test_acc = test_acc
    return final_test_acc

if __name__ == '__main__':
    parser = argparse.ArgumentParser("torch-quiver training")
    # parser.add_argument('--gpu', type=int, default=0,
    #                        help="GPU device ID. Use -1 for CPU training")
    # parser.add_argument('--num-epochs', type=int, default=10)
    # parser.add_argument('--num-hidden', type=int, default=256)
    # parser.add_argument('--num-layers', type=int, default=3)
    # parser.add_argument('--fan-out', type=str, default='5,10,15')
    # parser.add_argument('--batch-size', type=int, default=1024)
    # parser.add_argument('--lr', type=float, default=0.003)
    # parser.add_argument('--dropout', type=float, default=0.5)
    # parser.add_argument('--num-workers', type=int, default=4,
    #                        help="Number of sampling processes. Use 0 for no extra process.")
    # parser.add_argument('--save-pred', type=str, default='')
    # parser.add_argument('--wd', type=float, default=0)
    # parser.add_argument('--sample-gpu', action='store_true')
    parser.add_argument('--data', type=str, default='quiver', choices=('cpu', 'gpu', 'quiver', 'unified', 'uva'))
    parser.add_argument('--device-cache-size', type=str, default='200M')
    parser.add_argument('--cache-policy', type=str, default='device_replicate', 
                        help='''features cache policy on multi-gpu : 'device_replicate', 'p2p_clique_replicate'.''')

    parser.add_argument("--gnn-type", type=str, default='quiver-sto-sage',
                        help='''loader type ('ezoo-sage','dgl-sage','dgl-gcn', 'ezoo-gcn', 'quiver-sto-sage',
                        'ezoo-sto-sage', 'ezoo-sampler-sto-sage', 'ezoo-sampler-edge-sto-sage', 'ezoo-dgl-sampler-edge-sto-sage')''')
    parser.add_argument("--dataset", type=str, default="ogbn-products",
                        help="Dataset name ('cora', 'citeseer', 'pubmed', 'ogbn-products', 'wn18').")
    parser.add_argument("--label-name", type=str, default="label",
                        help="Label's column name in dataset.")
    parser.add_argument("--id-name", type=str, default="id",
                        help="Id's column name in dataset.")
    parser.add_argument("--node-type", type=str, default="node",
                        help="Default node type.")
    parser.add_argument("--edge-type", type=str, default="edge",
                        help="Default edge type.")
    parser.add_argument("--unique-type", type=str, default="number",
                        help="Default edge type.")
    parser.add_argument("--dropout", type=float, default=0.5,
                        help="dropout probability")
    parser.add_argument("--url", type=str, default='',
                        help="thrift url (default=''), format: 'IP:Port'")
    parser.add_argument("--cfg-file", type=str, default="/home/ezoo/suyy/Projects/ezoodb/.tmp/config/conf_ogbn.conf",
                        help="Database config file path.")
    parser.add_argument("--gpu", type=int, default=0,
                        help="gpu")
    parser.add_argument("--use-uva", type=bool, default=False,
                        help="Use uva in DGL dataloader or not")
    parser.add_argument("--lr", type=float, default=0.003,       # 1e-2
                        help="learning rate")
    parser.add_argument("--n-epochs", type=int, default=10,
                        help="number of training epochs")
    parser.add_argument("--n-hidden", type=int, default=256,    # 16
                        help="number of hidden gcn units")
    parser.add_argument("--n-layers", type=int, default=3,      # 2
                        help="number of hidden gcn layers")
    parser.add_argument("--n-classes", type=int, default=-1,
                        help="number of classes in result. -1 represents it will be calculated by the system.")
    parser.add_argument('--fan-out', type=str, default='5,10,15',     # 10,25
                        help="Sample nodes number per layer.")
    parser.add_argument('--batch-size', type=int, default=1024,
                        help="Batch size of stochastic training.")
    parser.add_argument('--one-hot', type=bool, default=False,
                        help="Should change the feature values into one hot format or not.")
    parser.add_argument('--log-every', type=int, default=20,
                        help="Logging frequence when training.")
    parser.add_argument('--eval-every', type=int, default=5,
                        help="Logging frequence when evaluation.")
    parser.add_argument("--weight-decay", type=float, default=5e-4,
                        help="Weight for L2 loss")
    parser.add_argument("--aggregator-type", type=str, default="gcn",
                        help="Aggregator type: mean/gcn/pool/lstm")
    parser.add_argument('--n-workers', type=int, default=4,     # 0
                        help="Number of sampling processes. Use 0 for no extra process.")
    parser.add_argument('--sample-gpu', action='store_true',
                        help="Perform the sampling process on the GPU. Must have 0 workers.")
    parser.add_argument('--inductive', action='store_true',
                        help="Inductive learning setting")
    parser.add_argument("--self-loop", action='store_true',
                        help="graph self-loop (default=False)")
    parser.add_argument('--data-cpu', action='store_true',
                        help="By default the script puts all node features and labels "
                             "on GPU when using it to save time for data copy. This may "
                             "be undesired if they cannot fit in GPU memory at once. "
                             "This flag disables that.")
    parser.add_argument('--gdi-ptr', type=int, default=0,
                        help="Pass to cython as a pointer to shared_ptr<void>, DO NOT USE IN CMD LINE.")
    parser.add_argument('--restore-file', type=str, default='',
                        help='''The source graph files path from which the training graph is restored,
                        e.g. "file:///home/suyy/ezoodb/data/graphs/cora_local"''')
    parser.add_argument('--restore-url', type=str, default='',
                        help='''The ezoo-server url from which the training graph is restored,
                        e.g. "ezoodb://127.0.0.1:9091:9092/cora"''')
    parser.add_argument('--task-type', type=str, default='train',
                        help="The type of the task, 'train' or 'inference'.")
    parser.add_argument('--graph-task-type', type=str, default='node',
                        help="The type of the graph task, 'node' or 'edge' or 'graph'. default edge")
    parser.add_argument('--save-model', type=bool, default=True,
                        help="Saving the result model of training into file or not.")
    parser.add_argument('--inference-node', type=int, default=0,
                        help="Saving the result model of training into file or not.")
    parser.add_argument('--exclude-list', type=str, default='',
                        help="Exclude properties when load whole graph, e.g.'predict'.")
    parser.add_argument("--use-cache", type=bool, default=False,
                        help="Use cache in ezoo loader or not")
    parser.set_defaults(self_loop=True)


    args = parser.parse_args()

    if args.gpu >= 0:
        device = th.device('cuda:%d' % args.gpu)
    else:
        device = th.device('cpu')

    dataset = EzooWholeGraphLoader(name=args.dataset, url=args.url, cfg_file=args.cfg_file, one_hot=args.one_hot, train_rate=0.2, test_rate=0.1,
                                gdi_ptr=args.gdi_ptr, restore_file=args.restore_file, restore_url=args.restore_url,
                                node_type=args.node_type, id_name=args.id_name, label_name=args.label_name)
    dgl_graph = dataset.graph
    labels = dgl_graph.ndata['label'].to(device)
    train_idx = dgl_graph.ndata['train_mask'].nonzero().squeeze()
    val_idx = dgl_graph.ndata['val_mask'].nonzero().squeeze()
    test_idx = dgl_graph.ndata['test_mask'].nonzero().squeeze()

    # load ogbn-products data
    # data = DglNodePropPredDataset(name='ogbn-products', root='dataset')
    # splitted_idx = data.get_idx_split()
    # train_idx, val_idx, test_idx = splitted_idx['train'], splitted_idx['valid'], splitted_idx['test']
    # graph, labels = data[0]
    # labels = labels[:, 0].to(device)

    nfeat = dataset.set_feature_cache(args.data, args.gpu, args.device_cache_size, args.cache_policy)
    in_feats = nfeat.shape[1]
    n_classes = (labels.max() + 1).item()

    # Create csr/coo/csc formats before launching sampling processes
    # This avoids creating certain formats in each data loader process, which saves momory and CPU.
    dgl_graph.create_formats_()
    # Pack data
    data = train_idx, val_idx, test_idx, in_feats, labels, n_classes, nfeat, dgl_graph

    test_accs = []
    for i in range(1, 11):
        print(f'\nRun {i:02d}:\n')
        test_acc = run(args, device, data)
        test_accs.append(test_acc)
    test_accs = th.tensor(test_accs)
    print('============================')
    print(f'Final Test: {test_accs.mean():.4f} ± {test_accs.std():.4f}')
