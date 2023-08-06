import pytest


@pytest.fixture(scope="module")
def setup_mixhop():

    import os
    from ezoognnexample.fullgraph.mixhop.main import main
    from easydict import EasyDict
    current_dir = os.path.dirname(os.path.abspath(__file__))
    cfg_path = os.path.join(current_dir, '../../../resources/conf/ezoodb.conf')

    # data source params
    args = EasyDict({
        'dataset':"Cora",
        'gpu': -1, 
        # training params
        'epochs': 2000, 
        'early_stopping': 200, 
        'lr': 0.5, 
        'lamb': 5e-4, 
        'step_size': 40, 
        'gamma': 0.01, 
        # model params
        "hid_dim": 60, 
        "num_layers": 4, 
        "input_dropout": 0.7, 
        "layer_dropout": 0.9, 
        'p': [0, 1, 2],
        "cfg_file": cfg_path,
        "nni_yaml":'',
        "device":-1,
        "ezoo_fullgraph":True})

    return main(args)

def test_mixhop_metric(setup_mixhop):
    assert setup_mixhop > 0.77, f"accuracy {setup_mixhop} is out of range"