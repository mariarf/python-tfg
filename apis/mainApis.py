#from trafficApi import dataIngestion
#from airQualityApi import *
import trafficApi
import airQualityApi
import os
import pandas as pd
import numpy as np
"""
#creando archivo compatible con pandas
    data_folder = os.getcwd().split("\TFG")[0] + "/TFG/apis_data"
    data_result = data_folder + "/timeRegister.json"

    list =[("2021-03-13T00:00:00.000","1","1")]
    df = pd.DataFrame(list, columns = ['trafficTime','airQualityTime','weatherTime']) 
    df.to_csv(data_result, index=False)
    #df.to_json(data_result)
"""

#metodo que de momento ejecuta el script de trafico

#seleccion de carpeta, cargando archivo de registro de ultimo dato
data_folder = os.getcwd().split("\TFG")[0] + "/TFG/apis_data"
file_to_open = data_folder + "/timeRegister.csv"
results_df = pd.read_csv(file_to_open)
lastTraffic = results_df.loc[results_df.index[-1], "trafficTime"]

#ejecutas dato y guardas nueva fecha
newLastRegister = dataIngestion(5, lastTraffic)

#guardas valores nuevos
results_df =results_df.append({'trafficTime': newLastRegister, 'airQualityTime' : 'pepe', 'weatherTime' : 'yano'}, ignore_index=True)
results_df.to_csv(file_to_open, index=False)
