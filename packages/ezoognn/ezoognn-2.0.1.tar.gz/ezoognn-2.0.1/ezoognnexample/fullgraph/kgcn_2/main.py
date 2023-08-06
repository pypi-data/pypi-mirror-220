# @Time   : 2021/1/28
# @Author : Tianyu Zhao
# @Email  : tyzhao@bupt.edu.cn

import argparse
import sys
sys.path.insert(0, '/opt/soft/miniconda3/envs/zz_2/lib/python3.9/site-packages')
from ezoognnexample.fullgraph.kgcn_2.KGCN.experiment import Experiment
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', '-m', default='KGCN', type=str, help='name of models')
    parser.add_argument('--task', '-t', default='recommendation', type=str, help='name of task')
    # link_prediction / node_classification
    parser.add_argument('--dataset', '-d', default='LastFM4KGCN', type=str, help='name of datasets')
    parser.add_argument('--gpu', '-g', default='-1', type=int, help='-1 means cpu')
    parser.add_argument('--use_best_config', action='store_true', help='will load utils.best_config')
    parser.add_argument('--load_from_pretrained', action='store_true', help='load model from the checkpoint')

    args = parser.parse_args()

    experiment = Experiment(model=args.model, dataset=args.dataset, task=args.task, gpu=args.gpu,
                            use_best_config=args.use_best_config)
    experiment.run()
