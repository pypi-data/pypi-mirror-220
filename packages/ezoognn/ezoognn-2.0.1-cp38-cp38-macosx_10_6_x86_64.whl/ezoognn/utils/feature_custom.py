# -*- coding: utf-8 -*-
# @Time    : 2023/1/11 10:48 AM
# @Author  : lch
# @Email   : iltie165@163.com
# @File    : feature_custom.py
from abc import abstractmethod


class GnnOpsWrapper:
    @abstractmethod
    def call(self, data):
        pass


class TransformUdf:
    @abstractmethod
    def transform(self, data, **kwargs):
        pass


class DataSplitUdf:
    @abstractmethod
    def split_tvt(self, graph, **kwargs):
        pass


class DataBalanceUdf:
    @abstractmethod
    def balance(self, src_graph, **kwargs):
        pass


def call_udf_transform(data, **kwargs):
    py_file = kwargs['udf_file']
    func_name = kwargs['cls_name']
    del kwargs['udf_file']
    del kwargs['cls_name']
    res = None
    import importlib
    import sys
    import os
    import inspect
    path, module = os.path.split(os.path.splitext(py_file)[0])
    sys.path.insert(0, path)
    udf_obj = importlib.import_module(module)
    udf_cls = inspect.getmembers(udf_obj, inspect.isclass)
    for cls_name, cls in udf_cls:
        if cls_name == func_name:
            if issubclass(cls, TransformUdf):
                res = cls().transform(data, **kwargs)
                break
            elif issubclass(cls, DataSplitUdf):
                res = cls().split_tvt(data, **kwargs)
                break
            elif issubclass(cls, DataBalanceUdf):
                res = cls().balance(data, **kwargs)
                break

    return res
