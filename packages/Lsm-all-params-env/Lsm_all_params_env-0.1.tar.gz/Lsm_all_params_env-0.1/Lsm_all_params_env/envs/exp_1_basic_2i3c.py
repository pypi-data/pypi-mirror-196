# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File     : exp_1_basic_2i3c.py
@Project  : PerfusionCompartmentModel
@Software : PyCharm
@Author   : Xiong YiWei
@Time     : 2022/1/4 20:01
-------------------------------------------------------
                    @Description
             对三房室双输入模型的一次基础实验
-------------------------------------------------------
@Last Modify Time      @Version     @Description
2022/1/4 20:01        1.0             None
"""

import multiprocessing  # 多进程
from module_for_exp import *


def fun_exp_1_basic_2i3c(directory, param_l, model_str, method, config, **kws):  # noqa

    sheetName_l = load_workbook(filename=directory[0] + directory[1]).sheetnames
    model = CompartmentModel(model_str)

    # region 初始化用于存储实验结果的数据结构 tables
    tables = {}  # noqa
    for p in model.params_l:
        tables.update({p: pd.DataFrame([], columns=['name', 'N-value', 'T-value'])})
    tables.update({'RMSE': pd.DataFrame([], columns=['name', 'N-value', 'T-value'])})
    tables = {model.params_l[0]: pd.DataFrame([], columns=['name', 'N-value', 'T-value']),  # noqa
              model.params_l[1]: pd.DataFrame([], columns=['name', 'N-value', 'T-value']),
              model.params_l[2]: pd.DataFrame([], columns=['name', 'N-value', 'T-value']),
              model.params_l[3]: pd.DataFrame([], columns=['name', 'N-value', 'T-value']),
              model.params_l[4]: pd.DataFrame([], columns=['name', 'N-value', 'T-value']),
              model.params_l[5]: pd.DataFrame([], columns=['name', 'N-value', 'T-value']),
              'RMSE'           : pd.DataFrame([], columns=['name', 'N-value', 'T-value'])}
    # endregion 初始化用于存储实验结果的数据结构 tables

    kws_exp = {
        'plot': 'fit_compare'
    }

    time_point_1 = time.perf_counter()  # HACK

    if 'multiProcessing' in kws:  # 多进程进行实验
        # 生成args_l，在pool.map()传给函数exp_for_oneCase_oneArg
        args_l = []
        for sheetName in sheetName_l:
            kws_exp.update({'xlsx_sheetName': sheetName})
            args_l.append(
                (directory[0], directory[1], param_l, model, method, config, copy.deepcopy(kws_exp))
            )

        print('---------- S T A R T ----------')
        # multiprocessing.Pool进程池
        n_processor = kws['multiProcessing']['pool size']  # 设置进程池大小
        pool = multiprocessing.Pool(processes=n_processor)
        res_l = pool.map(exp_for_oneCase_oneArg, args_l)
        pool.close()
    else:  # 单进程进行实验
        res_l = []
        for sheetName in sheetName_l:  # 遍历数据文件中所有sheet进行实验
            kws_exp.update({'xlsx_sheetName': sheetName})
            patientName, res_normal, res_tumor = exp_for_oneCase(directory[0], directory[1], param_l, model, method,
                                                                 config, **kws_exp)
            res_l.append((patientName, res_normal, res_tumor))

    # region 导出到tables
    idx_table = 0
    for name, res_normal, res_tumor in res_l:
        for idx_p, p_str in enumerate(model.params_l):
            p_normal = res_normal.final_params[p_str]
            p_tumor = res_tumor.final_params[p_str]
            tables[p_str].loc[idx_table] = [name, p_normal, p_tumor]
        residual_normal = res_normal.residual['RMSE']
        residual_tumor = res_tumor.residual['RMSE']
        tables['RMSE'].loc[idx_table] = [name, residual_normal, residual_tumor]
        idx_table += 1
    # endregion 导出到tables

    time_point_2 = time.perf_counter()  # HACK
    print(f'Spend {(time_point_2 - time_point_1):.4n}s on all cases of exp!!!!!')  # HACK
    return tables


if __name__ == '__main__':
    directory = ('.//data//xlsx//5min+60min//', '5s_12frame 1min_4frame 1frame_at_60min 24cases.xlsx')
    # directory = ('.//data//xlsx//5min+60min//', '5s_12frame 1min_4frame 1frame_at_60min 4cases.xlsx')
    # region init and bound
    #                  k1    k2    k3    k4    fa    vb
    p0    = np.array([1.00, 1.00, 0.20, 0.02, 0.50, 0.05])  # 起始值
    min_p = np.array([0.00, 0.00, 0.00, 0.00, 0.01, 0.00])  # 最小值
    max_p = np.array([1.60, 1.60, 0.40, 0.20, 0.99, 0.40])  # 最大值
    # min_p = np.array([-np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf])  # 最小值
    # max_p = np.array([ np.inf,  np.inf,  np.inf,  np.inf,  np.inf,  np.inf])  # 最大值
    param_l = [p0, min_p, max_p]
    # endregion
    model_str = '2input3compart'
    # prior_info_2inout3compart = {
    #     # trf
    #     'all': {
    #         'mean': {'k1': 1.324, 'k2': 1.352, 'k3': 0.010, 'k4': 0.044, 'fa': 0.219, 'vb': 0.035},
    #         'std': {'k1': 0.406, 'k2': 0.394, 'k3': 0.045, 'k4': 0.069, 'fa': 0.392, 'vb': 0.081}
    #     }
    # }
    method = {
        'name': 'trf',
        'hyperparams': {
            # 'individual number': 8,
            # 'mutation probability': 0.01,
        },
        'conditions': {'generate time': 4},
        'others': {
            'optConfig': {
                'init': {
                    'init type': 'uniform',
                    'init info': {
                    }
                }
            },
            'outConfig': {
                'final log': False,
                'each generation log': False,
                'generation record': False
            }
        }
    }
    # splitConfig = {
    #     'start': 1,
    #     'end': 16
    # }
    config = {
        # 'splitConfig': splitConfig
    }
    kws_fun_exp_1 = {
        # 'multiProcessing': {'pool size': 4}
        # 'multiProcessing': {'pool size': 5}
        # 'multiProcessing': {'pool size': 6}
        # 'multiProcessing': {'pool size': 7}
        # 'multiProcessing': {'pool size': 8}
        # 'multiProcessing': {'pool size': 11}
        # 'multiProcessing': {'pool size': 14}
    }
    exp_str = 'exp_1_basic_' + \
              '_' + str(method['name']) + \
              '_5min+60min' + \
              '_uniform_init' + \
              '_0'

    repeat = 1
    # repeat = 20
    for i_exp in range(repeat):
        i_exp += 1  # 实验次数序号
        print(f'>>>>>> 第{i_exp:n}次实验：')
        tables = fun_exp_1_basic_2i3c(directory, param_l, model_str, method, config, **kws_fun_exp_1)

        outDirectory = './/output//'
        if repeat > 1:  # 多次重复实验时
            exp_str_end = exp_str + '_repeat_' + str(i_exp)
        elif repeat == 1:
            exp_str_end = exp_str
        else:
            exp_str_end = exp_str
        # 导出数据到xlsx工作簿
        export_paramsTables(outDirectory, exp_str_end, tables)
        # 生成实验统计报告
        report_exp_1(outDirectory, exp_str_end, tables)
