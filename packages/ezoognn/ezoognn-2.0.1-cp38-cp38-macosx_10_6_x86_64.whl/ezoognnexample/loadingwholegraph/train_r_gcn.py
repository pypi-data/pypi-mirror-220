from operator import itemgetter
from itertools import groupby
import torch.nn.functional as F

import dgl
import torch as th
import numpy
import itertools
from tqdm import tqdm
import torch.nn.functional as F
from ogb.nodeproppred import Evaluator
from ezoognn.loader.loadwholegraph import EzooDGLBuiltinDataset
from ezoognn.loader.dataset.ezoo_data_graph import EzooShapeGraphEnum, EzooExampleDatasetEnum
from ezoognn.loader.dataset.ogb_ezoo_data_graph import OgbnEzooHeteroGraphDataset

from .r_gcn import *


class TrainRGCN:

    def __init__(self, args):
        self.args = args
        

    def train(self):
        # Static parameters
        hyperparameters = dict(
            num_layers=2,
            fanout=[25, 20],
            batch_size=1024,
        )
        hyperparameters.update(vars(self.args))
        print(hyperparameters)

        device = f'cuda:0' if th.cuda.is_available() else 'cpu'

        (g, labels, num_classes, split_idx,
        logger, train_loader) = self.prepare_data(hyperparameters)

        embed_layer, model = self.get_model(g, num_classes, hyperparameters)
        model = model.to(device)

        for run in range(hyperparameters['n_epochs']):
            embed_layer.reset_parameters()
            model.reset_parameters()

            # optimizer
            all_params = itertools.chain(model.parameters(), embed_layer.parameters())
            optimizer = th.optim.Adam(all_params, lr=hyperparameters['lr'])

            logger = self.train_x(g, model, embed_layer(), optimizer, train_loader, split_idx,
                        labels, logger, device, run, hyperparameters)

            logger.print_statistics(run)

        print("Final performance: ")
        logger.print_statistics()

    def train_x(self, g, model, node_embed, optimizer, train_loader, split_idx,
            labels, logger, device, run, args):
        # training loop
        print("start training...")
        category = 'paper'

        for epoch in range(args['n_epochs']):
            N_train = split_idx['node_mask']['train'][category].shape[0]
            pbar = tqdm(total=N_train)
            pbar.set_description(f'Epoch {epoch:02d}')
            model.train()

            total_loss = 0

            for input_nodes, seeds, blocks in train_loader:
                blocks = [blk.to(device) for blk in blocks]
                seeds = seeds[category]  # we only predict the nodes with type "category"
                batch_size = seeds.shape[0]

                emb = self.extract_embed(node_embed, input_nodes)
                # Add the batch's raw "paper" features
                emb.update({'paper': g.ndata['feat']['paper'][input_nodes['paper']]})
                lbl = labels[seeds]

                if th.cuda.is_available():
                    emb = {k: e.cuda() for k, e in emb.items()}
                    lbl = lbl.cuda()

                optimizer.zero_grad()
                logits = model(emb, blocks)[category]

                y_hat = logits.log_softmax(dim=-1)
                loss = F.nll_loss(y_hat, lbl)
                loss.backward()
                optimizer.step()

                total_loss += loss.item() * batch_size
                pbar.update(batch_size)

            pbar.close()
            loss = total_loss / N_train

            result = self.test(g, model, node_embed, labels, device, split_idx, args)
            logger.add_result(run, result)
            train_acc, valid_acc, test_acc = result
            print(f'Run: {run + 1:02d}, '
                f'Epoch: {epoch + 1 :02d}, '
                f'Loss: {loss:.4f}, '
                f'Train: {100 * train_acc:.2f}%, '
                f'Valid: {100 * valid_acc:.2f}%, '
                f'Test: {100 * test_acc:.2f}%')

        return logger

    def extract_embed(self, node_embed, input_nodes):
        emb = {}
        for ntype, nid in input_nodes.items():
            nid = input_nodes[ntype]
            if ntype in node_embed:
                emb[ntype] = node_embed[ntype][nid]
        return emb
    
    def prepare_data(self, args):
        import time
        start = time.time()
        # 获取异构图；graph: dgl graph object, label: torch tensor of shape (num_nodes, num_tasks)
        dataset = OgbnEzooHeteroGraphDataset(name=EzooExampleDatasetEnum.OGBN_MAG.value, cfg_file=self.args.cfg_file)
        g, _ = dataset[EzooShapeGraphEnum.WHOLE]
        split_idx = dataset.get_idx_split()
        label_dict = dataset.get_label_list()
        end = time.time()
        print('耗时', (end - start))
        labels = label_dict['nlabel']['paper'].long().flatten()

        # 从0开始，所以要 + 1
        num_classes = labels.numpy().max() + 1
        def add_reverse_hetero(g, combine_like=True):
            r"""
            Parameters
            ----------
            g : DGLGraph
                The heterogenous graph where reverse edges should be added
            combine_like : bool, optional
                Whether reverse-edges that have identical source/destination
                node types should be combined with the existing edge-type,
                rather than creating a new edge type.  Default: True.
            """
            relations = {}
            num_nodes_dict = {ntype: g.num_nodes(ntype) for ntype in g.ntypes}
            for metapath in g.canonical_etypes:
                src_ntype, rel_type, dst_ntype = metapath
                src, dst = g.all_edges(etype=rel_type)

                if src_ntype == dst_ntype and combine_like:
                    # Make edges un-directed instead of making a reverse edge type
                    relations[metapath] = (th.cat([src, dst], dim=0), th.cat([dst, src], dim=0))
                else:
                    # Original edges
                    relations[metapath] = (src, dst)

                    reverse_metapath = (dst_ntype, 'rev-' + rel_type, src_ntype)
                    relations[reverse_metapath] = (dst, src)  # Reverse edges

            new_g = dgl.heterograph(relations, num_nodes_dict=num_nodes_dict)
            # Remove duplicate edges
            new_g = dgl.to_simple(new_g, return_counts=None, writeback_mapping=False, copy_ndata=True)

            # copy_ndata:
            for ntype in g.ntypes:
                for k, v in g.nodes[ntype].data.items():
                    new_g.nodes[ntype].data[k] = v.detach().clone()

            return new_g

        g = add_reverse_hetero(g)
        print("Loaded graph: {}".format(g))

        logger = Logger(args['n_epochs'], args)

        # train sampler
        sampler = dgl.dataloading.MultiLayerNeighborSampler(args['fanout'])
        train_loader = dgl.dataloading.NodeDataLoader(
            g, split_idx['node_mask']['train'], sampler,
            batch_size=args['batch_size'], shuffle=True, num_workers=0)

        return (g, labels, num_classes, split_idx,
                logger, train_loader)

    def get_model(self, g, num_classes, args):
        embed_layer = RelGraphEmbed(g, 128, exclude=['paper'])

        model = EntityClassify(
            g, 128, args['n_hidden'], num_classes,
            num_hidden_layers=args['num_layers'] - 2,
            dropout=args['dropout'],
            use_self_loop=True,
        )

        print(embed_layer)
        print(f"Number of embedding parameters: {sum(p.numel() for p in embed_layer.parameters())}")
        print(model)
        print(f"Number of model parameters: {sum(p.numel() for p in model.parameters())}")

        return embed_layer, model

    @th.no_grad()
    def test(self, g, model, node_embed, y_true, device, split_idx, args):
        model.eval()
        category = 'paper'
        evaluator = Evaluator(name='ogbn-mag')

        sampler = dgl.dataloading.MultiLayerFullNeighborSampler(args['num_layers'])
        loader = dgl.dataloading.NodeDataLoader(
            g, {'paper': th.arange(g.num_nodes('paper'))}, sampler,
            batch_size=16384, shuffle=False, num_workers=0)

        N = y_true.size(0)
        pbar = tqdm(total=N)
        pbar.set_description(f'Full Inference')

        y_hats = list()

        for input_nodes, seeds, blocks in loader:
            blocks = [blk.to(device) for blk in blocks]
            seeds = seeds[category]  # we only predict the nodes with type "category"
            batch_size = seeds.shape[0]

            emb = self.extract_embed(node_embed, input_nodes)
            # Get the batch's raw "paper" features
            emb.update({'paper': g.ndata['feat']['paper'][input_nodes['paper']]})

            if th.cuda.is_available():
                emb = {k: e.cuda() for k, e in emb.items()}

            logits = model(emb, blocks)[category]
            y_hat = logits.log_softmax(dim=-1).argmax(dim=1, keepdims=True)
            y_hats.append(y_hat.cpu())

            pbar.update(batch_size)

        pbar.close()

        y_pred = th.cat(y_hats, dim=0)
        y_true = th.unsqueeze(y_true, 1)

        train_acc = evaluator.eval({
            'y_true': y_true[split_idx['node_mask']['train']['paper']],
            'y_pred': y_pred[split_idx['node_mask']['train']['paper']],
        })['acc']
        valid_acc = evaluator.eval({
            'y_true': y_true[split_idx['node_mask']['valid']['paper']],
            'y_pred': y_pred[split_idx['node_mask']['valid']['paper']],
        })['acc']
        test_acc = evaluator.eval({
            'y_true': y_true[split_idx['node_mask']['test']['paper']],
            'y_pred': y_pred[split_idx['node_mask']['test']['paper']],
        })['acc']

        return train_acc, valid_acc, test_acc
    

    def process(self):
            pass

    def __len__(self):
        return 1
