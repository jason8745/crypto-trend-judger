import pandas as pd
import datetime
import time
import os
###
# subpackage
from subpackage.influxdb import influxdb_cli
import subpackage.loggers as loggers
#####
# 環境變數
INFLUXDB_URL = os.environ.get('INFLUXDB_URL') 
INFLUXDB_TOKEN = os.environ.get('INFLUXDB_TOKEN') 
INFLUXDB_ORG = os.environ.get('INFLUXDB_ORG')
#####



def enter_15m(symbol,time_dim,time_int):
    """
    :param sym : symbol
    :time_dim: 交易維度
    :time_int: 交易維度的整數部分(以分鐘為單位)
    """
    while True: 
        if (datetime.datetime.now().minute%time_int ==0 and datetime.datetime.now().second>50):
            time_range='24h'
            #######
            cli = influxdb_cli(url = INFLUXDB_URL,token = INFLUXDB_TOKEN,org = INFLUXDB_ORG)
            supertrend = cli.get_supertrend_index(symbol,time_dim,time_range) # 取得supertrend訊號
            squeze = cli.get_squeze_index(symbol,time_dim,time_range)
            rsi_index = cli.get_rsi_index(symbol,time_dim,time_range) # 最新一筆
            entries1 = (supertrend.close > supertrend['final_lowerband']) 
            entries2 =(supertrend.close < supertrend['final_upperband']) 
            # 先將資料拋至influxdb視覺化,後續再設計進出場邏輯
            long = entries1.astype(int).rename('long')
            short = entries2.astype(int).rename('short')
            signal =  pd.concat([long,short],axis=1)
            try:
                time_index = signal.index[-1]
                supertrend_info = supertrend.iloc[-1]
                squeze_15m_info = squeze.iloc[-1]
                rsi_info = rsi_index._value[-1]
                tunnel=False
                sig= None
                if (squeze_15m_info.upper_BB-squeze_15m_info.upper_KC>supertrend_info.atr) or (squeze_15m_info.lower_KC-squeze_15m_info.lower_BB>supertrend_info.atr) :
                    tunnel = True
                # 判斷趨勢
                if (tunnel == True) and(rsi_info<=35):
                    sig='short'
                elif (tunnel == True) and(rsi_info>70):
                    sig='long'
                    
                if tunnel ==False:
                    sig='interval'
                cli.writedata(sig,symbol,time_dim,time_index) 
            except Exception as e:
                loggers.logger.error(e)
            ################
            time.sleep(time_int*40) 

        time.sleep(5)

            









