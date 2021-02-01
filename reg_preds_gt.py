import pandas as pd
import datetime

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

import requests

with open('temp/preds_and_gt_file_dict.json') as json_file: 
    data = json.load(json_file)

preds = data['predictions']
ground_truth = data['ground_truth']

for name in preds:
    
    file_name = os.path.basename(name)
    
    url = "https://trial.dmm.domino.tech/api/v0/models/5f84cf02e4cd7ff1b8e75a48/add_predictions"

    payload = "{\n  \"dataLocation\": \"https://s3.us-east-2.amazonaws.com/dmm-cg-2/"+file_name+"\"\n}"
    headers = {
               'Authorization': 'eyJhbGciOiJIUzUxMiJ9.eyJpZCI6IjVlZThjMDA0YjJjYjJmNTliMGRiYmU4NiIsInVzZXJuYW1lIjoiY29saW4uZGVtby5kZGwudHJpYWwiLCJ1c2VyX3R5cGUiOiJhcGkiLCJvcmdhbml6YXRpb25faWQiOiI1ZWQ2NWRhZGQ5ZmFiZjAwMDE0ZjI5MmYifQ.bTuQUr57LtU9By6pXUP_TVMCj_MIbhYLo4ULamcafWJogx4oe8r_p8tQ5xARFQiJQzoOQL2u9-GO5FS6y7Wgpw',
               'Content-Type': 'application/json'
              }

    response = requests.request("PUT", url, headers=headers, data = payload)

    print(response.text.encode('utf8'))

for name in ground_truth:
    
    file_name = os.path.basename(name)
    
    url = "https://trial.dmm.domino.tech/api/v0/models/5f84cf02e4cd7ff1b8e75a48/add_ground_truths"

    payload = "{\n  \"dataLocation\": \"https://s3.us-east-2.amazonaws.com/dmm-cg-2/"+file_name+"\"\n}"
    headers = {'Authorization': 'eyJhbGciOiJIUzUxMiJ9.eyJpZCI6IjVlZThjMDA0YjJjYjJmNTliMGRiYmU4NiIsInVzZXJuYW1lIjoiY29saW4uZGVtby5kZGwudHJpYWwiLCJ1c2VyX3R5cGUiOiJhcGkiLCJvcmdhbml6YXRpb25faWQiOiI1ZWQ2NWRhZGQ5ZmFiZjAwMDE0ZjI5MmYifQ.bTuQUr57LtU9By6pXUP_TVMCj_MIbhYLo4ULamcafWJogx4oe8r_p8tQ5xARFQiJQzoOQL2u9-GO5FS6y7Wgpw',
               'Content-Type': 'application/json'
              }

    response = requests.request("PUT", url, headers=headers, data = payload)

    print(response.text.encode('utf8'))


