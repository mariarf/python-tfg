from datetime import datetime as dt
from datetime import timedelta as timedelta


from numpy import equal, true_divide
from trafficApi import *
from airQualityApi import *
from weatherApi import *
import pandas as pd
import threading, time, os, csv, pytz

tz_NY = pytz.timezone('America/New_York') 
ini_datetime = dt.now(tz_NY).strftime("%Y-%m-%dT%H:%M:%S")
ini_datetime = "2021-01-31T00:00:00"
print(ini_datetime)

current_dir = os.getcwd().split("\TFG")[0] + "/TFG/pruebas_maria/"

merge_file = current_dir + "merge.csv"
traffic_file = current_dir + "traffic.csv"
airQuality_file = current_dir + "airQuality.csv"
weather_file = current_dir + "weather.csv"

list_traffic = ["datetime","datetime_traffic","weekday","id","speed","travel_time","link_name"]
list_airQuality = ["datetime","AQI_PM2.5","Parameter_PM2.5","Unit_PM2.5","Value_PM2.5","Category_PM2.5","AQI_OZONE","Parameter_OZONE","Unit_OZONE","Value_OZONE","Category_OZONE"]
list_weather = ["datetime","Minimum Temperature","Maximum Temperature","Temperature","Dew Point","Relative Humidity","Heat Index","Wind Speed","Wind Gust","Wind Direction","Wind Chill","Precipitation","Precipitation Cover","Snow Depth","Visibility","Cloud Cover","Sea Level Pressure","Conditions"]
list_merge = list_traffic + list_airQuality[1:] + list_weather[1:]

def trafficApi(iter_time):
    print("traffic: executed")

    while not os.path.isfile(traffic_file):
        print("traffic: file not found")
        time.sleep(iter_time)
        if trafficDataIngestion(10000, ini_datetime, traffic_file):
            write_thread = threading.Thread(target=write, args = (traffic_file,) )
            write_thread.start()
    count = 0
    while True:
        print(f"traffic: call {count}")
        time.sleep(iter_time)
        traffic= pd.read_csv(traffic_file)
        datetime = traffic.loc[traffic.index[-1], "datetime_traffic"]
        if trafficDataIngestion(10000, datetime, traffic_file):
            write_thread = threading.Thread(target=write, args = (traffic_file,) )
            write_thread.start()
        else:
            print("traffic: WAITING TO NEW VALUES!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        count += 1 

def airApi(iter_time):
    print("air: executed")

    start_datetime = ini_datetime
    while not os.path.isfile(airQuality_file) :
        print("air: file not found")
        time.sleep(iter_time)
        if airQualityDataIngestion(start_datetime, airQuality_file):
            start_datetime = dt.strptime(start_datetime, "%Y-%m-%dT%H:%M:%S") + timedelta(hours=1)
            start_datetime = str(start_datetime).replace(" ","T")
        
    write_thread = threading.Thread(target=write, args = (airQuality_file,) )
    write_thread.start()
    count = 0
    while True:
        print(f"air: call {count}")
        time.sleep(iter_time)
      
        if airQualityDataIngestion(start_datetime, airQuality_file):
            write_thread = threading.Thread(target=write, args = (airQuality_file,) )
            next_iter = write_thread.start()
            while not next_iter:
                print("wait to next traffic value")
                time.sleep(iter_time)
                next_iter = write(airQuality_file)
            start_datetime = dt.strptime(str(start_datetime), "%Y-%m-%dT%H:%M:%S")+timedelta(hours=1)
            start_datetime = str(start_datetime).replace(" ","T")
        else:
            print("air: WAITING TO NEW VALUES!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        count += 1

def weatherApi(iter_time):
    print("weather entrando")

    if not os.path.isfile(weather_file) :
        time.sleep(iter_time)
        current_datetime = datetime.datetime.now(tz_NY).strftime("%Y-%m-%dT%H:%M:%S")
        weatherDataIngestion( ini_datetime, current_datetime, weather_file)
        write(weather_file)

    while True:
        print("call weather")
        time.sleep(iter_time)

        weather= pd.read_csv(weather_file)
        start_datetime = weather.loc[weather.index[-1], "datetime"]
        current_datetime = datetime.datetime.now(tz_NY).strftime("%Y-%m-%dT%H:%M:%S")

        weatherDataIngestion(1000000, start_datetime, current_datetime, weather_file)
        write(weather_file)

def write(file_name):
    print("write type:" + str(file_name))

    df0= pd.read_csv(merge_file)
    df0["datetime"] = pd.to_datetime(df0["datetime"])
    df0["datetime_traffic"] = pd.to_datetime(df0["datetime_traffic"])


    df1 = pd.read_csv(file_name)
    df1["datetime"] = pd.to_datetime(df1["datetime"])

    next_iter = True

    if file_name == traffic_file:
        df0 = pd.concat([df0, df1])
        df0.to_csv(merge_file, index= False)
        return True
    elif df0.shape[0] <= 0:
        return False

    if file_name == airQuality_file:
        fileContatMerge(df0, df1.loc[0], list_airQuality, "datetime")
    if file_name == weather_file:
        fileContatMerge(df0, df1, list_weather, "datetime")
    
    df0.to_csv(merge_file, index= False)
    traffic_time = df0.loc[df0.index[-1], "datetime_traffic"]
    data_time = dt.strptime(str(df1.loc[0, "datetime"]), "%Y-%m-%d %H:%M:%S")
    res = traffic_time - data_time
    if res.seconds < 3599:
         next_iter = False
    return next_iter

#pasados dos dataframe los indices de las columnas y la condicion de union
#se escribe en @df0 cuando se cumpla @condition en las columnas dadas @columns 
#los valores de @df1 en cada columna que se especifique y en cada linea que cumpla la condicion
#devuelve true si ingresa aunque sea una vez, si la fecha es mayor de a la de los datos guardados ya salimos
def fileContatMerge(df0, df1, columns, condition):
    write = False
    for index, row in df0[::-1].iterrows():   #se itera desde detras
        if row["datetime"] < df1["datetime"]:  #si el valor a escribir es mayor que la ultima fecha registrada en merge se sale
            print("End")
            return write
        if row["datetime"] == df1["datetime"]:  #si se escribe ponemos write a true
            print("Written:")
            print(df1["datetime"])
            for i in columns[1:]:
                df0.loc[index, i ] = df1[i]
            write = True
    return write

def ini():

    fileCreator(merge_file, list_merge) 

    min_5 = 300
    min_1 = 60
    min_59 = 3540

    traffic_api = threading.Thread(target = trafficApi, args = (1,))
    #se espera hora para que esten todos los resultados 
    air_api = threading.Thread(target=airApi, args = (1,) )
    weather_api = threading.Thread(target=weatherApi, args = (min_59,) )
    
    
    traffic_api.start()
    #air_api.start()
    
    #airApi(min_29, hour_1)
    #weatherApi(min_29, hour_1)
    


def fileCreator(file_name, list): 
    if not os.path.isfile(file_name) :
            file = open(file_name, 'w')
            with file:
                # identifying header  
                writer = csv.DictWriter(file, fieldnames = list)
                # writing data row-wise into the csv file
                writer.writeheader()

ini()


#weatherDataIngestion("2021-04-11T11:00:00", "2021-04-11T11:00:00", f"{current_dir}weather1.csv")
#weatherDataIngestion("2021-04-11T12:00:00", "2021-04-11T12:00:00", f"{current_dir}weather2.csv")
#weatherDataIngestion("2021-04-11T13:00:00", "2021-04-11T13:00:00", f"{current_dir}weather3.csv")
#weatherDataIngestion("2021-04-11T14:00:00", "2021-04-11T14:00:00", f"{current_dir}weather4.csv")
#airQualityDataIngestion("2021-04-11T11:05:05", "2021-04-11T11:10:05", f"{current_dir}air1.csv")
#airQualityDataIngestion("2021-04-11T12:05:05", "2021-04-11T12:10:05", f"{current_dir}air2.csv")
#airQualityDataIngestion("2021-04-11T13:05:05", "2021-04-11T13:10:05", f"{current_dir}air3.csv")
#airQualityDataIngestion("2021-04-11T14:05:05", "2021-04-11T14:10:05", f"{current_dir}air4.csv")
#trafficDataIngestion(1000000, "2021-04-11T11:00:00","2021-04-11T12:59:59", f"{current_dir}traffic1.csv")
#trafficDataIngestion(1000000, "2021-04-11T13:00:00","2021-04-11T14:59:59", f"{current_dir}traffic2.csv")
#trafficDataIngestion(1000000, "2021-04-11T15:00:00","2021-04-11T15:10:59", f"{current_dir}traffic3.csv")
#trafficApi()
#airApi()
#weatherApi()
#write(2)
    