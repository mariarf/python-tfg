# make sure to install these packages before running:
# pip install pandas
# pip install sodapy

from auxMethods import apiHistoricalData
from numpy import empty
import pandas as pd
from sodapy import Socrata
import os, datetime

#Date tiene que ser de formato: yyyy-mm-ddThh:mm:ss
def trafficDataIngestion(dataLimit, date):

    # Unauthenticated client only works with public data sets. Note 'None'
    # in place of application token, and no username or password:
    client = Socrata("data.cityofnewyork.us", None)

    # First dataLimit results, returned as JSON from API / converted to Python list of
    # dictionaries by sodapy.
    date = "data_as_of >" + "'" + date + "'" 
    results = client.get("i4gi-tjb9", limit=dataLimit, borough = "Manhattan", where = date)
    
    # Convert to pandas DataFrame
    results_df = pd.DataFrame.from_records(results)
    
    #tipografia de los datos, separando datos de fecha en fecha y hora     ---------------------------------------
    results_df["time"] = results_df["data_as_of"].str.split("T").str.get(1) 
    results_df["time"] = results_df["time"].str.replace(".000", "")
    results_df["time_hour"] = results_df["time"].str.split(":").str.get(0) + ":00:00"
    results_df["time"] = pd.to_datetime(results_df["time"])
    results_df["date"] = results_df["data_as_of"].str.split("T").str.get(0) 
    results_df["date"]=pd.to_datetime(results_df["date"])
    results_df["weekday"] = results_df['date'].dt.day_name()

   
    #filtrando datos ---------------------------------------------------------------------------
    traffic = results_df[["id", "speed", "travel_time", "date", "time","borough", "link_name", "weekday", "time_hour"]]
    
    #guardando -----------------------------------------------------------------------------------------
    current_dir = os.getcwd().split("\TFG")[0] 
    filename = current_dir + "/TFG/apis_data/traffic_dataIngestion.csv"

    traffic.to_csv(filename, index=False)
    


    
#lastRegister = trafficDataIngestion(10, "2021-03-21T01:00:00.000")
#lastRegister = trafficDataIngestion(10, "2021-03-22T02:00:00.000")

