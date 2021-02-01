import pandas as pd
import datetime
import os

import requests
import subprocess

import pystan
from fbprophet import Prophet

import matplotlib.pyplot as plt
import numpy as np

import data_refresh

import pickle

import upload_to_S3

def data_prep():
    print("visualizing & preparing training data..")
    # read in our data from Domino Dataset - this is refreshed on a monthly basis with last 90 days of data
    #df =pd.read_csv('/domino/datasets/local/BMRS_total/data.csv', skiprows=1, skipfooter=1, header=None, engine='python')
    #df =pd.read_csv('/domino/datasets/domino-goyetc/ds-lifecycle-demo/scratch/data.csv', skiprows=1, skipfooter=1, header=None, engine='python')
    df =pd.read_csv('/mnt/data/training_data.csv', skiprows=1, skipfooter=1, header=None, engine='python')

    # rename the columns
    df.columns = ['HDF', 'date', 'half_hour_increment',
                      'CCGT', 'OIL', 'COAL', 'NUCLEAR',
                      'WIND', 'PS', 'NPSHYD', 'OCGT',
                      'OTHER', 'INTFR', 'INTIRL', 'INTNED',
                       'INTEW', 'BIOMASS', 'INTEM']

    # Create a new column datetime that represents the starting datetime of the measured increment
    df['datetime'] = pd.to_datetime(df['date'], format="%Y%m%d")
    df['datetime'].describe()

    df['datetime'] = df.apply(lambda x:x['datetime']+ datetime.timedelta(minutes=30*(int(x['half_hour_increment'])-1)), 
                              axis = 1)

    # Visualize the data to see how each fuel type is used during the day by plotting the data
    df.drop(['HDF', 'date', 'half_hour_increment'], axis = 1).set_index('datetime').plot(figsize=(15,8));
    plt.savefig(os.environ['DOMINO_WORKING_DIR']+'/results/fuel_daily.png')

    # ### Train our model
    # Let's try to predict TOTAL power production using all available generation types

    df['y'] = df.drop(['date','HDF','half_hour_increment'],axis=1).sum(axis=1)

    df.drop(['HDF', 'date', 'half_hour_increment'], axis = 1).set_index('datetime').plot(figsize=(15,8));
    plt.savefig(os.environ['DOMINO_WORKING_DIR']+'/results/total_daily.png')

    print(df.columns)

    plt.gcf()
    df['y'].plot.hist(grid=True, bins=20, rwidth=0.9,
                       color='#607c8e')
    plt.title('Total Power Production')
    plt.xlabel('Counts')
    plt.ylabel('Power, MW')
    plt.grid(axis='y', alpha=0.75)
    plt.savefig(os.environ['DOMINO_WORKING_DIR']+'/results/total_hist.png')

    # Prep our data - for Facebook Prophet, the time series data needs to be in a DataFrame with 2 columns named ds and y
    df = df.rename(columns = {'datetime':'ds'})
    prepped = df[['ds', 'y']]
    
    return df, prepped

def data_split(target, train_prop):
    print("splitting data for training with {}/{} split..".format(train_prop,(1-float(train_prop))))   
    # Split the dataset into train and test sets
    X = target.copy()
    y = target['y']

    split_index = int(train_prop*len(y))
    print("split index is {}".format(split_index))

    train = X.iloc[:split_index]
    test, labels = X.iloc[split_index:], y.iloc[split_index:]
    
    return train, test, labels, split_index

def train_model(training_data):
    print("training model using Prophet..")
    m = Prophet(yearly_seasonality=False)
    m.fit(training_data);
    
    ## Trained models are meant to be used. There is no reason to re-train the model each time you use the model. 
    #Export or serialize the model to a file to load and reuse the model later. In Python, the pickle module implements protocols for serializing and de-serializing objects.
    m.stan_backend.logger = None    #uncomment if using Python 3.6 and fbprophet==0.6
    with open("trained_models/model.pkl", "wb") as f:
        pickle.dump(m, f)
    
    return m

def make_preds(model, test_data, test_labels):
    print("generating predictions..")
    
    #Make a DataFrame to hold the predictions and predict future values of total power generation
    future = model.make_future_dataframe(periods=int(len(test_labels)), freq='30min')
    forecast = model.predict(future)

    plt.gcf();
    fig = model.plot(forecast);
    plt.plot(test_data['ds'].dt.to_pydatetime(), test_data['y'], 'r', linewidth = 1, linestyle = '--', label = 'real');
    plt.legend();
    plt.savefig(os.environ['DOMINO_WORKING_DIR']+'/results/power_forecast.png')
    
    return forecast

## Export train, test+predictions, and ground truth labels for DMM example

def split_data_export(df,n,prefix):
    print("exporting {} data..".format(df))
    arrays = np.array_split(df,n)
    df_dict = {}
    file_names = list()
    
    for i in range(n):
        df_dict["partition{0}".format(i+1)] = arrays[i]
   
    for key, value in df_dict.items():
        if n ==1:
            name = os.environ['DOMINO_WORKING_DIR']+'/results/{0}_total.csv'.format(prefix)
        else:
            name = os.environ['DOMINO_WORKING_DIR']+'/results/{0}_total_{1}.csv'.format(prefix,key)
            
        file_names.append(name)   
        value.to_csv(name)

    return file_names

## DEVELOP ##

#data refresh
data_refresh.refresh('/mnt/data/training_data.csv', 90)

#data prep
full, df_for_prophet = data_prep()

#train/test splits
X_train, X_test, y_test, split_index = data_split(df_for_prophet, 0.9)

#training
m = train_model(X_train)

## INFERENCE ##

#prediction
forecast = make_preds(m, X_test, y_test)

## EXPORT RESULTS (for DMM) ##
logged_tr_data = full.iloc[:split_index].set_index('ds')
training = split_data_export(logged_tr_data,1,'tr')

# preds - add input data back into prediction dataset
pred_data = full.iloc[split_index:].drop(columns=['HDF','date','half_hour_increment','y']).set_index('ds')
preds = forecast[['yhat','ds']].set_index('ds').rename(columns = {'yhat':'y'})
preds = pd.merge(pred_data, preds, how='inner', on='ds')
validation = split_data_export(preds,2,'val_preds')

# ground truth
gt = pd.concat([y_test, X_test[['ds']]], axis=1, sort=False).rename(columns = {'y':'y_gt'}).reset_index(drop=True).set_index('ds')
val_labels = split_data_export(gt,2,'val_labels')

#listOfFile = os.listdir('results')

## UPLOAD RESULTS TO S3 BUCKET

for name in training:
    upload_to_S3.upload(name, 'dmm-cg-1')
    
for name in validation:
    upload_to_S3.upload(name, 'dmm-cg-1')
    
for name in val_labels:
    upload_to_S3.upload(name, 'dmm-cg-1')
