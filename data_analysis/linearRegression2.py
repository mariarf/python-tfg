import tensorflow as tf 
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import os


def linearRegression():
    training_file =  os.getcwd().split("\TFG")[0] + "/TFG/apis_data/historicalMerge.csv"
    testing_file = os.getcwd().split("\TFG")[0] + "/TFG/apis_data/2021/trainingDataMerge.csv"
    
    dftrain = pd.read_csv(training_file, low_memory=False) # training data
    dfeval = pd.read_csv(testing_file, low_memory=False) # testing data   


    
    #print(dftrain["Parameter_OZONE"].unique())
    # print(dftrain.shape[0])
    # print(dftrain["Conditions"].value_counts())
    # print(dftrain["Conditions"].value_counts().sum())
    # print(dftrain["Conditions"].nunique())
    
    
    dftrain = dftrain.drop([ "datetime_traffic","id", "travel_time", "Parameter_PM2.5", "Unit_PM2.5", "Parameter_OZONE", "Unit_OZONE", "Category_OZONE", "Dew Point", "Relative Humidity", "Heat Index", "Wind Speed", "Wind Gust", "Wind Direction", "Wind Chill", "Precipitation Cover", "Cloud Cover", "Sea Level Pressure"],axis=1)
    
    #print(dftrain.dtypes)
    dftrain['Snow Depth'] = dftrain['Snow Depth'].replace(["Partially cloudy", "Clear", "Rain Partially cloudy", "Rain", "Overcast", "Rain Overcast"],0.0)
    #print(dftrain["Snow Depth"].unique())
    dftrain = dftrain.dropna()
    #print(dftrain.dtypes)
    

    #print(dftrain.head(60))
    #print(dftrain.shape[0])


    #print(dftrain.isna().sum())






linearRegression()