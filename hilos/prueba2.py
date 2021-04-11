from trafficApi import *
from airQualityApi import *
from weatherApi import *
import pandas as pd
import threading, time, os

current_dir = os.getcwd().split("\TFG")[0] + "/TFG/pruebas_maria/"


def trafficApi():
    print("trafico entrando")
    rest = 2
    hora = 10
    merge = pd.read_csv(f"{current_dir}merge.csv")
    start_datetime = merge.loc[merge.index[-1], "datetime_traffic"].replace(" ","T")
    print(start_datetime)
    while True:
        print("call traffic")
        time.sleep(rest)
        trafficDataIngestion(1, start_datetime, "0000-00-00T00:00:00", f"{current_dir}traffic.csv")
        hora += 1
        traffic = threading.Thread(target = write, args = (1,))
        traffic.start()
        merge = pd.read_csv(f"{current_dir}merge.csv")
        start_datetime = merge.loc[merge.index[-1], "datetime"]
        
        if hora == 15:
            break
"""

def airApi():
    print("air entrando")
    while True:
        print("call air")
        time.sleep(4)
        airQualityDataIngestion("2021-04-11T11:05:05", "2021-04-11T16:05:05", f"{current_dir}air.csv")
        air_quality = threading.Thread(target = write, args = (2,))
        air_quality.start()
        break



def weatherApi():
    print("weather entrando")
    ret = 0
    while True:
        print("call weather")
        time.sleep(5)
        weatherDataIngestion("2021-04-11T11:05:05", "2021-04-11T16:05:05", f"{current_dir}weather.csv")
        ret += 1
        weather = threading.Thread(target = write, args = (ret,))
        weather.start()
        break

"""
def write(type):
    print("write" + str(type))

    traffic_file = current_dir + "traffic.csv"
    airQuality_file = current_dir + "air.csv"
    weather_file = current_dir + "weather.csv"

    traffic_df = pd.read_csv(traffic_file)
    #airQuality_df = pd.read_csv(airQuality_file)
    #weather_df = pd.read_csv(weather_file)

    traffic_df["datetime"] = pd.to_datetime(traffic_df["datetime"])
    #airQuality_df["datetime"] = pd.to_datetime(airQuality_df["datetime"])
    #weather_df["datetime"] = pd.to_datetime(weather_df["datetime"])
   
    time.sleep(2)
    #df = pd.merge(traffic_df,airQuality_df, how= 'outer', on = 'datetime', suffixes= ('_TRAFFIC', '_AIR'))
    #df = pd.merge(df, weather_df, how="outer", on="datetime", suffixes= ('','_WEATHER'))
    
    #df = df.sort_values("datetime")

    file_name = data_folder + f"/merge.csv"

    #df.to_csv(file_name,index=False)

    print(f"Merge Traffic, AirQuality, Weather: {file_name}")


trafficApi()
#airApi()
#weatherApi()
