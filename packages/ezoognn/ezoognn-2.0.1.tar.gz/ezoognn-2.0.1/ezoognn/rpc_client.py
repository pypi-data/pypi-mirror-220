from pyezoo.connections import Connection

class RpcClient:
    def __init__(self, url, db_name):
        _host = '127.0.0.1'
        _port = 9090
        if url.index(':'):
            address = url.split(':')
            if address is not None:
                if len(address) >= 2:
                    _host = address[0]
                    _port = address[1]
        conn = Connection(host=_host, port=_port, auth=False)
        self.client = conn.client
        self.client.open_graph(db_name, {})
        self.db_name = db_name

    def __del__(self):
        self.client.close_graph(self.db_name)

    def get_nodes_num(self, node_type):
        self.nodes_num = self.client.get_graph_node_size(
            self.db_name, node_type).size
        return self.nodes_num

    def get_node_id_batch(self, node_type, start_id, number):
        # TODO, node_type should be considered
        self.nodes = self.client.get_node_s_batch(
            self.db_name, start_id, number).nodes
        return [node.int_id for node in self.nodes]

    def get_node_prop_num(self, node_type):
        schema_list = self.client.get_graph_schema_list([self.db_name])
        node_schema_list = schema_list.schema_simple_list[0].node_schema_list
        for node_schema in node_schema_list:
            if node_schema.type == node_type:
                return len(node_schema.props)
        return 0

    def get_label_num_and_max_feats(self, node_type, label_name, exclude_columns):
        if not hasattr(self, 'nodes_num'):
            self.get_nodes_num(node_type)
        if not hasattr(self, 'nodes'):
            self.get_node_id_batch(node_type, 0, self.nodes_num)

        labels_set = set()
        max_feature_val = 0
        for node in self.nodes:
            current_node = self.client.get_node_with_id(
                self.db_name, node.int_id)
            labels_set.add(int(current_node.props[label_name]))

            for key, val in current_node.props.items():
                if key not in exclude_columns:
                    ret_val = int(eval(val))
                    if ret_val > max_feature_val:
                        max_feature_val = ret_val

        return len(labels_set), max_feature_val

    def sampling_no_weight(self, node_type, node_ids, number_walk, repeat, p):
        # TODO, consider node_type, repeat, p
        src_nodes = []
        dst_nodes = []
        for node in node_ids:
            node_id = int(node)
            neighbors = self.client.query_simple_neighbour_limit(
                self.db_name, node_id, 1, 1, 0, '', number_walk)
            sampling_list = neighbors.nodes[0]
            for n in sampling_list:
                dst_nodes.append(node_id)
                src_nodes.append(n)
        return dst_nodes, src_nodes

    def get_features_batch2float(self, node_type, node_ids):
        nodes = self.client.get_nodes_with_ids(self.db_name, node_ids).nodes
        features = []
        for node in nodes:
            node_features = []
            node_features.append(float(node.props['id']))
            node_features.append(float(node.props['label']))
            for key, val in node.props.items():
                if key != 'id' and key != 'label':
                    node_features.append(float(val))
            features.append(node_features)

        return features

    def __getattr__(self, attr):
        return getattr(self.client, attr)
