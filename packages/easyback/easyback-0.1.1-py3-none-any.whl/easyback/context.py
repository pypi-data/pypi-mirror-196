'''
    全局上下文信息,全局属性均只有一个
'''

import datetime as dt

from easyback.vex import DataSlice,Trade
import easyback.broker.account as at

# import easyback.broker.account as ac



def singleton(cls):
    _instance = {}

    def inner():
        if cls not in _instance:
            _instance[cls] = cls()
        return _instance[cls]
    return inner
    
@singleton
class Context(object):
    '''
        全局上下文对象
    '''
    def __init__(self):
        self.current_date:dt.datetime = None
        self.g_account:at.Account  = None
        self.ds :DataSlice = None

# 全局对象
ctx:Context = Context()

