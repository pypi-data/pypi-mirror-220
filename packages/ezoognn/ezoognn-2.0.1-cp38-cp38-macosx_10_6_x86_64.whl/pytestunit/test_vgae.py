import pytest


@pytest.fixture(scope="module")
def setup_vgae():
    import sys 
    import os
    from ezoognnexample.fullgraph.vgae.train import dgl_main
    from easydict import EasyDict
    current_dir = os.path.dirname(os.path.abspath(__file__))
    cfg_path = os.path.join(current_dir, '../../../resources/conf/ezoodb.conf')
    args = EasyDict(
    {
    'learning_rate': 0.01,
    'epochs': 200,
    'hidden1': 32,
    'hidden2': 16,
    'datasrc': 'dgl',
    'dataset': 'cora',
    'gpu_id': 0,
    'cfg_file': cfg_path,
    'nni_yaml': '',
    'ezoo_fullgraph': True
})
    
    return dgl_main(args)




def test_vgae_metric(setup_vgae):
    assert setup_vgae > 0.85, f"accuracy {setup_vgae} is out of range"