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

import sys

def register_pred(bucket, file_name, MODEL_ID):
    
    try:
        file_name = sys.argv[1]
    except:
        pass
    
    #file_name = os.path.basename(file_path)
    #file_location = 'https://{}.s3.amazonaws.com/automation-test/{}'.format(bucket,file_name)
    
    url = "https://dmm-hartford.domino-pilot.com/api/v0/models/{}/add_predictions".format(MODEL_ID)
    
    payload = '{\n  \"dataLocation\": \"https://s3.amazonaws.com/'+bucket+'/'+file_name+'\"\n}'
    print("pred payload: {}".format(payload))
    headers = {
      'Authorization': auth,
      'Content-Type': 'application/json'
    }

    response = requests.request("PUT", url, headers=headers, data = payload)
    print(response.text.encode('utf8'))
    return True

def ground_truth_reg(bucket, file_name, MODEL_ID):
    
    try:
        file_name = sys.argv[2]
    except:
        pass
    
    #file_name = os.path.basename(file_path)
    #file_location = 'https://{}.s3.amazonaws.com/automation-test/{}'.format(bucket,file_name)
    
    url = "https://dmm-hartford.domino-pilot.com/api/v0/models/{}/add_ground_truths".format(MODEL_ID)
    
    payload = "{\n  \"dataLocation\": \"https://s3.amazonaws.com/"+bucket+"/"+file_name+"\"\n}"
    print("gt payload: {}".format(payload))
    
    headers = {
      'Authorization': auth,
      'Content-Type': 'application/json'
    }

    response = requests.request("PUT", url, headers=headers, data = payload)
    print(response.text.encode('utf8'))
    return True

#model_id = '5f1f3bd70a1f1e64a4a41f71'

#dev - 
model_id = '5f2204da127595122a537e7f'

## To Do: embed auth into environment var
auth = 'eyJhbGciOiJIUzUxMiJ9.eyJpZCI6IjVlZmNkZGVkYjIzYTNjMDAwMTQ2MzZmNCIsInVzZXJuYW1lIjoiRERMVGVzdE9yZ0FkbWluIiwidXNlcl90eXBlIjoiYXBpIiwib3JnYW5pemF0aW9uX2lkIjoiNWVmY2RkZWRiMjNhM2MwMDAxNDYzNmY1In0.JWOJsJ1BX6-rMa_69qEljudCLxZN161Gi1efOUJCuOjfRYdAGsTTnq7s2sPqhAUSIEtU8lhFPqT7fng63yV51g'

# make these command line arguments
inputs_preds = 'mnt/results/val_preds_total_partition2.csv'
ground_truth = 'mnt/results/val_labels_total_partition2.csv'

#DMM API call: Register Prediction Data
print(os.path.basename(inputs_preds))
register_pred('dmm-cg-1', os.path.basename(inputs_preds), model_id)

#DMM API call: Register Ground Truth Data
print(os.path.basename(ground_truth))
ground_truth_reg('dmm-cg-1', os.path.basename(ground_truth), model_id)

