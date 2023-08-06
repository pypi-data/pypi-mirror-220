import pytest

# gnn-based anti-spam model 
@pytest.fixture(scope="module")
def setup_gas():

    import sys
    import os
    from ezoognnexample.fullgraph.gas.main import main
    from easydict import EasyDict
    current_dir = os.path.dirname(os.path.abspath(__file__))
    cfg_path = os.path.join(current_dir, '../../../resources/conf/ezoodb.conf')
    args = EasyDict({
        'dataset': 'pol',
        'gpu': -1,
        'e_hid_dim': 128,
        'u_hid_dim': 128,
        'v_hid_dim': 128,
        'num_layers': 2,
        'max_epoch': 70,
        'lr': 0.001,
        'dropout': 0.0,
        'weight_decay': 0.0005,
        'precision': 0.9,
        'cfg_file': cfg_path,
        'ezoo_fullgraph': True,
        'nni_yaml': ''
    })
    return main(args)

def test_vgae_metric(setup_gas):
    assert setup_gas > 0.98, f"accuracy {setup_gas} is out of range"
