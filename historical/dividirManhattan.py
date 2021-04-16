import pandas as pd
import numpy as np
import csv
import datetime
from datetime import date
import os
from pathlib import Path

def createUniqueStreets():
    file_to_open =  os.getcwd().split("\TFG")[0] + "/TFG/historical_data/salidaManhattan.csv"
    file_output = os.getcwd().split("\TFG")[0] + "/TFG/historical_data/uniqueStreets.csv"
    df=pd.read_csv(file_to_open, names=["ID","Speed", "TravelTime", "STATUS", "Date", "LINK_ID", "LINK_POINTS", "ENCODED_POLY_LINE", "ENCODED_POLY_LIKE_LVLS", "OWNER", "TRANSCOM_ID", "Borough", "Link_name"])

    df_uniqueStreets = pd.DataFrame(columns= ["Link_name", "LINK_POINTS"])
    df_uniqueStreets["Link_name"] = df["Link_name"].unique()
    df_uniqueStreets["LINK_POINTS"] = df["LINK_POINTS"].unique()
    
    df_uniqueStreets.to_csv(file_output, index=False)
    print(df_uniqueStreets.head(20))



def dividirManhattan():
    file_to_open =  os.getcwd().split("\TFG")[0] + "/TFG/historical_data/salidaManhattan.csv"
    #file_to_open =  os.getcwd().split("\TFG")[0] + "/TFG/historical_data/uniqueStreets.csv"
    df=pd.read_csv(file_to_open, names=["ID","Speed", "TravelTime", "STATUS", "Date", "LINK_ID", "LINK_POINTS", "ENCODED_POLY_LINE", "ENCODED_POLY_LIKE_LVLS", "OWNER", "TRANSCOM_ID", "Borough", "Link_name"])

    #df=pd.read_csv(file_to_open, names=["Link_name","LINK_POINTS"])

    df.drop(["ID","Speed", "TravelTime", "STATUS", "Date", "LINK_ID", "ENCODED_POLY_LINE", "ENCODED_POLY_LIKE_LVLS", "OWNER", "TRANSCOM_ID", "Borough"],axis=1,inplace=True)
    
    
    df_unico = pd.DataFrame(columns=["Link_name", "LINK_POINTS"])
    df_unico["Link_name"] = df["Link_name"].unique()
    df_unico["LINK_POINTS"] = df["LINK_POINTS"].unique()
    #print(df_unico)
    df_espacio =  df_unico["LINK_POINTS"].str.split(" ")
    #print(df_espacio)

    for fila in df_espacio:

        
        fila = str(fila).replace("[", "")
        fila = str(fila).replace("'", "")
        fila = str(fila).replace("]", "")
        
        loopvar = str(fila).split(",")
        
        coord_x = 0
        coord_y = 0
        num_coord = 0


        valor = str(fila).split(",")[0]
        valorfloat = float(valor)
        
        for separateCoord in loopvar:
            
            coord_x = coord_x + float(str(fila).split(",")[0])
            coord_y = coord_y + float(str(fila).split(",")[1])
            num_coord = num_coord + 1 
            
        coord_x = coord_x / num_coord
        coord_y = coord_y / num_coord

        print("X: " + str(coord_x))
        print("Y: " + str(coord_y))
        """
    


    #print(df_espacio.head(20))
    #print(df["LINK_POINTS"].describe())
    #df.drop(["STATUS","LINK_ID", "LINK_POINTS", "ENCODED_POLY_LINE", "ENCODED_POLY_LIKE_LVLS", "OWNER", "TRANSCOM_ID"],axis=1,inplace=True)
    """
dividirManhattan()

#createUniqueStreets()