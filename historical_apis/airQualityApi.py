import pandas as pd
import json, os, urllib3, certifi, datetime, pytz

def convertTimeStr(time, from_time, to_time):
    from_time = pytz.timezone(from_time)
    to_time = pytz.timezone(to_time)

    res = datetime.datetime.strptime(time,"%Y-%m-%dT%H:%M:%S")
    res = from_time.localize(res)
    res = res.astimezone(to_time)
    res = res.strftime("%Y-%m-%dT%H:%M:%S")
    return res

##Metodo que se conecta con la api y guarda datos en un rango de fecha  --------------------------------------------
def airQualityDataIngestion(start_datetime, end_datetime):
    
    #data saving
    current_dir = os.getcwd().split("\TFG")[0] 
    file_name = current_dir + f"/TFG/apis_data/airQuality_historical/airQuality_dataIngestion_{start_datetime[0:13]}_to_{end_datetime[0:13]}.csv"

    #pasando hora de NY a UTC para hacer la solicitud a la hora deseada
    start_datetime = convertTimeStr(start_datetime, 'America/New_York', 'UTC')[0:13]
    end_datetime = convertTimeStr(end_datetime, 'America/New_York', 'UTC')[0:13]
    
    # handle certificate verification and SSL warnings
    # https://urllib3.readthedocs.io/en/latest/user-guide.html#ssl
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where())

    # get data from the API
    #keys: 3085AC4D-D4B0-4876-BF8F-FFE541AC6932
    #      7FD50518-C721-4C9A-861F-883367594091
    url = f"https://www.airnowapi.org/aq/data/?startDate={start_datetime}&endDate={end_datetime}&parameters=OZONE,PM25&BBOX=-74.020308,40.700155,-73.940657,40.827572&dataType=B&format=application/json&verbose=0&nowcastonly=0&includerawconcentrations=0&API_KEY=7FD50518-C721-4C9A-861F-883367594091"
    response = http.request('GET', url)
    
    # decode json data into a dict object
    data = json.loads(response.data.decode('utf-8'))
    results_df = pd.DataFrame(data)
    
    if results_df.empty:
        airQuality_df = airQualityApiDay(start_datetime + ":00:00", end_datetime + ":00:00")

    else:
        results_df = results_df.rename(columns={"UTC": "datetime"}) 
        results_df["datetime"] = pd.to_datetime(results_df["datetime"])
        results_df = results_df[["datetime", "AQI", "Parameter", "Unit", "Value", "Category"]]
    
        results_df["datetime"] = results_df["datetime"].dt.tz_localize('UTC').dt.tz_convert('America/New_York').dt.strftime("%Y-%m-%dT%H:%M:%S")

        pm25_df = results_df.drop(results_df[results_df['Parameter']=="OZONE"].index)
        ozone_df = results_df.drop(results_df[results_df['Parameter']=="PM2.5"].index)

        #se guardan los valores en una sola fila por hora
        airQuality_df = pd.merge(pm25_df, ozone_df, on = "datetime", how = "outer", suffixes= ("_PM2.5", "_OZONE"))
        #aseguramos guardar valor en orden de fecha
        airQuality_df = airQuality_df.sort_values("datetime")

    #data saving as csv
    airQuality_df.to_csv(file_name, index=False)

    print(f"AirQualityApi: {file_name}")
  
def airQualityApiDay(start_datetime, end_datetime):

# handle certificate verification and SSL warnings
    # https://urllib3.readthedocs.io/en/latest/user-guide.html#ssl
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where())

    res = True
    datetime_value = datetime.datetime.strptime(start_datetime,"%Y-%m-%dT%H:%M:%S")
    airQuality_df = pd.DataFrame(columns=["datetime"])
    while res:
        date = str(datetime_value)[0:10]
        url = f"https://www.airnowapi.org/aq/observation/latLong/historical/?format=application/json&latitude=40.754932&longitude=-73.984016&date={date}T00-0000&distance=25&API_KEY=020336F7-8B54-482A-AF80-B8224328A0C6" 
        response = http.request('GET', url)
        
        data = json.loads(response.data.decode('utf-8'))
        results_df = pd.DataFrame(data)
        
        results_df = results_df.rename(columns={"DateObserved": "datetime", "ParameterName": "Parameter"}) 
        results_df["datetime"] = results_df["datetime"].str.replace(" ","T00:00:00") 

        datetime_value += datetime.timedelta(days=1)
        res = datetime_value <= datetime.datetime.strptime(end_datetime,"%Y-%m-%dT%H:%M:%S")
        
        results_df["Category"] = results_df["Category"].apply(pd.Series)
    
        results_df = results_df[["datetime", "AQI", "Parameter", "Category"]]
        
        pm25_df = results_df.drop(results_df[results_df['Parameter']=="OZONE"].index)
        ozone_df = results_df.drop(results_df[results_df['Parameter']=="PM2.5"].index)
       
        #se guardan los valores en una sola fila por hora
        results_df = pd.merge(pm25_df, ozone_df, on = "datetime", how = "outer", suffixes= ("_PM2.5", "_OZONE"))
        i = 1
        results_df["datetime"] = pd.to_datetime(results_df["datetime"])
        for i in range(24):
            results_df.loc[i] = results_df.loc[0]
            results_df.loc[i, "datetime"] += datetime.timedelta(hours=i)
        
        airQuality_df = pd.concat([airQuality_df,results_df])
    
    return airQuality_df

#airQualityDataIngestion("2019-02-16T00:00:00", "2019-02-28T23:59:59")