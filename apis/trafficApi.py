# make sure to install these packages before running:
# pip install pandas
# pip install sodapy

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
    results_df["date"] = results_df["data_as_of"].str.split("T").str.get(0) 
    
    results_df["weekday"] = results_df["date"]
    weekDay(results_df["weekday"])
    
    #filtrando datos ---------------------------------------------------------------------------
    traffic = results_df[["id", "speed", "travel_time", "status", "date", "time","borough", "link_name", "weekday"]]
    
    #guardando -----------------------------------------------------------------------------------------
    current_dir = os.getcwd().split("\TFG")[0] 
    filename = current_dir + "/TFG/apis_data/traffic_dataIngestion.csv"

    traffic.to_csv(filename, index=False)

## Metodo que actualiza dataframe que se le pasa  
def weekDay(date):

    week_days=["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sabado", "Domingo"]
    for index, fecha in date.items():
        fecha = fecha.split("-")
        year = int(fecha[0])
        month = int(fecha[1])
        day = int(fecha[2])

        week_num=datetime.date(year, month, day).weekday()
        date[index] = week_days[week_num]
        
    return date
    
lastRegister = trafficDataIngestion(1000000, "2021-03-22T00:00:00.000")

