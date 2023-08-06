import pytest
import os

from ezoognnexample.fullgraph.NGCF.NGCF.main import main
from ezoognnexample.fullgraph.NGCF.NGCF.main import set_global_var
from ezoognnexample.fullgraph.NGCF.NGCF.utility.parser_ngcf import parse_args
from ezoognnexample.fullgraph.NGCF.NGCF.utility.load_data import Data
from ezoognn.loader.dataset.gowalla_ezoo_data_graph import GowallaEzooGraphDataset, EzooShapeGraphEnum


@pytest.fixture(scope="module")
def train_ngcf():
    args = parse_args()
    args.cfg_file = '../../../resources/conf/ezoodb.conf'
    args.epoch = 100
    if args.ezoo_fullgraph is not None and args.ezoo_fullgraph:
        data_generator = GowallaEzooGraphDataset(cfg_file=args.cfg_file)[
            EzooShapeGraphEnum.WHOLE]
        data_generator.batch_size = args.batch_size
    else:
        data_generator = Data(
            path=args.data_path + args.dataset, batch_size=args.batch_size
        )

    Ks = eval(args.Ks)

    ITEM_NUM = data_generator.n_items
    BATCH_SIZE = args.batch_size
    set_global_var(args, Ks, ITEM_NUM, BATCH_SIZE, data_generator)

    if not os.path.exists(args.weights_path):
        os.mkdir(args.weights_path)
    args.mess_dropout = eval(args.mess_dropout)
    args.layer_size = eval(args.layer_size)
    args.regs = eval(args.regs)
    print(args)
    return main(args)


def test_ngcf_gowalla_metric(train_ngcf):
    assert train_ngcf >= 0.080, f"Recall {train_ngcf} is out of range"
