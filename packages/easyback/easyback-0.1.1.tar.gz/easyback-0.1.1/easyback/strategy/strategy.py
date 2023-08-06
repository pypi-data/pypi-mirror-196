'''
    策略类
'''
import abc
import typing as tp


class Strategy(abc.ABC):
    def __init__(self) -> None:
        pass

    @abc.abstractmethod
    def trade(self):
        '''交易'''
        # data = context.ds.history(['000001.XSHE'], ['Open', 'High','Close','Low'], length=20)
        # sma_5 = talib.SMA(data['Close'],timeperiod=5)
        # sma_10 = talib.SMA(data['Close'],timeperiod=10)
        # date_key = time_2_date_str(context.current_date)
        # postion = context.g_account.get_position('000001.XSHE',Order.Side.LONG)
        # if  postion is None  and  sma_5[date_key] >  sma_10[date_key]:
        #     # 买入
        #     order(symbol='000001.XSHE',action=Order.Action.OPEN,amount=100,type=Order.MarketType(),side=Order.Side.LONG)
        # elif postion and sma_5[date_key] < sma_10[date_key]:
        #     # 卖出
        #     close_amount = postion.closeable_amount
        #     order(symbol='000001.XSHE',action=Order.Action.CLOSE,amount=close_amount,type=Order.MarketType(),side=Order.Side.LONG)                
                

        # raise NotImplementedError()

    def trade_bar(self):
        '''根据 bar 交易'''
        pass

    def trade_tick(self):
        '''根据 tick 交易'''
        pass

    def befor_trade(self):
        '''交易前执行'''
        pass
        # raise NotImplementedError()

    def after_trade(self):
        '''交易后执行'''
        pass
        # raise NotImplementedError()
    @tp.final
    def start(self):
        '''
            执行策略
        '''
        self.befor_trade()
        self.trade()
        self.after_trade()
