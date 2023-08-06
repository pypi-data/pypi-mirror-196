import backtrader as bt
import joblib
import pandas as pd


class base_strategy(bt.Strategy):
    """
    策略基类
    """

    # params = (
    #     ('model_path', ""),
    # )

    def __init__(self):
        # 买卖列表
        self.buying_list = []
        self.selling_list = []

    # 日志列表
    def log(self, txt, dt=None):
        """
        Logging function fot this strategy
        :param txt:
        :param dt:
        :return:
        """
        dt = dt or self.datas[0].datetime.date(0)
        print(f'{dt.isoformat()},{txt}')

    def start(self):
        """
        策略启动时执行
        :return:
        """
        # self.model = joblib.load(self.params.model_path)

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
            aliases = self.datas[index].lines.getlinealiases()
            data = {}
            for alias in aliases:
                data[alias] = getattr(self.datas[index].lines, alias)[0]
            # print(data)
            model_data = pd.DataFrame([data])
            model_data.drop(['datetime', 'open', 'high', 'low', 'close', 'volume', 'openinterest'], axis=1, inplace=True)
            ## 判断模型是否为1
            self.datas[index]._name
            if self.model.predict(model_data)[0] == 1:
                self.log('%s : %s , %s' % (self.datas[index].lines.datetime.date(0), self.datas[index]._name, "判断为1"))
            else:
                self.log('%s : %s , %s' % (self.datas[index].lines.datetime.date(0), self.datas[index]._name, "判断为0"))
        #         #buying_list.append(self.datas[index])
        #
        #         # 判断是否持仓 如果持仓 则忽略 否则计入买入列表
        #         if self.getposition(self.datas[index]).size != 0:
        #
        #             pass
        #
        #         #判断是否在持仓列表中，如果有则放入
        #
        # # 判断待买列表是否为空，否则选择几只买入

    # # 现金记录
    # def notify_cashvalue(self, cash, value):
    #     self.log('Cash: %.2f Value: %.2f' % (cash, value))
    #
    # def notify_order(self, order):
    #     self.log('Order ref: %s Status: %s' % (order.ref, order.getstatusname()))
    #
    # def stop(self):
    #     print('stop函数')
    #     pass

    def _get_data(self, datas, index):
        data = pd.DataFrame()
        for v, k in enumerate(datas._colmapping):
            if v is None:
                continue
            exec(f"data.loc[0,'{k}'] = self.datas[index].lines.{k}[0]")
        return data


class test_strategy(bt.Strategy):
    """
    策略基类
    """

    def __init__(self):
        # 买卖列表
        self.buying_list = []
        self.selling_list = []

    def next(self):
        for index in range(len(self.datas)):
            data = self._get_data(datas=self.datas[index], index=index)
            print(data)

            # 进行预测

    def _get_data(self, datas, index):
        data = pd.DataFrame()
        for v, k in enumerate(datas._colmapping):
            if v is None:
                continue
            exec(f"data.loc[0,'{k}'] = self.datas[index].lines.{k}[0]")
        return data
