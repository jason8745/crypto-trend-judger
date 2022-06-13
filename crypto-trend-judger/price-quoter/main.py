from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import datetime
import time
from binance.client import Client
import os
#####
# 環境變數
INFLUXDB_URL = os.environ.get('INFLUXDB_URL') 
INFLUXDB_TOKEN = os.environ.get('INFLUXDB_TOKEN') 
INFLUXDB_ORG = os.environ.get('INFLUXDB_ORG')
BINANCE_API_KEY = os.environ.get('BINANCE_API_KEY')
BINANCE_API_SECRET = os.environ.get('BINANCE_API_SECRET')
#####
def insertdata(url,token,org,bucket,api_key,api_secret):

    with InfluxDBClient(url, token=token, org=org) as client:
        try:
            write_api = client.write_api(write_options=SYNCHRONOUS)
            for crypto in subscribe:
                client = Client(api_key, api_secret)
                try:
                    # get data
                    klines5 = client.get_historical_klines(crypto, Client.KLINE_INTERVAL_5MINUTE, "30 minutes ago UTC")
                    klines15 = client.get_historical_klines(crypto, Client.KLINE_INTERVAL_15MINUTE, "360 minutes ago UTC")
                    klines30 = client.get_historical_klines(crypto, Client.KLINE_INTERVAL_30MINUTE, "360 minutes ago UTC")
                    klines60 = client.get_historical_klines(crypto, Client.KLINE_INTERVAL_1HOUR, "1 day ago UTC")
                    klinesday = client.get_historical_klines(crypto, Client.KLINE_INTERVAL_1DAY, "1 day ago UTC")
                except Exception as e:
                    print(e)
                    pass
                data = []              
                for ind , ds in enumerate(klines15):
                    point = Point(crypto) \
                    .tag("type", '15m') \
                    .field("open", float(ds[1])) \
                    .field("high", float(ds[2])) \
                    .field("low", float(ds[3])) \
                    .field("close", float(ds[4])) \
                    .field("volume", float(ds[5])) \
                    .time(datetime.datetime.fromtimestamp(ds[0]/ 1e3),WritePrecision.NS)
                    data.append(point)
                try:    
                    write_api.write(bucket, org, data)
                except Exception as e:
                    print(e)
                data = []              
                for ind , ds in enumerate(klines30):
                    point = Point(crypto) \
                    .tag("type", '30m') \
                    .field("open", float(ds[1])) \
                    .field("high", float(ds[2])) \
                    .field("low", float(ds[3])) \
                    .field("close", float(ds[4])) \
                    .field("volume", float(ds[5])) \
                    .time(datetime.datetime.fromtimestamp(ds[0]/ 1e3),WritePrecision.NS)
                    data.append(point)
                try:    
                    write_api.write(bucket, org, data)
                except Exception as e:
                    print(e)

                data = []              
                for ind , ds in enumerate(klines5):
                    point = Point(crypto) \
                    .tag("type", '5m') \
                    .field("open", float(ds[1])) \
                    .field("high", float(ds[2])) \
                    .field("low", float(ds[3])) \
                    .field("close", float(ds[4])) \
                    .field("volume", float(ds[5])) \
                    .time(datetime.datetime.fromtimestamp(ds[0]/ 1e3),WritePrecision.NS)
                    data.append(point)
                try:    
                    write_api.write(bucket, org, data)
                except Exception as e:
                    print(e)
                data = []              
                for ind , ds in enumerate(klines60):
                    point = Point(crypto) \
                    .tag("type", '1h') \
                    .field("open", float(ds[1])) \
                    .field("high", float(ds[2])) \
                    .field("low", float(ds[3])) \
                    .field("close", float(ds[4])) \
                    .field("volume", float(ds[5])) \
                    .time(datetime.datetime.fromtimestamp(ds[0]/ 1e3),WritePrecision.NS)
                    data.append(point)
                try:    
                    write_api.write(bucket, org, data)
                except Exception as e:
                    print(e)
                data = []              
                for ind , ds in enumerate(klinesday):
                    point = Point(crypto) \
                    .tag("type", '1d') \
                    .field("open", float(ds[1])) \
                    .field("high", float(ds[2])) \
                    .field("low", float(ds[3])) \
                    .field("close", float(ds[4])) \
                    .field("volume", float(ds[5])) \
                    .time(datetime.datetime.fromtimestamp(ds[0]/ 1e3),WritePrecision.NS)
                    data.append(point)
                try:    
                    write_api.write(bucket, org, data)
                except Exception as e:
                    print(e)
                print("寫入symbol:{sym} to InfluxDB".format(sym = crypto ))

        except Exception as e:
            print(e)




if __name__ == "__main__":
    subscribe=['BTCUSDT','ETHUSDT'] # 訂閱清單
    while True:
        # bucket先使用"cryptocurrency" 也可以自行設置
        insertdata(INFLUXDB_URL,INFLUXDB_TOKEN,INFLUXDB_ORG,"cryptocurrency",BINANCE_API_KEY,BINANCE_API_SECRET)
        time.sleep(30)