# Predicting Total Power Production from UK BMRS data
- Time Series Regression

- Three stage pipeline set up as scheduled jobs:
1. [Automated Monthly Model Training](view/train_pred_pipeline.py) - 90 days worth of data
2. [Daily inference via batch transform & ground truth service](view/Batch_Transform.py) for power generation on 30 minute increment
3. [Registration of predictions & ground truth data](view/reg_preds_gt.py) in DMM via API calls

## Power Gen by Source/Method
---
![image](raw/latest/results/total_hist.png)

## Predicted Power Generation
--- 
![image](raw/latest/results/total_forecast.png)
---
This project is based on the code, data, and artifacts for the *Getting Started in Domino* Tutorial, found 
[here](https://docs.dominodatalab.com/en/4.1/get_started/index.html) for Python and 
[here](https://docs.dominodatalab.com/en/4.1/get_started_r/index.html) for R.

This tutorial will guide you through a common model lifecycle in Domino. 
You will start by working with data from the Balancing Mechanism Reporting Service in the UK. 
We will be exploring the Electricty Generation by Fuel Type and predicting the electricty generation in the future. 
You’ll see examples of Jupyter, Dash, pandas, and the FB Prophet package used in Domino.

---
Table of Contents:

* Forecast_Power_Generation.ipynb
* Scheduled_Forecast_Power_Generation.ipynb
* Forecast_Power_Generation_for_Launcher.ipynb
* forecast.ipynb
* forecast_predictor.py
* data.csv
* app.sh

TO DO:
* update readme
* - scheduled data ingestion
* - data verison control in Domino Datasets
* - Exploratory notebook converted to jupyter notebook
* - graphical results saved 
* add tabular results to batch job (dominostats.json)
* publish app
* publish model API
* set up DMM
* - store data for predictions against historical model to simulate real-world prediction data with GT available

This is an update.