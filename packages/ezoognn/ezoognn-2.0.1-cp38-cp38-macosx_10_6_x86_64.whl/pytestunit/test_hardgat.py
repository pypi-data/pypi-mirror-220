import pytest


@pytest.fixture(scope="module")
def setup_hardgat():

    import sys
    import os
    from easydict import EasyDict
    from ezoognnexample.fullgraph.hardgat.train import main
    current_dir = os.path.dirname(os.path.abspath(__file__))
    cfg_path = os.path.join(current_dir, '../../../resources/conf/ezoodb.conf')

    args = EasyDict({
        "dataset":'Cora', 
        "gpu": -1,
        "epochs": 200,
        "num_heads": 8,
        "num_out_heads": 1,
        "num_layers":1,
        "num_hidden": 8,
        "residual": False,
        "in_drop":0.6,
        "attn_drop":0.6,
        "lr":0.01,
        "weight_decay":5e-4,
        "negative_slope":0.2,
        "early_stop":False,
        "fastmode":False,
        "k":8,
        "cfg_file":cfg_path,
        "nni_yaml":'',
        "ezoo_fullgraph":True,
    })

    return main(args)
def test_hardgat_metric(setup_hardgat):
    assert setup_hardgat > 0.78, f"accuracy {setup_hardgat} is out of range"