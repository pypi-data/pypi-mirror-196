# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File     : deOpt.py
@Project  : PerfusionCompartmentModel
@Software : PyCharm
@Author   : Xiong YiWei
@Time     : 2022/10/9 16:47
-------------------------------------------------------
                    @Description
    
-------------------------------------------------------
@Last Modify Time      @Version     @Description
2022/10/9 16:47        1.0             None
"""

from opt_selfimple.opt import Optimization
from sko.DE import DE
import numpy as np
import scipy.stats as stats
import copy


hyperparams_DeOpt_default = {
    'individual number': 50,
    'mutation probability': 0.01,
    'precision': 1e-7
}
conditions_DeOpt_default = {
    'generate times': 20
}
optConfig_DeOpt_default = {
    'init': {'init type': 'uniform'},
}
outConfig_DeOpt_default = {

}


class DeOpt(Optimization):
    def __init__(self, object_fn, constraints, hyperparams=None, conditions=None, minimize=True, optConfig=None,
                 outConfig=None):
        """
        遗传算法实现（scikit-opt）
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
        self._lb = np.array([lu[0] for lu in self._constraints])
        self._ub = np.array([lu[1] for lu in self._constraints])
        # hyper parameters
        self._num_indiv = self._hyperparams['individual number']
        self._p_mut = self._hyperparams['mutation probability']
        self._precision = self._hyperparams['precision']

        self._optConfig = optConfig
        self._dim = len(self._constraints)
        if 'generate times' in self._conditions:
            self._num_gener = self._conditions['generate times']

    def _init_population(self):
        """初始化群体并返回，返回的是未经编码的群体"""
        if self._optConfig['init']['init type'] == 'uniform':  # 均匀分布
            popul = np.random.uniform(low=self._lb, high=self._ub, size=(self._num_indiv, self._dim))
        elif self._optConfig['init']['init type'] == 'normal':  # 正态分布
            mean = self._optConfig['init']['init info']['mean']
            std = self._optConfig['init']['init info']['std']
            popul = stats.truncnorm((self._lb - mean) / std, (self._ub - mean) / std, loc=mean, scale=std).rvs(
                size=(self._num_indiv, self._dim))
        elif self._optConfig['init']['init type'] == 'histogram':  # 自定义直方图分布
            popul_raw = [stats.rv_histogram(histogram=hist).rvs(size=self._num_indiv) for hist in
                         self._optConfig['init']['init info']['histogram']]
            popul_raw = np.stack(popul_raw, axis=-1)
            popul = np.clip(popul_raw, self._lb, self._ub)  # 直方图的边界设定可能和constraint不同，故clip修正之
        elif self._optConfig['init']['init type'] == 'given':  # 使用直接给定的初始群体
            popul = self._optConfig['init']['init info']['given data']
        else:
            raise Exception('没有在_optConfig给出init设置！')
        return popul

    def optimize(self):
        """进行优化"""
        ga = GA(func=self._object,
                n_dim=self._dim,
                size_pop=self._num_indiv,
                max_iter=self._num_gener,
                prob_mut=self._p_mut,
                lb=self._lb, ub=self._ub,
                precision=self._precision
                )
        # region 初始化
        popul = self._init_population()
        ga.Chrom = ga.x2chrom(popul)
        # endregion
        best_x, best_y = ga.run()
        return best_x
