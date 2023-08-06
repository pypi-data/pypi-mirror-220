# -*- coding: utf-8 -*-
# @Time    : 2022/12/19 10:13 AM
# @Author  : lch
# @Email   : iltie165@163.com
# @File    : feature_transform.py
import featuretools.primitives as ft
import numpy as np
from ezoognn.utils.feature_custom import TransformUdf, GnnOpsWrapper


class ThridtyTransformUdf(TransformUdf):
    def transform(self, data, **kwargs):
        return call_thridty_transform(data, **kwargs)


def call_thridty_transform(data, **kwargs):
    op = kwargs['op']
    return op.call(data)


class FtWrapper(GnnOpsWrapper):
    def __init__(self, primitive):
        self.primitive = primitive

    def call(self, data):
        return self.primitive(*data) if isinstance(data, list) else self.primitive(data)


class SkWrapper(GnnOpsWrapper):
    def __init__(self, transformer):
        self.transformer = transformer

    def call(self, data):
        if isinstance(data, list):
            data = np.asarray(data)
            data = data.T
        else:
            data = data.reshape(-1, 1 if len(data.shape) == 1 else data.shape[1])

        return np.squeeze(self.transformer(data))


class NoWrapper(GnnOpsWrapper):
    def __init__(self, func):
        self.func = func

    def call(self, data):
        return self.func(data)


class NpWrapper(GnnOpsWrapper):
    def __init__(self, func):
        self.func = func

    def call(self, data):
        if isinstance(data, list):
            data = np.asarray(data)

        return np.squeeze(self.func(data))


class Ops:
    """
    基于python直接完成四则运算，标量
    """
    @classmethod
    def arithmetic_scalar(cls, value, operator, reverse=False):
        def func(data):
            assert data.shape[0] == 1, '标量四则运算，只能指定一列数据！'
            if operator == '+':
                return value + data
            elif operator == '-':
                return value - data if reverse else data - value
            elif operator == '*':
                return value * data
            elif operator == '/':
                return value / data if reverse else data / value
            elif operator == '%':
                return value % data if reverse else data % value

        return NpWrapper(func)

    @classmethod
    def arithmetic(cls, operator):
        def func(data):
            # TODO 只支持两列数据，后面扩展
            assert data.shape[0] == 2, '列表四则运算，需要指定两列数据！'
            if operator == '+':
                return data[0, :] + data[1, :]
            elif operator == '-':
                return data[0, :] - data[1, :]
            elif operator == '*':
                return data[0, :] * data[1, :]
            elif operator == '/':
                return data[0, :] / data[1, :]
            elif operator == '%':
                return data[0, :] % data[1, :]

        return NpWrapper(func)

    @classmethod
    def compare_scalar(cls, value, operator):
        def func(data):
            assert data.shape[0] == 1, '标量比较运算，只能指定一列数据！'
            if operator == '>':
                return data > value
            elif operator == '>=':
                return data >= value
            elif operator == '<':
                return data < value
            elif operator == '<=':
                return data <= value
            elif operator == '=':
                return data == value
            elif operator == '!=':
                return data != value
        return NpWrapper(func)

    @classmethod
    def compare(cls, operator):
        def func(data):
            # TODO 只支持两列数据，后面扩展
            assert data.shape[0] == 2, '列表比较运算，需要指定两列数据！'
            if operator == '>':
                return data[0, :] > data[1, :]
            elif operator == '>=':
                return data[0, :] >= data[1, :]
            elif operator == '<':
                return data[0, :] < data[1, :]
            elif operator == '<=':
                return data[0, :] <= data[1, :]
            elif operator == '=':
                return data[0, :] == data[1, :]
            elif operator == '!=':
                return data[0, :] != data[1, :]
        return NpWrapper(func)

    @classmethod
    def logic(cls, operator):
        def func(data):
            # TODO 只支持两列数据，后面扩展
            assert data.shape[0] == 2, '列表逻辑运算，需要指定两列数据！'
            if operator == 'and':
                return np.logical_and(data[0, :], data[1, :])
            elif operator == 'or':
                return np.logical_or(data[0, :], data[1, :])

        return NpWrapper(func)

    # =============================================	基础计算 ======================================
    @classmethod
    def date_basic(cls, operator):
        if operator == 'year':
            ops = ft.Year()
        elif operator == 'month':
            ops = ft.Month()
        elif operator == 'week':
            ops = ft.Week()
        elif operator == 'day':
            ops = ft.Day()
        elif operator == 'minute':
            ops = ft.Minute()
        elif operator == 'second':
            ops = ft.Second()

        def exec_ft(data):
            assert len(data.shape) == 1, '日期运算，只能指定一列数据，且必须为timestamp(毫秒)类型'
            from datetime import datetime
            # from ezoo timestamp is ms
            if isinstance(data, list):
                res = []
                for one in data:
                    res.append([datetime.fromtimestamp(time) for time in (one / 1000).tolist()])
            else:
                res = [datetime.fromtimestamp(time) for time in (data / 1000).tolist()]

            return ops(res)

        return FtWrapper(exec_ft)

    @classmethod
    def divide_by(cls, value):
        """
        example:
            >>> divide_by_feature = DivideByFeature(value=2)
            >>> divide_by_feature([4, 1, 2]).tolist()
            [0.5, 2.0, 1.0]
`       """
        import featuretools.primitives as ft

        op = FtWrapper(ft.DivideByFeature(value))
        return op

    @classmethod
    def add_numeric_scalar(cls, value):
        """
        example:
            >>> add_numeric_scalar = AddNumericScalar(value=2)
            >>> add_numeric_scalar([3, 1, 2]).tolist()
            [5, 3, 4]

`       """

        operation = FtWrapper(ft.AddNumericScalar(value))
        return operation

    @classmethod
    def add_numeric(cls):
        """
        example:
            >>> add_numeric = AddNumeric()
            >>> add_numeric([2, 1, 2], [1, 2, 2]).tolist()
            [3, 3, 4]

`       """

        operation = FtWrapper(ft.AddNumeric())
        return operation

    @classmethod
    def divide_numeric_scalar(cls, value):
        """
        example:
            >>> divide_numeric_scalar = DivideNumericScalar(value=2)
            >>> divide_numeric_scalar([3, 1, 2]).tolist()
            [1.5, 0.5, 1.0]

`       """

        operation = FtWrapper(ft.DivideNumericScalar(value))
        return operation

    @classmethod
    def equal(cls):
        """
        example:
            >>> equal = Equal()
            >>> equal([2, 1, 2], [1, 2, 2]).tolist()
           [False, False, True]

`       """

        operation = FtWrapper(ft.Equal())
        return operation

    @classmethod
    def equal_scalar(cls, value):
        """
        example:
            >>> equal_scalar = EqualScalar(value=2)
            >>> equal_scalar([3, 1, 2]).tolist()
            [False, False, True]

`       """

        operation = FtWrapper(ft.EqualScalar(value))
        return operation

    @classmethod
    def greater_than(cls):
        """
        example:
            >>> greater_than = GreaterThan()
            >>> greater_than([2, 1, 2], [1, 2, 2]).tolist()
            [True, False, False]
`       """

        operation = FtWrapper(ft.GreaterThan())
        return operation

    @classmethod
    def greater_than_equal_to(cls):
        """
        example:
            >>> greater_than_equal_to = GreaterThanEqualTo()
            >>> greater_than_equal_to([2, 1, 2], [1, 2, 2]).tolist()
            [True, False, True]
`       """

        operation = FtWrapper(ft.GreaterThanEqualTo())
        return operation

    @classmethod
    def greater_than_equal_to_scalar(cls, value):
        """
        example:
            >>> greater_than_equal_to_scalar = GreaterThanEqualToScalar(value=2)
            >>> greater_than_equal_to_scalar([3, 1, 2]).tolist()
            [True, False, True]

`       """

        operation = FtWrapper(ft.GreaterThanEqualToScalar(value))
        return operation

    @classmethod
    def greater_than_scalar(cls, value):
        """
        example:
            >>> add_numeric = AddNumeric()
            >>> add_numeric([2, 1, 2], [1, 2, 2]).tolist()
            [3, 3, 4]

`       """

        operation = FtWrapper(ft.GreaterThanScalar(value))
        return operation

    @classmethod
    def less_than(cls):
        """
        example:
            >>> less_than = LessThan()
            >>> less_than([2, 1, 2], [1, 2, 2]).tolist()
            [False, True, False]
`       """

        operation = FtWrapper(ft.LessThan())
        return operation

    @classmethod
    def less_than_equal_to(cls):
        """
        example:
            >>> less_than_equal_to = LessThanEqualTo()
            >>> less_than_equal_to([2, 1, 2], [1, 2, 2]).tolist()
            [False, True, True]
        """

        operation = FtWrapper(ft.LessThanEqualTo())
        return operation

    @classmethod
    def less_than_equal_to_scalar(cls, value):

        """
        example:
            >>> less_than_equal_to_scalar = LessThanEqualToScalar(value=2)
            >>> less_than_equal_to_scalar([3, 1, 2]).tolist()
            [False, True, True]

`       """

        operation = FtWrapper(ft.LessThanEqualToScalar(value))
        return operation

    @classmethod
    def less_than_scalar(cls, value):
        """
        example:
            >>> less_than_scalar = LessThanScalar(value=2)
            >>> less_than_scalar([3, 1, 2]).tolist()
            [False, True, False]

`       """
        operation = FtWrapper(ft.LessThanScalar(value))
        return operation

    @classmethod
    def multiply_numeric_scalar(cls, value):
        """
        example:
            >>> multiply_numeric_scalar = MultiplyNumericScalar(value=2)
            >>> multiply_numeric_scalar([3, 1, 2]).tolist()
            [6, 2, 4]

`       """

        operation = FtWrapper(ft.MultiplyNumericScalar(value))
        return operation

    @classmethod
    def not_equal(cls):
        """
        example:
            >>> not_equal = NotEqual()
            >>> not_equal([2, 1, 2], [1, 2, 2]).tolist()
            [True, True, False]
        """

        operation = FtWrapper(ft.NotEqual())
        return operation

    @classmethod
    def not_equal_scalar(cls, value):
        """
        example:
            >>> not_equal_scalar = NotEqualScalar(value=2)
            >>> not_equal_scalar([3, 1, 2]).tolist()
            [True, True, False]

`       """

        operation = FtWrapper(ft.NotEqualScalar(value))
        return operation

    @classmethod
    def scalar_subtract_numeric_feature(cls, value):
        """
        example:
            >>> scalar_subtract_numeric_feature = ScalarSubtractNumericFeature(value=2)
            >>> scalar_subtract_numeric_feature([3, 1, 2]).tolist()
            [-1, 1, 0]

`       """

        operation = FtWrapper(ft.ScalarSubtractNumericFeature(value))
        return operation

    @classmethod
    def subtract_numeric_scalar(cls, value):
        """
        example:
            >>> subtract_numeric_scalar = SubtractNumericScalar(value=2)
            >>> subtract_numeric_scalar([3, 1, 2]).tolist()
            [1, -1, 0]
`       """

        operation = FtWrapper(ft.SubtractNumericScalar(value))
        return operation

    # =============================================	累加计算======================================

    @classmethod
    def cum_count(cls):
        """
        example:
            >>> cum_count = CumCount()
            >>> cum_count([1, 2, 3, 4, None, 5]).tolist()
            [1, 2, 3, 4, 5, 6]

`       """

        operation = FtWrapper(ft.CumCount())
        return operation

    @classmethod
    def cum_sum(cls):
        """
        example:
            >>> cum_sum = CumSum()
            >>> cum_sum([1, 2, 3, 4, None, 5]).tolist()
            [1.0, 3.0, 6.0, 10.0, nan, 15.0]

`       """

        operation = FtWrapper(ft.CumSum())
        return operation

    @classmethod
    def cum_mean(cls):
        """
        example:
            >>> cum_mean = CumMean()
            >>> cum_mean([1, 2, 3, 4, None, 5]).tolist()
            [1.0, 1.5, 2.0, 2.5, nan, 2.5]

        """

        operation = FtWrapper(ft.CumMean())
        return operation

    @classmethod
    def cum_min(cls):
        """
        example:
            >>> cum_min = CumMin()
            >>> cum_min([1, 2, -3, 4, None, 5]).tolist()
            [1.0, 1.0, -3.0, -3.0, nan, -3.0]

        """

        operation = FtWrapper(ft.CumMin())
        return operation

    @classmethod
    def cum_max(cls):
        """
        example:
            >>> cum_max = CumMax()
            >>> cum_max([1, 2, 3, 4, None, 5]).tolist()
            [1.0, 2.0, 3.0, 4.0, nan, 5.0]

        """
        operation = FtWrapper(ft.CumMax())
        return operation

    # =======================时序处理=========================================

    @classmethod
    def lag(cls, periods):
        """
        example:
            >>> lag = Lag()
            >>> lag([1, 2, 3, 4, 5], pd.Series(pd.date_range(start="2020-01-01", periods=5, freq='D'))).tolist()
            [nan, 1.0, 2.0, 3.0, 4.0]
            You can specify the number of periods to shift the values
            >>> lag_periods = Lag(periods=3)
            >>> lag_periods([True, False, False, True, True], pd.Series(pd.date_range(start="2020-01-01", periods=5, freq='D'))).tolist()
            [nan, nan, nan, True, False]
 `       """
        import pandas as pd
        ft_op = ft.Lag(periods)

        def exec_ft(data):
            return ft_op(data, pd.Series(pd.date_range(start="2020-01-01", periods=len(data), freq='D')))

        operation = FtWrapper(exec_ft)
        return operation

    # ==============================文本处理==========================================================
    # TODO:to be implemented

    # @classmethod
    # def upper(cls):
    #     operation = upper()
    #     return operation

    # @classmethod
    # def lower(cls,periods):
    #     operation  = lower()
    #     return operation

    # @classmethod
    # def split(cls,string):
    #     operation = split(string)
    #     return operation

    # ====================================布尔运算======================================
    @classmethod
    def is_in(cls, list_of_outputs):
        """
        example:
            items = ['string', 10.3, False]
            >>> is_in = IsIn(list_of_outputs=items)
            >>> is_in(['string', 10.5, False]).tolist()
            [True, False, True]

`       """

        operation = FtWrapper(ft.IsIn(list_of_outputs))
        return operation

    # and / or/ not haven't been tested yet
    @classmethod
    def b_and(cls):
        """
        example:
            >>> _and = And()
            >>> _and([False, True, False], [True, True, False]).tolist()
            [False, True, False]

`       """
        operation = FtWrapper(ft.And())
        return operation

    @classmethod
    def b_or(cls):
        """
        example:
            >>> _or = Or()
            >>> _or([False, True, False], [True, True, False]).tolist()
            [True, True, False]
                    operation = FtWrapper(ft.Or())
                    return operation
        """
        operation = FtWrapper(ft.Or())
        return operation

    @classmethod
    def b_not(cls):
        """
        example:

            >>> not_func = Not()
            >>> not_func([True, True, False]).tolist()
            [False, False, True]
`       """
        operation = FtWrapper(ft.Not())
        return operation

    """
    example from ft:
        >>> subtract_numeric = SubtractNumeric()
        >>> subtract_numeric([2, 1, 2], [1, 2, 2]).tolist()
        [1, -1, 0]
    """

    @classmethod
    def substract_numeric(cls):
        op = FtWrapper(ft.SubtractNumeric())
        return op

    # ============================== 特征转换 ===================================
    @classmethod
    def email_address_to_domain(cls):
        """
        example:
        >>> email_address_to_domain = EmailAddressToDomain()
        >>> email_address_to_domain(['name@gmail.com', 'name@featuretools.com']).tolist()
        ['gmail.com', 'featuretools.com']
`       """

        operation = FtWrapper(ft.EmailAddressToDomain())
        return operation

    @classmethod
    def url_to_domain(cls):

        operation = FtWrapper(ft.URLToDomain())
        return operation

    # -----------------------fillna-----------------------------------------
    # @classmethod
    # def fillna(cls, with_mean=True, with_std=True):
    #
    #     operation = FtWrapper(ft.Lag(periods))
    #     return operatio

    @classmethod
    def natural_logarithm(cls):

        """
        example:
        >>> log = NaturalLogarithm()
        >>> results = log([1.0, np.e]).tolist()
        >>> results = [round(x, 2) for x in results]
        results
`       """

        operation = FtWrapper(ft.NaturalLogarithm())
        return operation

    # ===========================sk learn components=====================================
    """
    example from sklearn:
        >>> from sklearn.feature_selection import VarianceThreshold
        >>> X = [[0, 0, 1], [0, 1, 0], [1, 0, 0], [0, 1, 1], [0, 1, 0], [0, 1, 1]]
        >>> sel = VarianceThreshold(threshold=(.8 * (1 - .8)))
        >>> sel.fit_transform(X)
        array([[0, 1],
            [1, 0],
            [0, 0],
            [1, 1],
            [1, 0],
            [1, 1]])
    """

    @classmethod
    def variance_threshold(cls, threshold=0.0):
        from sklearn.feature_selection import VarianceThreshold
        sk_op = VarianceThreshold(threshold=threshold)

        def exec_sk(data):
            return sk_op.fit_transform(data)

        op = SkWrapper(exec_sk)
        
        return op

    @classmethod
    def variance_threshold_get_support(cls, threshold=0.0):
        from sklearn.feature_selection import VarianceThreshold
        sk_op = VarianceThreshold(threshold=threshold)

        def exec_sk(data):
            sk_op.fit_transform(data)
            return sk_op.get_support()

        op = SkWrapper(exec_sk)
        
        return op
    """
    example from sk:
        >>> data = [[0, 0], [0, 0], [1, 1], [1, 1]]
        >>> scaler = StandardScaler()
        >>> print(scaler.fit(data))
        StandardScaler()
        >>> print(scaler.mean_)
        [0.5 0.5]
        >>> print(scaler.transform(data))
        [[-1. -1.]
         [-1. -1.]
         [ 1.  1.]
         [ 1.  1.]]
    """

    @classmethod
    def standard_scaler(cls, with_mean=True, with_std=True):
        from sklearn.preprocessing import StandardScaler
        sk_op = StandardScaler(with_mean=with_mean, with_std=with_std)

        def exec_sk(data):
            return sk_op.fit_transform(data)

        op = SkWrapper(exec_sk)
        return op

    """
    example from sk:
        >>> data = [[-1, 2], [-0.5, 6], [0, 10], [1, 18]]
        >>> scaler = MinMaxScaler()
        >>> print(scaler.fit(data))
        MinMaxScaler()
        >>> print(scaler.data_max_)
        [ 1. 18.]
        >>> print(scaler.transform(data))
        [[0.   0.  ]
         [0.25 0.25]
         [0.5  0.5 ]
         [1.   1.  ]]
    """

    @classmethod
    def max_min_scalar(cls, feature_range=(0, 1)):
        from sklearn.preprocessing import MinMaxScaler
        sk_op = MinMaxScaler(feature_range=feature_range)

        def exec_sk(data):
            return sk_op.fit_transform(data)

        op = SkWrapper(exec_sk)
        return op

    """
    example from sk:
        >>> X = [[ 1., -2.,  2.],
        ...      [ -2.,  1.,  3.],
        ...      [ 4.,  1., -2.]]
        >>> transformer = RobustScaler().fit(X)
        >>> transformer
        RobustScaler()
        >>> transformer.transform(X)
        array([[ 0. , -2. ,  0. ],
               [-1. ,  0. ,  0.4],
               [ 1. ,  0. , -1.6]])
    """

    @classmethod
    def robust_scaler(cls, with_centering=True, with_scaling=True,
                      quantile_range_start=25.0,
                      quantile_range_end=75.0,
                      unit_variance=True):
        from sklearn.preprocessing import RobustScaler
        sk_op = RobustScaler(with_scaling=with_scaling, with_centering=with_centering,
                             quantile_range=(quantile_range_start, quantile_range_end),
                             unit_variance=unit_variance)

        def exec_sk(data):
            return sk_op.fit_transform(data)

        op = SkWrapper(exec_sk)
        return op

    """
    example from sk:
        >>> X = [[-2, 1, -4,   -1],
        ...      [-1, 2, -3, -0.5],
        ...      [ 0, 3, -2,  0.5],
        ...      [ 1, 4, -1,    2]]
        >>> est = KBinsDiscretizer(n_bins=3, encode='ordinal', strategy='uniform')
        >>> est.fit(X)
        KBinsDiscretizer(...)
        >>> Xt = est.transform(X)
        >>> Xt  
        array([[ 0., 0., 0., 0.],
               [ 1., 1., 1., 0.],
               [ 2., 2., 2., 1.],
               [ 2., 2., 2., 2.]])
    """

    @classmethod
    def kbins_discretizer(cls, n_bins=5, encode='ordinal', strategy='quantile'):
        from sklearn.preprocessing import KBinsDiscretizer
        # TODO 先写死方法，后面调
        encode = 'ordinal'
        strategy = 'quantile'
        sk_op = KBinsDiscretizer(n_bins=n_bins, encode=encode, strategy=strategy)

        def exec_sk(data):
            return sk_op.fit_transform(data)

        op = SkWrapper(exec_sk)
        return op

    """
    example from sk:
        >>> X = np.array([[-1, -1], [-2, -1], [-3, -2], [1, 1], [2, 1], [3, 2]])
        >>> pca = PCA(n_components=2)
        >>> pca.fit(X)
        PCA(n_components=2)
        >>> print(pca.explained_variance_ratio_)
        [0.9924... 0.0075...]
        >>> print(pca.singular_values_)
        [6.30061... 0.54980...]
        >>> pca.transform(X)
        array([[ 1.38340578,  0.2935787 ],
               [ 2.22189802, -0.25133484],
               [ 3.6053038 ,  0.04224385],
               [-1.38340578, -0.2935787 ],
               [-2.22189802,  0.25133484],
               [-3.6053038 , -0.04224385]])
    """
    @classmethod
    def __pca(cls, n_components, whiten=False, svd_solver='auto', tol=0.0,
              iterated_power=-1, n_oversamples=10,
              power_iteration_normalizer='auto', random_state=None,
              return_explained_variance_ratio=False,
              transform_data=None):
        if n_components > 1:
            n_components = int(n_components)
        elif n_components == -1:
            n_components = 'mle'

        if iterated_power == -1:
            iterated_power = 'auto'

        from sklearn.decomposition import PCA
        sk_op = PCA(n_components=n_components, whiten=whiten, svd_solver=svd_solver, tol=tol,
                    iterated_power=iterated_power, n_oversamples=n_oversamples,
                    power_iteration_normalizer=power_iteration_normalizer, random_state=random_state)

        def exec_sk(data):
            sk_op.fit(data)
            res = sk_op.transform(data if transform_data is None else transform_data)
            return (res, sk_op.explained_variance_ratio_) if return_explained_variance_ratio else res

        return exec_sk

    @classmethod
    def pca(cls, n_components, whiten=False, svd_solver='auto', tol=0.0,
            iterated_power=-1, n_oversamples=10,
            power_iteration_normalizer='auto', random_state=None,
            transform_data=None):

        func = cls.__pca(n_components, whiten, svd_solver, tol, iterated_power,
                  n_oversamples, power_iteration_normalizer,
                  random_state, False, transform_data)
        op = SkWrapper(func)

        return op

    @classmethod
    def pca_(cls, n_components, whiten=False, svd_solver='auto', tol=0.0,
            iterated_power=-1, n_oversamples=10,
            power_iteration_normalizer='auto', random_state=None,
            return_explained_variance_ratio=False,
            transform_data=None):

        func = Ops.__pca(n_components, whiten, svd_solver, tol, iterated_power,
                         n_oversamples, power_iteration_normalizer,
                         random_state, return_explained_variance_ratio, transform_data)

        op = NoWrapper(func)
        return op

    """
    example from sk
        >>> X = [[4, 1, 2, 2],
        ...      [1, 3, 9, 3],
        ...      [5, 7, 5, 1]]
        >>> transformer = Normalizer().fit(X)  # fit does nothing.
        >>> transformer
        Normalizer()
        >>> transformer.transform(X)
        array([[0.8, 0.2, 0.4, 0.4],
               [0.1, 0.3, 0.9, 0.3],
               [0.5, 0.7, 0.5, 0.1]])
    """

    @classmethod
    def norm(cls, norm='l2'):
        from sklearn.preprocessing import Normalizer
        sk_op = Normalizer(norm=norm)

        def exec_sk(data):
            return sk_op.fit_transform(data)

        op = SkWrapper(exec_sk)
        return op
    #### endregion
