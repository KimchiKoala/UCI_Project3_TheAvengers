# import dependencies
import math
import json
import pymongo
import requests
import numpy as np
import pandas as pd
from config import api_key
from pymongo import MongoClient
from datetime import date, datetime, timedelta
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM
import matplotlib.pyplot as plt
import plotly.express as px
plt.style.use('fivethirtyeight')

# Pull NASDAQ 100 information from nasdaq_constituent API 
# Set url
url = "https://financialmodelingprep.com/api/v3/nasdaq_constituent?apikey="+ api_key

# Get response using requests.request("GET", url).json()
response = requests.request("GET", url).json()

# Display reponse in order to use response
response

# Create empty list to store stock_symbols
stock_symbols = []

# for loop through response to append symbol data
for r in response:
    collect_symbols = r['symbol']
    stock_symbols.append(collect_symbols)
    
print('Symbol data collected')

# Create connection to mongoDB
client = MongoClient('mongodb://localhost:27017')

# Set variables to database and collection names
database_name = 'testing_stock' ### change back to stock_db ###
collection_name = 'dummy_test' ### change back to stock_data ###

# Connect to database in mongoDB
db = client.database_name

# Create function to gather stored data from MongoDB.stock_db
def get_stored_data(s):

    # Retrive data
    one_stock = db.collection_name.find_one({'symbol': s})

    # Isolate symbol and historical data
    symbol = one_stock['symbol']
    historical_data = one_stock['historical']

    stock_date = []
    close = []

    for h in historical_data:
        
        collect_dates = h['date']
        stock_date.append(collect_dates)
        
        collect_close = h['close']
        close.append(collect_close)
    
    return stock_date, close

def get_update(s, sd):

    # Create date variables for API request
    # Set variable for current date 
    current_date = date.today()
    #print(current_date)
    # Retrive last date stored in MongoDB
    last_date = max(sd)
    #print(last_date)

    #Create new_start_date to be a day after the last date
    date_datetime = datetime.strptime(last_date, '%Y-%m-%d') 
    #print(date)
    modified_date = date_datetime + timedelta(days=1)
    #print(modified_date)
    new_start_date = datetime.strftime(modified_date, '%Y-%m-%d')
    #print(new_start_date)

    #print(new_start_date)

    # Set new url to update data
    url = f"https://financialmodelingprep.com/api/v3/historical-price-full/{s}?from={new_start_date}&to={current_date}&apikey={api_key}"

    # conditional statement to determine if an update query is needed
    # based on if last_data in MongDb < current_date being requested
    if str(last_date) < str(current_date):
    print(f"Last date in MongoDB for {s} is: {last_date}")
    # if so send new request fro url with new start and end date
    new_results = requests.request("GET", url).json()
    print(f"API Completed for {s}")

    if new_results == False:
        print("not null")
        # Isolate historical data
        historical_update = new_results['historical']
        #for loop through historacal_update to retrive updated data
        for h in historical_update:
            # Retrieve new date and close data
            date_update = h['date']
            close_update = h['close']

            # Send update to MongoDb and push tp historical list
            #db.stock_data.update_one({'symbol': new_input}, {'$push': {'historical': {'date': date_update, 'close': close_update}}})
            #print(f"{s} MongoDb update complete")   
    else:
        print(f"{s} data up to date")

def machine_learning(s, sd, c):

    get_stored_data(s)

    df = pd.DataFrame({'Date': sd,
                    'close': c})

    df['Date'] = pd.to_datetime(df['Date'])

    new_df = df.set_index('Date')

    new_df.shape

    # Create new df with only the 'Close' column
    data = new_df.filter(['close'])

    # Convert df to a numpy array
    dataset = data.values

    # Get the number of rows to train the model on
    training_data_len = math.ceil(len(dataset) * .8)

    training_data_len

    # Scale the data to apply preprocessing scaling before presenting to nueral network
    scaler = MinMaxScaler(feature_range=(0,1))
    scaled_data = scaler.fit_transform(dataset)

    # Show scaled data representing values between 0-1
    #scaled_data

    # Create the training dataset 
    # Create the scaled training dataset
    train_data = scaled_data[0:training_data_len , :]

    # Split the data into x_train and y_train data sets
    # x_train will be the independent training variables
    # y_train will be the dependent variables
    x_train = []
    y_train = []

    for i in range(60, len(train_data)):
    # Append past 60 values to x_train
    # contains 60 vals index from position 0 to position 59
    x_train.append(train_data[i-60:i, 0])

    #y_train will contain the 61st value 
    y_train.append(train_data[i,0])

    # Run below to visualize the x & y trains. x should be an array of 60 values and y should be 1 value being the 61st
    # Changing to if i<=61 will provide a 2nd pass through
    if i<=60:
    # print(x_train)
    # print(y_train)
    # print()

    # Convert x_train & y_train to numpy arrays  so we can use them for training the LSTM model
    x_train, y_train = np.array(x_train), np.array(y_train)

    # Reshape the data because LSTM network expects input to be 3 dimensional and as of now our x_train is 2D
    # number of sample(rows), timesteps(columns), and features(closing price)
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
    x_train.shape

    # Build LSTM model
    model = Sequential()
    # add LSTM with 50 neurons 
    model.add(LSTM(50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
    model.add(LSTM(50, return_sequences=False))
    model.add(Dense(25))
    model.add(Dense(1))

    # Compile the model
    model.compile(optimizer='adam', loss='mean_squared_error')

    # Train the model
    model.fit(x_train, y_train, batch_size=1, epochs=1)

    # Create testing dataset
    # Create new array containing scaled values from index 2057 to 2646
    test_data = scaled_data[training_data_len - 60: , :]

    # Create the data sets x_test and y_test
    x_test = []
    # y_test contains actual 61st values (not scaled)
    y_test = dataset[training_data_len: , :]

    for i in range(60, len(test_data)):
    x_test.append(test_data[i-60:i, 0])

    # Convert data to numpy array to use is LSTM model
    x_test = np.array(x_test)

    # Reshape the data because data is 2D and we need 3D for LSTM
    # number of samples(rows), timesteps(col), features(closing price)
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

    # Get the models predicted price values for x_test dataset
    predictions = model.predict(x_test)
    predictions = scaler.inverse_transform(predictions)

    # Get the root mean squared error. Closer to 0 the better
    rmse = np.sqrt(np.mean(predictions - y_test) **2)
    rmse

    # Plot the data
    train = data[:training_data_len]
    valid = data[training_data_len:]
    valid['Predictions'] = predictions

    return valid

def store_predictions(v):

    index_valid = v.reset_index()
    index_valid_df = pd.DataFrame(index_valid)
    index_valid_df.head()

    stock_date = index_valid_df['Date']
    stock_date_list = []

    for stock in stock_date:
    collect_dates = stock
    clean_dates = datetime.strftime(collect_dates, '%Y-%m-%d')
    stock_date_list.append(clean_dates)

    #print(stock_date_list)

    close_data = index_valid_df['close']
    close_data_list = []

    for close in close_data:
    collect_close = close
    close_data_list.append(collect_close)

    #close_data_list

    predictions_data = index_valid_df['Predictions']
    predicted_data_list = []

    for predict in predictions_data:
    collect_predict = predict
    predicted_data_list.append(collect_predict)

    #predicted_data_list

    prediction_data = {
    'Date': stock_date_list,
    'Actual Close': close_data_list,
    'Predictions': predicted_data_list
    }
    #prediction_data

    current_date = date.today().strftime('%Y-%m-%d')
    print(current_date)

    #db.dummy_test.update_one({'symbol': new_input}, {'$push': {'prediction': {'date': current_date, 'prediction_data': prediction_data}}})
    #print(f'{s} predictions stored in MongoDB')

# for stock in stock_symbols:
#     get_stored_data(stock)
#     get_update(stock, stock_date)
#     machine_learning(stock, stock_date, close)
#     store_predictions(valid)