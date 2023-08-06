# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File     : kinetic_modeling.py
@Project  : PerfusionCompartmentModel
@Software : PyCharm
@Author   : Xiong YiWei
@Time     : 2021/11/17 20:14
-------------------------------------------------------------------------------
@Last Modify Time      @Version     @Description
2022/06/29 20:41        beta
"""

import copy
from scipy import interpolate
from scipy.linalg import expm
from scipy.special import roots_legendre  # 实现gauss-legendre quadrature

from curve_fit import *


class Patient(object):
    """
    一位PET/CT动态扫描受测者的信息和扫描数据
    Attributes:
        data: dict 扫描数据
            timeData: ndarray 时间自变量数据
            activityData: dict 活度因变量数据
                artery: ndarray 肝动脉活度数据
                vein: ndarray 门静脉活度数据
                normal: ndarray 肝组织活度数据
                tumor: ndarray 肿瘤活度数据
        info: dict 受测者个人信息
    Methods:

    """

    def __init__(self, patientName=None, data=None, info=None):
        if patientName is None:
            self.patientName = 'anonymity'
        else:
            self.patientName = patientName
        if data is None:
            self.data = {
                'timeData': np.linspace(0, 1, 5),
                'activityData': {
                    'artery': np.linspace(0, 0, 5),
                    'vein': np.linspace(0, 0, 5),
                    'normal': np.linspace(0, 0, 5),
                    'tumor': np.linspace(0, 0, 5)
                }
            }
        else:
            timeLen = len(data['time'])  # 时间向量长度，即扫描总帧数
            self.data = {
                'timeData': data['time'],
                'activityData': {
                    'artery': np.linspace(0, 0, timeLen),
                    'vein': np.linspace(0, 0, timeLen),
                    'normal': np.linspace(0, 0, timeLen),
                    'tumor': np.linspace(0, 0, timeLen)
                }
            }  # 初始化data为空数据
            if isinstance(data['concentration'], list):
                for time_cnt in range(timeLen):  # 迭代为各帧赋初始值
                    self.data['activityData']['artery'][time_cnt] = data['concentration'][time_cnt]['artery']
                    self.data['activityData']['vein'][time_cnt] = data['concentration'][time_cnt]['vein']
                    self.data['activityData']['normal'][time_cnt] = data['concentration'][time_cnt]['normal']
                    self.data['activityData']['tumor'][time_cnt] = data['concentration'][time_cnt]['tumor']
            elif isinstance(data['concentration'], dict):
                self.data['activityData'] = data['concentration']

        if info is None:
            self.info = {'weight': 0, 'height': 0, 'sex': None}
        else:
            self.info = info

    def update_data(self, new_data):
        self.data = new_data

    def update_info(self, new_info):
        self.info = new_info

    def reset_params(self):
        params = [1.00, 1.00, 0.20, 0.02, 0.50, 0.05]
        self.err = 0.0
        self.err_err = 0.0
        return params, self.err, self.err_err


class CompartmentModel(object):
    """
    房室模型 class
    TODO: 更多
    """

    def __init__(self, modelName=None, **kws):
        if modelName is None:
            self.modelName = 'nothing'
        else:
            self.modelName = modelName
        if modelName == '2input3compart':
            self.params_l = ['k1', 'k2', 'k3', 'k4', 'fa', 'vb']


class CompartmentModelling(Patient):  # 以 Patient 为父类、
    """
    对一例受测者的dPET活度数据进行房室模型参数估计
    Attributes:
        attributes from class Patient
        model: CompartmentModel 使用的房室模型
        interpData: dict 插值处理后的数据
    Methods:
        compartment_model_tissue_out: 计算给定动力学参数下的模型组织输出
        compartment_model_residual: 计算给定动力学参数下的模型组织输出和实测组织输出之间的残留误差，误差公式形式由kws给定
        model_params_estimate: 使用curve_fit模块执行优化算法来拟合模型曲线，得到参数估计结果
    """
    def __init__(self, patientName=None, data=None, info=None, model=CompartmentModel(), n_quad=8):
        super().__init__(patientName, data, info)  # 对父类（Patient）的 __init__ 调用
        self.model = model
        self.interpData = copy.deepcopy(self.data)
        self.r, self.w = roots_legendre(n_quad)

    def compartment_model_tissue_out(self, params, **kws):
        """
        房室模型的肝脏输出函数，以params为参数，计算args中血流输入下的肝脏输出
        Args:
            params: 1-d ndarray 房室模型参数数组
                0: k1
                1: k2
                2: k3
                3: k4
                4: fa
                5: vb
            **kws:

        Returns: 2-d ndarray 时间自变量-活度因变量 输出TAC曲线计算结果
            0 ndarray 时间自变量
            1 ndarray 活度因变量

        """
        if self.model.modelName == '2input3compart':  # 模型为 双输入三房室模型 时
            # 初始化
            k1 = params[0]
            k2 = params[1]
            k3 = params[2]
            k4 = params[3]
            fa = params[4]
            vb = params[5]
            x_time = self.data['timeData']  # 各输入、输出函数时间自变量
            i_artery = self.data['activityData']['artery']  # 肝动脉输入函数活度因变量
            i_vein = self.data['activityData']['vein']  # 门静脉输入函数活度因变量

            # time_point_1 = time.perf_counter()  # HACK
            if x_time[0] != 0.:  # 添加零点
                x_time = np.insert(x_time, 0, 0)
                i_artery = np.insert(i_artery, 0, 0)
                i_vein = np.insert(i_vein, 0, 0)
            i_blood = fa * i_artery + (1 - fa) * i_vein

            def fun_i_blood(t):  # 插值得到其他时间帧的i_blood（因为fun_quadrature涉及到计算其他时间帧的浓度值）
                return interpolate.pchip_interpolate(x_time, i_blood, t)

            M = np.array([[-(k2 + k3), k4], [k3, -k4]])
            C = np.mat(np.zeros((2, len(x_time))))

            def quadrature(fun, low, up):  # 用roots和weights进行gauss-legendre求定积分
                value = np.mat([[0.], [0.]])
                for i in range(len(self.r)):  # noqa
                    value += (up - low) / 2 * self.w[i] * fun((up - low) / 2 * self.r[i] + (low + up) / 2)
                return value

            for i in range(len(x_time[1:])):
                ind_time = i + 1

                def fun_quadrature(tau):  # 该函数为gauss-legendre quadrature的被积分函数
                    return k1 * np.mat(expm(M * (x_time[ind_time] - tau))) * np.mat([[fun_i_blood(tau)], [0]])

                # time_point_start_oneFrame = time.perf_counter()  # HACK
                C[:, ind_time] = np.mat(expm((x_time[ind_time] - x_time[ind_time - 1]) * M)) * \
                    C[:, ind_time - 1] + quadrature(fun_quadrature, x_time[ind_time - 1], x_time[ind_time])
                # time_point_end_oneFrame = time.perf_counter()  # HACK
                # print(f'Spend {(time_point_end_oneFrame - time_point_start_oneFrame):.4n}s on the calculation \
# of No.{ind_time:n} frame!')  # HACK
            o_tissue = (np.mat([1 - vb, 1 - vb]) * C).A.reshape(-1) + vb * i_blood
            if x_time[0] == 0.:  # 把添加的零点去除
                x_time = x_time[1:]
                o_tissue = o_tissue[1:]

            outCurve_tissue = np.concatenate((x_time.reshape((1, len(x_time))), o_tissue.reshape((1, len(x_time)))),
                                             axis=0)
            # time_point_2 = time.perf_counter()  # HACK
            # print(f'Spend {(time_point_2 - time_point_1):.4n}s on this calculation of tissue_out!')  # HACK
            return outCurve_tissue

    def compartment_model_residual(self, params, *args, **kws):
        """
        房室模型的残留误差函数，将在minimize调用时作为参数，迭代寻找最佳params使残留误差最小化
        Args:
            params: dict 参数字典
                key str 为参数的名称标识
                    (1) modelName = '2input3compart' 时，key如下
                    'k1'、'k2'、'k3'、'k4'、'fa'、'vb'
                word 为参数取值
            kws: dict
                'out_option': str 指定输出项（必须） (1):'normal' (2):'tumor'

        Returns:
            residual: 计算出的残留误差值
        """
        assert 'out_option' in kws, '必须在kws的out_option中指定以normal还是tumor为输出项'
        # 初始化
        # 输出函数因变量 测量数据
        y_tissue = self.data['activityData'][kws['out_option']]
        # 计算当前参数的模型输出函数因变量 拟合数据
        y_tissue_fit = (self.compartment_model_tissue_out(params, **kws))[1]
        # 计算残留误差residual
        if 'time weight' in kws:
            error_series = kws['time weight'] * (y_tissue - y_tissue_fit)
        else:
            error_series = y_tissue - y_tissue_fit
        if kws['out_form'] == 'SSE_value':
            residual = sum(error_series ** 2.0)
        elif kws['out_form'] == 'MSE_value':
            residual = sum(error_series ** 2.0) / len(y_tissue)
        elif kws['out_form'] == 'RMSE_value':
            residual = np.sqrt(sum(error_series ** 2.0) / len(y_tissue))
        elif kws['out_form'] == 'error_series':
            residual = error_series
        else:
            residual = np.sqrt(sum(error_series ** 2.0) / len(y_tissue))
        return residual

    def compartment_model_compute_new_residual(self, new_params, **kws):
        res = self.compartment_model_residual(self, new_params, **kws)
        return res

    def model_params_estimate(self, param_l, out_option, method):
        """
        Args:
            param_l: list 包含各参数的起始值、下界和上界
                0 ndarray 各参数起始值一维数组
                1 ndarray 各参数下界一维数组
                2 ndarray 各参数上界一维数组
            out_option: str 选择哪个TAC输出曲线数据作为目标函数输出
                (1) 'normal'
                (2) 'tumor'
            method: dict 指定参数估计所用的算法

        Returns:
            result:

        """
        # region 参数设置
        if len(param_l) == 3:
            p_l = param_l[0]
            min_l = param_l[1]
            max_l = param_l[2]
            init_params = p_l
            paramsBounds = (min_l, max_l)
        elif len(param_l) == 2:
            min_l = param_l[0]
            max_l = param_l[1]
            init_params = None
            paramsBounds = (min_l, max_l)
        else:
            init_params = None
            paramsBounds = None
        # endregion

        # 执行参数估计
        kws = {}
        if 'time weight' in method['others']['optConfig']:
            kws.update({'time weight': method['others']['optConfig']['time weight']})
        result = curve_fit(self.compartment_model_residual, paramsBounds, init_params=init_params, method=method,
                           **{**kws, 'out_option': out_option})
        return result
