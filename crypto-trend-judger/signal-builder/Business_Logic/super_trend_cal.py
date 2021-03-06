import os
import datetime
import time
###
# subpackage
from subpackage.influxdb import influxdb_cli
import subpackage.loggers as loggers
from subpackage.strategy import supertrend
#####
# 環境變數
INFLUXDB_URL = os.environ.get('INFLUXDB_URL') 
INFLUXDB_TOKEN = os.environ.get('INFLUXDB_TOKEN') 
INFLUXDB_ORG = os.environ.get('INFLUXDB_ORG')
#####





def super_trend_calculate_15m():
    """
    supertrend strategy有五個欄位
    Supertrend: True or False,決定Final_Lowerband 跟 Final_Upperband 是否為nan
    Final_Lowerband:最終下界
    Final_Upperband:最終上界
    dema144: dema(144)
    dema169: dema(169)
    """
    time_dim='15m'
    while True:
        if (datetime.datetime.now().minute%15 ==0) and  (datetime.datetime.now().second>35):
            cli = influxdb_cli(url = INFLUXDB_URL,token = INFLUXDB_TOKEN,org = INFLUXDB_ORG)
            # get btc data
            symbol = ['BTCUSDT','LTCUSDT','TRXUSDT'] 
            for sym in symbol:
                try:
                    data = cli.get_ohlc_data(sym,time_dim,time_range='2d')
                    try:
                        supertrend_df=supertrend(data)
                    except Exception as e:
                        loggers.logger.error(e)
                    # send to influxdb
                    try:
                        cli.writedata(supertrend_df[-1:],sym,time_dim)
                    except Exception as e:
                        loggers.logger.error(e)
                except:
                    pass
            time.sleep(600) # 休息10分鐘
            

        time.sleep(5)







