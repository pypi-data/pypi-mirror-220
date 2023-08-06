import pytest

from ezoognn.ezoo_graph import EzooEntityPropertyType
from ezoognn.loader.dataset.ezoo_data_graph import EzooHeteroGraphDataset
from ezoognn.utils.feature_maker import FeatureMaker
from ezoognnexample.fullgraph.pinsage.model import get_feat_mapping


@pytest.fixture(scope="module")
def setup_pin():
    import os
    from ezoognnexample.fullgraph.pinsage.model import train
    from ezoognn.loader.dataset.ezoo_data_graph import EzooShapeGraphEnum
    from easydict import EasyDict
    import torch
    import numpy as np
    current_dir = os.path.dirname(os.path.abspath(__file__))
    cfg_path = os.path.join(current_dir, '../../../resources/conf/ezoodb.conf')
    args = EasyDict({
        "random_walk_length": 2,
        "random_walk_restart_prob": 0.5,
        "num_random_walks": 10,
        "num_neighbors": 3,
        "num_layers": 2,
        "hidden_dims": 16,
        "batch_size": 32,
        "device": 'cpu',
        "num_epochs": 1,
        "batches_per_epoch": 20000,
        "num_workers": 0,
        "lr": 3e-5,
        "k": 10,
        "cfg_file": cfg_path

    })
    # 先获取原始图
    EzooHeteroGraphDataset("ml-1m", cfg_file=args.cfg_file, force_download=True)[EzooShapeGraphEnum.WHOLE]
    fm = FeatureMaker(cfg_file=args.cfg_file)
    fm.graph_projection(dst_db_name="ml-1m-str-new", src_db_name="ml-1m", directly_use_return=True)
    # 对文本特征进行编码
    textset, need_merge_field_len = fm.text_encoder('ml-1m-str-new', 'movie', ['title'], "ml-1m-str-new")

    # 对一些特征进行数值化
    genre_columns = ['Comedy', 'Animation', "Children's", 'Adventure', 'Fantasy', 'Romance', 'Drama', 'Thriller',
                     'Action', 'Crime', 'Horror', 'Sci-Fi', 'Documentary', 'War', 'Musical', 'Mystery', 'Film-Noir',
                     'Western']
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
    ezoodataset = EzooHeteroGraphDataset("ml-1m-str-new", cfg_file=args.cfg_file, node_exclude_list=node_exclude_list,
                                         feat_mapping=feat_mapping)[EzooShapeGraphEnum.WHOLE]
    full_g = ezoodataset[0]
    # 将movie的title__len加入进去
    full_g.nodes['movie'].data["title__len"] = torch.tensor([need_merge_field_len['title']] * full_g.num_nodes("movie"))
    train(full_g, textset, args)
    return train(full_g, textset, args)


def test_pin_metric(setup_pin):
    assert setup_pin > 0.015, f"accuracy {setup_pin} is out of range"  # flucuate between 0.025 and 0.305
