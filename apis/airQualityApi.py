import pandas as pd
import json, os, urllib3, certifi, csv
from auxMethods import *

##Metodo que se conecta con la api y guarda datos en un rango de fecha --------------------------------------------
def airQualityDataIngestion():
    #parametros-------------------------------------------------------------
    start_datetime ="2021-03-20T19:00:00"
    end_datetime ="2021-03-21T19:00:00"

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
    results_df["date"] = results_df["date"].str.replace("-", "/")


    #data filtering
    airQuality_df = results_df[["date", "time", "indexes.baqi.aqi", "indexes.baqi.color", "indexes.baqi.category", "indexes.baqi.dominant_pollutant"]]
    airQuality_df = airQuality_df.rename(columns={"indexes.baqi.aqi": "aqi", "indexes.baqi.color": "color", "indexes.baqi.category": "category", "indexes.baqi.dominant_pollutant": "dominant_pollutant" })

    #data saving as csv
    current_dir = os.getcwd().split("\TFG")[0] 
    filename = current_dir + "/TFG/apis_data/airQualityData_dataIngestion.csv"
    airQuality_df.to_csv(filename, index=False)


def airQualityFormat():
    file_to_open =  os.getcwd().split("\TFG")[0] + "/TFG/apis_data/airQualityData_dataIngestion.csv"
    data_result = os.getcwd().split("\TFG")[0] + "/TFG/apis_data/airQualityFormat_dataIngestion.csv"

    with open(file_to_open) as csv_file:
        with open(data_result, mode='w', newline='') as out:
            csv_reader = csv.reader(csv_file, delimiter=',')
            fill_output = csv.writer(out, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            line_count = 0
            
            data = ["date", "time", "aqi", "color", "category", "dominant_pollutant"]
            for row in csv_reader: 
                if line_count>=1: 
                    data[1]=timeFormat(row[1])
                    data[2:6]=row[2:6]   
    
                fill_output.writerow(data)
    
                line_count += 1
                
            print(f'Processed {line_count} lines.')


airQualityDataIngestion()
airQualityFormat()
