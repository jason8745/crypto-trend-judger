#############
# Author : Yujun Wen
# Last edit: 2022/2/26
# email: yujunwen0517@gmail.com
#####
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import subpackage.loggers as loggers




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
        
        

    def writedata(self,df,sym,time_dim):
        with InfluxDBClient(url=self.url, token=self.token, org=self.org) as client:          
            write_api = client.write_api(write_options=SYNCHRONOUS)
            data=[]
            for ind,ds in enumerate(df.values):
                # 非nan值
                try:
                    point = Point('crypto_supertrend')\
                    .tag('dimention',time_dim)\
                    .tag('symbol',sym)\
                    .field('final_lowerband',ds[1])\
                    .field('final_upperband',ds[2])\
                    .field('dema25',ds[3])\
                    .field('dema40',ds[4])\
                    .field('close',ds[5])\
                    .field('atr',ds[6])\
                    .time(df.index[ind],WritePrecision.NS)
                    data.append(point)
                
                except Exception as e:
                        loggers.logger.error(e)
            # 一次寫入influxdb
            write_api.write("cryptocurrency", self.org, data)
            loggers.logger.info(f'Write {sym}: {time_dim} success.')
    
    def writesqueze(self,df,sym,time_dim):
        with InfluxDBClient(url=self.url, token=self.token, org=self.org) as client:          
            write_api = client.write_api(write_options=SYNCHRONOUS)
            data=[]
            for ind,ds in enumerate(df.values):
                # 非nan值
                try:
                    point = Point('crypto_ttmsqueze')\
                    .tag('dimention',time_dim)\
                    .tag('symbol',sym)\
                    .field('squezeoff',ds[0])\
                    .field('upper_KC',ds[1])\
                    .field('lower_KC',ds[2])\
                    .field('upper_BB',ds[3])\
                    .field('lower_BB',ds[4])\
                    .time(df.index[ind],WritePrecision.NS)
                    data.append(point)
                
                except Exception as e:
                        loggers.logger.error(e)
            # 一次寫入influxdb
            write_api.write("cryptocurrency", self.org, data)
            loggers.logger.info(f'Write {sym}: {time_dim} squeeze success.')
    

    def writersi(self,df,sym,time_dim):
        with InfluxDBClient(url=self.url, token=self.token, org=self.org) as client:          
            write_api = client.write_api(write_options=SYNCHRONOUS)
            data=[]
            for ind,ds in enumerate(df.values):
                # 非nan值
                try:
                    point = Point('crypto_rsi')\
                    .tag('dimention',time_dim)\
                    .tag('symbol',sym)\
                    .field('rsi',round(ds,2))\
                    .time(df.index[ind],WritePrecision.NS)
                    data.append(point)
                
                except Exception as e:
                        loggers.logger.error(e)
            # 一次寫入influxdb
            write_api.write("cryptocurrency", self.org, data)
            loggers.logger.info(f'Write {sym}: {time_dim} rsi success.')
                




        
    
    
    
    
        
    



            


        


        

          


