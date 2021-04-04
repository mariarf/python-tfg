# make sure to install these packages before running:
# pip install pandas
# pip install sodapy

from numpy import select
import pandas as pd
from sodapy import Socrata
import os

#Date tiene que ser de formato: yyyy-mm-ddThh:mm:ss
def trafficDataIngestion(datalimit, start_datetime, end_datetime):

    # Unauthenticated client only works with public data sets. Note 'None'
    # in place of application token, and no username or password:
    client = Socrata("data.cityofnewyork.us", None)

    # First dataLimit results, returned as JSON from API / converted to Python list of
    # dictionaries by sodapy.
    #date = "data_as_of >" + "'" + date + "'"  #para a partir de una fecha
    date = f"data_as_of between '{start_datetime}' and '{end_datetime}'"
    
    columns = "data_as_of, id, speed, travel_time, link_name"

    #results = client.get("i4gi-tjb9", limit=dataLimit, borough = "Manhattan", where = date) #para a partir de una fecha
    results = client.get("i4gi-tjb9", limit = datalimit, borough = "Manhattan", where = date, select = columns)
    
    # Convert to pandas DataFrame
    results_df = pd.DataFrame.from_records(results)
   
    #-----------------------------------------datetime - time_hour --------------------------------------#
    results_df["time"] = results_df["data_as_of"].str[11:19]
    results_df["date"] = results_df["data_as_of"].str[0:11]
    results_df["time_hour"] = results_df["time"].str[0:3] + "00:00"

    results_df["datetime"] = results_df["date"] + results_df["time_hour"]
    results_df["datetime_traffic"] = results_df["date"] + results_df["time"]

    results_df["date"]=pd.to_datetime(results_df["date"])
    results_df["weekday"] = results_df['date'].dt.day_name()
   
    results_df["datetime"] = pd.to_datetime(results_df["datetime"])
    results_df["datetime_traffic"] = pd.to_datetime(results_df["datetime_traffic"])

    results_df = results_df[["datetime", "datetime_traffic", "weekday", "id", "speed", "travel_time", "link_name"]]
   
    #guardando -----------------------------------------------------------------------------------------
    current_dir = os.getcwd().split("\TFG")[0] 
    file_name = current_dir + f"/TFG/apis_data/traffic_historical/traffic_dataIngestion_{start_datetime[0:13]}_to_{end_datetime[0:13]}.csv"

    results_df.to_csv(file_name, index=False)
    print(f"TrafficApi: {file_name}")


#trafficDataIngestion(1000000, "2021-02-01T00:00:00", "2021-02-28T23:59:59")
#trafficDataIngestion(1000000, "2021-03-01T00:00:00", "2021-03-31T23:59:59")


