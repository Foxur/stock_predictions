import numpy as np
import stock_data.processing.get_stock_data as gsd
import matplotlib.pyplot as plt
import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout
from sklearn.preprocessing import MinMaxScaler
from datetime import date, timedelta
import time
from os import listdir
import pickle

# SET Variables
scaler = MinMaxScaler(feature_range=(0, 1))
path_to_stock_data = '../stock_data/input/'
path_to_predictions = '../stock_data/predictions/'
path_to_prediction_imgs = '../webserver/static/'


def get_new_predictions(stock_name):
    # Read the Date into a Dataframe
    files = listdir(path_to_stock_data)
    # print(files)
    stock = stock_name + '.csv'
    if files.__contains__(stock):
        print(path_to_stock_data + str(stock))
        df = pd.read_csv(path_to_stock_data + str(stock))
    else:
        # print('Stock data not found Start loading')
        # print(stock)
        gsd.get_stonks_data(stock_name)
        df = pd.read_csv(path_to_stock_data + str(stock))

    # Set Data up for training
    train_size = int(len(df) * 0.8)
    df_train, df_test = df[:train_size], df[train_size:len(df)]
    train_data = df_train.iloc[:, 1:2].values
    train_data_scaled = scaler.fit_transform(train_data)
    x_train = []
    y_train = []
    # Set Time Windows we want to Choose for our predictions max is 60
    time_window = 60
    for i in range(time_window, len(train_data_scaled)):
        x_train.append(train_data_scaled[i - time_window:i, 0])
        y_train.append(train_data_scaled[i, 0])
    x_train, y_train = np.array(x_train), np.array(y_train)
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

    # Model creation, training and saving
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50, return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50))
    model.add(Dropout(0.2))
    model.add(Dense(units=1))

    model.compile(optimizer='adam', loss='mean_squared_error')
    start1 = time.time_ns()
    model.fit(x_train, y_train, epochs=50, batch_size=30, use_multiprocessing=True, verbose=2)
    end1 = time.time_ns()
    print(f'First iteration:{end1 - start1}')

    # Prepare Data for predictions
    actual_stock_price = df_test.iloc[:, 1:2].values

    total_data = pd.concat((df_train['Open'], df_test['Open']), axis=0)
    test_data = total_data[len(total_data) - len(df_test) - time_window:].values
    test_data = test_data.reshape(-1, 1)
    test_data = scaler.transform(test_data)

    total_dates = pd.concat((df_train['Date'], df_test['Date']), axis=0)
    test_dates = total_dates[len(total_dates) - len(df_test) - time_window:].values
    test_dates = test_dates.reshape(-1, 1)

    x_test = []
    for i in range(time_window, len(test_data)):
        x_test.append(test_data[i - time_window:i, 0])

    x_test = np.array(x_test)
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

    # Predict Model accuracy
    # predicted_stock_price = model.predict(x_test)
    # predicted_stock_price = scaler.inverse_transform(predicted_stock_price)

    # plt_test_dates = [dt.datetime.strptime(d, '%Y-%m-%d') for d in test_dates[time_window:, 0]]
    # plt.plot(plt_test_dates, actual_stock_price[:, 0], color='black', label='Actual TWTR Price')
    # plt.plot(plt_test_dates, predicted_stock_price[:, 0], color='green', label='Predicted TWTR Price')
    # plt.xticks(rotation=90)
    # plt.title('TWTR Share Price')
    # plt.xlabel('Time')
    # plt.ylabel('TWTR Share Price')
    # plt.legend()
    # plt.show()

    # Make Further Predictions
    future_predictions = []
    for i in range(0, 30):
        real_data = [test_data[len(test_data) + i - time_window:len(test_data + i), 0]]
        real_data = np.array(real_data)
        real_data = np.reshape(real_data, (real_data.shape[0], real_data.shape[1], 1))
        prediction = model.predict(real_data)
        prediction = scaler.inverse_transform(prediction)
        future_predictions.append(prediction)
        # for i in range(0, len(future_predictions)):
        #     print(f'Prediction {i}: {future_predictions[i]}')
        # Create a trace
        pickle.dump(future_predictions, open(path_to_predictions + stock_name + '.sav', 'wb'))

    data = future_predictions
    for i in range(0, len(data)):
        data[i] = data[i][0][0]

    time2 = []
    for i in range(0, len(data)):
        time2.append(date.today() + timedelta(days=i))

    xpoints = np.array(time2)
    ypoints = np.array(data)
    plt.clf()
    plt.plot(xpoints, ypoints, label=stock_name)
    plt.xticks(rotation=20)
    plt.title('Predicted Stock Price')
    plt.xlabel('Time')
    plt.ylabel('Price in EU')
    plt.legend()
    plt.autoscale(enable=True, axis='both', tight=None)
    plt.savefig(path_to_prediction_imgs + stock_name + '.png')


def load_predictions(stonk_name):
    predictions = pickle.load(open(path_to_predictions + stonk_name + '.sav', 'rb'))
    return predictions

# For testing
# get_new_predictions('TSLA')
# print(load_predictions('TSLA'))
