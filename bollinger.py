# -*- coding: utf-8 -*-
"""
Stock Tracker -- Bollinger Bands
https://www.fidelity.com/learning-center/trading-investing/technical-analysis/technical-indicator-guide/bollinger-bands#:~:text=Bollinger%20Bands%20are%20envelopes%20plotted,Period%20and%20Standard%20Deviations%2C%20StdDev.
"""

import numpy as np
import pandas as pd

df = pd.read_csv("",index_col='Date',parse_dates=(True))
df_close = df['Close']

st_av = df_close.sort_index(ascending=False).head(10).mean()
st_std = df_close.sort_index(ascending=False).head(10).std()
st_bolu = st_av + (st_std * 1.5)
st_bold = st_av - (st_std * 1.5)

mt_av = df_close.sort_index(ascending=False).head(20).mean()
mt_std = df_close.sort_index(ascending=False).head(20).std()
mt_bolu = mt_av + (mt_std * 2)
mt_bold = mt_av - (mt_std * 2)

lt_av = df_close.sort_index(ascending=False).head(50).mean()
lt_std = df_close.sort_index(ascending=False).head(50).std()
lt_bolu = lt_av + (lt_std * 2.5)
lt_bold = lt_av - (lt_std * 2.5)

print('Long-term BOLU: $',round(lt_bolu,2))
print('Long-term Rolling Average: $',round(lt_av,2))
print('Long-term BOLD: $',round(lt_bold,2))

print('Medium-term BOLU: $',round(mt_bolu,2))
print('Medium-term Rolling Average: $',round(mt_av,2))
print('Medium-term BOLD: $',round(mt_bold,2))

print('Short-term BOLU: $',round(st_bolu,2))
print('Short-term Rolling Average: $',round(st_av,2))
print('Short-term BOLD: $',round(st_bold,2))