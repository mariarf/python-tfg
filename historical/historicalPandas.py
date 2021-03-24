import pandas as pd
import numpy as np
import csv
import datetime
from datetime import date
import os
from pathlib import Path




def historicalValues():
    file_to_open =  os.getcwd().split("\TFG")[0] + "/TFG/historical_data/salidaManhattan.csv"
    file_contamination = os.getcwd().split("\TFG")[0] + "/TFG/originals/calidadAire.csv"
    output_csv = os.getcwd().split("\TFG")[0] + "/TFG/historical_data/finalOutput.csv"
    df=pd.read_csv(file_to_open, names=["ID","Speed", "TravelTime", "STATUS", "Date", "LINK_ID", "LINK_POINTS", "ENCODED_POLY_LINE", "ENCODED_POLY_LIKE_LVLS", "OWNER", "TRANSCOM_ID", "Borough", "Link_name"])
    df.drop(["STATUS","LINK_ID", "LINK_POINTS", "ENCODED_POLY_LINE", "ENCODED_POLY_LIKE_LVLS", "OWNER", "TRANSCOM_ID"],axis=1,inplace=True)
    
    
    #print(df.head(20))
    #print(df["Date"].head(20))
    df["Time"] = df["Date"].str.split(" ").str.get(1) +  " " + df["Date"].str.split(" ").str.get(2)
    df["Date"] = df["Date"].str.split(" ").str.get(0) 
    
    df["Date"]=pd.to_datetime(df["Date"])
    df["Time"]=pd.to_datetime(df["Time"]).dt.strftime('%H:%M:%S')
    df["Weekday"] = df['Date'].dt.day_name()


    column_reorder = ["ID","Speed","TravelTime", "Date", "Time", "Weekday", "Link_name"]
    df=df.reindex(columns=column_reorder)
    print("llega1")
    df_contamination = pd.read_csv(file_contamination, names=["DateCont","ValueCont","i1","i2", "i3"], header=None)
    df_contamination["DateCont"]=pd.to_datetime(df_contamination["DateCont"])
    print(df_contamination["DateCont"].head(20))
    print("llega2")

    #print(df_contamination.head(20))
    df = pd.merge(df,df_contamination, left_on="Date", right_on="DateCont")
    print(df.head(20))
    df.drop(["i1","i2", "i3"],axis=1,inplace=True)
    df.to_csv(output_csv, index=False)
    #for col in df.columns:
        #print(col)

historicalValues()
    

