import datetime
import time
from talib import abstract
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



def rsi_15m():
    time_dim='15m'
    while True:
        if (datetime.datetime.now().minute%15==0) and  (datetime.datetime.now().second>35):
            cli = influxdb_cli(url = INFLUXDB_URL,token = INFLUXDB_TOKEN,org = INFLUXDB_ORG)
            # get btc data
            symbol = ['BTCUSDT'] 
            for sym in symbol:
                try:
                    data = cli.get_ohlc_data(sym,time_dim,time_range='5h')
                    try:
                        rsi_df=abstract.RSI(data,7).rename('rsi')
                    except Exception as e:
                        loggers.logger.error(e)
                    # send to influxdb
                    try:
                        cli.writersi(rsi_df[-1:],sym,time_dim)
                    except Exception as e:
                        loggers.logger.error(e)
                except:
                    pass
            time.sleep(600) # 休息10分鐘
            

        time.sleep(10)