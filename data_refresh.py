import datetime
import requests
import subprocess

def refresh(save_location, days):
    #note: shift one extra day to facilitate producing 'latest' data in Batch Transform script
    today = (datetime.datetime.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    
    duration = (datetime.datetime.today() - datetime.timedelta(days)).strftime('%Y-%m-%d')

    process = subprocess.run(["curl", "-o", save_location, "https://www.bmreports.com/bmrs/?"
                   "q=ajax/filter_csv_download/FUELHH/csv/FromDate%3D{"+duration+"}%26ToDate%3D{"+today+"}/&"
                   "filename=GenerationbyFuelType_20191002_1657"])
    
    print("saved {} days of data to {}".format(days, save_location))
    
    return True

#refresh('/mnt/data/data.csv', 90)
#refresh('/domino/datasets/out/data.csv')


