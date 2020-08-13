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

import json

import upload_to_S3

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

with open('temp/output_files.json') as json_file: 
    data = json.load(json_file)

'''train = data['train']
preds1 = data['predictions']
ground_truth1 = data['ground_truth']

for name in train:
    upload_to_S3.upload(name, 'dmm-cg-1')
    
for name in preds1:
    upload_to_S3.upload(name, 'dmm-cg-1')
    
for name in ground_truth1:
    upload_to_S3.upload(name, 'dmm-cg-1')'''
    
with open('temp/preds_and_gt_file_dict.json') as json_file: 
    data = json.load(json_file)

preds = data['predictions']
ground_truth = data['ground_truth']

for name in preds:
    upload_to_S3.upload(name, 'dmm-cg-1')
    
for name in ground_truth:
    upload_to_S3.upload(name, 'dmm-cg-1')
    

'''
#dev - 
model_id = '5f2204da127595122a537e7f'

## To Do: embed auth into environment var
auth = 'eyJhbGciOiJIUzUxMiJ9.eyJpZCI6IjVlZmNkZGVkYjIzYTNjMDAwMTQ2MzZmNCIsInVzZXJuYW1lIjoiRERMVGVzdE9yZ0FkbWluIiwidXNlcl90eXBlIjoiYXBpIiwib3JnYW5pemF0aW9uX2lkIjoiNWVmY2RkZWRiMjNhM2MwMDAxNDYzNmY1In0.JWOJsJ1BX6-rMa_69qEljudCLxZN161Gi1efOUJCuOjfRYdAGsTTnq7s2sPqhAUSIEtU8lhFPqT7fng63yV51g'

# make these command line arguments
preds = 'mnt/results/val_preds_total_partition2.csv'
ground_truth = 'mnt/results/val_labels_total_partition2.csv'

#DMM API call: Register Prediction Data
print(os.path.basename(inputs_preds))
register_pred('dmm-cg-1', os.path.basename(preds), model_id)

#DMM API call: Register Ground Truth Data
print(os.path.basename(ground_truth))
ground_truth_reg('dmm-cg-1', os.path.basename(ground_truth), model_id)'''

