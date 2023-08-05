import datetime as dt
import pandas as pd
import typing as tp

# from .trade import Order
# 这个导入会收到 trade 文件中导入的影响
from easyback.vex import Quote,Order
from easyback.utils import create_key

# 全局变量
import easyback.context as cs



'''
    证券账户相关信息
'''
class Position():
    '''
        持仓信息
    '''

    # class Unit(object):
    #     '''这个是Order'''
    #     def __init__(self, symbol: str = None, side: Order.Type = None, price: float = 0,  amount: float = None, datetime: datetime.datetime = context.current_date) -> None:
    #         self.__datetime = datetime  # 日期
    #         self.__symbol: str = symbol  # 代码
    #         self.__side: Order.Type = side  # 多空
    #         self.__price: float = price
    #         self.__amount: float = amount

    def __init__(self,  symbol: str = None, side: Order.Type = None, cost_price: float = 0,  amount: float = None, datetime: dt.datetime = None) -> None:
        self.datetime: dt.datetime = 0  # 日期
        self.symbol: str = 0  # 代码
        self.side: Order.Side = 0  # 多空
        self.cost_price: float = 0  # 当日开仓成本
        self.closeable_amount: float = 0  # 可卖出数量
        self.pending_amount: float = 0  # 挂单数量
        self.open_amount: float = 0  # 当日开仓数量
        self.fill_amount: float = 0  # 当日成交数量
        self.total_amount: float = 0  # 总持仓数量(不包含挂单数量)
        self.total_cost_price: float = 0  # 总持仓成本

    def add_unit(self, unit: any):
        '''
            增加新的开仓单元
        '''
        pass

    def update(self, order: Order):
        # 根据order对象更新持仓信息 position
        pass


class Account():
    '''
        账户信息
    '''

    def __init__(self) -> None:
        # 历史持仓信息 key->value  key:date+symbol+side  value:Position
        self.his_positions: tp.Dict[str,  Position] = {}
        # 最新的持仓情况 key->value key:symbol+side  value:Position
        # ps: {'000001_long:Position}
        self.positions: tp.Dict[str, Position] = {}
        self.trade_signal: tp.Dict[str, pd.DataFrame] = {}

        self.available_cash = 1000000  # 可用资金, 可用来购买证券的资金
        self.start_assets = 0  # 初始资金, 现在等于 inout_cash

        # 实时计算的属性
        self.total_assets = 0  # 总的权益, 包括现金, 保证金(期货)或者仓位(股票)的总价值, 可用来计算收益
        self.total_value = 0     # 总的持仓价值
        self.his_assets : tp.Dict[dt.datetime,float] = {}# 历史每天的持仓情况  # 用来计算总资产

        # 暂时用不上的属性
        # self.datetime = 0  # 日期
        # self.lock_cash = 0  # 挂单锁住资金
        # 多单的仓位, 一个 dict, key 是证券代码, value 是 [Position]对象
        # self.long_positions = 0
        # 空单的仓位, 一个 dict, key 是证券代码, value 是 [Position]对象
        # self.short_positions = 0

    def init_account(self, cash: float):
        '''账户初始化'''
        self.start_assets = cash
        self.available_cash = self.start_assets

    def check_position_available(self, order: Order):
        '''检测持仓是否有效'''
        # 检测账户资金和持仓数量是否充足
        # side = order.side
        action = order.action
        amount = order.amount

        av: bool = None
        if action == Order.Action.OPEN and amount * order.price <= self.available_cash:  # 账户资金是否足够
            # order.status = Order.Status.FILLED
            av = True
        # 账户持仓数量是否足够，需要结合 SIDE 一起判断
        elif action == Order.Action.CLOSE and self.positions[order.get_key()] and self.positions[order.get_key()].closeable_amount >= amount:
            order.status = Order.Status.FILLED
            av = True
        else:
            # order.status = Order.Status.REJECTED
            av = False
        return av

    def update_position(self, order: Order):
        '''
            更新总仓位
        '''
        # 暂只接受全部成交订单
        if order.status != Order.Status.FILLED:
            return
        positon_key = order.get_key()
        if positon_key in self.positions:
            # 由于模拟测试，要么成交要么拒绝
            positon = self.positions[positon_key]
            # 开仓操作
            if order.action == Order.Action.OPEN:
                # 更新数量
                positon.open_amount = positon.open_amount + order.amount
                positon.fill_amount = positon.fill_amount + order.amount
                positon.total_amount = positon.total_amount + order.amount
                # T + 1 操作需要处理这行代码  TODO
                positon.closeable_amount = positon.closeable_amount + order.amount
                # 更新成本
                positon.cost_price = ((positon.cost_price * positon.open_amount) + (
                    order.cost_price * order.amount)) / (positon.open_amount + order.amount)
                # 更新总的持仓成本
                positon.total_cost_price = ((positon.total_cost_price * positon.total_amount) + (
                    order.cost_price * order.amount)) / (positon.total_amount + order.amount)
            # 平仓操作
            elif order.action == Order.Action.CLOSE:
                # 更新数量
                # positon.open_amount = positon.open_amount - order.amount
                positon.fill_amount = positon.fill_amount - order.amount
                positon.total_amount = positon.total_amount - order.amount
                positon.closeable_amount = positon.closeable_amount - order.amount

                if positon.total_amount <= 0:
                    # 删除持仓
                    del self.positions[positon_key]
                # 更新成本
                positon.cost_price = ((positon.cost_price * positon.open_amount) + (
                    order.cost_price * order.amount)) / (positon.open_amount + order.amount)
                # 更新总的持仓成本
                positon.total_cost_price = ((positon.total_cost_price * positon.total_amount) + (
                    order.cost_price * order.amount)) / (positon.total_amount + order.amount)
        else:
            # TODO 创建新的持仓
            positon = Position()
            # TODO  symbols 是一个列表,需要处理
            positon.symbol = order.symbol
            positon.open_amount = positon.open_amount + order.amount
            positon.fill_amount = positon.fill_amount + order.amount
            positon.total_amount = positon.total_amount + order.amount
            # T + 1 操作需要处理这行代码
            positon.closeable_amount = positon.closeable_amount + order.amount
            # 新建的仓位成本价 和 开仓价格一直
            # 更新成本
            positon.cost_price = order.price
            # 更新总的持仓成本
            positon.total_cost_price = order.price
            self.positions[positon_key] = positon

        his_key = order.get_key_his()
        if his_key not in self.his_positions:
            self.his_positions[his_key] = Position()

        # 历史持仓数据
        his_position_value: Position = self.his_positions[his_key]

        # T + 0 交易规则会有问题 TODO
        his_position_value.datetime = order.create_time
        # TODO 这里需要处理
        his_position_value.symbol = order.symbol
        his_position_value.side = order.side
        # 先计算成本价格
        his_position_value.cost_price = ((his_position_value.cost_price * his_position_value.open_amount) + (
            order.price * order.amount))/(his_position_value.open_amount + order.amount)
        his_position_value.total_cost_price = (his_position_value.total_amount * his_position_value.total_cost_price +
                                               order.price * order.amount) / (his_position_value.total_amount + order.amount)
        # 再计算数量
        his_position_value.open_amount = his_position_value.open_amount + order.amount
        his_position_value.fill_amount = his_position_value.fill_amount + order.fill_amount
        his_position_value.total_amount = his_position_value.total_amount + order.amount
        # 需要使用昨天的数据 TODO
        his_position_value.closeable_amount = None

    def update_account(self, order: Order = None):
        ''' 更新新账户信息 '''
        # 暂只接受全部成交订单

        if order is not None:  # 根据订单更新持仓
            if order.status != Order.Status.FILLED:
                return

            # 检测订单开仓操作
            if order.action == Order.Action.OPEN:
                # 减少可用现金
                self.available_cash = self.available_cash - order.price * order.amount
            elif order.action == Order.Action.CLOSE:
                # 增加可用现金
                self.available_cash = self.available_cash + order.price * order.amount

    def update_account_daily(self):
        '''每天跟新账户信息（资产），目前只支持 做多的资产统计  TODO'''
        # 多头持仓
        symbol_sides:tp.List[str] = []
        # 每个symbol的数量
        # symbol_amount_dict:tp.Dict[str,float] = {}
        for symbol_side, pos in self.positions.items():
            if str(Order.Side.SHORT)  in symbol_side: # 做空资产先不做统计
                continue
            elif str(Order.Side.LONG) in symbol_side: # 做多资产
                # symbols.append(pos.symbol)
                symbol_sides.append(symbol_side)
        market_value = 0.0
        if len(symbol_sides) > 0:
            # 拆分出 symbol
            symbols = list(map(lambda x: x.split('_')[0],symbol_sides))
            quote:pd.DataFrame = cs.ctx.ds.history(symbols=symbols)
            if quote.empty:
                print(f'行情数据不存在{symbols}')
                return
            # TODO 这里可以使用多列索引做优化
            # 选取各个symbol当然的close price
            quote.index = pd.DatetimeIndex(quote.index)
            
            # 这种获取方式依然是 dataFrame
            temp_data :pd.DataFrame= quote.loc[[cs.ctx.current_date]]
            # temp_data =temp_data.append(temp_data,ignore_index = True)
            close_price = None
            for item in symbols:
                # 获取某 symbol 列为 {item}的数据，数据格式为dateSeries,转换为 list
                close_prices = temp_data[temp_data['symbol'] == item][Quote.Column.CLOSE.value].tolist()
                # 获取某列的数据,格式为dateSeries
                if len(close_prices) > 0:
                    close_price = close_prices[0]
                ps = self.positions[item + '_' + str(Order.Side.LONG)]
                if ps is None:
                    continue
                market_value  = market_value + ps.total_amount * close_price
        self.his_assets[cs.ctx.current_date] = self.available_cash + market_value 
        print(f'account info date:{cs.ctx.current_date} total_asset:{self.his_assets[cs.ctx.current_date]} availabel_cash:{self.available_cash} market_value:{market_value}')

    def update_signal(self, order: Order, quote: tp.Dict[Quote.Column, float]):
        ''' 更新交易信号，用于绘图使用 '''
        symbol = order.symbol

        if symbol not in self.trade_signal:
            self.trade_signal[symbol] = {}
        dict_symbol = self.trade_signal[symbol]

        if cs.ctx.current_date not in dict_symbol:
            dict_symbol[cs.ctx.current_date] = {}
        dict_trade = dict_symbol[cs.ctx.current_date]
        # 设置交易信号为 high 或者 low
        dict_trade[order.action] = quote[Quote.Column.LOW.value] * \
            0.98 if order.action == Order.Action.OPEN else quote[Quote.Column.HIGH.value] * 1.02
        # print(self.trade_signal)

    def get_position(self, symbol: str, side: Order.Side) -> Position:
        '''
            获取标的先关持仓，不存在返回None
        '''
        key = create_key(symbol, side)
        if key in self.positions:
            return self.positions[key]
        return None
