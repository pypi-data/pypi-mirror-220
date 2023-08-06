# -*- coding: utf-8 -*-
# @Time    : 2023/1/31 6:18 PM
# @Author  : lch
# @Email   : iltie165@163.com
# @File    : split_custom.py
import typing
from ezoognn.ezoocall import SearchDirectionType
from ezoognn.utils.feature_custom import DataBalanceUdf, DataSplitUdf
import numpy as np
import random
import pandas as pd


class RandomSplitUdf(DataSplitUdf):
    def split_tvt(self, entity, rate: typing.List[float]):
               
        """    
        Parameters
        ----------
        graph: EzooGraph
        rate: List[float]

        """
        n_samples = entity.get_nodes_num()
        n_train, n_val = np.floor(rate[0] * n_samples), np.floor(rate[1] * n_samples)
        n_test = n_samples - n_train - n_val if sum(rate) == 1 else np.floor(rate[2] * n_samples)
        n_fill = n_samples - n_train - n_val - n_test

        l = 'a'*int(n_train) + 'b'*int(n_val) + 'c'*int(n_test) + 'd'*int(n_fill)
        s = "".join(random.sample(l, len(l)))
        series = pd.Series(list(s))
        df = pd.get_dummies(series)
        train, test = df['a'].values, df['c'].values
        return train, np.zeros(n_samples) if n_val == 0 else df['b'].values, test
        
    
class TimeWindowSplitUdf(DataSplitUdf):
    def split_tvt(self, entity, col_name, window: typing.List[tuple]):

        """    
        Parameters
        ----------
        graph: EzooGraph
        node_type: string
        field_name: feature name
        window: list of tuples of timestamps: start timestamp, end timestamp

        """
        train_window, val_window, test_window = window[0], window[1], window[2]
        time_stamp_col = entity[col_name]
            
        train_mask = np.logical_and(train_window[0] <= time_stamp_col, time_stamp_col < train_window[1])
        val_mask = np.logical_and(val_window[0] <= time_stamp_col, time_stamp_col < val_window[1])
        test_mask = np.logical_and(test_window[0] <= time_stamp_col, time_stamp_col < test_window[1])

        l_train = np.where(train_mask, 1, 0)
        l_val = np.where(val_mask, 1, 0)
        l_test = np.where(test_mask, 1, 0)
        return l_train, l_val, l_test

class DownSamplingUdf(DataBalanceUdf):
    def balance(self, src_graph, dst_gname, ntype, col_name, hop, search_direction=SearchDirectionType.InOut,
                reserved_rank=[1], from_rank=0, target_rank=1, sampling_rate=1):
        feats = src_graph.ndata[ntype][col_name]
        unique, counts = np.unique(feats, return_counts=True)
        sorted_ind = np.argsort(-counts)
        sampling_from_value = unique[sorted_ind][from_rank]

        node_ids = src_graph.get_all_node_id(ntype)
        chosen_nodes_idx = np.where(feats == sampling_from_value)[0]
        chosen_nodes = node_ids[chosen_nodes_idx]
        target_num = int(counts[sorted_ind[target_rank]] * sampling_rate)
        chosen_nodes = np.random.choice(
            chosen_nodes, target_num, replace=False)

        # Append the reserved nodes
        for reserved in reserved_rank:
            reserved_value = unique[sorted_ind][reserved]
            reserved_nodes_idx = np.where(feats == reserved_value)[0]
            reserved_nodes = node_ids[reserved_nodes_idx]
            chosen_nodes = np.append(chosen_nodes, reserved_nodes)

        src_graph.create_subgraph_with_node_neighbour(
            chosen_nodes, search_direction.value, hop, dst_gname)