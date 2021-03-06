
"""
Built using inspiration from KD Nuggets:
https://www.kdnuggets.com/2020/01/stock-market-forecasting-time-series-analysis.html

"""
import os
import warnings
warnings.filterwarnings('ignore')
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
from pylab import rcParams
rcParams['figure.figsize'] = 10, 6

from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.arima_model import ARIMA
from pmdarima.arima import auto_arima
from sklearn.metrics import mean_squared_error, mean_absolute_error
import math
import numpy as np

df = pd.read_csv(r"data.csv",index_col='Date',parse_dates=(True))

df_close = df['Close']

"""
Augmented Dickey Fuller Test for stationarity
def test_stationarity(timeseries):
    rolmean = timeseries.rolling(12).mean()
    rolstd = timeseries.rolling(12).std()
    
    plt.plot(timeseries, color='blue', label='Original')
    plt.plot(rolmean, color='red',label='Rolling Mean')
    plt.plot(rolstd, color='black', label='Rolling Std')
    plt.legend(loc='best')
    plt.title('Rolling Mean and Standard Deviation')
    plt.show(block=False)
    
    print("Results of dickey fuller test")
    adft = adfuller(timeseries,autolag='AIC')
    
    output = pd.Series(adft[0:4],index=['Test Statistics','p-value','No. of lags used','No. of observations used'])
    for key,values in adft[4].items():
        output['critical value (%s)'%key] = values
    print(output)
    
test_stationarity(df_close)
"""
"""
identify seasonality
result = seasonal_decompose(df_close, model="multiplicative",freq=30)
fig = plt.figure()
fig = result.plot()
fig.set_size_inches(16,9)
"""

df_log = np.log(df_close)
moving_avg = df_log.rolling(12).mean()
std_dev = df_log.rolling(12).std()

"""
plt.legend(loc='best')
plt.title('Moving Average')
plt.plot(std_dev,color="black",label="Standard Deviation")
plt.plot(moving_avg,color="red",label="Mean")
plt.legend()
plt.show()
"""

#split data into train adn test data
train_data, test_data = df_log[3:int(len(df_log)*0.9)], df_log[int(len(df_log)*0.9):]

"""
plt.figure(figsize=(10,6))
plt.grid(True)
plt.xlabel('Dates')
plt.ylabel('Closing Prices')
plt.plot(df_log, 'green', label='Train Data')
plt.plot(test_data, 'blue', label='Test Data')
plt.legend()
"""

model_autoARIMA = auto_arima(train_data, start_p=0, start_q=0,
                             test='adf', 
                             max_p=3, max_q=3,
                             m=1,
                             d=None,
                             seasonal=False,
                             start_P=0,
                             D=0,
                             trace=True,
                             error_action='ignore',
                             suppress_warnings=True,
                             stepwise=True)

model = ARIMA(train_data, order=(0,1,0))
fitted = model.fit(disp=1)

fc, se, conf = fitted.forecast(86, alpha=0.05)  # 95% confidence
fc_series = pd.Series(fc, index=test_data.index)
lower_series = pd.Series(conf[:, 0], index=test_data.index)
upper_series = pd.Series(conf[:, 1], index=test_data.index)
plt.figure(figsize=(12,5), dpi=100)
plt.plot(train_data, label='training')
plt.plot(test_data, color = 'blue', label='Actual Stock Price')
plt.plot(fc_series, color = 'orange',label='Predicted Stock Price')
plt.fill_between(lower_series.index, lower_series, upper_series, 
                 color='k', alpha=.10)
plt.title('QLGN Stock Price Prediction')
plt.xlabel('Time')
plt.ylabel('Actual Stock Price')
plt.legend(loc='upper left', fontsize=8)
plt.show()

mse = mean_squared_error(test_data, fc)
print('MSE: '+str(mse))
mae = mean_absolute_error(test_data, fc)
print('MAE: '+str(mae))
rmse = math.sqrt(mean_squared_error(test_data, fc))
print('RMSE: '+str(rmse))
mape = np.mean(np.abs(fc - test_data)/np.abs(test_data))
print('MAPE: '+str(mape))

