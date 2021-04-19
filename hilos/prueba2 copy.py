from datetime import datetime as dt
from datetime import timedelta as timedelta
from typing import List
from trafficApi import *
from airQualityApi import *
from weatherApi import *
import pandas as pd
import threading, time, os, csv, pytz

""" DEFINICIÓN DE VARIABLES
    Se registra la hora de ejecución
    Se guardan en variables las rutas de los archivos
    Se guardan en listas las cabeceras para cada archivo
"""
tz_NY = pytz.timezone('America/New_York') 
ini_datetime = dt.now(tz_NY).strftime("%Y-%m-%dT%H:%M:%S")
ini_datetime = "2021-01-31T00:00:00"  #--------------------------------fecha para pruebas en directo

current_dir = os.getcwd().split("\TFG")[0] + "/TFG/pruebas_maria/"

merge_file = current_dir + "merge.csv"
traffic_file = current_dir + "traffic.csv"
airQuality_file = current_dir + "airQuality.csv"
weather_file = current_dir + "weather.csv"

list_traffic = ["datetime","datetime_traffic","weekday","id","speed","travel_time","link_name"]
list_airQuality = ["datetime","AQI_PM2.5","Parameter_PM2.5","Unit_PM2.5","Value_PM2.5","Category_PM2.5","AQI_OZONE","Parameter_OZONE","Unit_OZONE","Value_OZONE","Category_OZONE"]
list_weather = ["datetime","Minimum Temperature","Maximum Temperature","Temperature","Dew Point","Relative Humidity","Heat Index","Wind Speed","Wind Gust","Wind Direction","Wind Chill","Precipitation","Precipitation Cover","Snow Depth","Visibility","Cloud Cover","Sea Level Pressure","Conditions"]
list_merge = list_traffic + list_airQuality[1:] + list_weather[1:]

""" METODOS PARA LLAMAR A LAS APIS
"""
def trafficApi(iter_time):
    print("traffic: executed")

    """ Si existe el archivo de tráfico primera consulta es a partir de la hora actual
        -- mientras método de API retorne falso se espera
        -- cuando método de API retorna verdadero se escribe el valor en merge y se empieza a iterar
    """
    write_thread = threading.Thread(target=write, args = (traffic_file,) )
    if os.path.isfile(traffic_file):
        print("traffic: file found")
        while not trafficDataIngestion(100000, ini_datetime, traffic_file):
            time.sleep(iter_time)
        write_thread.start()
    else:
        while not os.path.isfile(traffic_file):   #MIENTRAS NO EXISTA EL ARCHIVO PARA TRAFICO ESPERAMOS
            print("traffic: file not found")
            time.sleep(iter_time)
            if trafficDataIngestion(100000, ini_datetime, traffic_file):
                write_thread.start()
    
    """ Se empieza a iterar
        -- los valores para la consulta a la api se toman del último valor registrado en el archivo merge
    """
    count = 0 #-------------------------------------------------------contador que debe BORRARSE para hacer ejecución mas rápida
    while True:
        print(f"traffic: call {count}")
        time.sleep(iter_time)
        traffic= pd.read_csv(merge_file)     #SE LEE EL ULTIMO REGISTRO DE FECHA REGISTRADO EN MERGE PARA TRAFICO ---borrar: de esta forma se evita que por cuestiones de computo se consulte más rápido de lo que se escribe y se haga un salto en el registro de merge
        datetime = traffic.loc[traffic.index[-1], "datetime_traffic"]
        if trafficDataIngestion(100000, datetime, traffic_file):
            write_thread = threading.Thread(target=write, args = (traffic_file,) )
            write_thread.start()
        else:
            print("traffic: WAITING TO NEW VALUES")
        count += 1 

""" AirApi y Weather:
    Se consultan datos que se traen por hora
    --Al registrarlos en merge:
        * La fecha consultada debe ser menor que o igual a la fecha del último registro para tráfico en merge
        * Si se detecta un salto temporal en los datos de tráfico se introduce la línea en orden sin datos de tráfico
        * Si no hay valores para una Fecha y han pasado más de 2 horas se guarda el valor anterior

    --Se toma la hora de ejecución y a medida que se rellenen los datos se le va sumando 1 hora

    --Recomendaciones: hacer iteraciones cada 30 minutos al menos. 
                       Las apis tardan entre 1 hora y 2 horas en devolver los datos deseados. 
                       Por lo que de esta forma si se consulta a la 1 de ejecución y la api 
                       genera el valor para 1h25min no se tiene que esperar 2 horas enteras.
"""
def airApi(iter_time):
    print("air: executed")

    start_datetime = ini_datetime
    next_iter = False 

    """ Lógica para la primera vez que se ejecuta el código
    """
    while not os.path.isfile(airQuality_file) :
        print("air: file not found")
        time.sleep(iter_time)
        if airQualityDataIngestion(start_datetime, airQuality_file):
            start_datetime = dt.strptime(start_datetime, "%Y-%m-%dT%H:%M:%S") + timedelta(hours=1)
            start_datetime = str(start_datetime).replace(" ","T")
    while not next_iter:
        write_thread = threading.Thread(target=write, args = (airQuality_file,) )
        next_iter = write_thread.start()
        if not next_iter:
            time.sleep(iter_time/2)
      
    """ Se empieza a iterar
    """
    count = 0 #-------------------------------------------------------contador que debe BORRARSE para hacer ejecución mas rápida
    while True:
        print(f"air: call {count}")
        time.sleep(iter_time/2)
        while not airQualityDataIngestion(start_datetime, airQuality_file):
            time.sleep(iter_time)
         
        write_thread = threading.Thread(target=write, args = (airQuality_file,) )
        next_iter = write_thread.start()
        while not next_iter:
                print("air: WAITING TO NEW VALUES FOR TRAFFIC")
                time.sleep(iter_time/2)
                write_thread = threading.Thread(target=write, args = (airQuality_file,) )
                next_iter = write_thread.start()
        start_datetime = dt.strptime(str(start_datetime), "%Y-%m-%dT%H:%M:%S")+timedelta(hours=1)
        start_datetime = str(start_datetime).replace(" ","T")
        count += 1

#yaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa no leas más
#devuelve falso si faltan valores para trafico
def write(file_name, merge_file_used=merge_file, list=[]):
    """
        write("tests_threads/1T-new_date.csv","tests_threads/1T-merge_file.csv", list_airQuality)
        pd.read_csv("test_threads/1T.expected.csv")
    """
       
    print("write type:" + str(file_name))
    
    df0= pd.read_csv(merge_file_used)
    df0["datetime"] = pd.to_datetime(df0["datetime"])
    df0["datetime_traffic"] = pd.to_datetime(df0["datetime_traffic"])

    df1 = pd.read_csv(file_name)
    df1["datetime"] = pd.to_datetime(df1["datetime"])
    
    next_iter = False

    if file_name == traffic_file:
        df0 = pd.concat([df0, df1])
        df0.to_csv(merge_file_used, index= False)
        return True
    elif df0.shape[0] <= 0:  #es decir aun no se guardan datos de trafico
        return False
    """ CONDICIÓN ^^Línea de arriba - if TRUE: FIN FALSE: CONTINUE
        -- Si el documento no tiene ni un solo registro guardado no se ejecuta el resto del código
    """

    res = fileConcatMerge(df0, df1, list, "datetime")
    next_iter = res[0]
    df0 = res[1]
            
    df0.to_csv(merge_file_used, index= False)
  
    return next_iter

#pasados dos dataframe los indices de las columnas y la condicion de union
#se escribe en @df0 cuando se cumpla @condition en las columnas dadas @columns 
#los valores de @df1 en cada columna que se especifique y en cada linea que cumpla la condicion
#devuelve true si ingresa aunque sea una vez, si la fecha es mayor de a la de los datos guardados ya salimos
def fileConcatMerge(df0, df1, columns, condition):
    
    written = False #si se escribe aunque sea una linea se pone a TRUE
    first_in = True #si es la primera vez que se entra
    
    """ 1T: PRIMERA HORA: TRÁFICO SIN VALORES
        --Si para la primera hora consultada al inicio del programa no se encontraron valores de tráfico
            *se guarda el nuevo valor y se devuelve true
    """
    res = pd.to_datetime(df0.iloc[0,0], format="%Y-%m-%d %H:%M:%S") > pd.to_datetime(df1["datetime"], format="%Y-%m-%d %H:%M:%S")
    if res.bool():
        df0 = pd.merge(df0, df1, on=list_airQuality, how="outer", sort=True) 
        print(df0.head())  
        return [True, df0, "PRIMERA HORA: TRÁFICO SIN VALORES"]

    #La fecha de df1 se encuentra en la tabla df0
    if df0.loc[df0.index[-1], "datetime"] >= df1["datetime"]:     
            #La fecha se encuentra pero todavía no están todos los datos correspondientes a la hora
            #consultada por lo que se espera a tener todos los datos de traffico para escribir
            traffic_time = df0.loc[df0.index[-1], "datetime_traffic"]
            data_time = dt.strptime(str(df1["datetime"]), "%Y-%m-%d %H:%M:%S")
            res = traffic_time - data_time
            if res.seconds < 3599:
                print("fileconcat: WAITING TO NEW VALUES OF TRAFFIC!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                return False
            else:
                first_in ==False
    else:
        #si pasa esto es que aun no hay valores de trafico disponibles para la fecha buscada
        #se espera
        print("WAITING TO NEW VALUES OF TRAFFIC!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        return False

    for index, row in df0[::-1].iterrows():   #se itera en reversa 
        if row["datetime"] == df1["datetime"]:
            #coinciden las fechas por lo que se rellena la fila
            print("Written:")
            print(df1["datetime"])
            for i in columns[1:]:
                df0.loc[index, i ] = df1[i]
            written = True
        if row["datetime"] < df1["datetime"]:  #la fecha en df1 es mayor por lo que ya no tiene sentido seguir iterando ya que esta ordenado
            if not written:
                #se encontro un salto en los datos de trafico
                #se introduce la fila para la fecha al documento
                print("JUMP")
                df0 = pd.merge(df0, df1, on=list_airQuality, how="outer", sort=True)     
            return True
                
    return written

def ini():
    fileCreator(merge_file, list_merge) 
    traffic_api = threading.Thread(target = trafficApi, args = (1,))
    #se espera 30mint para que esten todos los resultados 
    air_api = threading.Thread(target=airApi, args = (5,) )
    #weather_api = threading.Thread(target=weatherApi, args = (5,) )
    #traffic_api.start()
    #air_api.start() 
    #airApi(min_29, hour_1)
    #weatherApi(min_29, hour_1)

#metodo que crea el archivo merge crea cabecera
def fileCreator(file_name, list): 
    if not os.path.isfile(file_name) :
            file = open(file_name, 'w')
            with file:
                # identifying header  
                writer = csv.DictWriter(file, fieldnames = list)
                # writing data row-wise into the csv file
                writer.writeheader()

def pruebasMari():

    print("pepe")
    #write("tests_threads/1T-new_date.csv","tests_threads/1T-merge_file.csv", list_airQuality)


pruebasMari()

if __name__ == '__main__':
    import doctest
    doctest.testmod()