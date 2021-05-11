import tensorflow as tf 
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import os
import seaborn as sns
import matplotlib.pyplot as plt


def linearRegression():
    training_file =  os.getcwd().split("\TFG")[0] + "/TFG/apis_data/historicalMerge.csv"
    testing_file = os.getcwd().split("\TFG")[0] + "/TFG/apis_data/2021/trainingDataMerge.csv"
    
    dftrain = pd.read_csv(training_file, low_memory=False) # training data
    dfeval = pd.read_csv(testing_file, low_memory=False) # testing data   

    
    #dftrain["time"] = dftrain["datetime"].str.split(" ")[1]
    #print(dftrain["time"].head(20))
    #return



    #print(dftrain["Parameter_OZONE"].unique())
    # print(dftrain.shape[0])
    # print(dftrain["Conditions"].value_counts())
    # print(dftrain["Conditions"].value_counts().sum())
    # print(dftrain["Conditions"].nunique())
    

    dftrain = dftrain.drop(["datetime","datetime_traffic","id", "Maximum Temperature", "Minimum Temperature", "travel_time", "Parameter_PM2.5", "Unit_PM2.5", "Parameter_OZONE", "Unit_OZONE", "Category_OZONE", "Dew Point", "Relative Humidity", "Heat Index", "Wind Speed", "Wind Gust", "Wind Direction", "Wind Chill", "Precipitation Cover", "Cloud Cover", "Sea Level Pressure"],axis=1)
    
    #print(dftrain.dtypes)
    dftrain['Snow Depth'] = dftrain['Snow Depth'].replace(["Partially cloudy", "Clear", "Rain Partially cloudy", "Rain", "Overcast", "Rain Overcast"],0.0)
    #print(dftrain["Snow Depth"].unique())
    dftrain = dftrain.dropna()
    #print(dftrain.dtypes)
    
    print(dftrain['Conditions'].value_counts())
    dftrain['Conditions'] = dftrain['Conditions'].astype('category')
    dftrain['weekday'] = dftrain['weekday'].astype('category')
    dftrain['link_name'] = dftrain['link_name'].astype('category')
    dftrain['Zone'] = dftrain['Zone'].astype('category')


    #dftrain['Conditions'] = dftrain['Conditions'].cat.reorder_categories(['old', 'ren', 'new'], ordered=True)
    dftrain['Conditions'] = dftrain['Conditions'].cat.codes
    dftrain['weekday'] = dftrain['weekday'].cat.codes
    dftrain['link_name'] = dftrain['link_name'].cat.codes
    dftrain['Zone'] = dftrain['Zone'].cat.codes

    print(dftrain['Conditions'].value_counts())
    #print(dftrain['Conditions'])
    # print(dftrain['Conditions'].value_counts())
    # print(dftrain['weekday'].value_counts())
    # print(dftrain['link_name'].value_counts())
    # print(dftrain['Zone'].value_counts())
    #print(dftrain.shape[0])

    sns.pairplot(dftrain[["speed", "weekday"]], diag_kind="kde")

    #print(dftrain.isna().sum())






linearRegression()