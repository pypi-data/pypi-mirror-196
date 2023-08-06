# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File     : whaleOpt.py
@Project  : PerfusionCompartmentModel
@Software : PyCharm
@Author   : Xiong YiWei
@Time     : 2022/5/12 16:19
-------------------------------------------------------
                    @Description
    
-------------------------------------------------------
@Last Modify Time      @Version     @Description
2022/5/12 16:19        1.0             None
"""

from opt_selfimple.opt import Optimization
import numpy as np
import scipy.stats as stats
import copy
import time

hyperparams_WhaleOpt_default = {
    'individual number': 50,
    'a': 2.0,
    'b': 0.5,
    'step_a': 0.1,
    'step_b': 0.025,
    'select threshold': 0.5
}
conditions_WhaleOpt_default = {
    'generate times': 20
}
optConfig_WhaleOpt_default = {
    'init': {'init type': 'uniform'},
    'no sorted': True
}
outConfig_WhaleOpt_default = {
    'final log': False,
    'each generation log': False,
    'generation record': False
}


class WhaleOpt(Optimization):
    def __init__(self, object_fn, constraints, hyperparams=None, conditions=None, minimize=True, optConfig=None,
                 outConfig=None):
        """
        鲸鱼优化算法实现
            paper:
            Mirjalili, Seyedali, and Andrew Lewis. "The whale optimization algorithm." Advances in engineering software 95 (2016): 51-67.
            https://doi.org/10.1016/j.advengsoft.2016.01.008
            代码参考：https://github.com/docwza/woa
        Args:
            object_fn: function （单）目标函数 第一个固定参数为参数解向量
            constraints: tuple 约束条件元组
            hyperparams: dict 超参数
            conditions: dict 终止条件
            minimize: bool 最大化/最小化指示符
            optConfig: dict 优化算法设置
                'init': 群体初始化设置
                'no sorted': bool 是否在_rank_population中使用max()而非sorted()来找出best individual，从而获得更快的执行速度
            outConfig: dict 优化器输出设置
        """
        if hyperparams is None:
            hyperparams = hyperparams_WhaleOpt_default
        if conditions is None:
            conditions = conditions_WhaleOpt_default
        if optConfig is None:
            optConfig = optConfig_WhaleOpt_default
        if outConfig is None:
            outConfig = outConfig_WhaleOpt_default
        super().__init__(object_fn, constraints, hyperparams, conditions, minimize, outConfig)
        # hyper parameters
        self._num_indiv = self._hyperparams['individual number']
        self._a = self._hyperparams['a']
        self._b = self._hyperparams['b']
        self._step_a = self._hyperparams['step_a']
        self._step_b = self._hyperparams['step_b']
        self._select_threshold = self._hyperparams['select threshold']
        self.current_a = copy.deepcopy(self._a)
        self.current_b = copy.deepcopy(self._b)

        self._optConfig = optConfig
        self.inds_rank = [None] * self._num_indiv  # 群体中各个个体的适应度排名索引（None即该名次索引未得到）
        self._dim = len(self._constraints)
        self.population = np.zeros(shape=(self._num_indiv, self._dim))
        if 'generate times' in self._conditions:
            self._num_gener = self._conditions['generate times']

    def _init_population(self):
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

    def _rank_population(self):
        """
        对当前群体排列，排列顺序由_minimize决定并修改inds_rank，最小化时从小到大；最大化时从大到小
        _optConfig中 'no sorted' 为True时，仅找出最佳个体的索引
        """
        # time_point_start_rank = time.perf_counter()  # HACK
        fitness = [self._object(indiv) for indiv in self.population]
        if 'no sorted' in self._optConfig and self._optConfig['no sorted']:  # 仅找出最佳个体
            if self._minimize:
                self.inds_rank[0] = np.argmin(fitness)
            else:
                self.inds_rank[0] = np.argmin(-fitness)
        else:  # 对所有个体排序
            if self._minimize:
                self.inds_rank = list(np.argsort(fitness))
            else:
                self.inds_rank = list(np.argsort(-fitness))
        # time_point_end_rank = time.perf_counter()  # HACK
        # print(f'Spend {(time_point_end_rank - time_point_start_rank):.4n}s on this rank!')  # HACK

    def generate(self):
        """
        进行一次迭代，生成下一代群体。在执行前必须已经执行了_rank_population使inds_rank更新到当前群体的排列后索引
        Returns:
            popul_next: 2d-ndarray (_num_indiv, _dim) 迭代后的下一代群体
        """
        popul_next = []
        indiv_best = self.population[self.inds_rank[0]]
        for index, indiv in zip(range(self.population.shape[0]), self.population):  # 依次遍历所有个体，计算得到他们各自移动后得到的下一代个体
            if index == self.inds_rank[0]:  # 最佳个体不改变
                indiv_next = indiv
            else:
                if np.random.uniform(0.0, 1.0) > self._select_threshold:  # updating方式一：shrinking encircling
                    A = self._compute_A()
                    norm_A = np.linalg.norm(A)
                    if norm_A < 1.0:  # exploitation
                        # 以最佳个体为目标
                        indiv_target = indiv_best
                    else:  # exploration
                        # 以最佳随机为目标
                        indiv_target = self.population[np.random.randint(self.population.shape[0])]
                    indiv_next = self._encircle(indiv, indiv_target, A)
                else:  # xyw: updating方式二：spiral
                    # 以最佳个体为目标
                    indiv_target = indiv_best
                    indiv_next = self._spiral(indiv, indiv_target)

                # 约束化indiv_next
                for ind_params in range(self._dim):
                    if self._constraints[ind_params][0] > indiv_next[ind_params]:  # 下界约束
                        indiv_next[ind_params] = self._constraints[ind_params][0]
                    if self._constraints[ind_params][1] < indiv_next[ind_params]:  # 上界约束
                        indiv_next[ind_params] = self._constraints[ind_params][1]
            popul_next.append(indiv_next)  # 添加到下一代群体中
        popul_next = np.stack(popul_next, axis=0)
        self.current_a -= self._step_a  # 递减参数a
        self.current_b -= self._step_b  # 递减参数b
        return popul_next

    def _compute_A(self):
        r = np.random.uniform(0.0, 1.0, size=self._dim)
        return (2.0 * np.multiply(self.current_a, r)) - self.current_a

    def _compute_D(self, indiv, indiv_target, use_C=True):
        if use_C is True:
            C = 2.0 * np.random.uniform(0.0, 1.0, self._dim)
        else:
            C = np.ones(self._dim)
        D = abs(np.multiply(C, indiv_target) - indiv)
        return D

    def _encircle(self, indiv, indiv_target, A):  # updating方式一：shrinking encircling
        D = self._compute_D(indiv, indiv_target)
        return indiv_target - np.multiply(A, D)

    def _spiral(self, indiv, indiv_target):  # updating方式二：spiral
        D = self._compute_D(indiv, indiv_target, use_C=False)
        # L = np.random.uniform(-1.0, 1.0, size=self._dim)
        L = np.random.uniform(-1.0, 1.0, size=1)
        return np.multiply(np.multiply(D, np.exp(self.current_b * L)), np.cos(2.0 * np.pi * L)) + indiv_target

    def optimize(self):
        """
        根据已有设置进行优化，得到最终结果。在执行该方法时，属性population应该是初试群体。
        Returns:
        """
        self.population = self._init_population()
        self._rank_population()  # 每次迭代前必须排列找出最佳个体索引
        if self._outConfig['generation record'] or self._outConfig['each generation log']:
            # 对初试群体的种群和最佳个体进行日志打印或记录
            indiv_best = self.population[self.inds_rank[0]]
            fitness_best = self._object(indiv_best)
            if self._outConfig['generation record']:
                opt_table = [(self.population, indiv_best, fitness_best)]
            if self._outConfig['each generation log']:
                print('The init population:')
                print(f'    The best individual: {indiv_best}')
                print(f'    The best fitness: {fitness_best:.4n}')
        for _ in range(self._num_gener):
            self.population = self.generate()  # 迭代生成
            self._rank_population()
            if self._outConfig['generation record'] or self._outConfig['each generation log']:
                # 对更新后群体的种群和最佳个体进行日志打印或记录
                indiv_best = self.population[self.inds_rank[0]]
                fitness_best = self._object(indiv_best)
                if self._outConfig['generation record']:
                    opt_table.append((self.population, indiv_best, fitness_best))
                if self._outConfig['each generation log'] or (self._outConfig['final log'] and _+1 == self._num_gener):
                    print(f'The No.{_+1:n} generate:')
                    print(f'    The best individual: {indiv_best}')
                    print(f'    The best fitness: {fitness_best:.4n}')
        if not self._outConfig['generation record']:
            return self.population, self.inds_rank
        else:
            return self.population, self.inds_rank, opt_table
