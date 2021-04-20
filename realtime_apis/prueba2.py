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
    airQuality_file = current_dir + "air1.csv"
    weather_file = current_dir + "weather1.csv"
    """
    traffic_file = current_dir + "merge1.csv"
    airQuality_file = current_dir + "air2.csv"
    weather_file = current_dir + "weather2.csv"
    """
    df1= pd.read_csv(traffic_file)
    df2= pd.read_csv(airQuality_file)
    df3 = pd.read_csv(weather_file)
    print(df1.head(3))
    print(df2.head(3))
   
    df1["datetime"] = pd.to_datetime(df1["datetime"])
    df2["datetime"] = pd.to_datetime(df2["datetime"])
    df3["datetime"] = pd.to_datetime(df3["datetime"])

    
    #df = pd.concat([traffic_df, airQuality_df, weather_df], sort=False)
    #df = df1.merge(df2, left_index=True, right_index=True)
    #df = pd.concat([df1, df2], axis=1).reindex(df1.index)
    #df = df1.append(df2, sort=False)
    #df = pd.concat([df1, df2], ignore_index=True, sort=False)
    #print(df.head(20))
    
    #time.sleep(2)
    df = pd.merge(df1,df2, how= 'outer', on = 'datetime', suffixes= ('_TRAFFIC', '_AIR'))
    #df = pd.merge(df, weather_df, how="outer", on="datetime", suffixes= ('','_WEATHER'))
    print(df.head)
  
    #df = df.sort_values("datetime")

    file_name = current_dir + f"/merge2.csv"

    df.to_csv(file_name,index=False)

    #print(f"Merge Traffic, AirQuality, Weather: {file_name}")

#weatherDataIngestion("2021-04-11T11:00:00", "2021-04-11T13:00:00", f"{current_dir}weather1.csv")
#weatherDataIngestion("2021-04-11T14:00:00", "2021-04-11T16:00:00", f"{current_dir}weather2.csv")
#airQualityDataIngestion("2021-04-11T11:05:05", "2021-04-11T13:05:05", f"{current_dir}air1.csv")
#airQualityDataIngestion("2021-04-11T14:05:05", "2021-04-11T16:05:05", f"{current_dir}air2.csv")
#trafficDataIngestion(1000000, "2021-04-11T11:00:00","2021-04-11T16:00:00", f"{current_dir}traffic.csv")
#trafficApi()
#airApi()
#weatherApi()
write("hola")
