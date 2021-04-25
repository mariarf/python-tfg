#from __future__ import absolute_import, division, print_function, unicode_literals
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
import csv
import datetime
#from IPython.display import clear_output
#from six.moves import urllib
#import tensorflow.compat.v2.feature_column as fc

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

    training_file =  os.getcwd().split("\TFG")[0] + "/TFG/apis_data/historicalMerge.csv"
    testing_file = os.getcwd().split("\TFG")[0] + "/TFG/apis_data/2021/trainingDataMerge.csv"

    dftrain = pd.read_csv(training_file, low_memory=False) # training data
    dfeval = pd.read_csv(testing_file, low_memory=False) # testing data    

    #df.drop(["datetime","datetime_traffic", "CategoryPM2.5", ""],axis=1,inplace=True)
    #print(dftrain["Category_PM2.5"].head(30))

    dftrain.fillna('', inplace=True)
    dfeval.fillna('', inplace=True)
    """
    print(dftrain["Value_OZONE"].unique())
    print(dftrain["Value_OZONE"].head(60))
    #print(len(dftrain.loc[dftrain['Category_OZONE'] == 16.5]))
    
    
    for column in dftrain.columns:
        #df[column] = df[column].fillna(0)
        print(column)
        print(dftrain[column].unique())
    """
    #print(dftrain.columns)
    y_train = dftrain.pop("speed")
    y_eval = dfeval.pop("speed")
    """
    categorical: weekday, link_name, zone, Conditions
    numerical: speed, AQI_PM2.5, Value_PM2.5, Value_OZONE, AQI_OZONE, Minimum Temperature, Maximum Temperature, Temperature, Dew Point, Relative Humidity, Wind Speed, Wind Direction, Wind Chill, Precipitation, Snow Depth, Visibility, Cloud Cover, Sea level pressure, Heat Index, Wind Gust, 
    no se: datetime, datetime_traffic, CategoryPM2.5, ,  Precipitation Cover, Category_OZONE,
    quitar: id, Parameter_PM2.5, Unit_PM2.5, , Unit_OZONE,  Parameter_OZONE
    """
    
    CATEGORICAL_COLUMNS = ['weekday','link_name', 'Zone', 'Conditions']
    #print(len(dftrain["link_name"].unique()))
    #print(dftrain["link_name"].unique())
    NUMERIC_COLUMNS = ['AQI_PM2.5', 'Value_PM2.5', 'Value_OZONE', 'AQI_OZONE', 
                        'Minimum Temperature', 'Maximum Temperature', 'Temperature', 'Dew Point', 
                        'Relative Humidity', 'Wind Speed', 'Wind Direction', 'Wind Chill', 'Precipitation', 
                        'Snow Depth', 'Visibility', 'Cloud Cover', 'Sea level pressure', 'Heat Index', 'Wind Gust']

    feature_columns = []
    for feature_name in CATEGORICAL_COLUMNS:
        vocabulary = dftrain[feature_name].unique()  # gets a list of all unique values from given feature column
        feature_columns.append(tf.feature_column.categorical_column_with_vocabulary_list(feature_name, vocabulary))

    for feature_name in NUMERIC_COLUMNS:
        feature_columns.append(tf.feature_column.numeric_column(feature_name, dtype=tf.float32))

    #print(feature_columns)


    train_input_fn = make_input_fn(dftrain, y_train)  # here we will call the input_function that was returned to us to get a dataset object we can feed to the model
    eval_input_fn = make_input_fn(dfeval, y_eval, num_epochs=1, shuffle=False)

    linear_est = tf.estimator.LinearClassifier(feature_columns=feature_columns)

    linear_est.train(train_input_fn)  # train
    result = linear_est.evaluate(eval_input_fn)  # get model metrics/stats by testing on tetsing data

    clear_output()  # clears consoke output
    print(result['accuracy'])  # the result variable is simply a dict of stats about our model

    

linearRegression()

