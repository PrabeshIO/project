import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Flatten
from numpy import array
import pandas as pd
from dataframes import province as pr, timeline as t1
import matplotlib.pyplot as plt
from matplotlib import dates
import datetime
from datetime import timedelta
import math
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# a=pr.get_province()
# print(a)

b, last_date = t1.get_timeline()
# print(b)
prev_dates= b["Date"].tolist()
dataset = b['TotalCases'].tolist()
# print(prev_dates)


# preparing independent and dependent features
def prepare_data(timeseries_data, n_features):
    X, y = [], []
    for i in range(len(timeseries_data)):
        # find the end of this pattern
        end_ix = i + n_features
        # check if we are beyond the sequence
        if end_ix > len(timeseries_data) - 1:
            break
        # gather input and output parts of the pattern
        seq_x, seq_y = timeseries_data[i:end_ix], timeseries_data[end_ix]
        X.append(seq_x)
        y.append(seq_y)
    return np.array(X), np.array(y)

# define input sequence
timeseries_data = dataset
# choose a number of time steps
n_steps = 3
# split into samples
X, y = prepare_data(timeseries_data, n_steps)

# print(X),print(y)

# reshape from [samples, timesteps] into [samples, timesteps, features]
n_features = 1
X = X.reshape((X.shape[0], X.shape[1], n_features))
# print(X.shape)

# define model
model = Sequential()
model.add(LSTM(50, activation='relu', return_sequences=True, input_shape=(n_steps, n_features)))
model.add(LSTM(50, activation='relu'))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mse')
# fit model
model.fit(X, y, epochs=300, verbose=1)

# demonstrate prediction for next 10 days
x_input = array(dataset[len(dataset) - n_steps:])
temp_input = list(x_input)
lst_output = []
i = 0
days = int(input("Enter Number of days you want to predict for !"))
while i < days:

    if len(temp_input) > 3:
        x_input = array(temp_input[1:])
        # print("{} day input {}".format(i, x_input))
        # print(x_input)
        x_input = x_input.reshape((1, n_steps, n_features))
        # print(x_input)
        yhat = model.predict(x_input, verbose=0)
        # print("{} day output {}".format(i, yhat))
        temp_input.append(yhat[0][0])
        temp_input = temp_input[1:]
        # print(temp_input)
        lst_output.append(math.floor(yhat[0][0]))

        i = i + 1
    else:
        x_input = x_input.reshape((1, n_steps, n_features))
        yhat = model.predict(x_input, verbose=0)
        # print(yhat[0])
        temp_input.append(yhat[0][0])
        lst_output.append(math.floor(yhat[0][0]))
        i = i + 1



# print(lst_output)
# print(last_date)
dates = []
start_date = last_date
for i in range(days):
    a = start_date.strftime("%d")  # date
    b = start_date.strftime("%b")  # month
    c = a + " " + b
    dates.append(c)
    start_date = start_date + timedelta(days=1)

print(lst_output)
pred_dates= dates
total_dates= prev_dates + pred_dates

print(pred_dates)
