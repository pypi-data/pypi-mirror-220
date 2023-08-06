import argparse
import logging


def parse_args():
    import os
    current_dir = os.path.dirname(os.path.abspath(__file__))

    parser = argparse.ArgumentParser()

#    parser.add_argument('--model-dir', type=str, default='/opt/code/c++/realtime-fraud-detection-with-gnn-on-dgl-2.0.1/project/model')
    parser.add_argument('--compute-metrics', type=lambda x: (str(x).lower() in ['true', '1', 'yes']),
                        default=True, help='compute evaluation metrics after training')
    parser.add_argument('--threshold', type=float, default=0, help='threshold for making predictions, default : argmax')
    parser.add_argument('--num-gpus', type=int, default=0)
    parser.add_argument('--optimizer', type=str, default='adam')
    parser.add_argument('--lr', type=float, default=1e-2)
    parser.add_argument('--n-epochs', type=int, default=30)
    parser.add_argument('--n-hidden', type=int, default=16, help='number of hidden units')
    parser.add_argument('--n-layers', type=int, default=3, help='number of hidden layers')
    parser.add_argument('--weight-decay', type=float, default=5e-4, help='Weight for L2 loss')
    parser.add_argument('--dropout', type=float, default=0.2, help='dropout probability, for gat only features')
    parser.add_argument('--embedding-size', type=int, default=360, help="embedding size for node embedding")
    parser.add_argument("-cfg", "--cfg-file", type=str, default=os.path.join(current_dir, '../../../../../resources/conf/ezoodb.conf'),
                        help="ezoo cfg config")
    parser.add_argument("-nni-yaml", "--nni-yaml", type=str, default='',
                        help="nni_yaml")
    parser.add_argument("--ezoo-fullgraph", type=bool, default=True,
                        help="ezoo full graph")

    return parser.parse_args()

def get_logger(name):
    logger = logging.getLogger(name)
    log_format = '%(asctime)s %(levelname)s %(name)s: %(message)s'
    logging.basicConfig(format=log_format, level=logging.INFO)
    logger.setLevel(logging.INFO)
    return logger