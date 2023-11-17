# -*- coding: utf-8 -*-
"""
Created on Wed Dec 28 23:44:38 2022

@author: James
"""
# -*- coding: utf-8 -*-
"""

Built using: 
https://www.machinelearningplus.com/machine-learning/portfolio-optimization-python-example/

"""
#Load Packages
import numpy as np
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

#Load Data
tickers = ['AAVE-USD','APE18876-USD', 'BTC-USD','COMP5692-USD','ETH-USD','SNX-USD',
           'YFI-USD','SOL-USD','DOGE-USD']
end_date = datetime.today().strftime('%Y-%m-%d')
df = yf.download(tickers, start='2022-01-01',end=end_date,)
df = df["Close"]

df = pd.DataFrame(df, columns = ['AAVE-USD','APE18876-USD', 'BTC-USD','COMP5692-USD', 'ETH-USD','SNX-USD',
           'YFI-USD','SOL-USD','DOGE-USD'])

cov_matrix = df.pct_change().apply(lambda x: np.log(1+x)).cov()
corr_matrix = df.pct_change().apply(lambda x: np.log(1+x)).corr()

#APE has least data and drives periods
ind_er = df.pct_change(periods=df['APE18876-USD'].count()-1).mean()
ann_sd = df.pct_change().apply(lambda x: np.log(1+x)).std().apply(lambda x: x*np.sqrt(250))


assets = pd.concat([ind_er, ann_sd], axis=1)
assets.columns = ['Returns','Volatility']
print("Start date: 2022-01-01, End date: ",end_date)
print(assets)

p_ret = []
p_vol = []
p_weights = []

num_assets=len(df.columns)
num_portfolios = 1000

for portfolio in range(num_portfolios):
    weights = np.random.random(num_assets)
    weights = weights/np.sum(weights)
    p_weights.append(weights)
    returns = np.dot(weights, ind_er)
    
    p_ret.append(returns)
    var = cov_matrix.mul(weights, axis=0).mul(weights,axis=1).sum().sum()
    sd = np.sqrt(var)
    ann_sd = sd*np.sqrt(250)
    p_vol.append(ann_sd)

data = {'Returns':p_ret, 'Volatility':p_vol}


for counter, symbol in enumerate(df.columns.tolist()):
    data[symbol+'weight'] = [w[counter] for w in p_weights]

portfolios = pd.DataFrame(data)
rf = 0.01
optimal_risky_port = portfolios.iloc[((portfolios['Returns']-rf)/portfolios['Volatility']).idxmax()]

print(optimal_risky_port)

