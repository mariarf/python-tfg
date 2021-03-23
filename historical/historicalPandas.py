import pandas as pd
import numpy as np
import csv
import datetime
import os
from pathlib import Path

def diaSemana(año,mes,dia):
    #ESTE MÉTODO DEVUELVE EL DÍA DE LA SEMANA DADO EL AÑO, MES Y DÍA
    week_days=["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]
    week_num=datetime.date(año,mes,dia).weekday()
    return(week_days[week_num])


def historialValues():
    file_to_open =  os.getcwd().split("\TFG")[0] + "/TFG/historical_data/salidaManhattan.csv"
    df=pd.read_csv(file_to_open, names=["ID","Speed", "TravelTime", "STATUS", "Date", "LINK_ID", "LINK_POINTS", "ENCODED_POLY_LINE", "ENCODED_POLY_LIKE_LVLS", "OWNER", "TRANSCOM_ID", "Borough", "Link_name"])
    df.drop(["STATUS","LINK_ID", "LINK_POINTS", "ENCODED_POLY_LINE", "ENCODED_POLY_LIKE_LVLS", "OWNER", "TRANSCOM_ID"],axis=1,inplace=True)
    
    
    print(df.head(20))


historialValues()
