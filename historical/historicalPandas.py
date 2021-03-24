import pandas as pd
import numpy as np
import csv
import datetime
from datetime import date
import os
from pathlib import Path




def historicalValues():
    file_to_open =  os.getcwd().split("\TFG")[0] + "/TFG/historical_data/salidaManhattan.csv"
    df=pd.read_csv(file_to_open, names=["ID","Speed", "TravelTime", "STATUS", "Date", "LINK_ID", "LINK_POINTS", "ENCODED_POLY_LINE", "ENCODED_POLY_LIKE_LVLS", "OWNER", "TRANSCOM_ID", "Borough", "Link_name"])
    df.drop(["STATUS","LINK_ID", "LINK_POINTS", "ENCODED_POLY_LINE", "ENCODED_POLY_LIKE_LVLS", "OWNER", "TRANSCOM_ID"],axis=1,inplace=True)
    
    
    #print(df.head(20))
    print(df["Date"].head(20))
    df["Time"] = df["Date"].str.split(" ").str.get(1) +  " " + df["Date"].str.split(" ").str.get(2)
    df["Date"] = df["Date"].str.split(" ").str.get(0) 
    
    #print(df["Date"].str.split(" ").head(20))
    df["Date"]=pd.to_datetime(df["Date"])
    #df["Time"]=pd.to_datetime(df["Time"], format='%H:%M').dt.time
    #df["Time"]=pd.to_timedelta(df+':00')
    df["Time"]=pd.to_datetime(df.index,format="%I:%M:%S %p")
    #pd.to_datetime(day1['time'], format='%H:%M').dt.time

    #df["Time"]=df.strftime()
    
    

    df["Weekday"] = df['Date'].dt.day_name()

    #print(df["Weekday"].head(20))

    column_reorder = ["ID","Speed","TravelTime", "Date", "Time", "Weekday", "Link_name"]
    
    df=df.reindex(columns=column_reorder)
    #print(df["Date"].head(20))
    print(df.head(20))

    #for col in df.columns:
        #print(col)

historicalValues()
