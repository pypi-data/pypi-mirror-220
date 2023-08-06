import dask.dataframe as dd
import numpy as np
import scipy.sparse as ssp
import torch
import tqdm

import dgl


# This is the train-test split method most of the recommender system papers running on MovieLens
# takes.  It essentially follows the intuition of "training on the past and predict the future".
# One can also change the threshold to make validation and test set take larger proportions.
def train_test_split_by_time(df, timestamp, user):
    df["train_mask"] = np.ones((len(df),), dtype=np.bool_)
    df["val_mask"] = np.zeros((len(df),), dtype=np.bool_)
    df["test_mask"] = np.zeros((len(df),), dtype=np.bool_)
    df = dd.from_pandas(df, npartitions=10)

    def train_test_split(df):
        df = df.sort_values([timestamp])
        if df.shape[0] > 1:
            df.iloc[-1, -3] = False
            df.iloc[-1, -1] = True
        if df.shape[0] > 2:
            df.iloc[-2, -3] = False
            df.iloc[-2, -2] = True
        return df

    df = (
        df.groupby(user, group_keys=False)
            .apply(train_test_split)
            .compute(scheduler="processes")
            .sort_index()
    )
    return (
        df["train_mask"].to_numpy().nonzero()[0],
        df["val_mask"].to_numpy().nonzero()[0],
        df["test_mask"].to_numpy().nonzero()[0],
    )


def build_subgraph(g, indices, utype, itype, etype, etype_rev):
    sub_g = g.edge_subgraph(
        {etype: indices, etype_rev: indices}, relabel_nodes=False
    )

    # copy features
    for ntype in g.ntypes:
        for col, data in g.nodes[ntype].data.items():
            sub_g.nodes[ntype].data[col] = data
    for etype in g.etypes:
        for col, data in g.edges[etype].data.items():
            sub_g.edges[etype].data[col] = data[
                sub_g.edges[etype].data[dgl.EID]
            ]

    return sub_g


def build_matrix_by_indices(g, indices, utype, itype, etype):
    n_users = g.num_nodes(utype)
    n_items = g.num_nodes(itype)
    src, dst = g.find_edges(indices, etype=etype)
    src = src.numpy()
    dst = dst.numpy()
    val_matrix = ssp.coo_matrix(
        (np.ones_like(src), (src, dst)), (n_users, n_items)
    )
    return val_matrix


def linear_normalize(values):
    return (values - values.min(0, keepdims=True)) / (
            values.max(0, keepdims=True) - values.min(0, keepdims=True)
    )


def padding(array, yy, val):
    """
    :param array: torch tensor array
    :param yy: desired width
    :param val: padded value
    :return: padded array
    """
    w = array.shape[0]
    b = 0
    bb = yy - b - w
    return torch.nn.functional.pad(
        array, pad=(b, bb), mode="constant", value=val
    )