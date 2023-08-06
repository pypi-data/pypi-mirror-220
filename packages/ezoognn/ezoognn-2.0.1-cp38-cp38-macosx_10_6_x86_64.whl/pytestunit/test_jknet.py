import pytest


@pytest.fixture(scope="module")
def setup_jknet():

    import os
  
    from ezoognnexample.fullgraph.jknet.main import main
    from easydict import EasyDict
    current_dir = os.path.dirname(os.path.abspath(__file__))
    cfg_path = os.path.join(current_dir, '../../../resources/conf/ezoodb.conf')
    
   
    args = EasyDict({
        "dataset":'Cora', 
        "gpu": -1,
        "run": 10,
        "epochs": 500,
        "lr": 0.05,
        "lamb": 0.0005,
        "hid_dim":32,
        "num_layers": 5,
        "mode": 'cat',
        "dropout":0.5,
        "cfg_file": cfg_path,
        "nni_yaml": "",
        "ezoo_fullgraph": True,
    })

    return main(args)

def test_jknet_metric(setup_jknet):
    assert setup_jknet > 0.8, f"accuracy {setup_jknet} is out of range"
