#!/usr/bin/env python

# make sure to install these packages before running:
# pip install pandas
# pip install sodapy

import datetime
import pandas as pd
import csv
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
    traffic = results_df[["id", "speed", "travel_time", "status","borough", "link_name", "hour", "date"]]
    boroughFilter = traffic[traffic["borough"] == "Manhattan"]

    boroughFilter.to_csv("trafficData_dataIngestion.csv")
    


    print(boroughFilter.head())
    return

dataIngestion(100)

def columnasAcotadas():
    file_to_open ="trafficData_dataIngestion.csv"

    with open(file_to_open) as csv_file:
        with open('trafficData_dataIngestion.csv', mode='r', newline='') as csv_file1:
            with open('trafficManhattan.csv', mode='w', newline='') as salida:
                csv_reader = csv.reader(csv_file, delimiter=',')
                rellenarSalida = csv.writer(salida, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                line_count = 0
                columnasAcotadas = ["id", "speed", "traveltime", "weekday", "status","borough", "link_name", "hour", "date", "day"]
                #rellenarSalida.writerow(columnas_acotadas)
                for row in csv_reader:    
                    columnasAcotadas[0:9]=row[0:9]             
                    #fecha_año=int(row[8].split("-")[0])
                    #fecha_mes=int(row[8].split("-")[1])
                    #fecha_dia=int(row[8].split("-")[2])

                    #columnasAcotadas[9]=diaSemana(fecha_año,fecha_mes,fecha_dia)
                    #print(columnasAcotadas[9])

                    rellenarSalida.writerow(columnasAcotadas)
     

                        
              
                    
                    if line_count%100000==0:
                        print(line_count)
                    line_count += 1
                    
                print(f'Processed {line_count} lines.')
    

columnasAcotadas()
