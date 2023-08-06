import argparse
from dgl.data import CitationGraphDataset
from ogb.nodeproppred import *
from ezoognn.loader.dataset.ezoo_data_graph import EzooExampleDatasetEnum, EzooShapeGraphEnum
from ezoognn.loader.dataset.citation_ezoo_data_graph import *
from ezoognn.loader.dataset.ogb_ezoo_data_graph import OgbnEzooGraphDataset
from ezoognn.loader.dataset.ezoo_data_graph import EzooGraphDataset
from ezoognn.nni.nni_params_handler import MetricsReporter

def load_graph(args):
    name = args.dataset
    cite_graphs = ['cora', 'citeseer', 'pubmed']

    if args.cfg_file is not None and args.cfg_file != '':
        if name in cite_graphs:
            if args.dataset == 'cora':
                ezooGraph = EzooGraphDataset(cfg_file=args.cfg_file)
            elif args.dataset == 'citeseer':
                ezooGraph = CiteseerEzooGraphDataset(cfg_file=args.cfg_file)
            elif args.dataset == 'pubmed':
                ezooGraph = PubmedEzooGraphDataset(cfg_file=args.cfg_file)
            dataset = ezooGraph[EzooShapeGraphEnum.FRAME]
            graph = dataset[0]
            args.e_graph = dataset.e_graph

            nodes = graph.nodes()
            y = graph.ndata['label']
            train_mask = graph.ndata['train_mask']
            val_mask = graph.ndata['val_mask']

            nodes_train, y_train = nodes[train_mask], y[train_mask]  # train set and its labels
            nodes_val, y_val = nodes[val_mask], y[val_mask]
            eval_set = [(nodes_train, y_train), (nodes_val, y_val)] 

        elif name.startswith('ogbn'):
            # 目前仅支持ogbn-products数据集，其他数据集过大
            dataset = OgbnEzooGraphDataset(name=EzooExampleDatasetEnum.OGBN_PRODUCTS.value, cfg_file=args.cfg_file)[EzooShapeGraphEnum.FRAME]
            graph = dataset[0]
            args.e_graph = dataset.e_graph
            y = graph.ndata['label']
            split_nodes = dataset.idx_split['node_mask']
            nodes = graph.nodes()

            train_idx = split_nodes['train']
            val_idx = split_nodes['valid']

            nodes_train, y_train = nodes[train_idx], y[train_idx]
            nodes_val, y_val = nodes[val_idx], y[val_idx]
            eval_set = [(nodes_train, y_train), (nodes_val, y_val)]

        else:
            raise ValueError("Dataset name error!")
    else:
        if name in cite_graphs:
            dataset = CitationGraphDataset(name)
            graph = dataset[0]

            nodes = graph.nodes()
            y = graph.ndata['label']
            train_mask = graph.ndata['train_mask']
            val_mask = graph.ndata['test_mask']

            nodes_train, y_train = nodes[train_mask], y[train_mask]
            nodes_val, y_val = nodes[val_mask], y[val_mask]
            eval_set = [(nodes_train, y_train), (nodes_val, y_val)]

        elif name.startswith('ogbn'):

            dataset = DglNodePropPredDataset(name)
            graph, y = dataset[0]
            split_nodes = dataset.get_idx_split()
            nodes = graph.nodes()

            train_idx = split_nodes['train']
            val_idx = split_nodes['valid']

            nodes_train, y_train = nodes[train_idx], y[train_idx]
            nodes_val, y_val = nodes[val_idx], y[val_idx]
            eval_set = [(nodes_train, y_train), (nodes_val, y_val)]

        else:
            raise ValueError("Dataset name error!")
        
    return graph, eval_set


def parse_arguments():
    """
    Parse arguments
    """
    import os
    current_dir = os.path.dirname(os.path.abspath(__file__))
    print(current_dir)
    parser = argparse.ArgumentParser(description='Node2vec')
    parser.add_argument('--dataset', type=str, default='cora')
    # 'train' for training node2vec model, 'time' for testing speed of random walk
    parser.add_argument('--task', type=str, default='train')
    parser.add_argument('--runs', type=int, default=10)
    parser.add_argument('--device', type=str, default='cpu')
    parser.add_argument('--sampler', type=str, default='ezoo')
    parser.add_argument('--embedding_dim', type=int, default=128)
    parser.add_argument('--walk_length', type=int, default=50)
    parser.add_argument('--p', type=float, default=0.25)
    parser.add_argument('--q', type=float, default=4.0)
    parser.add_argument('--num_walks', type=int, default=10)
    parser.add_argument('--epochs', type=int, default=100)
    parser.add_argument('--batch_size', type=int, default=128)
    parser.add_argument("-cfg", "--cfg-file", type=str, default=os.path.join(current_dir, '../../../../../resources/conf/ezoodb.conf'),
                        help="ezoo cfg config")

    args = parser.parse_args()
    MetricsReporter.update_report_params(args)

    return args
