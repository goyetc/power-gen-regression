#!/usr/bin/env python
# coding: utf-8

# ## Batch Transform (in dev)
# 
# This is a placeholder notebook for running a batch transform on new time series data, with latest model, and exporting/logging predictions (along with gt data since we have it) for ingestion into DMM

import pandas as pd
import datetime

import pystan
from fbprophet import Prophet

import os
import numpy as np
import pickle

import boto3
from botocore.exceptions import NoCredentialsError

import datetime
import requests
import subprocess
from datetime import date

import data_refresh
# ## pseudocode

import upload_to_S3

# ### 1. access latest data
#  - pulls last 1 day of data from source into Domino Dataset. Based on data_refresh.py script
#  - read csv from Domino Dataset

def inference_prep(data):
    print("preparing target date range for inference..")

    data.columns = ['HDF', 'date', 'half_hour_increment',
                      'CCGT', 'OIL', 'COAL', 'NUCLEAR',
                      'WIND', 'PS', 'NPSHYD', 'OCGT',
                      'OTHER', 'INTFR', 'INTIRL', 'INTNED',
                       'INTEW', 'BIOMASS', 'INTEM']

    # Create a new column datetime that represents the starting datetime of the measured increment
    data['datetime'] = pd.to_datetime(data['date'], format="%Y%m%d")

    data['datetime'] = data.apply(lambda x:x['datetime']+ datetime.timedelta(minutes=30*(int(x['half_hour_increment'])-1)), 
                              axis = 1)

    # Let's try to predict TOTAL power production using all available generation types

    data['y'] = data.drop(['date','HDF','half_hour_increment'],axis=1).sum(axis=1)

    # Prep our data - for Facebook Prophet, the time series data needs to be in a DataFrame with 2 columns named ds and y

    data = data.rename(columns = {'datetime':'ds'})
    prepped = data[['ds', 'y']]
    
    return data, prepped

def load_model(model_loc):
    print("loading saved model from {}".format(model_loc))
    with open(model_loc, 'rb') as f:
        m = pickle.load(f)
    return m

#grab last day worth of data from source
data_refresh.refresh('/mnt/data/daily_pred_data.csv', 1)

#read in our data
df = pd.read_csv('/mnt/data/daily_pred_data.csv', skiprows=1, skipfooter=1, header=None, engine='python')

#prep data for inference
full, df_for_inf = inference_prep(df)

#Save for logging to DMM

#datetime range for inference
X = df_for_inf.copy()

#ground truth data is available in this demo scenario
y = df_for_inf['y']

# ### 2. load latest model
m = load_model('trained_models/model.pkl')

# ### 3. use loaded model to compute predictions of 'test data', aka latest loaded data
#  - note that this test data also contains the ground truth, since it is (in reality) historical

# Note: don't need to create future dataframe, because we already have the data, in this demo example
#Make a DataFrame to hold the predictions and predict future values of total power generation

# length of DF is up to two days worth of 30 minute predictions, depending on time it ran

#future = m.make_future_dataframe(periods=int(len(y)), freq='30min', include_history=False)
# ..instead, predict on 'ds' column isolated from new input data

forecast = m.predict(X[['ds']])

# ### 4. format data and export
#  - format predictions + test data
#  - format ground truth labels
#  
# #### Note on data to be used/exported
# 1. inputs --> df
# 2. predictions --> preds
# 3. preds for DMM --> df + preds (inner join on 'ds' index/column)
# 4. ground truth for DMM --> df_for_prophet, below.. or "X" below

# ### Dev: Export train, test+predictions, and ground truth labels for DMM example
# Trained models are meant to be used. There is no reason to re-train the model each time you use the model. Export or serialize the model to a file to load and reuse the model later. In Python, the pickle module implements protocols for serializing and de-serializing objects.

def split_data_export(df,n,prefix):
    arrays = np.array_split(df,n)
    df_dict = {}
    file_names = list()
    
    for i in range(n):
        df_dict["partition{0}".format(i+1)] = arrays[i]
   
    for key, value in df_dict.items():
        if n ==1:
            name = os.environ['DOMINO_WORKING_DIR']+'/results/{0}_total_{1}.csv'.format(prefix,date.today())
        else:
            name = os.environ['DOMINO_WORKING_DIR']+'/results/{0}_total_{1}_{2}.csv'.format(prefix,key,date.today())
            
        file_names.append(name)   
        value.to_csv(name)

    return file_names

# Note that here, we use the entire "new" dataset, no splitting needed

# In[77]:


#preds
#add underlying features back into prediction dataset
pred_data = X.set_index('ds')

# same thing with forecast data.. no splitting needed

preds = full.drop(columns=['HDF','date','half_hour_increment','y']).set_index('ds')
preds = pd.merge(pred_data, preds, how='inner', on='ds')

## DMM formatting

# column naming convention
preds = preds.rename(columns = {'yhat':'y'})

# make column order consistent with validation data produced via train_pred_pipeline.py
cols = preds.columns.tolist()
cols = cols[1:] + [cols[0]]
preds = preds[cols]
print(cols)

# Export predictions & associated inputs
inputs_preds = split_data_export(preds,1,'batch_preds')
print(inputs_preds)

# Now, ground truth
dt = X.rename(columns = {'y':'y_gt'}).reset_index(drop=True).set_index('ds')

# select datetimes from test dataset (ground truth) that match new prediction datetimes
gt = dt[dt.index.isin(preds.index)]

# Export
ground_truth = split_data_export(gt,1,'gt')
print(ground_truth)


# ### 5. Use S3 APIs to export input+pred and ground truth data directly to bucket of choice
#  - https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-uploading-files.html

#listOfFile = os.listdir('results')

for name in inputs_preds:
    upload_to_S3.upload(name, 'dmm-cg-1')
    
for name in ground_truth:
    upload_to_S3.upload(name, 'dmm-cg-1')
    
