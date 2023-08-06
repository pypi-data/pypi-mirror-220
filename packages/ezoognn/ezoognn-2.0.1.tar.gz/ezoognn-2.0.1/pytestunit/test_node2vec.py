import pytest


@pytest.fixture(scope="module")
def setup_node2vec():
    import os
    import sys
    import time
    from dgl.sampling import node2vec_random_walk
    from ezoognnexample.fullgraph.node2vec.model import Node2vecModel
    from ezoognnexample.fullgraph.node2vec.utils import load_graph
    from easydict import EasyDict
    current_dir = os.path.dirname(os.path.abspath(__file__))
    cfg_path = os.path.join(current_dir, '../../../resources/conf/ezoodb.conf')
    args = EasyDict({
        "dataset": 'cora',
        "task":'train', 
        "sampler":'ezoo',
        "runs": 10, 
        "device": 'gpu',
        "embedding_dim": 128, 
        "walk_length": 50, 
        "p": 0.25,
        "q": 4,  
        "num_walks": 10, 
        "epochs":70,
        "batch_size": 125, 
        "cfg_file":cfg_path,
    
})
    graph, eval_set = load_graph(args)
    print("Perform training node2vec model")
    
    def time_randomwalk(graph, args):
        """
        Test cost time of random walk
        """

        start_time = time.time()

        # default setting for testing
        params = {'p': 0.25,
                'q': 4,
                'walk_length': 50}

        for i in range(args.runs):
            node2vec_random_walk(graph, graph.nodes(), **params)
        end_time = time.time()
        cost_time_avg = (end_time-start_time)/args.runs
        print("Run dataset {} {} trials, mean run time: {:.3f}s".format(args.dataset, args.runs, cost_time_avg))


    def train_node2vec(graph, eval_set, args):
        """
        Train node2vec model
        """
        trainer = Node2vecModel(graph,
                                embedding_dim=args.embedding_dim,
                                walk_length=args.walk_length,
                                p=args.p,
                                q=args.q,
                                num_walks=args.num_walks,
                                eval_set=eval_set,
                                eval_steps=1,
                                device=args.device,
                                args=args)

        ret = trainer.train(epochs=args.epochs, batch_size=args.batch_size, learning_rate=0.01)
        print(ret)
        return ret
    
    return train_node2vec(graph, eval_set, args)
    



def test_node2vec_metric(setup_node2vec):

    assert setup_node2vec[0] <= 0.75, f"loss {setup_node2vec[0]} is out of range"
    assert setup_node2vec[1] >= 0.59, f"accuracy {setup_node2vec[1]} is out of range"
