import os
import json
import random as rd
import numpy as np
from ezoognn import get_ezoo_home
from .ezoo_data_graph import GetItemGraph, EzooShapeGraphEnum, EzooHeteroGraphDataset, EzooExampleDatasetEnum


class EzooGowallaGraph(GetItemGraph):
    def __init__(self, e_graph=None, _graph=None, name=None, data_generator={}):
        super(EzooGowallaGraph, self).__init__(
            e_graph=e_graph, _graph=_graph, name=name)
        self.num_classes = 2
        self.g = _graph

        # 映射内部id到原始id中
        self._mapping = {}
        for n_type in self.dgl_graph.ntypes:
            node_ids = self.dgl_graph.nodes(n_type).numpy()
            original_ids = self.dgl_graph.nodes[n_type].data['id'].numpy(
            ).tolist()
            _dict = {}
            for i in range(len(node_ids)):
                nodeid = node_ids[i]
                original_id = original_ids[i]
                _dict[original_id] = nodeid
            self._mapping[n_type] = _dict

        if data_generator is not None:
            if data_generator.__contains__('batch_size'):
                self.batch_size = data_generator['batch_size']
            if data_generator.__contains__('exist_users'):
                self.exist_users = data_generator['exist_users']
            if data_generator.__contains__('n_items'):
                self.n_items = data_generator['n_items']
            if data_generator.__contains__('n_users'):
                self.n_users = data_generator['n_users']
            if data_generator.__contains__('n_train'):
                self.n_train = data_generator['n_train']
            if data_generator.__contains__('n_interactions'):
                self.n_interactions = data_generator['n_interactions']
            if data_generator.__contains__('n_test'):
                self.n_test = data_generator['n_test']
            if data_generator.__contains__('train_items'):
                _train_items = {self._mapping['user'][int(k)]: [self._mapping['item'][item] for item in data_generator['train_items'][k]]
                                for k in data_generator['train_items'].keys()}
                self.train_items = _train_items
            if data_generator.__contains__('test_set'):
                _test_set = {self._mapping['user'][int(k)]: [self._mapping['item'][item] for item in data_generator['test_set'][k]]
                             for k in data_generator['test_set'].keys()}
                self.test_set = _test_set

    def sample(self):
        if self.batch_size <= self.n_users:
            users = rd.sample(self.exist_users, self.batch_size)
        else:
            users = [
                rd.choice(self.exist_users) for _ in range(self.batch_size)
            ]

        def sample_pos_items_for_u(u, num):
            # sample num pos items for u-th user
            # 使用映射找到原始id
            # u = self._mapping['user'][u]
            pos_items = self.train_items[u]
            # pos_items = [self._mapping['item'][i] for i in pos_items]
            n_pos_items = len(pos_items)
            pos_batch = []
            while True:
                if len(pos_batch) == num:
                    break
                pos_id = np.random.randint(low=0, high=n_pos_items, size=1)[0]
                pos_i_id = pos_items[pos_id]

                if pos_i_id not in pos_batch:
                    pos_batch.append(pos_i_id)
            return pos_batch

        def sample_neg_items_for_u(u, num):
            # sample num neg items for u-th user
            # 使用映射找到原始id
            # u = self._mapping['user'][u]
            neg_items = []
            while True:
                if len(neg_items) == num:
                    break
                neg_id = np.random.randint(low=0, high=self.n_items, size=1)[0]
                # neg_id = self._mapping['item'][neg_id]
                if (
                        neg_id not in self.train_items[u]
                        and neg_id not in neg_items
                ):
                    neg_items.append(neg_id)
            return neg_items

        pos_items, neg_items = [], []
        for u in users:
            pos_items += sample_pos_items_for_u(u, 1)
            neg_items += sample_neg_items_for_u(u, 1)

        return users, pos_items, neg_items

    def get_num_users_items(self):
        return self.n_users, self.n_items


class GowallaEzooGraphDataset(EzooHeteroGraphDataset):

    def __init__(self, name=EzooExampleDatasetEnum.GOWALLA.value, reverse=True, raw_dir=None, force_reload=False,
                 cfg_file=None, gdi_ptr=0, restore_file='', restore_url='',
                 split_ratio=None, data_path=None, force_download=False):
        self.reverse = reverse
        super(GowallaEzooGraphDataset, self).__init__(name, rpc_url=None, raw_dir=raw_dir, force_reload=force_reload,
                                                      cfg_file=cfg_file, gdi_ptr=gdi_ptr, restore_file=restore_file,
                                                      restore_url=restore_url, node_exclude_list=[],
                                                      edge_exclude_list=[
                                                          'edgeIds'],
                                                      force_download=force_download)

    def __getitem__(self, item):
        data_generator = self.get_data_genorator()
        super().__getitem__(item)
        return EzooGowallaGraph(self.e_graph, self.dgl_graph, self.db_name, data_generator=data_generator)

    def get_data_genorator(self):
        dataset_path = get_ezoo_home(
            self.cfg_file) + os.sep + self.db_name + os.sep + self.db_name
        if os.path.exists(dataset_path) is False:
            return
        data_info_path = os.path.join(dataset_path, "data_generator.json")
        with open(data_info_path, 'r', newline='', encoding='utf-8') as f:
            data_generator = json.loads(f.read())
        return data_generator


class AmazonBookEzooGraphDataset(EzooHeteroGraphDataset):

    def __init__(self, name=EzooExampleDatasetEnum.AMAZONBOOK.value, reverse=True, raw_dir=None, force_reload=False,
                 cfg_file=None, gdi_ptr=0, restore_file='', restore_url='',
                 split_ratio=None, data_path=None, force_download=False):
        self.reverse = reverse
        super(AmazonBookEzooGraphDataset, self).__init__(name, rpc_url=None, raw_dir=raw_dir, force_reload=force_reload,
                                                         cfg_file=cfg_file, gdi_ptr=gdi_ptr, restore_file=restore_file,
                                                         restore_url=restore_url, node_exclude_list=[],
                                                         edge_exclude_list=[
                                                             'edgeIds'],
                                                         force_download=force_download)

    def __getitem__(self, item):
        data_generator = self.get_data_genorator()
        super().__getitem__(item)
        return EzooGowallaGraph(self.e_graph, self.dgl_graph, self.db_name, data_generator=data_generator)

    def get_data_genorator(self):
        dataset_path = get_ezoo_home(
            self.cfg_file) + os.sep + self.db_name + os.sep + self.db_name
        if os.path.exists(dataset_path) is False:
            return
        data_info_path = os.path.join(dataset_path, "data_generator.json")
        with open(data_info_path, 'r', newline='', encoding='utf-8') as f:
            data_generator = json.loads(f.read())
        return data_generator
