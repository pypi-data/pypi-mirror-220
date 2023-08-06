import pytest
from ezoognn.loader.dataset.ezoo_data_graph import EzooShapeGraphEnum
from ezoognn.utils.feature_maker import FeatureMaker
from ezoognn.loader.dataset.ezoo_data_graph import EzooHeteroGraphDataset

@pytest.fixture(scope="function", name="graph_dataset")
def graph_dataset():
    from ezoognn.loader.dataset.ml1m_ezoo_data_graph import Ml1mEzooGraphhDataset
    import os
    from ezoognn.loader.dataset.ezoo_data_graph import EzooShapeGraphEnum

    current_dir = os.path.dirname(os.path.abspath(__file__))
    cfg_path = os.path.join(current_dir, '../../../resources/conf/ezoodb.conf')

    ezoodataset = EzooHeteroGraphDataset("ml-1m", cfg_file=cfg_path)[EzooShapeGraphEnum.WHOLE]
    return ezoodataset


def test_train_test_split_by_time(graph_dataset):
    import pandas as pd
    from ezoognn.utils.data_utils import train_test_split_by_time

    full_g = graph_dataset[0]

    ratings = pd.DataFrame()
    ratings['user_id'] = full_g.edges(etype=('user', 'watched', 'movie'))[0]  #
    ratings['movie_id'] = full_g.edges(etype=('user', 'watched', 'movie'))[1]  #
    ratings['rating'] = full_g.edges["watched"].data["rating"]  #
    ratings['timestamp'] = full_g.edges["watched"].data["timestamp"]

    train_indices, val_indices, test_indices = train_test_split_by_time(
        ratings, "timestamp", "user_id"
    )

    assert len(ratings)  == (len(train_indices) + len(val_indices) + len(test_indices))


def test_build_subgraph(graph_dataset):
    from ezoognn.utils.data_utils import build_subgraph
    import numpy as np

    full_g = graph_dataset[0]
    indices = np.arange(1, 10)
    subgraph = build_subgraph(full_g, indices, "user", "movie", "watched", "watched-by")

    assert  len(subgraph.edges[('user', 'watched', 'movie')].data['_ID']) == len(indices)


def test_build_matrix_by_indices(graph_dataset):
    import numpy as np
    from ezoognn.utils.data_utils import build_matrix_by_indices

    full_g = graph_dataset[0]
    indices = np.arange(1, 10)
    matrix = build_matrix_by_indices(full_g, indices, "user", "movie", "watched")

    assert len(matrix.toarray().nonzero()[0]) == len(indices)
