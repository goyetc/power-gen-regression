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

'''with open('temp/output_files.json') as json_file: 
    data = json.load(json_file)

train = data['train']
preds1 = data['predictions']
ground_truth1 = data['ground_truth']

for name in train:
    upload_to_S3.upload(name, 'dmm-cg-2')
    
for name in preds1:
    upload_to_S3.upload(name, 'dmm-cg-2')
    
for name in ground_truth1:
    upload_to_S3.upload(name, 'dmm-cg-2')'''
    
with open('temp/preds_and_gt_file_dict.json') as json_file: 
    data = json.load(json_file)

preds = data['predictions']
ground_truth = data['ground_truth']

for name in preds:
    upload_to_S3.upload(name, 'dmm-cg-2')
    
for name in ground_truth:
    upload_to_S3.upload(name, 'dmm-cg-2')

