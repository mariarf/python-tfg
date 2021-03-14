#!/usr/bin/env python

# make sure to install these packages before running:
# pip install pandas
# pip install sodapy
#import metodosFormatos
from apis.metodosFormatos import *
import pandas as pd
import csv
from sodapy import Socrata
import os
import requests
import json


def dataIngestion(dataLimit, date):

    # Unauthenticated client only works with public data sets. Note 'None'
    # in place of application token, and no username or password:
    client = Socrata("data.cityofnewyork.us", None)
    #client.timeout = 50

    # First dataLimit results, returned as JSON from API / converted to Python list of
    # dictionaries by sodapy.
    
    results = client.get("i4gi-tjb9", limit=dataLimit, borough = "Manhattan", where = "data_as_of > '2021-03-03T00:00:00.000' ")

    # Convert to pandas DataFrame
    results_df = pd.DataFrame.from_records(results)

    """
    #leyendo datos con request
    url= 'https://data.cityofnewyork.us/resource/i4gi-tjb9.json'
    results=requests.get(url, timeout=10)
        
    #print(results.content)
    response_json = json.loads(results.text)
    # Convert to pandas DataFrame
    results_df = pd.DataFrame.from_records(response_json)
    """
    print(results_df["data_as_of"])

    #separando datos de fecha en fecha y hora
    results_df["time"] = results_df["data_as_of"].str.split("T").str.get(1) 
    results_df["date"] = results_df["data_as_of"].str.split("T").str.get(0) 
    results_df["date"] = results_df["date"].str.replace("-", "/")

    #muestra la cabecera de la tabla y el tipo de dato
    print(results_df.dtypes)

    #filtrando datos
    traffic = results_df[["id", "speed", "travel_time", "status", "date", "time","borough", "link_name"]]
    
    #boroughFilter = traffic[traffic["borough"] == "Manhattan"]
    
    #guardando 
    current_dir = os.getcwd().split("\TFG")[0] 
    filename = current_dir + "/TFG/apis_data/trafficData_dataIngestion.csv"

   # boroughFilter.to_csv(filename, index=False)
    traffic.to_csv(filename, index=False)
    

def columnasAcotadas():

    file_to_open =  os.getcwd().split("\TFG")[0] + "/TFG/apis_data/trafficData_dataIngestion.csv"
    data_result = os.getcwd().split("\TFG")[0] + "/TFG/apis_data/trafficManhattan.csv"


    with open(file_to_open) as csv_file:
        
        with open(data_result, mode='w', newline='') as salida:
            csv_reader = csv.reader(csv_file, delimiter=',')
            rellenarSalida = csv.writer(salida, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            line_count = 0
            
            columnasAcotadas = ["id", "speed", "travel_time", "status", "date", "time", "weekday", "borough", "link_name"]
            #rellenarSalida.writerow(columnas_acotadas)
            for row in csv_reader: 
                if line_count>=1: 
                    print(row[4])
                    fecha_split= row[4].split("/")   
                    fecha_año=int(fecha_split[0])
                    fecha_mes=int(fecha_split[1])
                    fecha_dia=int(fecha_split[2])
                    columnasAcotadas[6]=diaSemana(fecha_año,fecha_mes,fecha_dia)
                    columnasAcotadas[5]=horaFormato(row[5])
                
                columnasAcotadas[0:5]=row[0:5]   
                columnasAcotadas[7:9]=row[7:9]   
            
                rellenarSalida.writerow(columnasAcotadas)
    
                if line_count%100000==0:
                    print(line_count)
                line_count += 1
                
            print(f'Processed {line_count} lines.')
    
#dataIngestion(2000, 50)
columnasAcotadas()
