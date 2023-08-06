 
import datetime as dt
import numpy as np
import typing as tp
import random
import math


def key_handler(*args):
    '''多个字段转换为key'''
    if args is not None:
        return '_'.join(map(lambda x : str(x),args))
    return None

def date_2_time(date:np.datetime64):
    return dt.datetime(date.year,date.month,date.day,0,0,0)

def time_2_date(time:dt.datetime):
    '''time 转换为 date'''
    return dt.date(time.year,time.month,time.day)

def time_2_date_str(time:dt.datetime):
    '''time 转换为 date'''
    return str(dt.date(time.year,time.month,time.day))


def generate_random_str(randomlength=16):
    """
    生成一个指定长度的随机字符串
    """
    random_str =''
    base_str ='ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
    length =len(base_str) -1
    for i in range(randomlength):
        random_str +=base_str[random.randint(0, length)]
    return random_str

def create_key(*args)->str:
    '''
        多个字段生成key
    '''
    if args is not None:
        return '_'.join(map(lambda x : str(x),args))
    return None

class IndicatorUtil():

    @staticmethod
    def return_series(datas: tp.List[float]) -> tp.List[float]:
        '''
        收益率序列
        datas：数值序列
        '''
        if datas is None or len(datas) < 2:
            return []
        next = datas[1:]
        now = datas[:-1]
        return ((np.array(next) - np.array(now)) / np.array(now)).tolist()

    @staticmethod
    def sharp_ratio(datas: tp.List[float]):
        '''
        夏普率
        datas: 收益率序列
        '''
        period = 252
        no_risk = 0
        n = len(datas)
        data = np.asarray(datas)
        erp_rf = data.sum()/n-no_risk/n
        sigmap = data.std()
        # 关于 period（数值，意义）：（252，日夏普），（52，周夏普），（12，月夏普），（1，年夏普）
        # 确认一下算法,这里计算的年sharp
        return erp_rf/sigmap*math.sqrt(period)
    @staticmethod
    def annual_return(datas:tp.List[float])->float or None:
        '''
        年化收益率

        '''
        if datas is None or len(datas) < 2 :
            return None
        # Rp=(1+R)^(m/n)-1
        return np.power((datas[-1] / datas[0]),252/(len(datas) - 1)) - 1
    @staticmethod
    def cum_return(datas:tp.List[float])->float or None:
        '''
        累计收益率
        '''
        if datas is None or len(datas) < 2 :
            return None
        return (datas[-1]/datas[0] - 1)
