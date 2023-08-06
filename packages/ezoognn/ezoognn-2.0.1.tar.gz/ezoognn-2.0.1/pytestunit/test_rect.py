import pytest


@pytest.fixture(scope="module")
def setup_rect():

    import os
    from ezoognnexample.fullgraph.rect.main import main
    from easydict import EasyDict
    current_dir = os.path.dirname(os.path.abspath(__file__))
    cfg_path = os.path.join(current_dir, '../../../resources/conf/ezoodb.conf')

    args = EasyDict({
        "model_opt":'RECT-L',
        "dataset":'cora', 
        "dropout": 0.0,
        "gpu": -1,
        "removed_class": [0, 1, 2],
        "lr": 1e-3,
        "n_epochs": 200,
        "n_hidden":200,
        "weight_decay": 5e-4,
        "cfg_file": cfg_path,
        "nni_yaml":'',  
        "ezoo_fullgraph": True,

    })
    return main(args)
 


def test_rect_metric(setup_rect):
    assert setup_rect > 0.65, f"accuracy {setup_rect} is out of range"