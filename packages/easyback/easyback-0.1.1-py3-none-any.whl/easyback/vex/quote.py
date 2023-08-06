'''
    数据加载器
'''
import pandas as pd
import typing as tp
import datetime
import numpy as np
from  enum import Enum


import easyback.context as cs


class DataPeriodType(Enum):
    '''
        时间类型
    '''
    MIN1 = 'min1'
    MIN5 = 'min5'
    MIN10 = 'min10'
    D1 = 'day1'
    D5 = 'day5'
    D10 = 'day10'
    M1 = 'month1'
    M5 = 'month5'
    M10 = 'month10'
    Y1 = 'year1'

class Quote():
    ''' 行情数据 '''
    class Column(Enum):
        OPEN = 'open'
        CLOSE = 'close'
        HIGH = 'high'
        LOW = 'low'
        VOLUME ='volume'
        DATETIME = 'datetime'
        SYMBOL = 'symbol'

        @staticmethod
        def getValues()->tp.List[str]:
            '''
                获取所有的枚举值
            '''
            cln_names = []
            for i in Quote.Column:
                cln_names.append(i.value)
            return cln_names

    def __init__(self) -> None:
        pass


class DataSlice():
    '''数据切片'''
    def __init__(self,data:pd.DataFrame) -> None:
        # 初始时间索引
        if data is None or data.empty:
            return 
        
        self.data :pd.DataFrame = data
        self.data.index = pd.DatetimeIndex(self.data.index)

    def history(self,symbols :tp.List[str] = None,columns:tp.List[str]=None,bar_type:str = None,length:int = 0)->pd.DataFrame:
        '''获取历史数据，可查询多个标的单个数据字段，返回数据格式为DataFrame'''
        new_columns = []
        data : pd.DataFrame  =  self.data if symbols is None else  self.data.query(f'symbol in {symbols}')
        if columns is None:
            return data
        
        new_columns.extend(columns)
        new_columns.extend([Quote.Column.SYMBOL.value])
        temp =  data[new_columns]
        if not temp.empty:
            return temp.tail(length)
        return temp

class DataCenter():
    def __init__(self) -> None:
        # 所有数据
        self.data:pd.DataFrame = None
        # 最长步长,默认为1
        self.__max_step : int =  30
        # 当前时间
        self.__datetime_series = None

    def __check_data_available(self,data:pd.DataFrame)->bool:
        '''检测数据的可用信'''
        if data is None :
            return False;
    
        # 判断索引
        index_name:str = data.index.name
        if index_name is not None and index_name.lower() != Quote.Column.DATETIME.value:
            return False
        
        # 判断名称
        columns_name:tp.List[str]  = data.columns.to_list()
        if index_name is not None:
            columns_name.append(index_name)
        new_names = list(map(lambda x : x.lower(),columns_name))
        if not set(Quote.Column.getValues()) <= set(new_names):
            return False

        # 列名转换
        column_dict = {}
        for i in range(len(columns_name)):
            column_dict[columns_name[i]] = columns_name[i].lower()
        data.rename(columns=column_dict,inplace=True)

        # 索引转换
        if index_name is None:
            data.set_index(Quote.Column.DATETIME.value,inplace=True)

        elif index_name != Quote.Column.DATETIME.value:
            data.rename(index={index_name:Quote.Column.DATETIME.value},inplace=True)
        # data.index.astype(np.dtype('datetime64[ns]'))
        data.index = pd.DatetimeIndex(data.index)

        # 按照时间正序排列
        data.sort_index(ascending=True,inplace=True)

        # columns  = data.columns.tolist()
        # # 如果各种检测合格,之后按照时间升序排序
        # data.sort_values(by=self.__date_index,inplace=True,ascending=True)
        # # 重新设置索引（应为顺序可能会乱点,直接丢弃原来的索引）
        # data.set_index(context.INDEX_DATATIME,inplace=True,drop=False)
        return True


    def load_data(self,data:pd.DataFrame,dateType:DataPeriodType = DataPeriodType.D1):
        if self.__check_data_available(data):
            self.data = data
            self.__datetime_series = data.index.to_list() 
            return self
        raise Exception('数据格式不符合要求')
    

    def generate_data(self):
        '''日级别数据生成器'''
        min_date = min(self.__datetime_series)
        max_date = max(self.__datetime_series) 
        now = min_date - datetime.timedelta(days=1)

        while True:
            now = now +  datetime.timedelta(days=1)
            if now < min_date or now > max_date:
                # 数据超出范围,返回 None 数据
                yield None
            
            # 如果遍历的时间点不在时间序列中,继续循环
            # start_date = now - datetime.timedelta(days = self.__max_step)
            if now not in self.__datetime_series or self.__datetime_series.index(now) + 1 < self.__max_step:
                continue
            end_index = self.__datetime_series.index(now)
            # iloc  end_index 使用的是包含内容
            data_slice = self.data.iloc[end_index  + 1  - self.__max_step :end_index + 1]
            # 设置全局数据源头
            cs.ctx.ds = DataSlice(data_slice)
            # 返回最新的时间点
            yield now
    





    