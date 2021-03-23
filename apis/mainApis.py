from trafficApi import *
from airQualityApi import *
from weatherApi import *
import os
import pandas as pd




"""

#seleccion de carpeta, cargando archivo de registro de ultimo dato
data_folder = os.getcwd().split("\TFG")[0] + "/TFG/apis_data"
#file_to_open = data_folder + "/traffic.csv"
results_df = pd.read_csv(file_to_open)
lastTraffic = results_df.loc[results_df.index[-1], "trafficTime"]

#ejecutas dato y guardas nueva fecha
newLastRegister = trafficDataIngestion(5, lastTraffic)

#guardas valores nuevos
results_df =results_df.append({'trafficTime': newLastRegister, 'airQualityTime' : 'pepe', 'weatherTime' : 'yano'}, ignore_index=True)
results_df.to_csv(file_to_open, index=False)
"""