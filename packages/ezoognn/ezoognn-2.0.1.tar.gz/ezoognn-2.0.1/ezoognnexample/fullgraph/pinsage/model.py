import argparse

import ezoognnexample.fullgraph.pinsage.evaluation as evaluation
import ezoognnexample.fullgraph.pinsage.layers as layers
import ezoognnexample.fullgraph.pinsage.sampler as sampler_module
import torch.nn as nn
from torch.utils.data import DataLoader

from ezoognn.ezoo_graph import EzooEntityPropertyType
from ezoognnexample.fullgraph.pinsage.data_utils import *
import pandas as pd
from ezoognn.utils.data_utils import build_subgraph, build_matrix_by_indices, train_test_split_by_time
from ezoognn.loader.dataset.ezoo_data_graph import EzooShapeGraphEnum
from ezoognn.utils.feature_maker import FeatureMaker
from ezoognn.loader.dataset.ezoo_data_graph import EzooHeteroGraphDataset


class PinSAGEModel(nn.Module):
    def __init__(self, full_graph, ntype, textsets, hidden_dims, n_layers):
        super().__init__()

        self.proj = layers.LinearProjector(
            full_graph, ntype, textsets, hidden_dims
        )
        self.sage = layers.SAGENet(hidden_dims, n_layers)
        self.scorer = layers.ItemToItemScorer(full_graph, ntype)

    def forward(self, pos_graph, neg_graph, blocks):
        h_item = self.get_repr(blocks)
        pos_score = self.scorer(pos_graph, h_item)
        neg_score = self.scorer(neg_graph, h_item)
        return (neg_score - pos_score + 1).clamp(min=0)

    def get_repr(self, blocks):
        h_item = self.proj(blocks[0].srcdata)
        h_item_dst = self.proj(blocks[-1].dstdata)
        return h_item_dst + self.sage(blocks, h_item)


def train(full_g, textset, args):
    user_ntype = "user"
    item_ntype = "movie"

    device = torch.device(args.device)
    ratings = pd.DataFrame()
    ratings['user_id'] = full_g.edges(etype=('user', 'watched', 'movie'))[0]  #
    ratings['movie_id'] = full_g.edges(etype=('user', 'watched', 'movie'))[1]  #
    ratings['rating'] = full_g.edges["watched"].data["rating"]  #
    ratings['timestamp'] = full_g.edges["watched"].data["timestamp"]

    train_indices, val_indices, test_indices = train_test_split_by_time(
        ratings, "timestamp", "user_id"
    )

    train_g = build_subgraph(full_g, train_indices, "user", "movie", "watched", "watched-by")

    val_matrix = build_matrix_by_indices(full_g, val_indices, "user", "movie", "watched")

    # Assign user and movie IDs and use them as features (to learn an individual trainable
    # embedding for each entity)
    train_g.nodes[user_ntype].data["id"] = torch.arange(train_g.num_nodes(user_ntype))
    train_g.nodes[item_ntype].data["id"] = torch.arange(train_g.num_nodes(item_ntype))

    # Sampler
    batch_sampler = sampler_module.ItemToItemBatchSampler(
        train_g, user_ntype, item_ntype, args.batch_size
    )
    neighbor_sampler = sampler_module.NeighborSampler(
        train_g,
        user_ntype,
        item_ntype,
        args.random_walk_length,
        args.random_walk_restart_prob,
        args.num_random_walks,
        args.num_neighbors,
        args.num_layers,
    )
    collator = sampler_module.PinSAGECollator(
        neighbor_sampler, train_g, item_ntype, textset
    )
    dataloader = DataLoader(
        batch_sampler,
        collate_fn=collator.collate_train,
        num_workers=args.num_workers,
    )
    dataloader_test = DataLoader(
        torch.arange(train_g.num_nodes(item_ntype)),
        batch_size=args.batch_size,
        collate_fn=collator.collate_test,
        num_workers=args.num_workers,
    )
    dataloader_it = iter(dataloader)

    # Model
    model = PinSAGEModel(
        train_g, item_ntype, textset, args.hidden_dims, args.num_layers
    ).to(device)
    # Optimizer
    opt = torch.optim.Adam(model.parameters(), lr=args.lr)
    list_hit = []
    # For each batch of head-tail-negative triplets...
    for epoch_id in range(args.num_epochs):
        model.train()
        for batch_id in tqdm.trange(args.batches_per_epoch):
            pos_graph, neg_graph, blocks = next(dataloader_it)
            # Copy to GPU
            for i in range(len(blocks)):
                blocks[i] = blocks[i].to(device)
            pos_graph = pos_graph.to(device)
            neg_graph = neg_graph.to(device)

            loss = model(pos_graph, neg_graph, blocks).mean()
            opt.zero_grad()
            loss.backward()
            opt.step()
        # Evaluate
        model.eval()
        with torch.no_grad():
            item_batches = torch.arange(train_g.num_nodes(item_ntype)).split(
                args.batch_size
            )
            h_item_batches = []
            for blocks in dataloader_test:
                for i in range(len(blocks)):
                    blocks[i] = blocks[i].to(device)

                h_item_batches.append(model.get_repr(blocks))
            h_item = torch.cat(h_item_batches, 0)

            eval_res = evaluation.evaluate_nn(
                train_g, val_matrix.tocsr(), h_item, args.k, args.batch_size)
            print(eval_res)
            list_hit.append(eval_res)
    return max(list_hit)


def get_feat_mapping(need_merge_field_len: dict):
    """
    :param need_merge_field_len: 字典
    :return:
    """
    feat_mapping = {'node': {'movie': {}}, 'edge': {}}
    for k in need_merge_field_len.keys():
        if isinstance(need_merge_field_len[k], list):
            feat_mapping['node']['movie'][k] = list(need_merge_field_len[k])
        else:
            feat_mapping['node']['movie'][k] = [f"{k}{i}" for i in range(need_merge_field_len[k])]
    return feat_mapping


if __name__ == "__main__":
    # Arguments
    parser = argparse.ArgumentParser()
    # parser.add_argument("--dataset-path", type=str, default='./out_dir')
    parser.add_argument("--random-walk-length", type=int, default=2)
    parser.add_argument("--random-walk-restart-prob", type=float, default=0.5)
    parser.add_argument("--num-random-walks", type=int, default=10)
    parser.add_argument("--num-neighbors", type=int, default=3)
    parser.add_argument("--num-layers", type=int, default=2)
    parser.add_argument("--hidden-dims", type=int, default=16)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument(
        "--device", type=str, default="cuda:0"
    )  # can also be "cuda:0"
    parser.add_argument("--num-epochs", type=int, default=1)
    parser.add_argument("--batches-per-epoch", type=int, default=20000)
    parser.add_argument("--num-workers", type=int, default=0)
    parser.add_argument("--lr", type=float, default=3e-5)
    parser.add_argument("-k", type=int, default=10)
    args = parser.parse_args()
    import os

    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_file = os.path.join(current_dir, '../../../../../resources/conf/ezoodb.conf')

    fm = FeatureMaker(cfg_file=config_file)
    fm.graph_projection(dst_db_name="ml-1m-str-new", src_db_name="ml-1m", directly_use_return=True)
    # 对文本特征进行编码
    textset, need_merge_field_len = fm.text_encoder('ml-1m-str-new', 'movie', ['title'], "ml-1m-str-new")

    # 对一些特征进行数值化
    genre_columns = ['Comedy', 'Animation', "Children's", 'Adventure', 'Fantasy', 'Romance', 'Drama', 'Thriller', 'Action', 'Crime', 'Horror', 'Sci-Fi', 'Documentary', 'War', 'Musical', 'Mystery', 'Film-Noir', 'Western']
    fm.transform_func(lambda input_values: np.array([1.0 if x == "True" else 0.0 for x in input_values]),
                      src_gname="ml-1m-str-new",
                      ntype="movie",
                      src_column_names=genre_columns,
                      dst_gname="ml-1m-str-new",
                      dst_column_names=genre_columns,
                      dst_column_types=[EzooEntityPropertyType.Float32.value])
    # fm.clear_graph_store()
    need_merge_field_len['genre'] = genre_columns
    feat_mapping = get_feat_mapping(need_merge_field_len)
    node_exclude_list = ["title"]
    ezoodataset = EzooHeteroGraphDataset("ml-1m-str-new", cfg_file=config_file, node_exclude_list=node_exclude_list,
                                         feat_mapping=feat_mapping)[EzooShapeGraphEnum.WHOLE]
    full_g = ezoodataset[0]
    # 将movie的title__len加入进去
    full_g.nodes['movie'].data["title__len"] = torch.tensor([need_merge_field_len['title']] * full_g.num_nodes("movie"))
    train(full_g, textset, args)
