import pandas as pd
import numpy as np
import datetime
import time
###
# subpackage
from subpackage.influxdb import influxdb_cli
import subpackage.loggers as loggers
###
# var
from var.param import token,org,influxdb_url


def enter_15m(symbol,time_dim,time_int,n):
    """
    :param sym : symbol
    :time_dim: 交易維度
    :time_int: 交易維度的整數部分(以分鐘為單位)
    :exchange: exchange名
    :queue queue名
    : n: 小數點後幾位,因為有的交易對很小數
    """
    while True: 
        # 統一在餘1的時候會有signal
        # 統一在餘1分30秒的時候會計算進場訊號
        if (datetime.datetime.now().minute%time_int ==0 and datetime.datetime.now().second>50):
            # 不會動
            time_range='24h'
            #######
            cli = influxdb_cli(url = influxdb_url,token = token,org = org)
            supertrend = cli.get_supertrend_index(symbol,time_dim,time_range) # 取得supertrend訊號
            ohlc = cli.get_ohlc_data(symbol,time_dim,time_range)
            squeze = cli.get_squeze_index(symbol,time_dim,time_range)
            rsi_index = cli.get_rsi_index(symbol,time_dim,time_range) # 最新一筆
            rsi = rsi_index._value[-1]
            entries1 = (supertrend.close > supertrend['final_lowerband']) 
            entries2 =(supertrend.close < supertrend['final_upperband']) 
            # 先將資料拋至influxdb視覺化,後續再設計進出場邏輯
            long = entries1.astype(int).rename('long')
            short = entries2.astype(int).rename('short')
            signal =  pd.concat([long,short],axis=1)
            # 檢查最新一筆是否送出MQ進出場訊號
            # 根據資料 12:00做的決定 應該是參考11:00的完整kbar
            # 寫入influxdb
            # 重新計算多空訊號
            ################
            try:
                time_index = signal.index[-1]
                supertrend_info = supertrend.iloc[-1]
                squeze_15m_info = squeze.iloc[-1]
                rsi_info = rsi_index._value[-1]
                # 空趨
                # 寫入進場資料
                tunnel=False
                sig= None
                if (squeze_15m_info.upper_BB-squeze_15m_info.upper_KC>supertrend_info.atr) or (squeze_15m_info.lower_KC-squeze_15m_info.lower_BB>supertrend_info.atr) :
                    tunnel = True
                # 判斷趨勢
                if (tunnel == True) and(rsi_info<=45):
                    sig='short'
                elif (tunnel == True) and(rsi_info>45):
                    sig='long'
                    
                if tunnel ==False:
                    sig='interval'
                cli.writedata(sig,symbol,time_dim,time_index) 
            except Exception as e:
                loggers.logger.error(e)
            ################
            time.sleep(time_int*40) 

        time.sleep(5)

            









