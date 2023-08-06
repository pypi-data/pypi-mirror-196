import pandas as pd
import pywencai as wc
import tushare as ts
import os
from kit import num_kit

'''
数据函数
'''


# 导入工程
class dataset_loader:
    """
    数据加载器
    通过问财获得股票列表
    通过tushare获得股票数据
    """

    def __init__(self, question, start, end, token):
        self.question = question
        self.start = start
        self.end = end
        self.token = token
        self.symbols_list = None  # 股票列表
        self.symbol_index = dict()  # 股票时间索引
        self.filter = set()
        self.data = pd.DataFrame()
        pass

    def __daily_data(self, symbol, start, end):
        """
        获取日线数据
        :param symbol:
        :param start:
        :param end:
        :return:
        """
        api = ts.pro_api(self.token)
        df = ts.pro_bar(
            ts_code=symbol,
            api=api,
            start_date=str(start) + "0101",
            end_date=str(end) + "1231",
            asset="E",  # E:沪深港通资金流向 F:港股通资金流向
            freq="D",  # D:日线 W:周 M:月
            adj="hfq",  # 不复权:None 前复权:qfq 后复权:hfq
            retry_count=99  # 重试次数
        )
        return df[::-1]

    def __daily(self, start_date, end_date, symbols=[]):
        """
        获取日线数据
        :param start_date:
        :param end_date:
        :param symbols:
        :return:
        """
        result = pd.DataFrame()
        if len(symbols) == 0:
            return pd.DataFrame()
        for symbol in symbols:
            df = self.__daily_data(symbol, start_date, end_date)
            result = pd.concat([result, df])
        return result

    def filter_symbols(self, symbols: list):
        """
        过滤数据列表
        :param symbols: 以列表的形式填入股票代码
        :return:
        """
        symbols_set = set(symbols)
        self.filter.update(symbols_set)

    def __get_symbols_by_wc(self, question, columns=[]):
        """
        股票列表
        通过问财获得股票列表
        """
        result = pd.DataFrame()
        for i in range(self.start, self.end + 1):
            quest = question % (i, i - 1)
            data = wc.get(question=quest, loop=True)
            data = data[columns]
            data = data[~data['股票代码'].isin(self.filter)]
            data['trade_date'] = i
            result = pd.concat([result, data])
        self.symbols_list = result
        return result

    def get_data(self, data_path='../data/data.csv'):
        """
        获取总数据集
        优先在本地读取，如果本地没有从互联网获取
        :param data_path: 默认的数据集路径
        :return:
        """
        if os.path.exists(data_path):
            print("读取本地数据集")
            self.data = pd.read_csv(data_path)

            # 本地数据缺少股票代码的时间索引
        else:
            print("从互联网获取数据集")
            symbols_list = self.__get_symbols_by_wc(self.question, columns=['股票代码'])
            print("从互联网获取数据集")
            for index, symbol in enumerate(symbols_list['股票代码'].unique()):
                print("数据进度百分比:%s" % (index / len(symbols_list['股票代码'].unique()) * 100), end="\r")
                # 获取股票代码的符合的年数据
                symbol_data = symbols_list[symbols_list['股票代码'] == symbol]
                # 获取股票代码的年数据的时间集合
                self.symbol_index.update({symbol: num_kit.date_split(symbol_data['trade_date'])})
                self.data = pd.concat([self.data, self.__daily_data(symbol, self.start, self.end)])
        return self.data

    def observe(self, mlflow):
        """
        观察数据集
        :return:
        """
        # 数据报告
        mlflow.log_text("data_report", "\n".join(self.__data_report()))
        # 新增数据集

    def save(self, file_path='../data/dataset.csv'):
        """
        保存数据集
        :param path:
        :return:
        """
        self.data.to_csv(file_path, index=False, encoding='utf-8')

    def __data_report(self):
        """
        数据报告
        常规基础数据
        :return:
        """
        data = []
        # stringbuffer的数据报告
        data.append("开始日期:%s" % self.start)
        data.append("结束日期:%s" % self.end)
        data.append("数据总量:%s" % len(self.data))
        data.append("数据列数:%s" % len(self.data.columns))
        data.append("数据列名:%s" % self.data.columns)
        data.append("数据集缺失值:%s" % self.data.isnull().sum())
        return data


# 特征工程
class dataset_feature:
    """
    数据特征工程
    1.添加特征
    2.观察数据集
    3.保存数据集
    """

    def __init__(self, data):
        self.base = data
        self.features_list = []
        self.data = pd.DataFrame()

    def add_feature(self, feature):
        """
        添加特征
        :param feature:
        :return:
        """
        for func in feature:
            self.features_list.append(func)
        # 添加特征后，重新初始化数据集

    def obverse(self):
        """
        观察数据集
        :return:
        """
        pass

    def save(self, path='../data/dataset.csv'):
        """
        保存数据集
        :param path:
        :return:
        """
        self.data.to_csv(path, index=False, encoding='utf-8')

    def execute(self):
        """
        执行特征工程
        :return:
        """
        symbol_list = self.base['ts_code'].unique()
        for symbol in symbol_list:
            symbol_data = pd.DataFrame(self.base[self.base['ts_code'] == symbol])
            for func in self.features_list:
                func(symbol_data)
            self.data = pd.concat([self.data, symbol_data])
        return self.data


# 训练测试工程
class dataset_train_test:

    def __init__(self, data, name):
        self.base = data
        self.name = name
        self.train_X = pd.DataFrame()
        self.train_y = pd.DataFrame()
        self.test_X = pd.DataFrame()
        self.test_y = pd.DataFrame()
        self.drop_column = []

    def drop_columns(self, columns):
        """
        删除指定列
        :param columns:
        :return:
        """
        for column in columns:
            self.drop_column.append(column)

    def train_split_by_time(self, start, end):
        """
        :param start:
        :param end:
        :return:
        """
        self.train_X = self.base[(self.base['trade_date'] > start) & (self.base['trade_date'] < end)]
        self.train_X = self.train_X.drop(self.drop_column, axis=1)
        self.train_y = self.base[(self.base['trade_date'] > start) & (self.base['trade_date'] < end)]
        self.train_y = self.train_y['flag']
        return self.train_X, self.train_y

    def test_split_by_time(self, start, end):
        """
        :param start:
        :param end:
        :return:
        """
        self.test_X = self.base[(self.base['trade_date'] > start) & (self.base['trade_date'] < end)]
        self.test_X = self.test_X.drop(self.drop_column, axis=1)
        self.test_y = self.base[(self.base['trade_date'] > start) & (self.base['trade_date'] < end)]
        self.test_y = self.test_y['flag']
        return self.test_X, self.test_y

    def obverse(self, mlflow):
        """
        观察数据集
        :return:
        """
        self.__data_report(self.train_X, self.train_y, mlflow)

    def __data_report(self, X, y, mlflow, name='train'):
        data_X = X.copy()
        data_y = y.copy()

        mlflow.log_metric("train_X_count", len(data_X))
        mlflow.log_metric("train_y_count", len(data_y))


    def save(self, path='../data/'):
        """
        保存数据集
        :param path:
        :return:
        """
        file_path = path + self.name + '/'
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        self.train_X.to_csv(file_path + 'train_X.csv', index=False, encoding='utf-8')
        self.train_y.to_csv(file_path + 'train_y.csv', index=False, encoding='utf-8')
        self.test_X.to_csv(file_path + 'test_X.csv', index=False, encoding='utf-8')
        self.test_y.to_csv(file_path + 'test_y.csv', index=False, encoding='utf-8')
        pass
