from auxMethods import apiHistoricalData
import pandas as pd
import json, os, urllib3, certifi, csv

##Metodo que se conecta con la api y guarda datos en un rango de fecha excluye la primera linea --------------------------------------------
def airQualityDataIngestion(start_datetime, end_datetime):

    ## handle certificate verification and SSL warnings
    # https://urllib3.readthedocs.io/en/latest/user-guide.html#ssl
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where())

    # get data from the API
    url = f"https://api.breezometer.com/air-quality/v2/historical/hourly?lat=40.6643&lon=-73.9385&key=4924f8f51fde48e0878c6f39c1be2405&start_datetime={start_datetime}&end_datetime={end_datetime}"
    request = http.request('GET',url)  

    # decode json data into a dict object
    data = json.loads(request.data.decode('utf-8'))

    # in this dataset, the data to extract is under 'data'
    results_df = pd.json_normalize(data, 'data')
    

    #tipografia de los datos, separando datos de fecha en fecha y hora -----------------------------------------------
    datetime = results_df["datetime"].str.split("T")
    results_df["time"] = datetime.str.get(1) 
    results_df["time"] = results_df["time"].str.replace("Z", " ")
    results_df["date"] = datetime.str.get(0) 
    
    #data filtering
    airQuality_df = results_df[["date", "time", "indexes.baqi.aqi", "indexes.baqi.color", "indexes.baqi.category", "indexes.baqi.dominant_pollutant"]]
    airQuality_df = airQuality_df.rename(columns={"indexes.baqi.aqi": "aqi", "indexes.baqi.color": "color", "indexes.baqi.category": "category", "indexes.baqi.dominant_pollutant": "dominant_pollutant" })

    #data saving as csv
    current_dir = os.getcwd().split("\TFG")[0] 
    file_name = current_dir + "/TFG/apis_data/airQuality_dataIngestion.csv"
    airQuality_df.to_csv(file_name, index=False)

    apiHistoricalData("airQuality_dataIngestion.csv", "airQuality_historical.csv" )

#airQualityDataIngestion("2021-03-21T00:00:00", "2021-03-21T08:00:00")
#airQualityDataIngestion("2021-03-21T08:30:00", "2021-03-21T23:59:59")