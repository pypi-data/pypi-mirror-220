import pytest


@pytest.fixture(scope="module")
def setup_dagnn():

    import sys
    import os
    from ezoognnexample.fullgraph.dagnn.main import main
    from easydict import EasyDict
    current_dir = os.path.dirname(os.path.abspath(__file__))
    cfg_path = os.path.join(current_dir, '../../../resources/conf/ezoodb.conf')

    args = EasyDict({
    'dataset':'Cora', 
     'gpu': -1, 
     'runs': 1, 
     'epochs': 150, 
     'early_stopping': 100,
     'lr': 0.01, 
     'lamb': 0.005,
     'k': 12, 
     'hid_dim': 64, 
     'dropout': 0.8,
     "cfg":cfg_path,
     "ezoo_fullgraph":True,
     "nni_yaml":"",
     "cfg_file":cfg_path
        
    })
    

    return main(args)
def test_dagnn_metric(setup_dagnn):
    assert setup_dagnn > 0.82, f"accuracy {setup_dagnn} is out of range"