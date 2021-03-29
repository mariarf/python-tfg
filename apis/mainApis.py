from trafficApi import *
from airQualityApi import *
from weatherApi import *
import os
import pandas as pd


data_folder = os.getcwd().split("\TFG")[0] + "/TFG/apis_data"
file_to_open = data_folder + "/traffic_dataIngestion.csv"

traffic_df = pd.read_csv(file_to_open)
last_traffic_date = traffic_df.loc[traffic_df.index[-1], "date"]
last_traffic_time = traffic_df.loc[traffic_df.index[-1], "time"]

start_datetime = last_traffic_date + "T" + last_traffic_time
start_datetime = "2021-03-01T00:00:00"
trafficDataIngestion(5000, start_datetime)

traffic_df = pd.read_csv(file_to_open)
last_traffic_date = traffic_df.loc[traffic_df.index[-1], "date"]
last_traffic_time = traffic_df.loc[traffic_df.index[-1], "time"]

end_datetime = last_traffic_date + "T" + last_traffic_time
airQualityDataIngestion(start_datetime, end_datetime)
weatherDataIngestion(start_datetime, end_datetime)
