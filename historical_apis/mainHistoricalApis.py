from historical_apis/trafficApi import *
from historical_apis/airQualityApi import *
from historical_apis/weatherApi import *
import os, time, datetime
import pandas as pd
import pytz, calendar
from datetime import datetime as dt


def apisRequest():
    data_folder = os.getcwd().split("\TFG")[0] + "/TFG/apis_data"
    file_to_open = data_folder + "/historical_register.csv"

    datetime_df = pd.read_csv(file_to_open)
    start_datetime = datetime_df.loc[datetime_df.index[-1], "datetime"]
    #start_datetime = "2021-03-27T23:59:04"

    tz_NY = pytz.timezone('America/New_York') 
    end_datetime = datetime.datetime.now(tz_NY)
    end_datetime = end_datetime - datetime.timedelta(hours=4)
    end_datetime = end_datetime.strftime("%Y-%m-%dT%H:%M:%S")

    start_datetime = datetime.datetime.strptime("2020-01-01T00:00:00","%Y-%m-%dT%H:%M:%S")
    end_datetime = start_datetime + datetime.timedelta(days=14, hours= 23, seconds=3599)
    end_datetime = str(end_datetime).replace(" ","T")
    start_datetime = str(start_datetime).replace(" ","T")
    print(end_datetime[0:19])
    #trafficDataIngestion(1000000, "2020-01-01T00:00:00", "2020-01-16T23:59:59")
    #2020-febrero
    #enero, marzo, mayo, julio, agosto, octubre, diciembre,
    count = 0
    while count < 24:  

    
        trafficDataIngestion(10000000, start_datetime, end_datetime)
        airQualityDataIngestion(start_datetime, end_datetime)
        weatherDataIngestion(start_datetime, end_datetime)
        res = start_datetime[0:13] + "_to_" + end_datetime[0:13]
        mergeByDatetime(res)

        start_datetime = dt.strptime(str(end_datetime), "%Y-%m-%dT%H:%M:%S") + datetime.timedelta(seconds = 1)
      
        if start_datetime.day == 1:
            plus = 14
        else:
            res = calendar.monthrange(start_datetime.year, start_datetime.month)
            plus = res[1] - 16
      
        end_datetime =  start_datetime + datetime.timedelta(days=plus, hours= 23, seconds=3599)

        start_datetime = str(start_datetime).replace(" ","T")
        end_datetime = str(end_datetime).replace(" ","T")
        count += 1
        
    #
    ##datetime_df=datetime_df.append({'datetime' : end_datetime} , ignore_index=True)
    #datetime_df.to_csv(file_to_open, index=False)
    #
    #res = start_datetime[0:13] + "_to_" + end_datetime[0:13]
    #mergeByDatetime(res)
    




def mergeByDatetime(datetime):

    data_folder = os.getcwd().split("\TFG")[0] + "/TFG/apis_data/"

    traffic_file = data_folder + f"/traffic_historical/traffic_dataIngestion_{datetime}.csv"
    airQuality_file = data_folder + f"/airQuality_historical/airQuality_dataIngestion_{datetime}.csv"
    weather_file = data_folder + f"/weather_historical/weather_dataIngestion_{datetime}.csv"

    traffic_df = pd.read_csv(traffic_file)
    airQuality_df = pd.read_csv(airQuality_file)
    weather_df = pd.read_csv(weather_file)

    traffic_df["datetime"] = pd.to_datetime(traffic_df["datetime"])
    airQuality_df["datetime"] = pd.to_datetime(airQuality_df["datetime"])
    weather_df["datetime"] = pd.to_datetime(weather_df["datetime"])
   

    df = pd.merge(traffic_df,airQuality_df, how= 'outer', on = 'datetime', suffixes= ('_TRAFFIC', '_AIR'))
    df = pd.merge(df, weather_df, how="outer", on="datetime", suffixes= ('','_WEATHER'))
    
    df = df.sort_values("datetime")

    file_name = data_folder + f"/merge_{datetime}.csv"

    df.to_csv(file_name,index=False)

    print(f"Merge Traffic, AirQuality, Weather: {file_name}")
  
apisRequest()

#mergeByDatetime("2021-02-01T00_to_2021-02-28T23")