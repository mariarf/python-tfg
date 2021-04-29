from __future__ import absolute_import, division, print_function, unicode_literals
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
import csv
import datetime
from IPython.display import clear_output
from six.moves import urllib
import tensorflow.compat.v2.feature_column as fc

from datetime import date
import os
from pathlib import Path

def make_input_fn(data_df, label_df, num_epochs=10, shuffle=True, batch_size=32):
    def input_function():  # inner function, this will be returned
        ds = tf.data.Dataset.from_tensor_slices((dict(data_df), label_df))  # create tf.data.Dataset object with data and its label
        if shuffle:
            ds = ds.shuffle(1000)  # randomize order of data
        ds = ds.batch(batch_size).repeat(num_epochs)  # split dataset into batches of 32 and repeat process for number of epochs
        return ds  # return a batch of the dataset
    return input_function  # return a function object for use

def linearRegression():

    #training_file =  os.getcwd().split("\TFG")[0] + "/TFG/apis_data/merge_2019-01-01T00_to_2019-01-15T23.csv"
    training_file =  os.getcwd().split("\TFG")[0] + "/TFG/apis_data/historicalMerge.csv"
    testing_file = os.getcwd().split("\TFG")[0] + "/TFG/apis_data/2021/trainingDataMerge.csv"

    dftrain = pd.read_csv(training_file, low_memory=False) # training data
    dfeval = pd.read_csv(testing_file, low_memory=False) # testing data    
    print(dftrain["Snow Depth"].unique())
    #dfeval["AQI_PM2.5"] = pd.to_numeric(dfeval['AQI_PM2.5'], downcast='float')

    dftrain["AQI_PM2.5"] = pd.to_numeric(dftrain['AQI_PM2.5'], downcast='float')
    dfeval["AQI_PM2.5"] = pd.to_numeric(dfeval['AQI_PM2.5'], downcast='float')

    dftrain['Category_PM2.5'] = dftrain['Category_PM2.5'].replace("OZONE","1")
    dfeval['Category_PM2.5'] = dfeval['Category_PM2.5'].replace("OZONE","1")
    
    dftrain['Category_PM2.5'] = dftrain['Category_PM2.5'].astype(float)
    dfeval['Category_PM2.5'] = dfeval['Category_PM2.5'].astype(float)

    dftrain['Snow Depth'] = dftrain['Snow Depth'].replace(["Partially cloudy", "Clear", "Rain Partially cloudy", "Rain", "Overcast", "Rain Overcast"],"0")
    dfeval['Snow Depth'] = dfeval['Snow Depth'].replace(["Partially cloudy", "Clear", "Rain Partially cloudy", "Rain", "Overcast", "Rain Overcast"] ,"0")

    dftrain['Snow Depth'] = dftrain['Snow Depth'].astype(float)
    dfeval['Snow Depth'] = dfeval['Snow Depth'].astype(float)


    dftrain.fillna(0.0, inplace=True)
    dfeval.fillna(0.0,inplace = True)

    dftrain["Conditions"] = dftrain["Conditions"].replace(0.0,"NoInfo")
    dfeval["Conditions"] = dfeval["Conditions"].replace(0.0,"NoInfo")

    #print(dftrain["Conditions"].unique())
    #print(dfeval["Conditions"].unique())
    dftrain["datetime"] = dftrain["datetime"].replace(0.0, "0.0")
    dftrain["datetime_traffic"] = dftrain["datetime_traffic"].replace(0.0, "0.0")
    dftrain["Parameter_PM2.5"] = dftrain["Parameter_PM2.5"].replace(0.0, "PM2.5")
    dftrain["Unit_PM2.5"] = dftrain["Unit_PM2.5"].replace(0.0, "UG/M3")
    dftrain["Parameter_OZONE"] = dftrain["Parameter_OZONE"].replace(0.0, "0.0")
    dftrain["Unit_OZONE"] = dftrain["Unit_OZONE"].replace(0.0, "PPB")



    dfeval["datetime"] = dfeval["datetime"].replace(0.0, "0.0")
    dfeval["datetime_traffic"] = dfeval["datetime_traffic"].replace(0.0, "0.0")
    dfeval["Parameter_PM2.5"] = dfeval["Parameter_PM2.5"].replace(0.0, "PM2.5")
    dfeval["Unit_PM2.5"] = dfeval["Unit_PM2.5"].replace(0.0, "UG/M3")
    dfeval["Parameter_OZONE"] = dfeval["Parameter_OZONE"].replace(0.0, "0.0")
    dfeval["Unit_OZONE"] = dfeval["Unit_OZONE"].replace(0.0, "PPB")
    """

    for column in dftrain.columns:
        
        print(f"{column} + {dftrain[column].dtype} || {column} + {dfeval[column].dtype}" )
        print(dftrain[column].unique())

    
    
    
    dftrain.pop("Parameter_OZONE")
    dftrain.pop("Unit_OZONE")
    dftrain.pop("Value_OZONE")
    dftrain.pop("Heat Index")
    dftrain.pop("Wind Chill")
    dftrain.pop("Wind Direction")
    dftrain.pop("Wind Gust")


    dfeval.pop("Parameter_OZONE")
    dfeval.pop("Unit_OZONE")
    dfeval.pop("Value_OZONE")
    dfeval.pop("Heat Index")
    dfeval.pop("Wind Chill")
    dfeval.pop("Wind Direction")
    dfeval.pop("Wind Gust")
    """
    #dftrain.drop(["datetime", "datetime_traffic"], axis=1, inplace=True)
    #print('Value_OZONE', 'AQI_OZONE','Heat Index', 'Wind Chill','Wind Direction', 'Wind Gust')


    """
    for column in dftrain.columns:
        #df[column] = df[column].fillna(0)
        print(column)
        print(dftrain[column].unique())
        #print(dftrain[column].dtype)
    """
    
    y_train = dftrain.pop("speed")
    y_eval = dfeval.pop("speed")
    print(dftrain.shape)
    print(dfeval.shape)
    #y_train = dftrain["speed"]
    #y_eval = dfeval["speed"]
    """
    categorical: weekday, link_name, Zone, Conditions
    numerical: speed, AQI_PM2.5, Value_PM2.5, Value_OZONE, AQI_OZONE, Minimum Temperature, Maximum Temperature, Temperature, Dew Point, Relative Humidity, Wind Speed, Wind Direction, Wind Chill, Precipitation, Snow Depth, Visibility, Cloud Cover, Sea level pressure, Heat Index, Wind Gust, 
    haven't decided yet: datetime, datetime_traffic, CategoryPM2.5, ,  Precipitation Cover, Category_OZONE,
    delete: id, Parameter_PM2.5, Unit_PM2.5, , Unit_OZONE,  Parameter_OZONE
    """
 
    CATEGORICAL_COLUMNS = ["weekday", "link_name"] #FALTA ZONE , "Conditions"
    pd.to_numeric(dftrain["AQI_OZONE"],errors='coerce')
    print(dftrain["AQI_OZONE"].unique())
    print(dftrain["AQI_OZONE"].dtype)

    #'Sea level pressure',
    NUMERIC_COLUMNS = ['AQI_PM2.5', 'Value_PM2.5', #'Value_OZONE', 'AQI_OZONE','Heat Index', 'Wind Chill','Wind Direction', 'Wind Gust'
                        'Minimum Temperature', 'Maximum Temperature', 'Temperature', 'Dew Point', 
                        'Relative Humidity', 'Wind Speed',  'Precipitation', 
                        'Snow Depth', 'Visibility', 'Cloud Cover'  ]

    feature_columns = []
    for feature_name in CATEGORICAL_COLUMNS:
        vocabulary = dftrain[feature_name].unique()  # gets a list of all unique values from given feature column
        feature_columns.append(tf.feature_column.categorical_column_with_vocabulary_list(feature_name, vocabulary))

    for feature_name in NUMERIC_COLUMNS:
        feature_columns.append(tf.feature_column.numeric_column(feature_name, dtype=tf.float32))

    
    print(feature_columns)

    
    train_input_fn = make_input_fn(dftrain, y_train)  # here we will call the input_function that was returned to us to get a dataset object we can feed to the model
    eval_input_fn = make_input_fn(dfeval, y_eval, num_epochs=1, shuffle=False)


    linear_est = tf.estimator.LinearRegressor(feature_columns=feature_columns)
    
    linear_est.train(train_input_fn)  # train
    


    result = linear_est.evaluate(eval_input_fn)  # get model metrics/stats by testing on tetsing data

    #clear_output()  # clears consoke output
    #print(result['accuracy'])  # the result variable is simply a dict of stats about our model
    print(result)



linearRegression()

