'''
   交易相关信息
'''
import pandas as pd
import datetime as dt
from enum import Enum

from .quote import Quote
from easyback.utils.common_util import generate_random_str,create_key,time_2_date

import easyback.context as cs


class Order():
    '''
        订单信息
    '''
    class Action(Enum):
        '''操作 开、平操作'''
        OPEN = 'open'
        CLOSE = 'close'


    class Side(Enum):
        '''方向'''
        SHORT = 'short'# 空方向
        LONG = 'long' # 多方向
    
    class Status(Enum):
        # 订单新创建未委托，用于盘前/隔夜单，订单在开盘时变为 open 状态开始撮合
        NEW = 0 
        # 订单未完成, 无任何成交
        OPEN = 1
        # 订单未完成, 部分成交
        FILLED_PART = 2
        # 订单完成
        FILLED = 3
        # 订单取消
        CANCELD = 4
        # 订单被拒绝
        REJECTED = 5 
    
    
    class Type():
        def __init__(self) -> None:
            pass

    class MarketType(Type):
        '''市价类型'''

        def __init__(self) -> None:
            pass

    class LimitType(Type):
        '''限价类型'''

        def __init__(self, price: float) -> None:
            self.__order_price = price

        def get_order_price(self) -> float:
            return self.__order_price

    def __init__(self,symbol: str = None, side: Type = None, price: float = 0, action:Action = None, amount: float = None, datetime: dt.datetime=None):
        if datetime is None:
            datetime = cs.ctx.current_date
        self.id = dt.datetime.timestamp(dt.datetime.now())  # 订单ID,每次闯将都重新生成
        self.symbol :str = symbol   # 股票代码
        self.side :Order.Side= side  # 多/空，'long'/'short'
        self.action :Order.Action= action # 开/平， 'open'/'close'
        self.price :float= price  # 挂单价格
        self.amount : float= amount  # 下单数量, 不管是买还是卖, 都是正数
        self.fill_amount :float= 0  # 已经成交的股票数量, 正数
        self.cost_price :float= 0  # 成交成本价格(模拟，保持和挂单价格一直 cost_price = price)
        self.commission :float = 0  # 交易费用（佣金、税费等）
        self.status :Order.Status= 0  # 状态, 一个OrderStatus值
        self.create_time :dt.datetime= datetime  # 订单添加时间, [datetime.datetime]对象

    def get_key(self)->str:
        '''
            获取当前订单的key
        '''
        return create_key(self.symbol,self.side)

    def get_key_his(self)->str:
        '''
            获取历史订单的key
        '''
        return create_key(time_2_date(self.create_time),self.symbol,self.side)


class Trade():
    '''
        交易类
    '''

    def __init__(self) -> None:
        pass

        

def order(symbol:str,amount:float,type:Order.Type,side:Order.Side,action:Order.Action)->Order:
    '''按股数下单'''

    #获取最新的价格数据
    quote :pd.DataFrame = cs.ctx.ds.history(symbols=[symbol],length= 1)
    if quote.empty:
        return None

    # 这里直接完成订单交易,更新持仓信息，更新订单信息，同时返回订单ID
    # 使用最新的数据
    data_dict = quote.to_dict(orient='records')[-1]

    # 初始化订单
    order = Order(symbol=symbol,amount=amount,action=action,side=side)
    order.id = generate_random_str()
    order.status  = Order.Status.NEW

    if isinstance (type,Order.LimitType):
        order.price :float = type.get_order_price()
        if order.price < data_dict[Quote.Column.LOW.value] and order.price > data_dict[Quote.Column.HIGH.value]:
            # 限价可能无法成交，订单会处于挂单状态
            # TODO 需要增加对挂单状态的订单处理
            order.status = Order.Status.OPEN
            return order
    elif isinstance(type,Order.MarketType):
        order.price = data_dict[Quote.Column.CLOSE.value]

    if cs.ctx.g_account.check_position_available(order):
            order.status = Order.Status.FILLED
            order.cost_price = order.price
            order.fill_amount = order.amount
            cs.ctx.g_account.update_position(order)
            cs.ctx.g_account.update_account(order)
            cs.ctx.g_account.update_signal(order,data_dict)
    else:
        order.status = Order.Status.REJECTED
    print(f'Date:{cs.ctx.current_date} OrderId:{order.id} Action:{action} OrderPrice:{order.price} Amount:{order.amount} OrderStatus:{order.status}')
    return order

def order_target():
    '''目标股数下单'''
    pass


def order_value():
    '''按价值下单'''
    pass


def order_target_value():
    '''目标价值下单'''
    pass


def cancel_order():
    '''撤单'''
    pass


def get_open_orders():
    '''获取未完成订单'''
    pass


def get_orders():
    '''获取订单信息'''
    pass


def get_trades():
    '''获取成交信息'''
    pass

def update_position(self,order:Order):
    '''
        根据submit 状态的订单，更新持仓信息
    '''
    pass