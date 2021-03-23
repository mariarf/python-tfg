#!/usr/bin/env python

# make sure to install these packages before running:
# pip install pandas
# pip install sodapy

from numpy import empty
import pandas as pd
from sodapy import Socrata
import os, csv
from auxMethods import *


def trafficDataIngestion(dataLimit, date):

    date = "data_as_of >" + "'" + "2021-03-21T00:00:00.000" + "'" 

    # Unauthenticated client only works with public data sets. Note 'None'
    # in place of application token, and no username or password:
    client = Socrata("data.cityofnewyork.us", None)


    # First dataLimit results, returned as JSON from API / converted to Python list of
    # dictionaries by sodapy.
    results = client.get("i4gi-tjb9", limit=dataLimit, borough = "Manhattan", where = date)
    

    # Convert to pandas DataFrame
    results_df = pd.DataFrame.from_records(results)
    print(results_df.head())

    #se guarda el valor de la fecha del ultimo registro -------------------------------------------------------------------------
    last_register = results_df.loc[results_df.index[-1], "data_as_of"]
    

    #tipografia de los datos, separando datos de fecha en fecha y hora     ---------------------------------------
    results_df["time"] = results_df["data_as_of"].str.split("T").str.get(1) 
    results_df["time"] = results_df["time"].str.replace(".000", " ")
    results_df["date"] = results_df["data_as_of"].str.split("T").str.get(0) 
    results_df["date"] = results_df["date"].str.replace("-", "/")

    #filtrando datos ---------------------------------------------------------------------------
    traffic = results_df[["id", "speed", "travel_time", "status", "date", "time","borough", "link_name"]]
    
    
    #guardando -----------------------------------------------------------------------------------------
    current_dir = os.getcwd().split("\TFG")[0] 
    filename = current_dir + "/TFG/apis_data/trafficData_dataIngestion.csv"

    traffic.to_csv(filename, index=False)

    #llamas metodo para darle formato al contenido --------------------------------------------------------------
    trafficFormat()


    return last_register

def trafficFormat():

    file_to_open =  os.getcwd().split("\TFG")[0] + "/TFG/apis_data/trafficData_dataIngestion.csv"
    data_result = os.getcwd().split("\TFG")[0] + "/TFG/apis_data/trafficDataFormat_dataIngestion.csv"

    with open(file_to_open) as csv_file:
        with open(data_result, mode='w', newline='') as out:
            csv_reader = csv.reader(csv_file, delimiter=',')
            fill_output = csv.writer(out, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            line_count = 0
            
            data = ["id", "speed", "travel_time", "status", "date", "time", "weekday", "borough", "link_name"]

            for row in csv_reader: 
                if line_count>=1: 
                    print(row[4])
                    date_split= row[4].split("/")   
                    date_year=int(date_split[0])
                    date_month=int(date_split[1])
                    date_day=int(date_split[2])
                    data[6]= weekDay(date_year,date_month,date_day)
                    data[5]= timeFormat(row[5])
                
                data[0:5]=row[0:5]   
                data[7:9]=row[7:9]   
            
                fill_output.writerow(data)
    
                if line_count%100000==0:
                    print(line_count)
                line_count += 1
                
            print(f'Processed {line_count} lines.')
    
lastRegister = trafficDataIngestion(1000000, "2021-03-13T00:00:00.000")
#print(lastRegister)
#dataIngestion(1000, "2021-03-12T00:00:00.000")
#columnasAcotadas()
#historicalTrafficApi()
