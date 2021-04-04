from trafficApi import *
from airQualityApi import *
from weatherApi import *
import os, time, datetime
import pandas as pd

def apisRequest():
    data_folder = os.getcwd().split("\TFG")[0] + "/TFG/apis_data"
    file_to_open = data_folder + "/historical_register.csv"

    datetime_df = pd.read_csv(file_to_open)
    start_datetime = datetime_df.loc[datetime_df.index[-1], "datetime"]
    #start_datetime = "2021-03-27T23:59:04"

    end_datetime = datetime.datetime.utcnow()
    end_datetime = end_datetime - datetime.timedelta(hours=4)
    end_datetime = str(end_datetime)[0:-7].replace(" ", "T")

    end_datetime = convertTimeStr(end_datetime, "UTC", "America/New_York")
    
    trafficDataIngestion(1000000, start_datetime, end_datetime)
    airQualityDataIngestion(start_datetime, end_datetime)
    weatherDataIngestion(start_datetime, end_datetime)
    
    #datetime_df=datetime_df.append({'datetime' : end_datetime} , ignore_index=True)
    datetime_df.to_csv(file_to_open, index=False)
    
    res = start_datetime[0:13] + "_to_" + end_datetime[0:13]
    mergeByDatetime(res)
    




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