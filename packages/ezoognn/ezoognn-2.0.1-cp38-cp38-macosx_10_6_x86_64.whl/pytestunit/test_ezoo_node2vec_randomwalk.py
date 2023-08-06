from dgl.sampling import node2vec_random_walk
from ezoognn.loader.dataset.ogb_ezoo_data_graph import OgbnEzooGraphDataset
from ezoognn.loader.dataset.ezoo_data_graph import EzooShapeGraphEnum
from ezoognn.sampler.sampling import node2vec_random_walk as ezoo_node2vec_random_walk

global cfg_file
cfg_file = '../../../resources/conf/ezoodb.conf'


class TestOgbnProductsNode2vecRandomWalk:

    @classmethod
    def setup_class(self):
        self.dataset = OgbnEzooGraphDataset(cfg_file=cfg_file)[EzooShapeGraphEnum.FRAME]
        self.dgl_graph = self.dataset[0]
        self.e_graph = self.dataset.e_graph
        self.p = 0.5
        self.q = 4
        self.walk_length = 50
        self.seeds = [726333, 2090402,  860507, 1865974,  384087, 2160694, 1047135, 1548218, 2400013,
                      372690, 2276251,  235116,  630256, 1778186,  119778, 2093165, 1797662, 1676289,
                      1533004,  595020, 1551954,  171893,  347126,   61590,  479196, 1590934, 2225387,
                      486063, 1475243, 1405451, 2234674, 2147540, 1981749,  477066,  243102,  955837,
                      329183,  972102, 1003320,  953417,  681856, 1075119, 1707098, 1007070, 1636960,
                      95389,  676988, 2372525, 1411945, 1370290, 2277726, 1170097,  322198,  107566,
                      187560, 1005668, 1303451, 1307347, 1507365,  897317, 1985507, 1592937, 1121160,
                      592636,  461565, 1820870,  323957,  195085,  872947, 1126735,  761110, 1656601,
                      1381461,  646900, 1477138, 1511149, 1118318, 2279311, 1003116,   14891, 1759970,
                      967734,  890471,  985725, 2318556, 2001983, 1256019,  550381,  153633,  852951,
                      463105,  723437,  188590,  234679,  989782, 1910070,  217454, 1961893,  385620,
                      1245074, 2125388,  166230, 2377499,  707854, 1494195, 1423540,  434633,  221333,
                      1447221, 1093447, 2270406, 1972199,  882371,  262963, 1171131, 1043012, 1679960,
                      1749590,  305300, 1325515,  295955,  263977, 1428107,  803786, 1714967,   15138,
                      912415, 1468123,  726333, 2090402,  860507, 1865974,  384087, 2160694, 1047135,
                      1548218, 2400013,  372690, 2276251,  235116,  630256, 1778186,  119778, 2093165,
                      1797662, 1676289, 1533004,  595020, 1551954,  171893,  347126,   61590,  479196,
                      1590934, 2225387,  486063, 1475243, 1405451, 2234674, 2147540, 1981749,  477066,
                      243102,  955837,  329183,  972102, 1003320,  953417,  681856, 1075119, 1707098,
                      1007070, 1636960,   95389,  676988, 2372525, 1411945, 1370290, 2277726, 1170097,
                      322198,  107566,  187560, 1005668, 1303451, 1307347, 1507365,  897317, 1985507,
                      1592937, 1121160,  592636,  461565, 1820870,  323957,  195085,  872947, 1126735,
                      761110, 1656601, 1381461,  646900, 1477138, 1511149, 1118318, 2279311, 1003116,
                      14891, 1759970,  967734,  890471,  985725, 2318556, 2001983, 1256019,  550381,
                      153633,  852951,  463105,  723437,  188590,  234679,  989782, 1910070,  217454,
                      1961893,  385620, 1245074, 2125388,  166230, 2377499,  707854, 1494195, 1423540,
                      434633,  221333]

    def teardown_class(self):
        del self.e_graph
        del self.dgl_graph
        del self.dataset

    def test_ezoo_node2vec_randomw_walk(self):
        dgl_trace_nodes = node2vec_random_walk(self.dgl_graph, self.seeds, self.p, self.q, self.walk_length)
        ezoo_trace_nodes = ezoo_node2vec_random_walk(self.dgl_graph, self.e_graph, self.seeds, self.p, self.q, self.walk_length)
        assert(dgl_trace_nodes.shape[0] == ezoo_trace_nodes.shape[0])
        assert(dgl_trace_nodes.shape[1] == ezoo_trace_nodes.shape[1])

