import math
import pandas_datareader as web
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM
import matplotlib.pyplot as plt
import plotly.express as px
plt.style.use('fivethirtyeight')

# Pull stock quote
df = web.DataReader('AAPL', data_source='yahoo', start='2010-01-01', end='2020-12-30')

# Create new df with only the 'Close' column
data = df.filter(['Close'])

# Convert df to a numpy array
dataset = data.values

# Get the number of rows to train the model on
training_data_len = math.ceil(len(dataset) * .8)

# Scale the data to apply preprocessing scaling before presenting to nueral network
scaler = MinMaxScaler(feature_range=(0,1))
scaled_data = scaler.fit_transform(dataset)

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

# Convert x_train & y_train to numpy arrays  so we can use them for training the LSTM model
x_train, y_train = np.array(x_train), np.array(y_train)

# Reshape the data because LSTM network expects input to be 3 dimensional and as of now our x_train is 2D
# number of sample(rows), timesteps(columns), and features(closing price)
x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
###### x_train.shape


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

# Plot the data
train = data[:training_data_len]
valid = data[training_data_len:]
valid['Predictions'] = predictions

df = px.data.stocks()
fig = px.line(df, x=train['Close'], y=valid[['Close', 'Predictions']])
fig.show()

