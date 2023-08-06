# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File     : opt.py.py
@Project  : PerfusionCompartmentModel
@Software : PyCharm
@Author   : Xiong YiWei
@Time     : 2022/8/1 22:52
-------------------------------------------------------
                    @Description
    
-------------------------------------------------------
@Last Modify Time      @Version     @Description
2022/8/1 22:52        1.0             None
"""


class Optimization(object):

    def __init__(self, object_fn, constraints, hyperparams, conditions, minimize=True, outConfig=None):
        """

        Args:
            object_fn: function 目标函数
            constraints: tuple 约束条件元组
                (1) <each element>: tuple/dict 某个参数的约束条件
                    (1) type is tuple:
                        0: 该参数的约束下限
                        1: 该参数的约束上限
                    (2) type is dict:
                        <key> 约束表达式形式: <value> 约束表达式 TODO: 更复杂约束条件的表达，待定
                (2) 约束下限、上限
                    0: 各参数的下限
                    1: 各参数的上限
            hyperparams: 超参数
            conditions: dict 终止条件
            minimize: bool 最大化/最小化指示符
            outConfig: dict 优化器输出设置
        """
        self._object = object_fn
        self._constraints = constraints
        self._hyperparams = hyperparams
        self._conditions = conditions
        self._minimize = minimize
        self._outConfig = outConfig
