import pytest


@pytest.fixture(scope="module")
def setup_sage():

    import os
    from ezoognnexample.fullgraph.graphsage.main import main
    from easydict import EasyDict
    current_dir = os.path.dirname(os.path.abspath(__file__))
    args = EasyDict({
        "gnn_type":'ezoo-sage',
        "dataset": 'cora',
        "label_name": "label",
        "id_name": "id",
        "node_type": "node",
        "edge_type": "edge",
        "unique_type":"number",
        "dropout": 0.5,
        "url": '',
        "cfg_file":os.path.join(current_dir, '../../../resources/conf/ezoodb.conf'),
        "gpu": -1,
        "use_uva": False,
        "lr": 1e-2,
        "n_epochs": 200,
        "n_hidden":16,
        "n_layers": 2,
        "n_classes": -1,
        "fan_out":'10,25',
        "batch_size": 1000,
        "one_hot": False,
        "log_every":20,
        "eval_every": 5,
        "weight_decay": 5e-4,
        "aggregator_type":"gcn",
        "n_workers":0,
        "gdi_ptr": 0,
        "restore_file":'',
        "restore_url":"",
        "task_type":"train",
        "save_model":True,
        "inference_node": 0,
        "node_exclude_list": "",
        "edge_exclude_list":"*",
        "use_cache":False,
        "ip_config":'ip_config.txt',
        "net_type": 'socket',
        "checkpoint":'',
        "check_interval":0,
        "epoch":100,
        "submit_type":0,
        "self_loop":True,
        "sample-gpu":True,
        "inductive":True,
        "data_cpu":True
    })
    return main(args)

    

def test_sage_metric(setup_sage):
    assert setup_sage > 0.82, f"accuracy {setup_sage} is out of range"