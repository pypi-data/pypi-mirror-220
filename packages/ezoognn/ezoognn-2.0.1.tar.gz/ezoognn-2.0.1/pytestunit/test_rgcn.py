import pytest


@pytest.fixture(scope="module")
def setup_rgcn():

    import sys

    
    from ezoognnexample.fullgraph.ogb.ogbn_mag.hetero_rgcn import main
    from easydict import EasyDict
    
    from easydict import EasyDict
    
    
    args = EasyDict({
    "cfg_file":"../../../resources/conf/ezoodb.conf",
    "runs":1,
    "num_workers":0,
    
})
    
    return main(args)
    

def test_rgcn_metric(setup_rgcn):
    assert setup_rgcn > 0.45, f"accuracy {setup_rgcn} is out of range"
