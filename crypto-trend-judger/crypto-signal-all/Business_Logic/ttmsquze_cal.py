import pandas as pd
import numpy as np
import datetime
import time
###
# subpackage
from subpackage.influxdb import influxdb_cli
import subpackage.loggers as loggers
from subpackage.strategy import ttmsqueze
###
# var
from var.param import influxdb_token,influxdb_org,influxdb_url

def ttmsqueze_calculate_15m():
    time_dim='15m'
    while True:
        if (datetime.datetime.now().minute%15 ==0)and (datetime.datetime.now().second>35):
            try:
                cli = influxdb_cli(url = influxdb_url,token = influxdb_token,org = influxdb_org)
                # get btc data
                symbol = ['BTCUSDT','LTCUSDT','TRXUSDT'] 
                for sym in symbol:
                    data = cli.get_ohlc_data(sym,time_dim,time_range='2d')
                    try:
                        ttmsquze_signal=ttmsqueze(data,20,3,20,2) # 重要參數，可自己調整
                    except Exception as e:
                        loggers.logger.error(e)
                    # send to influxdb
                    try:
                        cli.writesqueze(ttmsquze_signal[-2:],sym,time_dim)
                    except Exception as e:
                        loggers.logger.error(e)
            except:
                loggers.logger.error('error')
                pass
            time.sleep(600) # 休息10分鐘
            

        time.sleep(5)
