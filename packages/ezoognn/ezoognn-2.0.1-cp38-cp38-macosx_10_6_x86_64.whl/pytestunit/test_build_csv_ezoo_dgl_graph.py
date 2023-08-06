from ezoognn.loader.dataset.ezoo_data_graph import EzooShapeGraphEnum
from ezoognn.loader.dataset.csv_ezoo_data_graph import CsvEzooGraphDataset
from ezoognn.loader.dataset.knowledge_ezoo_data_graph import *

import os

CURR_DIR_PATH = os.path.dirname(os.path.abspath(__file__))
cfg_file = '../../../resources/conf/ezoodb.conf'
csv_path = CURR_DIR_PATH + '/test_data/mini_feature_dataset/mini_feature_dataset'


class TestCsvEzooGraphDataset: # optional
    
    ''''
    自定义mini的csv的数据集，以dgl格式为准
    '''
    @classmethod
    def setup_class(cls):
        cls.minifeature = CsvEzooGraphDataset(cfg_file=cfg_file, data_path=csv_path)[EzooShapeGraphEnum.WHOLE][0]

    @classmethod
    def teardown_class(cls):
        del cls.minifeature

    def test_nodeSize(self):
        assert(self.minifeature.number_of_nodes() == 5)
        
    def test_edgeSize(self):
        assert(self.minifeature.number_of_edges() == 10)
