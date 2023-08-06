import pytest


@pytest.fixture(scope="module")
def setup_gcn():
    
    import os
    from ezoognnexample.fullgraph.gcn.train import main
    from easydict import EasyDict

    current_dir = os.path.dirname(os.path.abspath(__file__))
    cfg_path = os.path.join(current_dir, '../../../resources/conf/ezoodb.conf')
    

    args = EasyDict({
    "dataset": 'cora',
    "dropout":0.5, 
    "gpu": -1, 
    "lr": 1e-2,
    "n_epochs": 200, 
    "n_hidden": 16, 
    "n_layers": 1,
    "weight_decay": 5e-4,  
    "cfg_file":cfg_path,
    "ezoo_fullgraph": True, 
    "use-cache":False,
    "self_loop": False
    
})
    return main(args)



def test_node2vec_metric(setup_gcn):

    assert setup_gcn > 0.78, f"accuracy {setup_gcn} is out of range"
