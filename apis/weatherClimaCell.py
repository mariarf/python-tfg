import pandas as pd
import json, os, urllib3, certifi, csv, requests


##Metodo que se conecta con la api y guarda datos en un rango de fecha --------------------------------------------
def weatherDataIngestion():
    url = "https://visual-crossing-weather.p.rapidapi.com/history"

    querystring = {"startDateTime":"2019-01-01T00:00:00","aggregateHours":"1","location":"Manhattan,NY,USA","endDateTime":"2019-01-03T00:00:00","unitGroup":"us","dayStartTime":"0:00:00","contentType":"csv","dayEndTime":"23:59:59","shortColumnNames":"0"}

    headers = {
        'x-rapidapi-key': "564857dda0msh05f30bc625bcd3ep1c10a8jsndf47856ab143",
        'x-rapidapi-host': "visual-crossing-weather.p.rapidapi.com"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    print(response.text)
 

weatherDataIngestion()
    
