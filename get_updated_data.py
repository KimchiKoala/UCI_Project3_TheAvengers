#!/usr/bin/env python
# coding: utf-8

# In[130]:


# import dependencies
import json
import requests
import pymongo
import pandas as pd
from datetime import date, datetime, timedelta
from pymongo import MongoClient
from config import api_key



# Create connection to mongoDB
client = MongoClient('mongodb://localhost:27017')

# Create connectino to collection stock_db
db = client.stock_db


# Create variable for new_input
new_input = "AAPL"



# from MongoDB pull data from requested input
one_stock = db.stock_data.find_one({'symbol': new_input})
# Get stock symbol
symbol = one_stock['symbol']
# Get historical data from stock
historical_data = one_stock['historical']



# Create empty list to gather data from MongoDB
dates = []
close = []

for h in historical_data:
    collect_dates = h['date']
    dates.append(collect_dates)
    
    collect_close = h['close']
    close.append(collect_close)



# Date variables for API request
# Set variable for current date 
current_date = date.today()
# Gather last date stored in MongoDB
last_date = max(dates)



# Create new_start_date to be a day after the last date
date = datetime.strptime(last_date, '%Y-%m-%d')
modified_date = date + timedelta(days=1)
new_start_date = datetime.strftime(modified_date, '%Y-%m-%d')



# URL fo
url = f"https://financialmodelingprep.com/api/v3/historical-price-full/{new_input}?from={new_start_date}&to={current_date}&apikey={api_key}"




def get_update(x):
    new_results = requests.request("GET", x).json()
    return new_results


# In[148]:


#def send_update(x):
    


# In[149]:


if str(last_date) < str(current_date):
    print(f"Last date in MongoDB is: {last_date}")
    get_update(url)
    print(new_results)
    #db{new_input}.insert_one(new_data)
    


# In[ ]:




