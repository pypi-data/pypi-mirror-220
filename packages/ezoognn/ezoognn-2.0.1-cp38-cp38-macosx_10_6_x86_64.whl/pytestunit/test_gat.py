import pytest


@pytest.fixture(scope="module")
def setup_gat():
    from ezoognnexample.fullgraph.gat.train import main
    from easydict import EasyDict
    import os
    current_dir = os.path.dirname(os.path.abspath(__file__))
    cfg_path = os.path.join(current_dir, '../../../resources/conf/ezoodb.conf')
    args = EasyDict({
        "dataset": 'Cora',
        "in_drop": 0.6,
        "attn_drop": 0.6,
        "cfg_file":cfg_path,
        "gpu": -1,
        "lr": 0.005,
        "epochs": 200,
        "num_heads":8,
        "num_out_heads":1,
        "num_hidden":8,
        "num_layers": 2,
        "residual":False,
        "negative_slope": 0.2,
        "fastmode":False,
        "weight_decay": 5e-4,
        "early_stop":False,
        "ezoo_fullgraph":True
    })
    return main(args)


def test_gat_metric(setup_gat):
    assert setup_gat > 0.79, f"accuracy {setup_gat} is out of range"
