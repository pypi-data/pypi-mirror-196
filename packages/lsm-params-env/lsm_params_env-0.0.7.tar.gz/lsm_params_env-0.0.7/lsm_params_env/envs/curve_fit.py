# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File     : curve_fit.py
@Project  : PerfusionCompartmentModel
@Software : PyCharm
@Author   : Xiong YiWei
@Time     : 2022/3/15 19:11
-------------------------------------------------------
                    @Description
            kinetic_modeling.py的曲线拟合模块
-------------------------------------------------------
@Last Modify Time      @Version     @Description
2022/3/15 19:11        1.0             None
"""

import numpy as np
from scipy.optimize import least_squares  # 用于实现LM算法的模型参数估计
import geatpy as ea  # http://geatpy.com/
import scipy.stats as stats
from opt_selfimple.whaleOpt import WhaleOpt  # 鲸鱼优化
from opt_selfimple.gaOpt import GaOpt  # 遗传算法
from opt_selfimple.pso import Pso  # 粒子群优化


method_default = {
    'name': 'trf'
}


def curve_fit(fn_residual, paramsBounds, init_params=None, method=None, **kws):
    """
    对模型输出TAC曲线拟合
    Args:
        fn_residual: callable 要进行最小化的residual函数
        paramsBounds: tuple 参数上下界
            0 list 参数下界列表
            1 list 参数上界列表
        init_params: array-like 初始参数
        method: dict 优化算法
        kws: 传给fn_residual的关键字参数
            out_option: str 选择哪个TAC输出曲线数据作为目标函数输出
                (1) 'normal'
                (2) 'tumor'

    Returns: CurveFitRes 曲线拟合结果

    """
    if method is None:
        method = method_default
    if method['name'] == 'lm':
        out_form = 'error_series'
        res = least_squares(fn_residual, init_params, jac='2-point', bounds=paramsBounds, method='lm',
                            kwargs={**kws, 'out_form': out_form})  # kwargs将传给fn_residual的kws
        final_params = res.x
        residual_value = fn_residual(final_params, **{**kws, 'out_form': 'RMSE_value'})
        residual = {'RMSE': residual_value}
        return CurveFitRes(final_params, residual)
    elif method['name'] == 'trf':
        if 'init' in method['others']['optConfig']:
            if method['others']['optConfig']['init']['init type'] == 'normal':
                init_params = [stats.truncnorm((l - mu) / sigma, (u - mu) / sigma, loc=mu, scale=sigma).rvs(1)[0]
                               for mu, sigma, l, u in
                               zip(method['others']['optConfig']['init']['init info']['mean'],
                                   method['others']['optConfig']['init']['init info']['std'],
                                   paramsBounds[0], paramsBounds[1])]
        res = least_squares(fn_residual, init_params, jac='3-point', bounds=paramsBounds, method='trf',
                            kwargs={**kws, 'out_form': 'error_series'})  # kwargs将传给fn_residual的kws
        final_params = res.x
        residual_value = fn_residual(final_params, **{**kws, 'out_form': 'RMSE_value'})
        residual = {'RMSE': residual_value}
        return CurveFitRes(final_params, residual)
    elif method['name'] == 'SGA' or method['name'] == 'EGA' or method['name'] == 'SEGA':

        @ea.Problem.single
        def evalVars(Vars):  # 定义专属的目标函数（含约束）
            f = fn_residual(Vars, **{**kws, 'out_form': 'RMSE_value'})
            CV = 0
            return f, CV

        constraints = []
        for lower, upper in zip(paramsBounds[0], paramsBounds[1]):
            constraints.append((lower, upper))
        if method['others']['optConfig']['init'] == 'normal':  # 状态分布初始化
            popul = [stats.truncnorm((c[0] - mu) / sigma, (c[1] - mu) / sigma, loc=mu, scale=sigma)
                     .rvs(method['hyperparams']['individual number'])
                     for mu, sigma, c in
                     zip(method['others']['optConfig']['init']['init info']['mean'],
                         method['others']['optConfig']['init']['init info']['std'],
                         constraints)]
            prophet = np.stack(popul, axis=-1)
        else:
            prophet = None
        dim = len(paramsBounds[0])
        problem = ea.Problem(name='TKM params estimation by ' + method['name'],
                             M=1,  # 目标函数维数
                             maxormins=[1],  # 目标最小最大化标记列表，1：最小化该目标；-1：最大化该目标
                             Dim=dim,  # 参数变量维数
                             varTypes=[0]*dim,  # 决策变量的类型列表，0：实数；1：整数
                             lb=paramsBounds[0],  # 决策变量下界
                             ub=paramsBounds[1],  # 决策变量上界
                             evalVars=evalVars)
        if method['name'] == 'SGA':
            algorithm = ea.soea_SGA_templet(problem,
                                            ea.Population(Encoding='RI',
                                                          NIND=method['hyperparams']['individual number']),
                                            MAXGEN=method['conditions']['generate time'],  # 最大进化代数
                                            # logTras=1,  # 表示每隔多少代记录一次日志信息，0表示不记录
                                            logTras=0,  # 表示每隔多少代记录一次日志信息，0表示不记录
                                            trappedValue=1e-6,  # 单目标优化陷入停滞的判断阈值
                                            maxTrappedCount=10)  # 进化停滞计数器最大上限值
        elif method['name'] == 'EGA':
            algorithm = ea.soea_EGA_templet(problem,
                                            ea.Population(Encoding='RI',
                                                          NIND=method['hyperparams']['individual number']),
                                            MAXGEN=method['conditions']['generate time'],  # 最大进化代数
                                            # logTras=1,  # 表示每隔多少代记录一次日志信息，0表示不记录
                                            logTras=0,  # 表示每隔多少代记录一次日志信息，0表示不记录
                                            trappedValue=1e-6,  # 单目标优化陷入停滞的判断阈值
                                            maxTrappedCount=10)  # 进化停滞计数器最大上限值
        else:  # SEGA
            algorithm = ea.soea_SEGA_templet(problem,
                                             ea.Population(Encoding='RI',
                                                           NIND=method['hyperparams']['individual number']),
                                             MAXGEN=method['conditions']['generate time'],  # 最大进化代数
                                             # logTras=1,  # 表示每隔多少代记录一次日志信息，0表示不记录
                                             logTras=0,  # 表示每隔多少代记录一次日志信息，0表示不记录
                                             trappedValue=1e-6,  # 单目标优化陷入停滞的判断阈值
                                             maxTrappedCount=10)  # 进化停滞计数器最大上限值
        res = ea.optimize(algorithm,
                          seed=1,  # 随机数种子
                          prophet=prophet,  # 先验知识
                          verbose=True,  # 控制是否在输入输出流中打印输出日志信息
                          drawing=0,  # 算法类控制绘图方式的参数，0表示不绘图；1表示绘制最终结果图；2表示实时绘制目标空间动态图；3表示实时绘制决策空间动态图
                          outputMsg=False,  # 控制是否输出结果以及相关指标信息
                          drawLog=False,  # 用于控制是否根据日志绘制迭代变化图像
                          saveFlag=False,  # 控制是否保存结果
                          dirName='result')  # 文件保存的路径
        final_params = (res['Vars'].tolist())[0]
        residual_value = fn_residual(final_params, **{**kws, 'out_form': 'RMSE_value'})
        residual = {'RMSE': residual_value}
        return CurveFitRes(final_params, residual)
    elif method['name'] == 'GA':

        def object_fn(params):
            f = fn_residual(params, **{**kws, 'out_form': 'RMSE_value'})
            return f

        constraints = tuple(((paramsBounds[0][idx], paramsBounds[1][idx]) for idx in range(len(paramsBounds[0]))))
        hyperparams = {
            'individual number': method['hyperparams']['individual number'],
            'mutation probability': method['hyperparams']['mutation probability'],
            'precision': method['hyperparams']['precision']
        }
        conditions = {
            'generate times': method['conditions']['generate time'],
        }
        isMinim = True
        optConfig = method['others']['optConfig']
        outConfig = method['others']['outConfig']
        ga_opter = GaOpt(object_fn, constraints, hyperparams, conditions, isMinim, optConfig, outConfig)
        final_params = ga_opter.optimize()
        residual_value = object_fn(final_params)
        residual = {'RMSE': residual_value}  # 最终的残留误差类型及值
        return CurveFitRes(final_params, residual)
    elif method['name'] == 'PSO':

        def object_fn(params):
            f = fn_residual(params, **{**kws, 'out_form': 'RMSE_value'})
            return f

        constraints = tuple(((paramsBounds[0][idx], paramsBounds[1][idx]) for idx in range(len(paramsBounds[0]))))
        hyperparams = {
            'individual number': method['hyperparams']['individual number'],
            'w': method['hyperparams']['w'],
            'c1': method['hyperparams']['c1'],
            'c2': method['hyperparams']['c2'],
            'v_max': method['hyperparams']['v_max']
        }
        conditions = {
            'generate times': method['conditions']['generate time'],
        }
        isMinim = True
        optConfig = method['others']['optConfig']
        outConfig = method['others']['outConfig']
        pso_opter = Pso(object_fn, constraints, hyperparams, conditions, isMinim, optConfig, outConfig)
        final_params = pso_opter.optimize()
        residual_value = object_fn(final_params)
        residual = {'RMSE': residual_value}  # 最终的残留误差类型及值
        return CurveFitRes(final_params, residual)
    elif method['name'] == 'WOA':

        def object_fn(params):
            f = fn_residual(params, **{**kws, 'out_form': 'RMSE_value'})
            return f

        constraints = tuple(((paramsBounds[0][idx], paramsBounds[1][idx]) for idx in range(len(paramsBounds[0]))))
        hyperparams = {
            'individual number': method['hyperparams']['individual number'],
            'a': method['hyperparams']['a'],
            'b': method['hyperparams']['b'],
            'step_a': method['hyperparams']['step_a'],
            'step_b': method['hyperparams']['step_b'],
            'select threshold': method['hyperparams']['select threshold'],
        }
        conditions = {
            'generate times': method['conditions']['generate time'],
        }
        isMinim = True
        optConfig = method['others']['optConfig']
        outConfig = method['others']['outConfig']
        woa_opter = WhaleOpt(object_fn, constraints, hyperparams, conditions, isMinim, optConfig, outConfig)
        res = woa_opter.optimize()
        popul_final = res[0]
        idxs_rank = res[1]
        final_params = popul_final[idxs_rank[0]]  # 拟合最后得到的参数解
        residual_value = object_fn(final_params)
        residual = {'RMSE': residual_value}  # 最终的残留误差类型及值
        if not outConfig['generation record']:
            return CurveFitRes(final_params, residual)
        else:
            opt_table = res[2]
            return CurveFitRes(final_params, residual, generation=opt_table)
    else:
        raise Exception('没有给出正确的method配置')


class CurveFitRes(object):
    """
    对TAC曲线进行拟合得到的结果数据
    TODO: 增加内容
    """

    def __init__(self, final_params, residual, generation=None):
        """

        Args:
            final_params: array-like 最终的参数结果列表
            residual: dict 拟合结果的残留误差
            generation: 群体算法的迭代记录
        """
        self.final_params = {
            'k1': final_params[0],
            'k2': final_params[1],
            'k3': final_params[2],
            'k4': final_params[3],
            'fa': final_params[4],
            'vb': final_params[5]
        }
        self.residual = residual
        self.generation = generation
