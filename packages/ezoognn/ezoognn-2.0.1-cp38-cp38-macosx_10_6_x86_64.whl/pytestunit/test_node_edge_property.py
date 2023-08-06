from ezoognn.loader.dataset.ezoo_data_graph import EzooShapeGraphEnum
from ezoognn.loader.dataset.ezoo_data_graph import EzooGraphDataset, EzooHeteroGraphDataset, EzooExampleDatasetEnum

# load and preprocess dataset
import numpy as np
import pytest

config_file = "../../../resources/conf/ezoodb.conf"


@pytest.fixture
def graph():
    """
    prepare graph use demo_1
    """
    ezooGraph = EzooGraphDataset(
        name=EzooExampleDatasetEnum.EDGE_PROPERTY.value, cfg_file=config_file)
    dataset = ezooGraph[EzooShapeGraphEnum.WHOLE]
    g = dataset.e_graph

    print("graph is created")
    return g


@pytest.fixture
def hetero_graph():
    """
    prepare graph use demo_1
    """
    dataset = EzooHeteroGraphDataset(
        name='modelroom1_v2', cfg_file=config_file, force_download=True)
    dataset = dataset[EzooShapeGraphEnum.WHOLE]
    g = dataset.e_graph

    print("heterograph is created")
    return g


def test_get_one_node_feature(graph):
    assert graph.ndata['node']['feat0'].all() == np.array([0, 8, 0, 0]).all()


def test_get_one_edge_feature(graph):
    assert graph.edata['edge']['feat0'].all(
    ) == np.array([1, 2, 3, 4, 5, 6, 7]).all()


def test_get_multiple_edge_feature(graph):
    assert (graph.edata['edge']['feat0', 'feat1'][0].all() == np.array([1, 2, 3, 4, 5, 6, 7]).all()) and \
           (graph.edata['edge']['feat0', 'feat1'][0].all()
            == np.array([1, 2, 3, 4, 5, 6, 7]).all())


def test_get_multiple_node_features(graph):
    assert (graph.ndata['node']['feat0', 'feat1'][0].all() == np.array([0, 8, 0, 0]).all()) and \
           (graph.ndata['node']['feat0', 'feat1'][0].all() == np.array(
               [8.5899, 1.2612, 0., 0.], dtype='float32').all())


def test_get_slice_all_node_feature(graph):
    assert list(graph.ndata['node'][:].keys()) == ['feat', 'id']


def test_get_slice_all_edge_feature(graph):
    assert list(graph.edata['edge'][:].keys()) == ['feat']


def test_get_slice_field_node_feature(graph):
    assert graph.ndata['node']["feat":["feat0", "feat1"]].all(
    ) == np.array([[0, 8], [8, 1], [0, 0], [0, 0]]).all()


def test_get_slice_field_edge_feature(graph):
    assert graph.edata['edge']["feat":["feat0", "feat1"]].all() == np.array(
        [[1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6], [7, 7]]).all()


def test_get_node_string_feature(hetero_graph):
    assert set(hetero_graph.ndata['person']['name']) == {
        'aa', 'bb', 'cc', 'dd'}
