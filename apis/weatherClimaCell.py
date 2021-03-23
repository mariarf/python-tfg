import pandas as pd
import os, csv, requests, io
from auxMethods import *


##Metodo que se conecta con la api y guarda datos en un rango de fecha --------------------------------------------
def weatherDataIngestion():
    #parametros-------------------------------------------------------------
    start_datetime ="2021-03-20T15:00:00"
    end_datetime ="2021-03-20T16:00:00"

    # get data from the API
    url = "https://visual-crossing-weather.p.rapidapi.com/history"
    querystring = {"startDateTime":f"{start_datetime}","aggregateHours":"1","location":"Manhattan,NY,USA","endDateTime":f"{end_datetime}","unitGroup":"us","dayStartTime":"0:00:00","contentType":"csv","dayEndTime":"23:59:59","shortColumnNames":"0"}
  
    headers = {
        'x-rapidapi-key': "564857dda0msh05f30bc625bcd3ep1c10a8jsndf47856ab143",
        'x-rapidapi-host': "visual-crossing-weather.p.rapidapi.com"
        }
    response = requests.request("GET",url, headers=headers, params = querystring)  

    results_df = pd.read_csv(io.StringIO(response.content.decode('utf-8')))
    print(results_df.head())
  
    #tipografia de los datos, separando datos de fecha en fecha y hora -----------------------------------------------
    datetime = results_df["Date time"].str.split(" ")

    results_df["time"] = datetime.str.get(1) 
    results_df["date"] = datetime.str.get(0) 

    results_df["date"] = dateOrderSeries(results_df["date"])

    results_df["Date time"] =  results_df["date"].str.replace("/","-") + "T" + results_df["time"]



    
    weather_df = results_df[["Address","date","time","Temperature","Dew Point","Relative Humidity","Wind Speed","Wind Gust","Wind Direction","Precipitation","Snow Depth","Visibility","Cloud Cover","Sea Level Pressure","Conditions", "Date time"]]
    print(weather_df.head())
    #guardando datos obtenidos en csv 
    current_dir = os.getcwd().split("\TFG")[0] 
    file_name = current_dir + "/TFG/apis_data/weatherData_dataIngestion.csv"
    weather_df.to_csv(file_name, index=False)

    weatherFormat()

def weatherFormat():
    file_to_open =  os.getcwd().split("\TFG")[0] + "/TFG/apis_data/weatherData_dataIngestion.csv"
    data_result = os.getcwd().split("\TFG")[0] + "/TFG/apis_data/weatherFormat_dataIngestion.csv"

    with open(file_to_open) as csv_file:
        with open(data_result, mode='w', newline='') as out:
            csv_reader = csv.reader(csv_file, delimiter=',')
            fill_output = csv.writer(out, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            line_count = 0
            
            data = ["Address","date","time","Temperature","Dew Point","Relative Humidity","Wind Speed","Wind Gust","Wind Direction","Precipitation","Snow Depth","Visibility","Cloud Cover","Sea Level Pressure","Conditions"]
            for row in csv_reader: 
                if line_count>=1: 
                    data[0:2] = row[0:2]
                    data[2]=timeFormat(row[2])
                    data[3:16]=row[3:16]   
    
                fill_output.writerow(data)
    
                line_count += 1
                
            print(f'Processed {line_count} lines.')


   
weatherDataIngestion()
    
