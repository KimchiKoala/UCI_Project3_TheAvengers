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

# Create connection to six month and one year database in mongoDB
# Select stock_data database from mongoDB
six_months_stock_db = client.six_months_stock_db.six_months
one_year_stock_db = client.one_year_stock_db.one_year

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

# Set new url to update data
url = f"https://financialmodelingprep.com/api/v3/historical-price-full/{new_input}?from={new_start_date}&to={current_date}&apikey={api_key}"

# conditional statement to determine if an update query is needed
# based on if last_data in MongDb < current_date being requested
if str(last_date) < str(current_date):
    print(f"Last date in MongoDB is: {last_date}")
    # if so send new request fro url with new start and end date
    new_results = requests.request("GET", url).json()
    #print(new_results)
    
    if new_results == False:
        print("not null")
        # Isolate historical data
        historical_update = new_results['historical']
        #for loop through historacal_update to retrive updated data
        for h in historical_update:
            # Retrieve new date and close data
            date_update = h['date']
            close_update = h['close']
            #print(f"Date update {date_update}")
            #print(f"Close update {close_update}")
            # Send update to MongoDb and push tp historical list
            #db.stock_data.update_one({'symbol': new_input}, {'$push': {'historical': {'date': date_update, 'close': close_update}}})
            print("Update complete")   
    else:
        print("Data up to date")