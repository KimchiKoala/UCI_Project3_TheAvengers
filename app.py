from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from pymongo import MongoClient

# Create connection to mongoDB
client = MongoClient('mongodb://localhost:27017')

# Select stock_data database from mongoDB
db = client.stock_db

#input = 
one_stock = db.stock_data.find_one({'symbol': 'TSLA'})
symbol = one_stock['symbol']
historical_data = one_stock['historical']

dates = []
close = []

for h in historical_data:

    collect_dates = h['date']
    dates.append(collect_dates)
    #print(dates)

    collect_close = h['close']
    close.append(collect_close)
    #print(close)
