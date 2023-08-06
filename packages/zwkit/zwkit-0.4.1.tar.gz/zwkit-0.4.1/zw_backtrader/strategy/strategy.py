import backtrader as bt
import joblib
import pandas as pd
import os
from kit import date_kit


class base_strategy(bt.Strategy):
    """
    策略基类
    """

    params = (
        ('model_path', ""),
        ('log_path', '../data/backtrader/'),
        ('log_name', f'logs_{date_kit.now()}.log'),
    )

    def __init__(self):
        # 买卖列表
        self.buying_list = []
        self.selling_list = []
        self.log_text = []

    def log(self, txt, dt=None):
        """
        Logging function fot this strategy
        :param txt:
        :param dt:
        :return:
        """
        dt = dt or self.datas[0].datetime.date(0)
        self.log_text.append(f'{dt.isoformat()}: {txt}')
        print(f'{dt.isoformat()}: {txt}')

    def start(self):
        """
        策略启动时执行
        :return:
        """
        self.model = joblib.load(self.params.model_path)

    # def prenext(self):
    #     '''策略准备阶段,对应第1根bar ~ 第 min_period-1 根bar'''
    #     # 该函数主要用于等待指标计算，指标计算完成前都会默认调用prenext()空函数
    #     # min_period 就是 __init__ 中计算完成所有指标的第1个值所需的最小时间段
    #     print('prenext函数')
    #
    # def nextstart(self):
    #     '''策略正常运行的第一个时点，对应第 min_period 根bar'''
    #     # 只有在 __init__ 中所有指标都有值可用的情况下，才会开始运行策略
    #     # nextstart()只运行一次，主要用于告知后面可以开始启动 next() 了
    #     # nextstart()的默认实现是简单地调用next(),所以next中的策略逻辑从第 min_period根bar就已经开始执行
    #     print('nextstart函数')

    def next(self):
        # 获取每只股票的信息
        # 并放入模型验证
        for index in range(len(self.datas)):
            data = self._get_data(datas=self.datas[index], index=index)
            if self.model.predict(data) == 1:
                self.log(f'买入{self.datas[index]._name}')

    def _get_data(self, datas, index):
        data = pd.DataFrame()
        for v, k in enumerate(datas._colmapping):
            if self.data.data_schema is not None:
                if k not in self.data.data_schema:
                    continue
                exec(f"data.loc[0,'{k}'] = self.datas[index].lines.{k}[0]")
        return data

    def stop(self):
        """
        策略结束时执行
        将日志进行保存
        :return:
        """
        if os.path.exists(self.params.log_path) is False:
            os.mkdir(self.params.log_path)

        with open(self.params.log_path+self.params.log_name, mode='w') as f:
            f.write('\n'.join(self.log_text))

# class test_strategy(bt.Strategy):
#     """
#     策略基类
#     """
#
#     def __init__(self):
#         # 买卖列表
#         self.buying_list = []
#         self.selling_list = []
#
#     def next(self):
#         for index in range(len(self.datas)):
#             data = self._get_data(datas=self.datas[index], index=index)
#             print(data)
#
#             # 进行预测
#
#     def _get_data(self, datas, index):
#         data = pd.DataFrame()
#         for v, k in enumerate(datas._colmapping):
#             if k is None:
#                 continue
#             exec(f"data.loc['{k}',0] = self.datas[index].lines.{k}[0]")
#         return data
