#!/usr/bin/env python

# make sure to install these packages before running:
# pip install pandas
# pip install sodapy

import datetime
import pandas as pd
from sodapy import Socrata



def diaSemana(año,mes,dia):
    week_days=["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]
    week_num=datetime.date(año,mes,dia).weekday()
    return(week_days[week_num])

def dataIngestion(dataLimit):

    # Unauthenticated client only works with public data sets. Note 'None'
    # in place of application token, and no username or password:
    client = Socrata("data.cityofnewyork.us", None)

    # First dataLimit results, returned as JSON from API / converted to Python list of
    # dictionaries by sodapy.
    results = client.get("i4gi-tjb9", limit=dataLimit)

    # Convert to pandas DataFrame
    results_df = pd.DataFrame.from_records(results)

    results_df["hour"] = results_df["data_as_of"].str.split("T").str.get(1) 
    results_df["date"] = results_df["data_as_of"].str.split("T").str.get(0) 

    print(results_df.dtypes)

    #filtrando datos
    traffic = results_df[["id", "speed", "status","borough", "link_name", "hour", "date"]]
    boroughFilter = traffic[traffic["borough"] == "Manhattan"]

    boroughFilter.to_csv("trafficData", index=False)
    


    print(boroughFilter.head())


dataIngestion(100)