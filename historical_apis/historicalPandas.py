import pandas as pd
import numpy as np
import csv
import datetime
from datetime import date
import os
from os import path
from os import walk
from pathlib import Path




def historicalValues():
    file_to_open =  os.getcwd().split("\TFG")[0] + "/TFG/historical_data/salidaManhattan.csv"
    file_unique_streets =  os.getcwd().split("\TFG")[0] + "/TFG/historical_data/uniqueStreets.csv"
    file_contamination = os.getcwd().split("\TFG")[0] + "/TFG/originals/calidadAire.csv"
    file_climate = os.getcwd().split("\TFG")[0] + "/TFG/originals/NYC+ROUTINE+NY.csv"
    output_csv = os.getcwd().split("\TFG")[0] + "/TFG/historical_data/finalOutput.csv"

    df=pd.read_csv(file_to_open, names=["ID","Speed", "TravelTime", "STATUS", "Date", "LINK_ID", "LINK_POINTS", "ENCODED_POLY_LINE", "ENCODED_POLY_LIKE_LVLS", "OWNER", "TRANSCOM_ID", "Borough", "Link_name"])
    df.drop(["ID", "STATUS","LINK_ID", "LINK_POINTS", "ENCODED_POLY_LINE", "ENCODED_POLY_LIKE_LVLS", "OWNER", "TRANSCOM_ID"],axis=1,inplace=True)
    
    
    #print(df.head(20))
    #print(df["Date"].head(20))
    df["Time"] = df["Date"].str.split(" ").str.get(1) +  " " + df["Date"].str.split(" ").str.get(2)
    df["Date"] = df["Date"].str.split(" ").str.get(0) 
    
    df["Date"]=pd.to_datetime(df["Date"])
    df["Time"]=pd.to_datetime(df["Time"]).dt.strftime('%H:%M:%S')
    df["Time"] = df["Time"].str.split(":").str.get(0) + ":00:00"
    #print(df["Time"].head(20))
    df["Weekday"] = df['Date'].dt.day_name()


    column_reorder = ["Speed","TravelTime", "Date", "Time", "Weekday", "Link_name"]
    df=df.reindex(columns=column_reorder)
    
    df_contamination = pd.read_csv(file_contamination, names=["DateCont","ValueCont","i1","i2", "i3"], header=None)
    df_contamination["DateCont"]=pd.to_datetime(df_contamination["DateCont"])
    #print(df_contamination["DateCont"].head(20))
    

    #print(df_contamination.head(20))
    df = pd.merge(df,df_contamination, left_on="Date", right_on="DateCont")
    #print(df.head(20))
    df.drop(["i1","i2", "i3"],axis=1,inplace=True)
    

    
    df_climate = pd.read_csv(file_climate, names=["station","valid","tmpf","dwpf","relh","drct","sknt","p01i","alti","mslp","vsby","gust","skyc1","skyc2","skyc3","skyc4","skyl1","skyl2","skyl3","skyl4","wxcodes","ice_accretion_1hr","ice_accretion_3hr","ice_accretion_6hr","peak_wind_gust","peak_wind_drct","peak_wind_time","feel","metar"], header=None)
    
    df_climate = df_climate.iloc[1:]
    df_climate["DateClimate"] = df_climate["valid"].str.split(" ").str.get(0)
    df_climate["TimeClimate"] = df_climate["valid"].str.split(" ").str.get(1)
    df_climate["TimeClimate"] = df_climate["TimeClimate"].str.split(":").str.get(0) + ":00:00"
    df_climate.drop(["valid", "station", "alti", "skyl1","skyl2","skyl3","skyl4", "ice_accretion_3hr","ice_accretion_6hr","peak_wind_gust","peak_wind_drct","peak_wind_time","feel","metar"],axis=1,inplace=True)
    column_reorder = ["DateClimate","TimeClimate","dwpf", "relh", "sknt", "gust", "drct", "p01i", "ice_accretion_1hr", "vsby", "skyc1", "mslp", "wxcodes"]
    df_climate = df_climate.reindex(columns=column_reorder)
    
    #print(df_climate.head(20))
    df["Date"]=df["Date"].astype('datetime64[ns]')
    df["Time"]=df["Time"].astype('datetime64[ns]')
    df_climate["DateClimate"]=df_climate["DateClimate"].astype('datetime64[ns]')
    df_climate["TimeClimate"]=df_climate["TimeClimate"].astype('datetime64[ns]')

    print(type(df["Date"]))
    print(type(df["Time"]))
    print(type(df_climate["DateClimate"]))
    print(type(df_climate["TimeClimate"]))
    df_streets = pd.read_csv(file_unique_streets, names=["Link_name","coordX","coordY","zonaX","zonaY","Zone"], header=None)
    df = pd.merge(df, df_streets, on="Link_name", sort=False)
    
    df = pd.merge(df, df_climate, how="outer" , left_on=["Date","Time"], right_on=["DateClimate","TimeClimate"])
    print(df.describe())

    df["Time"]=pd.to_datetime(df["Time"]).dt.strftime('%H:%M:%S')
    df["TimeClimate"]=pd.to_datetime(df["TimeClimate"]).dt.strftime('%H:%M:%S')
    
    

    #df.drop(["DateClimate", "TimeClimate", "DateCont","coordX","coordY","zonaX","zonaY"],axis=1,inplace=True)
    df.drop(["DateClimate", "TimeClimate", "DateCont"],axis=1,inplace=True)
    final_reorder = ["Date", "Time", "Weekday","Speed","TravelTime","Link_name", "Zone", "ValueCont","dwpf","relh","sknt","gust","drct","p01i","ice_accretion_1hr","vsby","skyc1","mslp","wxcodes"]
    """
    df.drop(["DateClimate", "TimeClimate", "DateCont"],axis=1,inplace=True)
    final_reorder = ["Date", "Time", "Weekday","Speed","TravelTime","Link_name", "ValueCont","dwpf","relh","sknt","gust","drct","p01i","ice_accretion_1hr","vsby","skyc1","mslp","wxcodes"]
    """
    df = df.reindex(columns=final_reorder)
    df.to_csv(output_csv, index=False)
    #print(df_climate["gust"].describe())
    """
    
    print((df_climate["skyc1"] != "CLR").describe())
    

    for col in df.columns:
        print(col)
    """
#historicalValues()

def mergeZones(location):

    #file_to_merge = os.getcwd().split("\TFG")[0] + location
    output_csv = os.getcwd().split("\TFG")[0] + location 
    zone_file = os.getcwd().split("\TFG")[0] + "/TFG/historical_data/uniqueStreets.csv"
    
    df_streets = pd.read_csv(zone_file, names=["link_name","coordX","coordY","zonaX","zonaY","Zone"], header=None, low_memory=False)
    df = pd.read_csv(location, names=["datetime","datetime_traffic","weekday","id","speed","travel_time","link_name","AQI_PM2.5","Parameter_PM2.5","Unit_PM2.5","Value_PM2.5","Category_PM2.5","AQI_OZONE","Parameter_OZONE","Unit_OZONE","Value_OZONE","Category_OZONE","Minimum Temperature","Maximum Temperature","Temperature","Dew Point","Relative Humidity","Heat Index","Wind Speed","Wind Gust","Wind Direction","Wind Chill","Precipitation","Precipitation Cover","Snow Depth","Visibility","Cloud Cover","Sea Level Pressure","Conditions"],header=None, low_memory=False, skiprows=2)
    os.remove(location)
    df = pd.merge(df, df_streets, on="link_name")
    df.drop(["coordX", "coordY", "zonaX", "zonaY"],axis=1,inplace=True)

    column_reorder = ["datetime","datetime_traffic","weekday","id","speed","travel_time","link_name","Zone","AQI_PM2.5","Parameter_PM2.5","Unit_PM2.5","Value_PM2.5","Category_PM2.5","AQI_OZONE","Parameter_OZONE","Unit_OZONE","Value_OZONE","Category_OZONE","Minimum Temperature","Maximum Temperature","Temperature","Dew Point","Relative Humidity","Heat Index","Wind Speed","Wind Gust","Wind Direction","Wind Chill","Precipitation","Precipitation Cover","Snow Depth","Visibility","Cloud Cover","Sea Level Pressure","Conditions"]
    
    #print(df.columns)
    df["Wind Gust"].fillna(0.0, inplace=True)
    df["AQI_OZONE"].fillna(0.0, inplace=True)
    df["Value_OZONE"].fillna(0.0, inplace=True)
    df["Category_OZONE"].fillna(0.0, inplace=True)
    df["Heat Index"].fillna(0.0, inplace=True)
    df["Wind Direction"].fillna(0.0, inplace=True)
    df["Wind Chill"].fillna(0.0, inplace=True)
    df["Snow Depth"].fillna(0.0, inplace=True)
    df["Category_PM2.5"].fillna(0, inplace=True)
    df["Snow Depth"].fillna(0.0, inplace=True)
 

    
    df = df.reindex(columns=column_reorder)
    df.to_csv(location, index=False)



def mergeFilesWithLocation(location, outputname):

    file_unique_streets =  os.getcwd().split("\TFG")[0] + "/TFG/historical_data/uniqueStreets.csv"
    path = os.getcwd().split("\TFG")[0] + location
    dirs = os.listdir(path)
    df = pd.DataFrame()

    undesired_paths = ["airQuality_dataIngestion.csv","airQuality_historical", "historical", "historical_register.csv", "traffic_dataIngestion.csv", "traffic_historical", "weather_dataIngestion.csv", "weather_historical", "2021", "merge_other_years", "prueba"]
    
    for file in dirs:
        
        if file in undesired_paths:
            continue
        else:
            file = path + file
            df_concat = pd.read_csv(file, header=None, low_memory=False) #PROBLEMA AQUI
            df = pd.concat([df,df_concat])
            print("fin" + file)

    print(df.shape[0])

    output_csv = os.getcwd().split("\TFG")[0] + location + outputname + ".csv"
    df.to_csv(output_csv, index=False)
    mergeZones(output_csv)
    
    

mergeFilesWithLocation("/TFG/apis_data/", "historicalMerge")

mergeFilesWithLocation("/TFG/apis_data/2021/", "trainingDataMerge")

#mergeFilesWithLocation("/TFG/apis_data/prueba/", "historicalMergePrueba")
