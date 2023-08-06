# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File     : pso.py
@Project  : PerfusionCompartmentModel
@Software : PyCharm
@Author   : Xiong YiWei
@Time     : 2022/8/22 20:12
-------------------------------------------------------
                    @Description
    
-------------------------------------------------------
@Last Modify Time      @Version     @Description
2022/8/22 20:12        1.0             None
"""

from opt_selfimple.opt import Optimization
from sko.PSO import PSO
import numpy as np
import scipy.stats as stats
import copy


hyperparams_GaOpt_default = {
    'individual number': 50,
    'w': 0.8,
    'c1': 0.5,
    'c2': 0.5
}
conditions_GaOpt_default = {
    'generate times': 20
}
optConfig_GaOpt_default = {
    'init': {'init type': 'uniform'},
}
outConfig_GaOpt_default = {
    # 'final log': False,
    # 'each generation log': False,
    # 'generation record': False
}


class Pso(Optimization):
    def __init__(self, object_fn, constraints, hyperparams=None, conditions=None, minimize=True, optConfig=None,
                 outConfig=None):
        """
        粒子群算法实现（scikit-opt）
        Args:
            object_fn:
            constraints:
            hyperparams:
            conditions:
            minimize:
            optConfig:
            outConfig:
        """
        if hyperparams is None:
            hyperparams = hyperparams_GaOpt_default
        if conditions is None:
            conditions = conditions_GaOpt_default
        if optConfig is None:
            optConfig = optConfig_GaOpt_default
        if outConfig is None:
            outConfig = outConfig_GaOpt_default
        super().__init__(object_fn, constraints, hyperparams, conditions, minimize, outConfig)
        # hyper parameters
        self._num_indiv = self._hyperparams['individual number']
        self._w = self._hyperparams['w']
        self._c1 = self._hyperparams['c1']
        self._c2 = self._hyperparams['c2']
        self._v_max = self._hyperparams['v_max']

        self._optConfig = optConfig
        self._dim = len(self._constraints)
        if 'generate times' in self._conditions:
            self._num_gener = self._conditions['generate times']

    def _init_population(self):
        """初始化"""
        if self._optConfig['init']['init type'] == 'uniform':  # 均匀分布
            popul = [np.random.uniform(c[0], c[1], size=self._num_indiv) for c in self._constraints]
            popul = np.stack(popul, axis=-1)
        elif self._optConfig['init']['init type'] == 'normal':  # 正态分布
            popul = [stats.truncnorm((c[0] - mu) / sigma, (c[1] - mu) / sigma, loc=mu, scale=sigma).rvs(self._num_indiv)
                     for mu, sigma, c in
                     zip(self._optConfig['init']['init info']['mean'],
                         self._optConfig['init']['init info']['std'],
                         self._constraints)]
            popul = np.stack(popul, axis=-1)
        elif self._optConfig['init']['init type'] == 'histogram':  # 自定义直方图分布
            popul = [stats.rv_histogram(histogram=hist).rvs(size=self._num_indiv) for hist in
                     self._optConfig['init']['init info']['histogram']]
            popul = np.stack(popul, axis=-1)
        elif self._optConfig['init']['init type'] == 'given':  # 使用直接给定的初始群体
            popul = self._optConfig['init']['init info']['given data']
        else:
            raise Exception('没有在_optConfig给出init设置！')
        return popul

    def optimize(self):
        """进行优化"""
        lb = np.array([lu[0] for lu in self._constraints])
        ub = np.array([lu[1] for lu in self._constraints])
        pso = PSO(func=self._object,
                  n_dim=self._dim,
                  pop=self._num_indiv,
                  max_iter=self._num_gener,
                  lb=lb, ub=ub,
                  w=self._w,
                  c1=self._c1, c2=self._c2,
                  v_max=self._v_max
                  )
        # region 初始化
        popul = self._init_population()
        pso.X = popul
        pso.cal_y()
        pso.update_gbest()
        pso.update_pbest()
        # endregion
        pso.run()
        return pso.gbest_x
