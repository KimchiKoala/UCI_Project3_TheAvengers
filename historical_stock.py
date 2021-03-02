# -*- coding: utf-8 -*-
"""***This script is for setting up our database***

Financial_Modeling_Prep_API_NASDAQ_100.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1B4flUqxa9HS8pSq2vfobfXv5yD9B3rXZ

# Financial Modeling Prep API

## NASDAQ 100 info

https://financialmodelingprep.com/developer/docs/#List-of-Nasdaq-100-companies
"""

# import dependencies
import json
import time
import pymongo
import requests
import pandas as pd
from config import api_key
from pymongo import MongoClient


# Pull NASDAQ 100 information from nasdaq_constituent API 
# Set url
url = "https://financialmodelingprep.com/api/v3/nasdaq_constituent?apikey="+ api_key

# Get response using requests.request("GET", url).json()
response = requests.request("GET", url).json()

# Display reponse in order to use response
#response

# Make response into a dataframe to gather symbol data
response_df_not_sorted = pd.DataFrame(response)
response_df = response_df_not_sorted.sort_values('symbol', ascending=False)
#response_df.head()

# Using endpoint we will extract company inform to render on page

"""## NASDAQ 100 History


https://financialmodelingprep.com/developer/docs/#Stock-Historical-Price
"""

# Extract ticker values from 'symbol' column in response_df
stock_symbol = response_df['symbol']
#stock_symbol.head()

# Empty list to gather ticker_names
ticker_names = []

# for loop ticker_column to append name to ticker_names list
for name in stock_symbol:
    ticker_names.append(name)

# Make url for each ticker 
# urls empty list to gather url's
urls = []
# for loop to itterate through ticker_names
for row in ticker_names:
    url_history = "https://financialmodelingprep.com/api/v3/historical-price-full/" + row + "?apikey=" + api_key
    urls.append(url_history)




count = 0

json_responses = []

# for loop through urls to get count 
for url in urls:
    response = requests.request("GET", urls[count]).json()
    # print(f'{count} /// {urls[count]}')
    # print(f'{count} ~~~ {response["historicalStockList"]}')
    # print('__________')
    
    json_responses.append(response)
    count +=1

#print(json_responses[0])

# Create connection to mongoDB
client = MongoClient('mongodb://localhost:27017')

# Select stock_data database from mongoDB
db = client.stock_db

# Need to reverse object order in list to be in ascending order

# for loop through response to isolate list of dictionary to sort
for response in json_responses:
    # Set symbol as variable
    symbol = response['symbol']
    # Isolate list of historical_data
    historical_data = response['historical']
    
    # Set variable to reverse date order. 
    # Note: reverse needs to =False since ojects are already in descending order *this is key for it to work*
    reversing_order = sorted(historical_data, key=lambda x: x['date'], reverse=False)
    # Create dictionary to upload with reversed data
    upload_ready = {'symbol': symbol, 'historical': reversing_order}
    
    # Send data to MongoDb and add to collection stock_data
    #db.stock_data.insert_one(upload_ready)
    #print("MongoDB stock_data updated")