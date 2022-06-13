#############
# Author : Yujun Wen
# Last edit: 2022/2/26
# email: yujunwen0517@gmail.com
#####
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import pandas as pd 
import numpy as np
import datetime
import time
import subpackage.loggers as loggers
import subpackage.global_var as gl
#####
# var
from var.param import token,org,influxdb_url



class influxdb_cli:
    def __init__(self,url,token,org):
        self.token = token
        self.org = org
        self.url = url
        self.client = InfluxDBClient(
            url=self.url,
            token=self.token,
            org=self.org
        )
    def get_supertrend_index(self,symbol,time_dim,time_range):
        
        
        # build query string
        query = f'from(bucket: "cryptocurrency")\
                |> range(start: -{time_range})\
                |> filter(fn: (r) => r["_measurement"] == "crypto_supertrend")\
                |> filter(fn: (r) => r["symbol"] == "{symbol}")\
                |> filter(fn: (r) => r["_field"] == "final_lowerband" or \
                r["_field"] == "final_upperband" or  r["_field"] == "close" or r["_field"] == "atr" or r["_field"] == "dema25" or r["_field"] == "dema40" )\
                |> filter(fn: (r) => r["dimention"] == "{time_dim}")\
                |> pivot(rowKey:["_time"],columnKey: ["_field"],valueColumn: "_value")\
                |> sort(columns: ["_time"], desc: false)\
                |> drop(columns: ["_start","_stop","dimention","_measurement"])'
        # w,m,d
        # connet to influxdb
        # 建立query api
        query_api = self.client.query_api()
        try:
            result = query_api.query_data_frame(org=self.org, query=query,data_frame_index='_time') # user time as index
        except Exception as e:
            loggers.logger.error(e)
        return result

    def get_squeze_index(self,symbol,time_dim,time_range):
        
        
        # build query string
        query = f'from(bucket: "cryptocurrency")\
                |> range(start: -{time_range})\
                |> filter(fn: (r) => r["_measurement"] == "crypto_ttmsqueze")\
                |> filter(fn: (r) => r["symbol"] == "{symbol}")\
                |> filter(fn: (r) => r["_field"] == "squezeoff" or r["_field"] =="lower_BB" or r["_field"] =="upper_BB" or r["_field"] =="lower_KC" or r["_field"] =="upper_KC" )\
                |> filter(fn: (r) => r["dimention"] == "{time_dim}")\
                |> pivot(rowKey:["_time"],columnKey: ["_field"],valueColumn: "_value")\
                |> sort(columns: ["_time"], desc: false)\
                |> drop(columns: ["_start","_stop","dimention","_measurement"])'
        # w,m,d
        # connet to influxdb
        # 建立query api
        query_api = self.client.query_api()
        try:
            result = query_api.query_data_frame(org=self.org, query=query,data_frame_index='_time') # user time as index
        except Exception as e:
            loggers.logger.error(e)
        return result


    def get_ohlc_data(self,symbol,time_dim,time_range):
        
        """
        :param symbol:交易對
        :param time_dim: 時間維度(15m,30m,1h)
        """
        # build query string
        query = f'from(bucket: "cryptocurrency")\
        |> range(start: -{time_range})\
        |> filter(fn: (r) => r["_measurement"] == "{symbol}")\
        |> filter(fn: (r) => r["_field"] == "close" or r["_field"] == "open" or r["_field"] == "high" or r["_field"] == "low" or r["_field"] == "volume")\
        |> filter(fn: (r) => r["type"] == "{time_dim}")\
        |> pivot(rowKey:["_time"],columnKey: ["_field"],valueColumn: "_value")\
        |> sort(columns: ["_time"], desc: false)\
        |> drop(columns: ["_start","_stop","_measurement","type"])'
        # w,m,d
        # connet to influxdb
        # 建立query api
        query_api = self.client.query_api()
        try:
            result = query_api.query_data_frame(org=self.org, query=query,data_frame_index='_time') # user time as index
        except Exception as e:
            loggers.logger.error(e)
        return result
    
    def get_rsi_index(self,symbol,time_dim,time_range):
        
        """
        :param symbol:交易對
        :param time_dim: 時間維度(15m,30m,1h)
        """
        # build query string
        query = f'from(bucket: "cryptocurrency")\
        |> range(start: -{time_range})\
        |> filter(fn: (r) => r["_measurement"] == "crypto_rsi")\
        |> filter(fn: (r) => r["symbol"] == "{symbol}")\
        |> filter(fn: (r) => r["_field"] == "rsi")\
        |> filter(fn: (r) => r["dimention"] == "{time_dim}")\
        |> sort(columns: ["_time"], desc: false)\
        |> drop(columns: ["_start","_stop","_measurement","type","_field","dimention","symbol"])'
        # w,m,d
        # connet to influxdb
        # 建立query api
        query_api = self.client.query_api()
        try:
            result = query_api.query_data_frame(org=self.org, query=query,data_frame_index='_time') # user time as index
        except Exception as e:
            loggers.logger.error(e)
        return result

    

    def writedata(self,sig,sym,time_dim,time_index):
        with InfluxDBClient(url=influxdb_url, token=token, org=org) as client:          
            write_api = client.write_api(write_options=SYNCHRONOUS)
            try:
                point = Point('crypto_enter')\
                .tag('symbol',sym)\
                .tag('dim',time_dim)\
                .tag('position',sig)\
                .field('signal',1)\
                .time(time_index,WritePrecision.NS)
            except Exception as e:
                loggers.logger.error(e)       
            # 一次寫入influxdb
            try:
                write_api.write("cryptocurrency", org, point)
                # loggers.logger.info('Success insert supertrend enter signal data')
            except Exception as e:
                loggers.logger.error(e)
    
                




        
    
    
    
    
        
    



            


        


        

          


