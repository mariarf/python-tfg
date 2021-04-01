from numpy import column_stack
from trafficApi import *
from airQualityApi import *
from weatherApi import *
import os
import pandas as pd

def apisRequest():
    data_folder = os.getcwd().split("\TFG")[0] + "/TFG/apis_data"
    file_to_open = data_folder + "/traffic_dataIngestion.csv"

    traffic_df = pd.read_csv(file_to_open)
    last_traffic_date = traffic_df.loc[traffic_df.index[-1], "date"]
    last_traffic_time = traffic_df.loc[traffic_df.index[-1], "time"]

    start_datetime = last_traffic_date + "T" + last_traffic_time
    #start_datetime = "2021-03-27T23:59:04"
    trafficDataIngestion(1000000, start_datetime)

    traffic_df = pd.read_csv(file_to_open)
    last_traffic_date = traffic_df.loc[traffic_df.index[-1], "date"]
    last_traffic_time = traffic_df.loc[traffic_df.index[-1], "time"]

    end_datetime = last_traffic_date + "T" + last_traffic_time
    airQualityDataIngestion(start_datetime, end_datetime)
    weatherDataIngestion(start_datetime, end_datetime)



def totalDate():

    data_folder = os.getcwd().split("\TFG")[0] + "/TFG/apis_data/historical"
    traffic_file = data_folder + "/traffic_historical.csv"
    airQuality_file = data_folder + "/airQuality_historical.csv"
    weather_file = data_folder + "/weather_historical.csv"

    traffic_df = pd.read_csv(traffic_file)
    airQuality_df = pd.read_csv(airQuality_file)
    weather_df = pd.read_csv(weather_file)
    
    airQuality_df["datetime"] = airQuality_df["date"] + "T" + airQuality_df["time"]
    weather_df["datetime"] = weather_df["date"] + "T" + weather_df["time"]
    traffic_df["datetime"] = traffic_df["date"] + "T" + traffic_df["time_hour"]


    airQuality_df["datetime"] = pd.to_datetime(airQuality_df["datetime"])
    weather_df["datetime"] = pd.to_datetime(weather_df["datetime"])
    traffic_df["datetime"] = pd.to_datetime(traffic_df["datetime"])

    print(traffic_df.head())
    print(airQuality_df.head())
    print(weather_df.head())

    df = pd.merge(traffic_df,airQuality_df, how= 'inner', on = 'datetime')
    df = pd.merge(df, weather_df, how="inner", on="datetime")
    print(df.dtypes)

    df = df[["date_x", "date_y", "date", "time_x", "time_y", "time", "weekday", "id", "speed", "travel_time", "link_name", "aqi", "Dew Point", "Relative Humidity", "Wind Speed", "Wind Gust", "Wind Direction", "Precipitation", "Snow Depth", "Visibility", "Cloud Cover", "Sea Level Pressure", "Conditions"]]




    file_name = data_folder + "/total_historical_march01_to_march27.csv"

    df.to_csv(file_name,index=False)


#apisRequest()
totalDate()