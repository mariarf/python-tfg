import pandas as pd
import numpy as np
import csv
import datetime
from datetime import date
import os
from pathlib import Path
import matplotlib.pyplot as plt
import math


"""
    orden de ejecución: Si no se ha ejecutado el código ninguna vez, ejecutar el método dividirManhattan() y después el método zonaManhattan(). 

    Si se desea visualizar la localización de las calles, ejecutar el método mostrarPuntos().

"""


def dividirManhattan():

    # Firstly, preparing the variables with the files that will be used. salidaManhattan.csv is the file containing all the values of traffic. It can be changed if the 
    # name of the traffic file or location is different. file_output variable is the file that will only store the unique street names found in salidaManhattan.csv

    file_to_open =  os.getcwd().split("\TFG")[0] + "/TFG/historical_data/salidaManhattan.csv"
    file_output = os.getcwd().split("\TFG")[0] + "/TFG/historical_data/uniqueStreets.csv"

    # We open the file with all the columns and we drop the ones we don't need. As we are trying to focus on the unique streets, we will only get the columns that reference streets.
    # This columns are LINK_POINTS and Link_name

    df=pd.read_csv(file_to_open, names=["ID","Speed", "TravelTime", "STATUS", "Date", "LINK_ID", "LINK_POINTS", "ENCODED_POLY_LINE", "ENCODED_POLY_LIKE_LVLS", "OWNER", "TRANSCOM_ID", "Borough", "Link_name"])
    df.drop(["ID","Speed", "TravelTime", "STATUS", "Date", "LINK_ID", "ENCODED_POLY_LINE", "ENCODED_POLY_LIKE_LVLS", "OWNER", "TRANSCOM_ID", "Borough"],axis=1,inplace=True)
    
    
    #Creating the dataframe that will be the one we will be working on and saving into the file_output file. It will have 4 columns. coordX and coordY are empty but they will 
    #be filled in. As we need the Link_name and LINK_POINTS column, we will copy them into df_unico but applying the .unique() function. It will only copy the unique values.

    df_unico = pd.DataFrame(columns=["Link_name", "LINK_POINTS", "coordX", "coordY"])
    df_unico["Link_name"] = df["Link_name"].unique()
    df_unico["LINK_POINTS"] = df["LINK_POINTS"].unique()

    #LINK_POINTS has an irregular format. This is an example of a row in LINK_POINTS: 
    # "40.75829,-73.997531 40.7605,-74.0032 40.7620605,-74.007021 40.7662905,-74.01706"
    # They are coordinates of the different points of the street. We are going to calculate the mean of these points for each street
    # to have an approximation of the street in coordinates. We are going to separate the coordinates and iterate to calculate the mean for the x and y coordinate. 

    df_espacio =  df_unico["LINK_POINTS"].str.split(" ")


    for index, fila in df_espacio.items():

        
        #These 3 lines are to delete the unwanted symbols in each position of df_espacio
        fila = str(fila).replace("[", "")
        fila = str(fila).replace("'", "")
        fila = str(fila).replace("]", "")
        
        loopvar = str(fila).split(",") #separating x and y coordinates

        #variables that will be used to calculate the mean x,y coordinate.
        coord_x = 0
        coord_y = 0
        num_coord = 0

        """
        valor = str(fila).split(",")[0]
        valorfloat = float(valor)
        """

        #adding all the different x and y coordinates to calculate the mean

        for separateCoord in loopvar:
            
            coord_x = coord_x + float(str(fila).split(",")[0])
            coord_y = coord_y + float(str(fila).split(",")[1])
            num_coord = num_coord + 1 
            
        coord_x = round((coord_x / num_coord), 6)
        coord_y = round((coord_y / num_coord), 6)

        #merging the values to the their corresponding rows.
        df_unico.loc[index, "coordX"] = coord_x
        df_unico.loc[index, "coordY"] = coord_y


    #taking off "LINK_POINTS as we already have the mean calculated. We then save the file."
    df_unico.pop("LINK_POINTS")
    df_unico.to_csv(file_output, index=False)    
    


#This method is a representation of the street coordinates in a graph

def mostrarPuntos():
    #opening the file where we have the unique streets with the coordinates
    file_to_open =  os.getcwd().split("\TFG")[0] + "/TFG/historical_data/uniqueStreets.csv"
    df=pd.read_csv(file_to_open, names=["Link_name", "coordX", "coordY", "zonaX", "zonaY", "zona"], skiprows=1)

    #dividing the zones for the xticks and yticks in the graph
    divisionX = round((df["coordX"].max() - df["coordX"].min()) /8, 2)
    divisionY = round((df["coordY"].max() - df["coordY"].min()) /5 ,2)
 
    #creating the scatter diagram with coordX and coordY values and adding useful information
    plt.scatter(df["coordX"], df["coordY"])
    plt.title("Link Points - Manhattan")
    plt.xlabel("x coordinate")
    plt.ylabel("y coordinate")


    plt.xticks(np.arange(df["coordX"].min() - 0.005 ,df["coordX"].max() , divisionX))
    plt.yticks(np.arange(df["coordY"].min() -0.005, df["coordY"].max(), divisionY))
    plt.grid()
    plt.show()
    
    #df.plot(kind='scatter',x="coordX" ,y="coordY",color='red')
    #plt.show()




# This method is meant to divide the different zones of Manhattan from the values of uniqueStreets file. This file contains the mean coordinate of each of the streets that
# contain traffic data. 
# We will start by opening the file with the unique streets and loading it into a Pandas dataFrame. 

def zonaManhattan():
    file =  os.getcwd().split("\TFG")[0] + "/TFG/historical_data/uniqueStreets.csv"

    df=pd.read_csv(file, names=["Link_name", "coordX", "coordY"], skiprows=1)


    #For the division in zones we will divide Manhattan's x value into 8 zones and Manhattan's Y values into 5 zones. There will be therefore 40 different zones. 
    #To calculate the zone for each of the coordinates we substract the value of that coordinate to the maximum value and divide by the division we have made for the zones.
    divisionX = (df["coordX"].max() - df["coordX"].min()) /8
    divisionY = (df["coordY"].max() - df["coordY"].min()) /5
    df["zonaX"] = abs(( df["coordX"] - df["coordX"].max()) / divisionX)
    df["zonaY"] = abs(( df["coordY"] - df["coordY"].max() ) / divisionY)

    #converting the X and Y values to int to get the exact zone where they land. Example: if the value is 5.88 it will be in zone 5
    df["zonaX"] = df["zonaX"].astype(int)
    df["zonaY"] = df["zonaY"].astype(int)

    #we will convert the values to string to concatenate them and get the zone.
    df["zonaX"] = df["zonaX"].astype(str)
    df["zonaY"] = df["zonaY"].astype(str)


    #We concatenate the values and get the zone. It works as follows:
    #If a X coordinate is in zone 5 and a Y coordinate is in zone 3, the value of the zone will be 53.
    df["zona"] = df["zonaX"] + df["zonaY"]

    #we will save the dataframe to the file specified. 
    df.to_csv(file, index=False)




#dividirManhattan() 

#zonaManhattan()

#mostrarPuntos()