from dgl.data import AIFBDataset, CoraGraphDataset, CiteseerGraphDataset, MUTAGDataset
from ezoognn.loader.dataset.rdf_ezoo_data_graph import AifbEzooGraphDataset
from ezoognn.loader.dataset.citation_ezoo_data_graph import CoraEzooGraphDatasetV2
from ezoognn.loader.dataset.ieee_fraud_detection_ezoo_data_graph import IeeeFraudDetectionEzooGraphDataset
from ezoognn.loader.dataset.ezoo_data_graph import EzooShapeGraphEnum, EzooGraphDataset, EzooHeteroGraphDataset
from ezoognn.loader.dataset.ogb_ezoo_data_graph import *
from ezoognn.loader.dataset.knowledge_ezoo_data_graph import *
from ezoognn.utils.graph_store import GraphStore

global cfg_file
cfg_file = '../../../resources/conf/ezoodb.conf'


class TestAifbAndBuildDglGraph:

    ''''
    Test 
    '''
    @classmethod
    def setup_class(cls):
        cls.graph_store = GraphStore(cfg_file=cfg_file)
        cls.aifb = AifbEzooGraphDataset(cfg_file=cfg_file, force_download=True)[
            EzooShapeGraphEnum.WHOLE][0]
        cls.dgl_graph = AIFBDataset()[0]

    @classmethod
    def teardown_class(cls):
        cls.graph_store.remove_graph(EzooExampleDatasetEnum.AIFB.value)
        print('xxx teardown_class called!!')
        del cls.aifb
        del cls.dgl_graph

    def test_nodeTypes(self):
        assert (len(self.dgl_graph.ntypes) == len(self.aifb.ntypes))
        assert (
            set([True for nt in self.dgl_graph.ntypes if nt in self.aifb.ntypes]) == {True})

    def test_edgeTypes(self):
        assert (len(self.dgl_graph.etypes) == len(self.aifb.etypes))
        assert (
            set([True for nt in self.dgl_graph.etypes if nt in self.aifb.etypes]) == {True})

    def test_nodeSize(self):
        assert (self.aifb.number_of_nodes() ==
                self.dgl_graph.number_of_nodes())

    def test_edgeSize(self):
        assert (self.aifb.number_of_edges() ==
                self.dgl_graph.number_of_edges())

    def test_nodeShape(self):
        for nt in self.dgl_graph.ntypes:
            assert (self.dgl_graph.nodes(nt).shape ==
                    self.aifb.nodes(nt).shape)

    def test_edgeShape(self):
        assert (len(self.dgl_graph.edata._etype) == len(
            set(self.dgl_graph.edata._etype + self.aifb.edata._etype)))
        for key in self.dgl_graph.edata:
            value1 = self.dgl_graph.edata[key]
            value2 = self.aifb.edata[key]
            for kk in value1:
                vv1 = value1[kk]
                vv2 = value2[kk]
                assert (vv1.shape == vv2.shape)


class TestCoraV2AndBuildDglGraph:
    ''''
    前置条件
    '''
    @classmethod
    def setup_class(cls):
        cls.graph_store = GraphStore(cfg_file=cfg_file)
        cls.cora = CoraEzooGraphDatasetV2(cfg_file=cfg_file, force_download=True)[
            EzooShapeGraphEnum.WHOLE]
        cls.dgl_graph = CoraGraphDataset()

    @classmethod
    def teardown_class(cls):
        cls.graph_store.remove_graph(EzooExampleDatasetEnum.CORA_V2.value)
        del cls.cora
        del cls.dgl_graph

    def test_nodeSize(self):
        assert (self.cora[0].number_of_nodes() ==
                self.dgl_graph._g.number_of_nodes())

    def test_edgeSize(self):
        assert (self.cora[0].number_of_edges() ==
                self.dgl_graph._g.number_of_edges())

    def test_nodeFeatures(self):
        assert (self.cora[0].ndata['feat'].shape ==
                self.dgl_graph._g.ndata['feat'].shape)

    def test_stop_None(self):
        # 获取所有属性, 判断，对应属性形状是否相同
        all_props = self.cora.e_graph.ndata['node'][:None:]
        assert (all_props['feat'].shape == self.cora[0].ndata['feat'].shape)


class TestEzooGraphAndBuildDglGraph:

    @classmethod
    def setup_class(cls):
        cls.graph_store = GraphStore(cfg_file=cfg_file)
        cls.dgl_graph = CiteseerGraphDataset()
        cls.citeseer = EzooGraphDataset(name='citeseer', cfg_file=cfg_file, force_download=True)[
            EzooShapeGraphEnum.WHOLE][0]

    @classmethod
    def teardown_class(cls):
        cls.graph_store.remove_graph('citeseer')
        del cls.citeseer
        del cls.dgl_graph

    def test_nodeSize(self):
        assert (self.citeseer.number_of_nodes() ==
                self.dgl_graph._g.number_of_nodes())

    def test_edgeSize(self):
        assert (self.citeseer.number_of_edges() ==
                self.dgl_graph._g.number_of_edges())

    def test_nodeFeatures(self):
        assert (self.citeseer.ndata['feat'].shape ==
                self.dgl_graph._g.ndata['feat'].shape)


class TestEzooHeteroGraphAndBuildDglGraph:

    @classmethod
    def setup_class(cls):
        cls.graph_store = GraphStore(cfg_file=cfg_file)
        cls.dgl_graph = MUTAGDataset()[0]
        cls.mutag = EzooHeteroGraphDataset(
            name='mutag', cfg_file=cfg_file, force_download=True)[EzooShapeGraphEnum.WHOLE][0]

    @classmethod
    def teardown_class(cls):
        cls.graph_store.remove_graph('mutag')
        del cls.mutag
        del cls.dgl_graph

    def test_nodeTypes(self):
        assert (len(self.dgl_graph.ntypes) == len(self.mutag.ntypes))
        assert (
            set([True for nt in self.dgl_graph.ntypes if nt in self.mutag.ntypes]) == {True})

    def test_edgeTypes(self):
        assert (len(self.dgl_graph.etypes) == len(self.mutag.etypes))
        assert (
            set([True for nt in self.dgl_graph.etypes if nt in self.mutag.etypes]) == {True})

    def test_nodeSize(self):
        assert (self.mutag.number_of_nodes() ==
                self.dgl_graph.number_of_nodes())

    def test_edgeSize(self):
        assert (self.mutag.number_of_edges() ==
                self.dgl_graph.number_of_edges())

    def test_nodeShape(self):
        for nt in self.dgl_graph.ntypes:
            assert (self.dgl_graph.nodes(nt).shape ==
                    self.mutag.nodes(nt).shape)


class TestIeeeFraudDetectionAndBuildDglGraph:

    ''''
    前置条件
    '''

    @classmethod
    def setup_class(cls):
        cls.graph_store = GraphStore(cfg_file=cfg_file)
        cls.ieee_fraud_detection = IeeeFraudDetectionEzooGraphDataset(
            cfg_file=cfg_file, force_download=True)[EzooShapeGraphEnum.WHOLE][0]

    @classmethod
    def teardown_class(cls):
        cls.graph_store.remove_graph('ieee-fraud-detection')
        del cls.ieee_fraud_detection

    def test_nodeSize(self):
        assert (self.ieee_fraud_detection.number_of_nodes() == 726345)

    def test_edgeSize(self):
        assert (self.ieee_fraud_detection.number_of_edges() == 19518802)


# =============
# class TestEzooRdfGraphhDatasetAndBuildDglGraph:

#     ''''
#     前置条件
#     '''
#     @classmethod
#     def setup_class(self):
#         self.graph_store = GraphStore(cfg_file=cfg_file)
#         self.mutag = EzooHeteroGraphDataset(
#             name='mutag', cfg_file=cfg_file, force_download=True)[EzooShapeGraphEnum.WHOLE][0]

#     def teardown_class(self):
#         self.graph_store.remove_graph('mutag')
#         del self.mutag

#     def test_nodeSize(self):
#         assert (self.mutag.number_of_nodes() == 27163)

#     def test_edgeSize(self):
#         assert (self.mutag.number_of_edges() == 148100)


class TestMutagEzooGraphDatasetAndBuildDglGraph:

    ''''
    前置条件
    '''
    @classmethod
    def setup_class(cls):
        cls.graph_store = GraphStore(cfg_file=cfg_file)
        cls.mutag = EzooHeteroGraphDataset(
            name='mutag', cfg_file=cfg_file, force_download=True)[EzooShapeGraphEnum.WHOLE][0]

    @classmethod
    def teardown_class(cls):
        cls.graph_store.remove_graph('mutag')
        del cls.mutag

    def test_nodeSize(self):
        assert (self.mutag.number_of_nodes() == 27163)

    def test_edgeSize(self):
        assert (self.mutag.number_of_edges() == 148100)


class TestOgbnEzooGraphDatasetAndBuildDglGraph:

    ''''
    前置条件
    '''
    @classmethod
    def setup_class(cls):
        cls.graph_store = GraphStore(cfg_file=cfg_file)
        cls.ogbn_products = OgbnEzooGraphDataset(
            cfg_file=cfg_file)[EzooShapeGraphEnum.WHOLE][0]

    @classmethod
    def teardown_class(cls):
        cls.graph_store.remove_graph(
            EzooExampleDatasetEnum.OGBN_PRODUCTS.value)
        del cls.ogbn_products

    def test_nodeSize(self):
        assert (self.ogbn_products.number_of_nodes() == 2449029)

    def test_edgeSize(self):
        assert (self.ogbn_products.number_of_edges() == 123718280)


class TestWn18EzooGraphDatasetAndBuildDglGraph:  # optional

    ''''
    WN18 link prediction dataset(Not Implemented): WordNet的子集，包含18种关系和40k种实体。
    '''
    @classmethod
    def setup_class(cls):
        cls.graph_store = GraphStore(cfg_file=cfg_file)
        cls.wn18 = Wn18EzooGraphDataset(cfg_file=cfg_file, force_download=True)[
            EzooShapeGraphEnum.WHOLE][0]

    @classmethod
    def teardown_class(cls):
        cls.graph_store.remove_graph(EzooExampleDatasetEnum.WN18.value)
        del cls.wn18

    def test_nodeSize(self):
        assert (self.wn18.number_of_nodes() == 40943)

    def test_edgeSize(self):
        assert (self.wn18.number_of_edges() == 151442)


class TestFB15KEzooGraphDatasetAndBuildDglGraph:  # optional

    ''''
    FB15k link prediction dataset: 包含知识库关系三元组和自由基实体对的文本提及。

    '''
    @classmethod
    def setup_class(cls):
        cls.graph_store = GraphStore(cfg_file=cfg_file)
        cls.FB15K = FB15KEzooGraphDataset(cfg_file=cfg_file, force_download=True)[
            EzooShapeGraphEnum.WHOLE][0]

    @classmethod
    def teardown_class(cls):
        cls.graph_store.remove_graph(EzooExampleDatasetEnum.FB15K.value)
        del cls.FB15K

    def test_nodeSize(self):
        assert (self.FB15K.number_of_nodes() == 14951)


class TestFB15K237EzooGraphDatasetAndBuildDglGraph:  # optional

    ''''
    FB15k237 link prediction dataset: 从Freebase中取出一小部分主题词组成的子图, FB15k的子集，其中逆关系被删除。
    '''
    @classmethod
    def setup_class(cls):
        cls.graph_store = GraphStore(cfg_file=cfg_file)
        cls.FB15k237 = FB15K237EzooGraphDataset(cfg_file=cfg_file, force_download=True)[
            EzooShapeGraphEnum.WHOLE][0]

    @classmethod
    def teardown_class(cls):
        cls.graph_store.remove_graph(EzooExampleDatasetEnum.FB15K_237.value)
        del cls.FB15k237

    def test_nodeSize(self):
        assert (self.FB15k237.number_of_nodes() == 14541)
