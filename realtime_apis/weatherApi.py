import pandas as pd
import requests, io, os
from airQualityApi import differenceDatetime 
from datetime import datetime as dt
from datetime import timedelta as timedelta

##Metodo que se conecta con la api y guarda datos en un rango de fecha en NY time--------------------------------------------
def weatherDataIngestion(start_datetime, file_dir):

    datetime= start_datetime[0:-5] + "00:00"

    # get data from the API
    url = "https://visual-crossing-weather.p.rapidapi.com/history"
    querystring = {"startDateTime":f"{datetime}","aggregateHours":"1","location":"Manhattan,NY,USA","unitGroup":"us","dayStartTime":"0:00:00","contentType":"csv","dayEndTime":"23:59:59","shortColumnNames":"0"}
  
    headers = {
        'x-rapidapi-key': "564857dda0msh05f30bc625bcd3ep1c10a8jsndf47856ab143",
        'x-rapidapi-host': "visual-crossing-weather.p.rapidapi.com"
        }
    response = requests.request("GET",url, headers=headers, params = querystring)  
   
    results_df = pd.read_csv(io.StringIO(response.content.decode('utf-8')))

    res = differenceDatetime(start_datetime)

    if results_df.empty or str(results_df.loc[0,"Info"]) == "No data available":
        #si han pasado mas de 3 horas (10800seg) y sigue estando vacio se pasa a la se consulta para la hora anterior
        if res.seconds > 10800:

            start_ = dt.strptime(start_datetime, "%Y-%m-%dT%H:%M:%S")  - timedelta(hours=1)
            weatherDataIngestion(str(start_).replace(" ", "T"), file_dir)
            
            result= pd.read_csv(file_dir)
            result["datetime"] = pd.to_datetime(result["datetime"])
            result.loc[0,"datetime"] = result.loc[0,"datetime"] + timedelta(hours=1)
            result["datetime"] =  result["datetime"].dt.strftime("%Y-%m-%dT%H:%M:%S")
            result.to_csv(file_dir, index = False)
            
            print(f"WeatherApi.empty: {start_datetime}")
            return True
        return False
    
    #tipografia de los datos,  -----------------------------------------------
    results_df["Date time"] = pd.to_datetime(results_df["Date time"]).dt.strftime("%Y-%m-%dT%H:%M:%S")
    results_df = results_df.rename(columns={"Date time": "datetime"}) 
    results_df = results_df.drop(["Address","Latitude","Longitude","Resolved Address","Name","Info", "Weather Type"], axis=1)
    
    results_df["Conditions"]= results_df["Conditions"].str.replace(",", "")

    #guardando datos obtenidos en csv 
    results_df.to_csv(file_dir, index=False)

    print(f"WeatherApi: {file_dir}")
    return True

#print(weatherDataIngestion("2021-04-29T12:00:00", "pepe.csv"))