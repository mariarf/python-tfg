from datetime import datetime as dt
from datetime import timedelta as timedelta
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
#ini_datetime = "2021-05-01T15:00:00"

next_iter_airQuality = False
next_iter_weather = False

#ini_datetime = "2021-01-31T00:00:00"  #--------------------------------fecha para pruebas en directo

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
def trafficApi(iter_time, limit):
    print("traffic: executed")
    
    """ Si existe el archivo de tráfico primera consulta es a partir de la hora actual
        -- mientras método de API retorne falso se espera
        -- cuando método de API retorna verdadero se escribe el valor en merge y se empieza a iterar
    """  
    while not trafficDataIngestion(limit, ini_datetime, traffic_file):
        print("traffic: file not found - waiting to new values")
        time.sleep(iter_time)

    write_thread = threading.Thread(target=write, args = (traffic_file,) )
    write_thread.start()
    time.sleep(10)
    
    """ Se empieza a iterar
        -- los valores para la consulta a la api se toman del último valor registrado en el archivo merge
    """
    count = 0 #-------------------------------------------------------contador que debe BORRARSE para hacer ejecución mas rápida
    while True:
        print(f"traffic: call {count}")
        traffic= pd.read_csv(merge_file)     #SE LEE EL ULTIMO REGISTRO DE FECHA REGISTRADO EN MERGE PARA TRAFICO ---borrar: de esta forma se evita que por cuestiones de computo se consulte más rápido de lo que se escribe y se haga un salto en el registro de merge
        datetime = traffic.loc[traffic.index[-1], "datetime_traffic"]
       
        while not trafficDataIngestion(limit, datetime, traffic_file):
            print("traffic: WAITING TO NEW VALUES")
            time.sleep(iter_time)
        
        write_thread = threading.Thread(target=write, args = (traffic_file,) )
        write_thread.start()
        time.sleep(10)
        count += 1 

""" AirApi y Weather:
    Se consultan datos que se traen por hora
    --Al registrarlos en merge:
        * La fecha consultada debe ser menor que la fecha del último registro para tráfico en merge
        * Si se detecta un salto temporal en los datos de tráfico se introduce la línea en orden sin datos de tráfico
        * APIS - Si no hay valores para una Fecha y han pasado más de 2 horas se guarda el valor anterior

    --Se toma la hora de ejecución y a medida que se rellenen los datos se le va sumando 1 hora

    --Recomendaciones: hacer iteraciones cada 30 minutos al menos. 
                       Las apis tardan entre 1 hora y 2 horas en devolver los datos deseados. 
                       Por lo que de esta forma si se consulta al pasar 1h de ejecución y la api 
                       genera el valor para cuando ha pasado 1h25min no se tiene que esperar 2h enteras.
"""
def weatherApi(iter_time):
    print("weather: executed")

    start_datetime = ini_datetime
    global next_iter_weather 
    while True:
        print(f"weather: call {start_datetime}")
        time.sleep(iter_time)
        while not weatherDataIngestion(start_datetime, weather_file):
            print(f"weather: WAITING TO NEW VALUES FOR WEATHER")
            time.sleep(iter_time)
         
        write_thread = threading.Thread(target=write, args = (weather_file, merge_file, list_weather) )
        write_thread.start()
        time.sleep(10)
    
        while not next_iter_weather:
                print(f"weather: WAITING TO NEW VALUES FOR TRAFFIC {start_datetime}")
                time.sleep(iter_time/2)
                write_thread = threading.Thread(target=write, args = (weather_file,) )
                write_thread.start()
                time.sleep(10)

        
        next_iter_weather = False
        start_datetime = dt.strptime(str(start_datetime), "%Y-%m-%dT%H:%M:%S") + timedelta(hours=1)
        start_datetime = str(start_datetime).replace(" ","T")



def airApi(iter_time):
    print("air: executed")

    start_datetime = ini_datetime
    global next_iter_airQuality

    while True:
        print(f"air: call {start_datetime}")
        time.sleep(iter_time)
        while not airQualityDataIngestion(start_datetime, airQuality_file):
            print(f"air: WAITING TO NEW VALUES FOR AIRQUALITY")
            time.sleep(iter_time)
         
        write_thread = threading.Thread(target=write, args = (airQuality_file, merge_file, list_airQuality) )
        write_thread.start()
        time.sleep(10)
        while not next_iter_airQuality:
                print(f"air: WAITING TO NEW VALUES FOR TRAFFIC {start_datetime}")
                time.sleep(iter_time/2)
                write_thread = threading.Thread(target=write, args = (airQuality_file,) )
                write_thread.start()
                time.sleep(10)

        
        next_iter_airQuality = False
           
        start_datetime = dt.strptime(str(start_datetime), "%Y-%m-%dT%H:%M:%S") + timedelta(hours=1)
        start_datetime = str(start_datetime).replace(" ","T")


""" write:
    *** recibe dos direcciones de archivos @file_name,  @merge_file_used y una lista @list con nombres de columnas
    - Si el @file_name es el correspondiente a tráfico
        *se registran los nuevos valores
    - Si @merge_file_used esta en blanco
        *se devuelve false y se sale del metodo
    - else
        *Se llama al metodo fileConcatMerge
            se devuelve el resultado de la llamada
"""

def write(file_name, merge_file_used=merge_file, list=[]):
    print("write type:" + str(file_name))
    
    df0= pd.read_csv(merge_file_used)
    df0["datetime"] = pd.to_datetime(df0["datetime"])

    df1 = pd.read_csv(file_name)
    df1["datetime"] = pd.to_datetime(df1["datetime"]) 

    """ 1T_W: SE REGISTRAN VALORES DE TRÁFICO
        2T_W: NO HAY VALORES DE TRÁFICO EN MERGE
            * se espera para guardar cualquier otro valor distinto a los de tráfico
    """   
    if file_name == traffic_file:
        df0 = pd.concat([df0, df1])
        df0.to_csv(merge_file_used, index= False)
        return
    elif df0.shape[0] <= 0:  #es decir aun no se guardan datos de trafico
        return
        #return False
    """ CONDICIÓN ^^Línea de arriba - if TRUE: FIN else FALSE: CONTINUE
        -- Si el documento no tiene ni un solo registro guardado no se ejecuta el resto del código
    """
    result = fileConcatMerge(df0, df1, list)

    if file_name == airQuality_file:
        global next_iter_airQuality
        next_iter_airQuality = result[0]        
    elif file_name == weather_file:
        global next_iter_weather 
        next_iter_weather= result[0]
    
    if not result[0]:
        return

    df0 = result[1]
    df0.to_csv(merge_file_used, index= False)
    print(result[2])
    


""" fileConcatMerge:   
    *** recibe dos dataframes @df0 y @df1 y una lista con nombres de columnas @columns
    -Incluye en @df0 los valores de @df1 de @columns cuando la columna "datetime" coincide
    -Sólo registra los valores de @df1 en @df0 
        *Si, se han recogido todos los valores de tráfico para el valor "datetime" en @df0
            es decir, se registra cuando el último valor de @df0["datetime"] es mayor que @df1["datetime"]
    -En caso de no encontrar coincidencias:
        *Si se cumple la condicion anterior, indica que no hay valores de tráfico para el "datetime" consultado
            entonces, se registran los valores de @df1 para "datetime" y se dejan en NaN los valores de tráfico
"""
def fileConcatMerge(df0, df1, columns):
    sms = "fileConcatMerge: executed"
    print(sms)
        
    res = pd.to_datetime(df0.loc[df0.index[-1], "datetime"], format="%Y-%m-%d %H:%M:%S") <= pd.to_datetime(df1["datetime"], format="%Y-%m-%d %H:%M:%S")
    if res.bool():
        """ 1T_W_F: AUN FALTAN VALORES DE TRÁFICO 
        -- Hasta que no se registre la hora entera de tráfico no se guardan los datos
            * return false, se espera a que esten todos los valores para la hora a registrar               
        """
        sms =  "fileConcatMerge: 1T_W AUN FALTAN VALORES PARA TRÁFICO"
        return [False, df0, sms]
    else:
        result = df0["datetime"].isin(df1["datetime"]).any().any()
        if not result: 
            """ 2T_W_F: SALTO EN VALORES DE TRÁFICO
            -- Hay valores de tráfico mayores a la hora consulta pero NO se encontraron coincidencias
                *return true, se registran los nuevos valores
            """
            df0 = pd.merge(df0, df1, on=list_airQuality, how="outer", sort=True) 
            sms = "fileConcatMerge: 2T_W SALTO EN VALORES DE TRÁFICO"
            return [True, df0, sms]
            
    """ ULTIMA HORA DE TRÁFICO ES MAYOR QUE LA HORA A REGISTRAR
        HAY AL MENOS UNA FECHA QUE COINCIDE
    """
    """ 3T_W_F: REGISTRO CORRECTO
        -- Se pasa una lista de valores y se registran cuando @datetime coincida
    """

    for i in columns[1:]:
        df0.loc[df0.datetime == df1.loc[0,"datetime"], i]= df1.loc[0, i]

    result = df0["datetime"].isin(df1["datetime"]).any().any()
    sms = "fileConcatMerge: 3T_W REGISTRO CORRECTO"
    
    return[True, df0, sms]

def ini():
    fileCreator(merge_file, list_merge) 
    traffic_api = threading.Thread(target = trafficApi, args = (15*60, 10000000), name="traffic_api")
    #se espera 30mint para que esten todos los resultados 
    air_api = threading.Thread(target=airApi, args = (30*60,), name="air_api")
    weather_api = threading.Thread(target=weatherApi, args = (45*60,) )
    traffic_api.start()
    air_api.start() 
    weather_api.start()
    

""" fileCreator:
    *** recibe una direccion/path @file_name y una lista @list con nombres de columnas
    - Si el archivo @file_name no existe
        *entonces lo crea y le asigna @list como cabecera
"""
def fileCreator(file_name, list): 
    if not os.path.isfile(file_name) :
            file = open(file_name, 'w')
            with file:
                # identifying header  
                writer = csv.DictWriter(file, fieldnames = list)
                # writing data row-wise into the csv file
                writer.writeheader()

ini()