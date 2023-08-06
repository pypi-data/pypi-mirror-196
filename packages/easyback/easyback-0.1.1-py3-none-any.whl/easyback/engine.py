'''
    回测引擎
'''

import pandas as pd
import numpy as np
import mplfinance as mpf

from .context import ctx

from easyback.broker import Account
from easyback.vex import Order,DataCenter
from easyback.utils import IndicatorUtil
from easyback.strategy import Strategy
from easyback.gateway import read_api,read_csv,read_db


class BackEngine():
    def __init__(self) -> None:
        self.__dataCenter: DataCenter = DataCenter()
        self.__strategy: Strategy = None
        ctx.g_account:Account = Account()

    def load_csv(self, path: str):
        '''
            从csv 中加载数据
        '''
        # self.__dataCenter.data = read_csv(path)

        self.__dataCenter.load_data(read_csv(path))

    def load_db(self):
        '''
            从db 中加载数据
        '''

    def load_api(self):
        '''
            从api中加载数据
        '''
        pass

    def load_dataCenter(self):
        pass

    def load_strategy(self, strategy: Strategy = None):
        '''加载策略'''
        self.__strategy = strategy
        # 将交易对象,和持仓对象创建好,均只有一个对象

        return self

    def start(self):
        '''回测运行'''
        generate = self.__dataCenter.generate_data()
        while True:
            date = next(generate)
            if date is None:
                break

            ctx.current_date = date
            self.__strategy.start()

            # 判断时间点（每5分钟、15分钟、20分钟、1天执行一次等）
            self.__daily_task()

    def __daily_task(self):
        # 每日定时任务
        # TODO DeprecationWarning replace by __schedule_task
        ctx.g_account.update_account_daily()
        
    def __schedule_task(self,type:str):
        '''
            执行定时任务
        '''
        pass

    def __show_trade_his(self):
        '''
            交易记录
        '''
        quote_data = self.__dataCenter.data

        a = pd.DataFrame(quote_data)
        a.index = pd.DatetimeIndex(a.index)
        # 需要使用 np.NaN 来做转换,绘图不能使用None 类型，NaN 代表数字类型
        a['signal_open'] = [np.NaN] * 253
        a['signal_close'] = [np.NaN] * 253
        for symbol, signal_dict in ctx.g_account.trade_signal.items():
            # 从原始数据中筛选 symbol 的相关数据  TODO
            # 设置索引为时间序列索引
            for datetime, action_data in signal_dict.items():
                # a.loc[datetime][]
                for action, price in action_data.items():
                    if action == Order.Action.OPEN:
                        a.loc[datetime, 'signal_open'] = price
                    elif action == Order.Action.CLOSE:
                        # 对某行的某个字段进行赋值
                        a.loc[datetime, 'signal_close'] = price
                    # print(a.loc[datetime])
        #可以查询 matplotlib库marker表
        add_plots = [mpf.make_addplot(a['signal_open'], scatter=True, marker='$B$', color='r', markersize=40),
                     mpf.make_addplot(a['signal_close'], scatter=True, marker='$S$', color='b', markersize=40,), ]

        my_color = mpf.make_marketcolors(
            up='red', down='green', edge='inherit',volume='inherit')
        my_style = mpf.make_mpf_style(marketcolors=my_color)
        # 添加移动均线
        mpf.plot(a, type='candle', volume = True,style=my_style, 
                 mav=(5, 10, 30), addplot=add_plots,ylabel_lower='volume')

    def __show_performance(self):
        '''
            持仓表现
        '''
        datas = list(ctx.g_account.his_assets.values())
        dateTimes = list(ctx.g_account.his_assets.keys())
        # 资金情况
        print(f'起始日期:{dateTimes[0]},期末日期:{dateTimes[-1]} 总交易日:{len(datas)}')
        print(f'期初资金:{round(datas[0],2)} 期末资金:{round(datas[-1],2)} 收益：{datas[-1] - datas[0]}')
        # 累计收益率
        print(f'累计收益:{round(IndicatorUtil.cum_return(datas) * 100,2) }%')
        # 年化收益率
        print(f'年化收益:{round(IndicatorUtil.annual_return(datas) * 100,2)}%')
        # 夏普比率
        return_list = IndicatorUtil.return_series(datas)
        print(f'夏普率:{round(IndicatorUtil.sharp_ratio(return_list),2)}')


    def show(self):
        self.__show_performance()
        self.__show_trade_his()