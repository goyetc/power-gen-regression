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

with open('temp/output_files.json') as json_file: 
    data = json.load(json_file)

train = data['train']
preds1 = data['predictions']
ground_truth1 = data['ground_truth']

for name in train:
    upload_to_S3.upload(name, 'dmm-cg-2')
    
for name in preds1:
    upload_to_S3.upload(name, 'dmm-cg-2')
    
for name in ground_truth1:
    upload_to_S3.upload(name, 'dmm-cg-2')
    
with open('temp/preds_and_gt_file_dict.json') as json_file: 
    data = json.load(json_file)

preds = data['predictions']
ground_truth = data['ground_truth']

for name in preds:
    upload_to_S3.upload(name, 'dmm-cg-2')
    
for name in ground_truth:
    upload_to_S3.upload(name, 'dmm-cg-2')
    

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

