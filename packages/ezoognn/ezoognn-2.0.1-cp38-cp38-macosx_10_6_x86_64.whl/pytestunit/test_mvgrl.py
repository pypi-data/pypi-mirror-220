import pytest


@pytest.fixture(scope="module")
def setup_mvgrl():

    import os
    from ezoognnexample.fullgraph.mvgrl.node.main import main
    from easydict import EasyDict
    import torch as th
    current_dir = os.path.dirname(os.path.abspath(__file__))
    cfg_path =  os.path.join(current_dir, '../../../resources/conf/ezoodb.conf')
    args = EasyDict({
            "dataname":'cora',
            "gpu":-1, 
            "epochs": 500,
            "patience": 20,
            "lr1": 0.001,
            "lr2": 0.01,
            "wd1": 0,
            "wd2":0,
            "epsilon": 0.01,
            "cfg_file": cfg_path,
            "nni_yaml":'',  
            "ezoo-fullgraph": True,
            "hid_dim":512,
            "ezoo_fullgraph":True
        

            })
    if args.gpu != -1 and th.cuda.is_available():
        args.device = 'cuda:{}'.format(args.gpu)
    else:
        args.device = 'cpu'
    return main(args)

def test_mvgrl_metric(setup_mvgrl):
    assert setup_mvgrl > 81.0, f"accuracy {setup_mvgrl} is out of range"