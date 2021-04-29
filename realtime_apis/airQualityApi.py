from numpy import NaN
import pandas as pd
import json, os, urllib3, certifi, pytz
from datetime import datetime as dt
from datetime import timedelta as timedelta



def convertTimeStr(time, from_time, to_time):
    from_time = pytz.timezone(from_time)
    to_time = pytz.timezone(to_time)
   
    res = dt.strptime(time,"%Y-%m-%dT%H:%M:%S")
    res = from_time.localize(res)
    res = res.astimezone(to_time)
    res = res.strftime("%Y-%m-%dT%H:%M:%S")
    return res

#metodo que devuelve la diferencia entre la fecha local en NY y la fecha pasada por parametro
def differenceDatetime(datetime_value):
        tz_NY = pytz.timezone('America/New_York') 
        current_datetime = dt.now(tz_NY)
        #current_datetime = "2021-04-29 01:00:000000000000000"
        current_datetime = dt.strptime(str(current_datetime)[0:-13],"%Y-%m-%d %H:%M:%S")
        datetime_value = dt.strptime(datetime_value, "%Y-%m-%dT%H:%M:%S")
        print(current_datetime)
        print(datetime_value)
        return current_datetime - datetime_value

##Metodo que se conecta con la api y guarda datos en un rango de fecha excluye la primera linea --------------------------------------------
def airQualityDataIngestion(start_datetime, file_dir):
    print(f"airQualityDataIngestion: {start_datetime}")

    #pasando hora de NY a UTC para hacer la solicitud a la hora deseada
    hour_datetime = convertTimeStr(start_datetime, 'America/New_York', 'UTC')[0:13]
    
    # handle certificate verification and SSL warnings
    # https://urllib3.readthedocs.io/en/latest/user-guide.html#ssl
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where())

    # get data from the API
    url = f"https://www.airnowapi.org/aq/data/?startDate={hour_datetime}&endDate={hour_datetime}&parameters=OZONE,PM25&BBOX=-74.020308,40.700155,-73.940657,40.827572&dataType=B&format=application/json&verbose=0&nowcastonly=0&includerawconcentrations=0&API_KEY=7FD50518-C721-4C9A-861F-883367594091"
    response = http.request('GET', url)
    
    # decode json data into a dict object
    data = json.loads(response.data.decode('utf-8'))
    results_df = pd.DataFrame(data)
    
    res = differenceDatetime(start_datetime)
    
    if results_df.empty:
        #si han pasado mas de dos horas y sigue estando vacio se pasa a la se consulta para la hora anterior
        if res.seconds > 7200:

            start_ = dt.strptime(start_datetime, "%Y-%m-%dT%H:%M:%S")  - timedelta(hours=1)
            airQualityDataIngestion(str(start_).replace(" ", "T"), file_dir)
            
            result= pd.read_csv(file_dir)
            result["datetime"] = pd.to_datetime(result["datetime"])
            result.loc[0,"datetime"] = result.loc[0,"datetime"] + timedelta(hours=1)
            result["datetime"] =  result["datetime"].dt.strftime("%Y-%m-%dT%H:%M:%S")
            result.to_csv(file_dir, index = False)
            
            print(f"AirQualityApi.empty: {start_datetime}")
            return True

        return False
    print(res.seconds)
    try:
        results_df.loc[1, "Parameter"]
    except:
        if res.days <= 0:
            if res.seconds <= 7200:      
                return False
 
    results_df = results_df.rename(columns={"UTC": "datetime"}) 
    results_df["datetime"] = pd.to_datetime(results_df["datetime"])
    
    results_df = results_df[["datetime", "AQI", "Parameter", "Unit", "Value", "Category"]]
    print(results_df.head())
    
    results_df["datetime"] = results_df["datetime"].dt.tz_localize('UTC').dt.tz_convert('America/New_York').dt.strftime("%Y-%m-%dT%H:%M:%S")

    pm25_df = results_df.drop(results_df[results_df['Parameter']=="OZONE"].index)
    ozone_df = results_df.drop(results_df[results_df['Parameter']=="PM2.5"].index)

    #se guardan los valores en una sola fila por hora
    airQuality_df = pd.merge(pm25_df, ozone_df, on = "datetime", how = "outer", suffixes= ("_PM2.5", "_OZONE"))
    #aseguramos guardar valor en orden de fecha
    airQuality_df = airQuality_df.sort_values("datetime")

    #data saving as csv
    airQuality_df.to_csv(file_dir, index=False)

    print(f"AirQualityApi: {file_dir}")
    return True
  

#print(airQualityDataIngestion("2021-04-29T14:00:00", "pepe.csv"))