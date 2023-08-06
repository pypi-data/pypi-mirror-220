"""test module for feature_maker in pytest """
from multiprocessing.context import ForkContext
import os
import sys
from pathlib import Path
from typing import *
from unittest import case
import pytest
from ezoognn.ezoo_graph import EzooEntityPropertyType
from ezoognn.utils.feature_maker import FeatureMaker

import numpy as np
from ezoognn.ezoocall import SearchDirectionType, HandlerGenerateType
# from ezoognn.utils.graph_store import GraphStore
from ezoognn.loader.dataset.ezoo_data_graph import EzooShapeGraphEnum
from ezoognn.loader.dataset.ezoo_data_graph import EzooGraphDataset, EzooExampleDatasetEnum

from ezoognn.utils.feature_maker import FeatureMaker

from ezoognn.utils.feature_transform import call_thridty_transform
from ezoognn.utils.feature_transform import Ops


CURR_DIR_PATH = Path(os.path.dirname(os.path.abspath(__file__)))
PARENT_DIR = CURR_DIR_PATH.parent.absolute()
sys.path.append(PARENT_DIR)

config_file = '../../../resources/conf/ezoodb.conf'
real_restore_url = 'file:///tmp/ezoodb/data/graphs/cora_v2'
fake_restore_url = 'file:///tmp/ezoodb/data/graphs/cora_v2_not_exist'
real_schema_path = './test_data/cora_v2/schema.txt'
fake_schema_path = './test_data/cora_v2/schema_not_exist.txt'

src_db_name = 'cora_v2'
dst_db_name = 'cora_v2_new_schema'


def generate_db():
    EzooGraphDataset(name=src_db_name, cfg_file=config_file,
                     force_download=True)


@pytest.fixture
def fm():
    """
    FeatureMaker is defined
    """
    print("fm is called")
    generate_db()
    fm = FeatureMaker(cfg_file=config_file)
    fm.clear_graph_store()
    return fm


# @pytest.fixture(scope="function", name="remote_restore")
# def remote_restore():
#     """
#     graph_projection has been created
#     """
#     print("graph is created")
#     FeatMaker = FeatureMaker(cfg_file=config_file)
#     FeatMaker.clear_graph_store()
#     FeatMaker.load_graph('test', init_type=HandlerGenerateType.OnlyDBM)
#     graph_pro = FeatMaker.graph_projection(
#         dst_db_name, restore_url='ezoodb://58.17.128.10:9091:9092/cora')
#     return (FeatMaker, graph_pro)

@pytest.fixture(scope="function", name="graph")
def graph():
    """
    graph_projection has been created
    """
    print("graph is created")
    FeatMaker = FeatureMaker(cfg_file=config_file)
    FeatMaker.clear_graph_store()
    graph_pro = FeatMaker.graph_projection(dst_db_name, src_db_name=src_db_name, del_props={'node': ['feat1', 'feat3']},
                                           add_props={'node': {'feat1446': EzooEntityPropertyType.Float32,
                                                               'feat1450': EzooEntityPropertyType.Float32}})
    return (FeatMaker, graph_pro)


def test_func_arithmetic_scalar(graph):
    graph[0].transform_func(call_thridty_transform, dst_db_name, 'node', [['label']], dst_db_name, [['feat1446']],
                            op=Ops.arithmetic_scalar(2, '+'))
    assert (graph[1].ndata['node']['feat1446'][:2] ==
            graph[1].ndata['node']['label'][:2] + 2).all()

    graph[0].transform_func(call_thridty_transform, dst_db_name, 'node', [['label']], dst_db_name, [['feat1446']],
                            op=Ops.arithmetic_scalar(2, '*'))
    assert (graph[1].ndata['node']['feat1446'][:2] ==
            graph[1].ndata['node']['label'][:2] * 2).all()

    graph[0].transform_func(call_thridty_transform, dst_db_name, 'node', [['label']], dst_db_name, [['feat1446']],
                            op=Ops.arithmetic_scalar(2, '-'))
    assert (graph[1].ndata['node']['feat1446'][:2] ==
            graph[1].ndata['node']['label'][:2] - 2).all()

    graph[0].transform_func(call_thridty_transform, dst_db_name, 'node', [['label']], dst_db_name, [['feat1446']],
                            op=Ops.arithmetic_scalar(2, '/'))
    assert (graph[1].ndata['node']['feat1446'][:2] ==
            graph[1].ndata['node']['label'][:2] / 2).all()

    graph[0].transform_func(call_thridty_transform, dst_db_name, 'node', [['label']], dst_db_name, [['feat1446']],
                            op=Ops.arithmetic_scalar(2, '-', True))
    assert (graph[1].ndata['node']['feat1446'][:2] ==
            2 - graph[1].ndata['node']['label'][:2]).all()

    graph[0].transform_func(call_thridty_transform, dst_db_name, 'node', [['label']], dst_db_name, [['feat1446']],
                            op=Ops.arithmetic_scalar(2, '/', True))
    assert (np.around(graph[1].ndata['node']['feat1446'][:2], 2).astype(np.float32)
            == np.around(2 / graph[1].ndata['node']['label'][:2], 2).astype(np.float32)).all()


def test_func_arithmetic(graph):
    graph[0].transform_func(call_thridty_transform, dst_db_name, 'node', [['label', 'id']], dst_db_name, [['feat1446']],
                            op=Ops.arithmetic('+'))


def test_func_add_numeric(graph):
    from ezoognn.utils.feature_custom import call_udf_transform

    graph[0].transform_func(call_udf_transform, dst_db_name, 'node', [['label', 'label']], dst_db_name, [['feat1446']],
                            op=Ops.add_numeric(),
                            udf_file=os.path.join(
                                CURR_DIR_PATH, '../ezoognn/utils/feature_transform.py'),
                            cls_name='ThridtyTransformUdf')
    assert (graph[1].ndata['node']['feat1446'][:2] ==
            graph[1].ndata['node']['label'][:2] * 2).all()


def test_func_divide_by(graph):
    # test divide_by(2)
    graph[0].transform_func(call_thridty_transform, dst_db_name, 'node', ['label'], dst_db_name, ['feat1446'],
                            op=Ops.divide_by(2))
    assert (graph[1].ndata['node']['feat1446'][:2] == np.array(
        [np.float32(0.666667), np.float32(0.5)])).all()
    # 3,4


def test_func_add_numeric_scalar(graph):
    # test AddNumericScalar
    graph[0].transform_func(call_thridty_transform, dst_db_name, 'node', ['label'], dst_db_name, ['feat1446'],
                            op=Ops.add_numeric_scalar(2))
    assert (graph[1].ndata['node']['feat1446'][:2] ==
            np.array([np.float32(5), np.float32(6)])).all()


def test_func_divide_numeric_scalar(graph):
    # test DivideNumericScalar
    graph[0].transform_func(call_thridty_transform, dst_db_name, 'node', ['label'], dst_db_name, ['feat1446'],
                            op=Ops.divide_numeric_scalar(2))
    assert (graph[1].ndata['node']['feat1446'][:2] ==
            np.array([np.float32(1.5), np.float32(2)])).all()


def test_func_euqal(graph):
    graph[0].transform_func(call_thridty_transform, dst_db_name, 'node', [['label', 'label']], dst_db_name, [['feat1446']],
                            op=Ops.equal())
    assert (graph[1].ndata['node']['feat1446']
            [:2] == np.array([True, True])).all()


def test_func_equal_scalar(graph):
    graph[0].transform_func(call_thridty_transform, dst_db_name, 'node', ['label'], dst_db_name, ['feat1446'],
                            op=Ops.equal_scalar(3))
    assert (graph[1].ndata['node']['feat1446']
            [:2] == np.array([True, False])).all()


def test_func_greater_than(graph):
    graph[0].transform_func(call_thridty_transform, dst_db_name, 'node', [['label', 'label']], dst_db_name, [['feat1446']],
                            op=Ops.greater_than())
    assert (graph[1].ndata['node']['feat1446'][:2]
            == np.array([False, False])).all()


def test_func_greater_than_equal_to(graph):
    graph[0].transform_func(call_thridty_transform, dst_db_name, 'node', [['label', 'label']], dst_db_name, [['feat1446']],
                            op=Ops.greater_than_equal_to())
    assert (graph[1].ndata['node']['feat1446']
            [:2] == np.array([True, True])).all()


def test_func_greater_than_equal_to_scalar(graph):
    graph[0].transform_func(call_thridty_transform, dst_db_name, 'node', ['label'], dst_db_name, ['feat1446'],
                            op=Ops.greater_than_equal_to_scalar(3))
    assert (graph[1].ndata['node']['feat1446']
            [:2] == np.array([True, True])).all()


def test_func_greater_than_scalar(graph):
    graph[0].transform_func(call_thridty_transform, dst_db_name, 'node', ['label'], dst_db_name, ['feat1446'],
                            op=Ops.greater_than_scalar(3))
    assert (graph[1].ndata['node']['feat1446']
            [:2] == np.array([False, True])).all()


def test_func_less_than(graph):
    graph[0].transform_func(call_thridty_transform, dst_db_name, 'node', [['label', 'label']], dst_db_name, [['feat1446']],
                            op=Ops.less_than())
    assert (graph[1].ndata['node']['feat1446'][:2]
            == np.array([False, False])).all()


def test_func_less_than_equal_to(graph):
    graph[0].transform_func(call_thridty_transform, dst_db_name, 'node', [['label', 'label']], dst_db_name, [['feat1446']],
                            op=Ops.less_than_equal_to())
    assert (graph[1].ndata['node']['feat1446']
            [:2] == np.array([True, True])).all()


def test_func_less_than_equal_to_scalar(graph):
    graph[0].transform_func(call_thridty_transform, dst_db_name, 'node', ['label'], dst_db_name, ['feat1446'],
                            op=Ops.less_than_equal_to_scalar(3))
    assert (graph[1].ndata['node']['feat1446']
            [:2] == np.array([True, False])).all()


def test_func_less_than_scalar(graph):
    graph[0].transform_func(call_thridty_transform, dst_db_name, 'node', ['label'], dst_db_name, ['feat1446'],
                            op=Ops.less_than_scalar(3))
    assert (graph[1].ndata['node']['feat1446'][:2]
            == np.array([False, False])).all()


def test_func_multiply_numeric_scalar(graph):
    graph[0].transform_func(call_thridty_transform, dst_db_name, 'node', ['label'], dst_db_name, ['feat1446'],
                            op=Ops.multiply_numeric_scalar(2))
    assert (graph[1].ndata['node']['feat1446'][:2] ==
            np.array([np.float32(6), np.float32(8)])).all()


def test_func_not_equal(graph):
    graph[0].transform_func(call_thridty_transform, dst_db_name, 'node', [['label', 'label']], dst_db_name, [['feat1446']],
                            op=Ops.not_equal())
    assert (graph[1].ndata['node']['feat1446'][:2]
            == np.array([False, False])).all()


def test_func_not_equal_scalar(graph):
    # test NotEqualScalar
    graph[0].transform_func(call_thridty_transform, dst_db_name, 'node', ['label'], dst_db_name, ['feat1446'],
                            op=Ops.not_equal_scalar(3))
    assert (graph[1].ndata['node']['feat1446']
            [:2] == np.array([False, True])).all()


def test_func_scalar_subtract_numeric_feature(graph):
    # test ScalarSubtractNumericFeature
    graph[0].transform_func(call_thridty_transform, dst_db_name, 'node', ['label'], dst_db_name, ['feat1446'],
                            op=Ops.scalar_subtract_numeric_feature(2))
    assert (graph[1].ndata['node']['feat1446'][:2] ==
            np.array([np.float32(-1), np.float32(-2)])).all()


def test_func_not_equal(graph):
    graph[0].transform_func(call_thridty_transform, dst_db_name, 'node', [['label', 'label']], dst_db_name, [['feat1446']],
                            op=Ops.not_equal())
    assert (graph[1].ndata['node']['feat1446'][:2]
            == np.array([False, False])).all()


def test_func_subtract_numeric_scalar(graph):
    graph[0].transform_func(call_thridty_transform, dst_db_name, 'node', ['label'], dst_db_name, ['feat1446'],
                            op=Ops.subtract_numeric_scalar(2))
    assert (graph[1].ndata['node']['feat1446'][:2] ==
            np.array([np.float32(1), np.float32(2)])).all()

##################################### culmulative calculation##########################
# # test CumCount


def test_func_cum_count(graph):
    graph[0].transform_func(call_thridty_transform, dst_db_name, 'node', ['label'], dst_db_name, ['feat1446'],
                            op=Ops.cum_count())
    assert (graph[1].ndata['node']['feat1446'][:2] ==
            np.array([np.float32(1), np.float32(2)])).all()


def test_func_cum_sum(graph):
    graph[0].transform_func(call_thridty_transform, dst_db_name, 'node', ['label'], dst_db_name, ['feat1446'],
                            op=Ops.cum_sum())
    assert (graph[1].ndata['node']['feat1446'][:2] ==
            np.array([np.float32(3), np.float32(7)])).all()


def test_func_cum_mean(graph):
    graph[0].transform_func(call_thridty_transform, dst_db_name, 'node', ['label'], dst_db_name, ['feat1446'],
                            op=Ops.cum_mean())
    assert (graph[1].ndata['node']['feat1446'][:2] ==
            np.array([np.float32(3), np.float32(3.5)])).all()


def test_func_cum_min(graph):
    graph[0].transform_func(call_thridty_transform, dst_db_name, 'node', ['label'], dst_db_name, ['feat1446'],
                            op=Ops.cum_min())
    assert (graph[1].ndata['node']['feat1446'][:2] ==
            np.array([np.float32(3), np.float32(3)])).all()


def test_func_cum_max(graph):
    graph[0].transform_func(call_thridty_transform, dst_db_name, 'node', ['label'], dst_db_name, ['feat1446'],
                            op=Ops.cum_max())
    assert (graph[1].ndata['node']['feat1446'][:2] ==
            np.array([np.float32(3), np.float32(4)])).all()


# ============================boolean==================================

def test_func_is_in(graph):
    graph[0].transform_func(call_thridty_transform, dst_db_name, 'node', ['label'], dst_db_name, ['feat1446'],
                            op=Ops.is_in([1, 2]))
    assert (graph[1].ndata['node']['feat1446'][:2]
            == np.array([False, False])).all()


def test_thirdty_func_from_sk_pca(graph):
    from ezoognn.utils.feature_transform import call_thridty_transform
    from ezoognn.utils.feature_transform import Ops
    params = {'n_components': 2}

    graph[0].transform_func(call_thridty_transform, dst_db_name, 'node', [['label', 'label',  'label']], dst_db_name, [['pca']],
                            op=Ops.pca(**params))
    assert graph[1].ndata['node']['pca_0'] is not None and graph[1].ndata['node']['pca_1'] is not None


def test_thirdty_func_from_sk_variance_threshold(graph):
    from ezoognn.utils.feature_transform import call_thridty_transform
    from ezoognn.utils.feature_transform import Ops

    # remove features that are not important,transform_func need some adjustment
    graph[0].transform_func(call_thridty_transform, dst_db_name, 'node', [['label', 'label',  'label']], dst_db_name, [['vs']],
                            op=Ops.variance_threshold(threshold=1))
    assert graph[1].ndata['node']['vs_0'] is not None and graph[1].ndata['node']['vs_1'] is not None


def test_thirdty_func_from_sk_standard(graph):
    from ezoognn.utils.feature_transform import call_thridty_transform
    from ezoognn.utils.feature_transform import Ops
    import math

    graph[0].transform_func(call_thridty_transform, dst_db_name, 'node', ['label'], dst_db_name, ['feat1446'],
                            op=Ops.standard_scaler())
    assert math.isclose(graph[1].ndata['node']
                        ['feat1446'].min(), -1.710713, abs_tol=0.00005)


def test_thirdty_func_from_sk_max_min(graph):
    from ezoognn.utils.feature_transform import call_thridty_transform
    from ezoognn.utils.feature_transform import Ops
    import math

    graph[0].transform_func(call_thridty_transform, dst_db_name, 'node', ['label'], dst_db_name, ['feat1446'],
                            op=Ops.max_min_scalar())
    assert math.isclose(graph[1].ndata['node']
                        ['feat1446'].min(), 0.0, abs_tol=0.00005)
    assert math.isclose(graph[1].ndata['node']
                        ['feat1446'].max(), 1.0, abs_tol=0.00005)


def test_thirdty_func_from_sk_robust(graph):
    from ezoognn.utils.feature_transform import call_thridty_transform
    from ezoognn.utils.feature_transform import Ops
    import math

    graph[0].transform_func(call_thridty_transform, dst_db_name, 'node', ['label'], dst_db_name, ['feat1446'],
                            op=Ops.robust_scaler())
    assert math.isclose(graph[1].ndata['node']
                        ['feat1446'].min(), -2.023469, abs_tol=0.00005)


def test_thirdty_func_from_sk_kbins(graph):
    from ezoognn.utils.feature_transform import call_thridty_transform
    from ezoognn.utils.feature_transform import Ops
    import math

    graph[0].transform_func(call_thridty_transform, dst_db_name, 'node', ['label'], dst_db_name, ['feat1446'],
                            op=Ops.kbins_discretizer())
    assert math.isclose(graph[1].ndata['node']
                        ['feat1446'].min(), 0.0, abs_tol=0.00005)


def test_thirdty_func_from_norm(graph):
    from ezoognn.utils.feature_transform import call_thridty_transform
    from ezoognn.utils.feature_transform import Ops
    import math

    graph[0].transform_func(call_thridty_transform, dst_db_name, 'node', ['label'], dst_db_name, ['feat1446'],
                            op=Ops.norm())
    assert math.isclose(graph[1].ndata['node']
                        ['feat1446'].min(), 0.0, abs_tol=0.00005)


# pytest test_feature_maker.py::test_thirdty_func
def test_thirdty_func(graph):
    from ezoognn.utils.feature_maker import FeatureMaker
    """
    test transform function
    """
    from ezoognn.utils.feature_transform import call_thridty_transform
    from ezoognn.utils.feature_transform import Ops

    # ========================================================================================================
    graph[0].transform_func(call_thridty_transform, dst_db_name, 'node', ['feat0'], dst_db_name, ['feat1446'],
                            op=Ops.divide_by(2))
    graph[0].transform_func(call_thridty_transform, dst_db_name, 'node', ['feat0'], dst_db_name, ['feat1446'],
                            op=Ops.add_numeric_scalar(2))
    # graph[0].transform_func(call_thridty_transform, dst_db_name, 'node', ['feat0'], dst_db_name, ['feat1446'], op=Ops.add(2))


def test_copy_graph(fm):
    graph_copy = fm.copy_graph(dst_db_name, src_db_name)
    ezooGraph = EzooGraphDataset(
        name=src_db_name, cfg_file=config_file)
    dataset = ezooGraph[EzooShapeGraphEnum.WHOLE]
    g = dataset.e_graph
    assert sum(graph_copy.ndata['node']['feat0'] == g.ndata['node']
               ['feat0']) == graph_copy.ndata['node']['feat0'].size


def test_graph_projection_src_db_not_exist(fm):
    """case 1: test when destination db name does not exist; should fail and throw exception"""
    graph_pro = fm.graph_projection(
        dst_db_name, src_db_name='database_not_exist')
    assert graph_pro == None


def test_graph_projection_given_src_db_name(fm):
    """case 2: source db is specified """
    graph_pro = fm.graph_projection(dst_db_name, src_db_name=src_db_name)
    assert len(graph_pro.describe()) == 58079


# 这两个都要启动ezoo-server
def test_graph_projection_url_not_exist(fm):
    """"case 3: test when restore_url given but does not exist; should fail and throw exception"""
    graph_pro = fm.graph_projection(dst_db_name, restore_url=fake_restore_url)
    assert graph_pro == None


def test_graph_projection_given_restore_url(fm):
    """case 4: test when restore_url is correctly specified
        ps: need to start the ezoo-server and zookeeper"""
    graph_pro = fm.graph_projection(dst_db_name, restore_url=real_restore_url)
    print('=============', graph_pro)
    assert graph_pro.ndata['node']['feat0'].size == 2708


def test_graph_projection_schema_not_exist(fm):
    """case 5: schema path does not exist"""
    graph_pro = fm.graph_projection(dst_db_name, schema_path=fake_schema_path)
    assert graph_pro == None


def test_graph_projection_given_schema(fm):
    """case 6:test when schema is given """
    graph_pro = fm.graph_projection(dst_db_name, src_db_name=src_db_name)
    graph_pro = fm.graph_projection(dst_db_name, schema_path=real_schema_path)
    assert len(graph_pro.describe()) == 58079


def test_graph_projection_del_prop(fm):
    """case 7: test when some features has been deleted"""
    graph_pro = fm.graph_projection(dst_db_name, src_db_name=src_db_name,
                                    del_props={'node': ['feat1', 'feat3']})
    assert len(graph_pro.describe()) == 58003


def test_graph_projection_add_prop(fm):
    """case 8: test when some features has been added"""
    graph_pro = fm.graph_projection(dst_db_name, src_db_name=src_db_name,
                                    add_props={'node': {'feat1449': EzooEntityPropertyType.Float32,
                                                        'feat1450': EzooEntityPropertyType.Float32}})
    assert len(graph_pro.describe()) == 58161


def test_down_sampling(fm):
    from ezoognn.utils.selection_function import DownSamplingUdf

    """Down sampling with one hop neighbors and the nodes of the second frequency rank reserved """
    fm.data_sampling(src_db_name, op=DownSamplingUdf(), dst_gname=dst_db_name, ntype='node', col_name='feat0', hop=1,
                     search_direction=SearchDirectionType.InOut, reserved_rank=[1], from_rank=0, target_rank=1, sampling_rate=1)
    graph_ds = EzooGraphDataset(name=dst_db_name, cfg_file=config_file,
                                node_type='node', train_rate=0.2)[EzooShapeGraphEnum.WHOLE].e_graph
    src_graph = EzooGraphDataset(name=src_db_name, cfg_file=config_file,
                                 node_type='node', train_rate=0.2)[EzooShapeGraphEnum.WHOLE].e_graph
    assert len(graph_ds.ndata['node']['feat0']) < len(
        src_graph.ndata['node']['feat0'])

    # """Down sampling with zero hop neighbors, only reserve the nodes of the first frequency rank """
    fm.clear_graph_store()
    fm.data_sampling(src_db_name, op=DownSamplingUdf(), dst_gname=dst_db_name, ntype='node', col_name='feat0', hop=0,
                     search_direction=SearchDirectionType.InOut, reserved_rank=[], from_rank=0, target_rank=1, sampling_rate=1)
    graph_ds = EzooGraphDataset(name=dst_db_name, cfg_file=config_file,
                                node_type='node', train_rate=0.2)[EzooShapeGraphEnum.WHOLE].e_graph
    assert len(graph_ds.ndata['node']['feat0']) == 4


# =====================value_copy===================
def test_node_value_copy(graph):
    """
    test s
    """

    graph[0].node_value_copy(src_db_name, 'node', [
        'feat0'], dst_db_name, ['feat1446'])
    assert (graph[1].ndata['node']['feat1446'][:2] ==
            np.array([np.float32(0), np.float32(0)])).all()


# ======================some data transformation/normalizaiton/min/max
def test_transform_func(graph):
    """
    test transform function
    """

    def func(data):
        return data * 2 + 1

    graph[0].transform_func(func, dst_db_name, 'node', [
        'feat0'], dst_db_name, ['feat1446'])
    assert (graph[1].ndata['node']['feat1446'][:2] ==
            np.array([np.float32(1), np.float32(1)])).all()


def test_min_max_scaler(graph):
    graph[0].min_max_scaler(dst_db_name, 'node', [
        'feat0'], dst_db_name, ['feat1446'])
    assert (graph[1].ndata['node']['feat1446'][:2] ==
            np.array([np.float32(0), np.float32(0)])).all()


def test_standard_scaler(graph):
    graph[0].standard_scaler(dst_db_name, 'node', [
        'feat0'], dst_db_name, ['feat1446'])
    assert (graph[1].ndata['node']['feat1446'][:2] == np.array(
        [np.float32(-0.076643), np.float32(-0.076643)])).all()


# ================ binning==================


def test_digitize(graph):
    bins = np.linspace(0, 1, 11)
    graph[0].digitize(bins, dst_db_name, 'node', [
        'feat0'], dst_db_name, ['feat1446'])
    assert (graph[1].ndata['node']['feat1446'][:2] ==
            np.array([np.float32(1), np.float32(1)])).all()


# =======================dummy/one-hot==================


def test_dummies(graph):
    graph[0].dummies(src_db_name, 'node', ['feat2'], dst_db_name)
    print('----------------', graph[1].describe()[-152:-128])
    # assert graph[1].describe()[-152:-128] == 'feat2_0.1111111119389534'


# =======================degree==================


def test_set_degree_prop(graph):
    graph[0].set_degree_prop(src_db_name, dst_db_name,
                             SearchDirectionType.InOut, 'node', 'feat1446')
    assert (graph[1].ndata['node']['feat1446'][:2] ==
            np.array([np.float32(6), np.float32(6)])).all()


# ========================mining==================
# case 1
def test_set_mining_score_prop_pagerank(graph):
    graph[0].set_mining_score_prop(
        dst_db_name, 'pagerank', dst_db_name, 'node', 'feat1446')
    assert (graph[1].ndata['node']['feat1446'][:2] == np.array(
        [np.float32(0.907292), np.float32(1.040543)])).all()


# case2
def test_set_mining_score_prop_wcc(graph):
    graph[0].set_mining_score_prop(
        dst_db_name, 'wcc', dst_db_name, 'node', 'feat1446')
    com_num = graph[1].wcc()[1]
    assert 73 <= com_num <= 83


# case3
def test_set_mining_score_prop_scc(graph):
    graph[0].set_mining_score_prop(
        dst_db_name, 'scc', dst_db_name, 'node', 'feat1446')
    com_num = graph[1].scc()[1]
    assert 73 <= com_num <= 83


# case4
def test_set_mining_score_prop_louvian(graph):
    graph[0].set_mining_score_prop(
        dst_db_name, 'louvain', dst_db_name, 'node', 'feat1446')
    # _, com_louvain = graph[0].com_louvain(graph[0].g_store.get_graph(g_name=dst_db_name), edge_type='', prop_name='', max_iter=10, max_levels=10, thread_num=1)
    com_num = graph[1].louvain('', '', 10, 10, 1)[1]
    assert 100 <= com_num <= 110


# case5
def test_set_mining_score_prop_lpa(graph):
    graph[0].set_mining_score_prop(
        dst_db_name, 'lpa', dst_db_name, 'node', 'feat1446')
    assert 660 <= np.count_nonzero(
        np.unique(graph[1].ndata['node']['feat1446'])) <= 720


# case6
def test_set_mining_score_prop_kcore(graph):
    graph[0].set_mining_score_prop(
        dst_db_name, 'k_core', dst_db_name, 'node', 'feat1446')
    assert (graph[1].ndata['node']['feat1446'][:2] ==
            np.array([np.float32(0), np.float32(0)])).all()
