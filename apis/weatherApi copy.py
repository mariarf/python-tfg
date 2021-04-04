import pandas as pd
import os, csv, requests, io
from auxMethods import *


##Metodo que se conecta con la api y guarda datos en un rango de fecha --------------------------------------------
def weatherDataIngestion(start_datetime, end_datetime):

    start_datetime= start_datetime[0:-5] + "00:00"

    # get data from the API
    url = "https://visual-crossing-weather.p.rapidapi.com/history"
    querystring = {"startDateTime":f"{start_datetime}","aggregateHours":"1","location":"Manhattan,NY,USA","endDateTime":f"{end_datetime}","unitGroup":"us","dayStartTime":"0:00:00","contentType":"csv","dayEndTime":"23:59:59","shortColumnNames":"0"}
  
    headers = {
        'x-rapidapi-key': "564857dda0msh05f30bc625bcd3ep1c10a8jsndf47856ab143",
        'x-rapidapi-host': "visual-crossing-weather.p.rapidapi.com"
        }
    response = requests.request("GET",url, headers=headers, params = querystring)  

    results_df = pd.read_csv(io.StringIO(response.content.decode('utf-8')))

    #tipografia de los datos, separando datos de fecha en fecha y hora -----------------------------------------------
    datetime = results_df["Date time"].str.split(" ")

    results_df["time"] = datetime.str.get(1) 
    results_df["date"] = datetime.str.get(0) 
 
    results_df["date"]= pd.to_datetime(results_df["date"])

    weather_df = results_df[["date","time","Temperature","Dew Point","Relative Humidity","Wind Speed","Wind Gust","Wind Direction","Precipitation","Snow Depth","Visibility","Cloud Cover","Sea Level Pressure","Conditions"]]

    #guardando datos obtenidos en csv 
    current_dir = os.getcwd().split("\TFG")[0] 
    file_name = current_dir + "/TFG/apis_data/weather_dataIngestion.csv"
    weather_df.to_csv(file_name, index=False)
    #apiHistoricalData("weather_dataIngestion.csv", "weather_historical.csv" )

#weatherDataIngestion("2021-03-28T00:00:00", "2021-03-29T00:00:00")
#weatherDataIngestion("2021-03-21T08:30:00", "2021-03-21T23:59:59")
