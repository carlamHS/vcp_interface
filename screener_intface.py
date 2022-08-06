#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import streamlit as st
import datetime as dt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import math
import os
from pandas_datareader import data as pdr
import yfinance as yf
from datetime import date, time,timedelta, datetime
yf.pdr_override()

total_info_name = "/Download/total_info.csv"    # For logging the stock statistic daily  收集每日.pdf數據作縱貫分析
if os.path.exists(total_info_name):
    df = pd.read_csv(total_info_name)

st.set_page_config(
    page_title="VCP Profile Chart",
    layout="wide")

uploaded_file = st.sidebar.file_uploader("Download the latest csv file from https://carlam.net and upload it to here")

if uploaded_file is None:
    # initialize list of lists
    data = [2022,1,1,2240,4058,432,1117,-22652219216,3.414,32.137,24.802,20.896,14.147,24.802,117,1.858,'[[TSLA, 0.81237], [AAPL, 0.81237]]']

    # Create the pandas DataFrame
    df = pd.DataFrame([data], columns=["Year",
                                     'Month',
                                     'Day',
                                     'Advanced stock(day)',
                                     'Declined stock(day)',
                                     'New High',
                                     'New Low',
                                     'Gauge',
                                     'Stock above its 50-DMA > 150-DMA > 200-DMA',
                                     'Stock above its 50-DMA',
                                     'Stock that its 20-DMA > 50-DMA',
                                     'Stock that its 50-DMA > 200-DMA',
                                     'Stock that its 50 > 150 > 200-DMA',
                                     'Stock that its 200-DMA is rising',
                                     'Number of Stock that fit condition',
                                     'Numbertion',
                                     'Tickers that fit the conditions',
                                     ])
else:
    df = pd.read_csv(uploaded_file)

df.rename(columns = {'Year':'year', 'Month':'month', 'Day':'day'}, inplace = True)
df['date']= pd.to_datetime(df[['year', 'month', 'day']])
date_list = df['date'].tolist()
date_list.sort(reverse=True)


df.set_index('date', inplace = True)
df.drop(['year', 'month', 'day'], axis = 1, inplace = True)
df.sort_index(inplace = True)
df.index = pd.to_datetime(df.index)
df.index = df.index.rename('date')

date = st.sidebar.selectbox(
    'Pick a date',
     date_list)

# Find the timedelta between today and the stock next earnings date and print it in days, hours, minutes, seconds.
def get_next_earnings_date(stock_symbol):
    from datetime import date, timedelta, datetime
    import yahoo_fin.stock_info as si

    # Get the next earnings date for the stock
    next_earnings_date = si.get_next_earnings_date(stock_symbol)

    return next_earnings_date

# Split the string into a list of strings
def split_string(string):
    lst = string.split(', ')
    return lst[::2]

# Replace all [] with ''
def replace_brackets(string):
    return string.replace('[', '').replace(']', '')

df['Tickers'] = df['Tickers that fit the conditions'].apply(replace_brackets).apply(split_string)


symbols = df.loc[date]['Tickers']
symbols = [i.replace("'", "") for i in symbols]

ticker = st.sidebar.selectbox(
    'Choose a Stock',
     symbols)

p = st.sidebar.number_input("How many days (10-260)",min_value=10, max_value=260, step=1)

risk_input = st.sidebar.text_input('Enter your risk($)', '100')

buy_at = st.sidebar.text_input('Enter your buy at price', '100')

stop_loss = st.sidebar.text_input('Enter your stop loss','99')

result = st.subheader(ticker + "------- Amt: " + str(math.floor(eval(risk_input)/(eval(buy_at) - eval(stop_loss)))) +", buy at: "+buy_at+ ",    stop Loss at: " + stop_loss +  ",  Risk(%):  " + str(round((eval(buy_at) - eval(stop_loss))/eval(buy_at)*100,2))+"%" )
earning_date = st.caption("Next earning date: "+str(get_next_earnings_date(ticker)))

# download dataframe
start = date - timedelta(days = p)

history_data = pdr.get_data_yahoo(ticker, start=start, end=date)

prices = history_data['Close']
volumes = history_data['Volume']

lower = prices.min()
upper = prices.max()
prices_ax = np.linspace(lower,upper, num=20)

vol_ax = np.zeros(20)

for i in range(0, len(volumes)):
    if(prices[i] >= prices_ax[0] and prices[i] < prices_ax[1]):
        vol_ax[0] += volumes[i]   
        
    elif(prices[i] >= prices_ax[1] and prices[i] < prices_ax[2]):
        vol_ax[1] += volumes[i]  
        
    elif(prices[i] >= prices_ax[2] and prices[i] < prices_ax[3]):
        vol_ax[2] += volumes[i] 
        
    elif(prices[i] >= prices_ax[3] and prices[i] < prices_ax[4]):
        vol_ax[3] += volumes[i]  
        
    elif(prices[i] >= prices_ax[4] and prices[i] < prices_ax[5]):
        vol_ax[4] += volumes[i]  
        
    elif(prices[i] >= prices_ax[5] and prices[i] < prices_ax[6]):
        vol_ax[5] += volumes[i] 
        
    elif(prices[i] >= prices_ax[6] and prices[i] < prices_ax[7]):
        vol_ax[6] += volumes[i] 

    elif(prices[i] >= prices_ax[7] and prices[i] < prices_ax[8]):
        vol_ax[7] += volumes[i] 

    elif(prices[i] >= prices_ax[8] and prices[i] < prices_ax[9]):
        vol_ax[8] += volumes[i] 

    elif(prices[i] >= prices_ax[9] and prices[i] < prices_ax[10]):
        vol_ax[9] += volumes[i] 

    elif(prices[i] >= prices_ax[10] and prices[i] < prices_ax[11]):
        vol_ax[10] += volumes[i] 

    elif(prices[i] >= prices_ax[11] and prices[i] < prices_ax[12]):
        vol_ax[11] += volumes[i] 

    elif(prices[i] >= prices_ax[12] and prices[i] < prices_ax[13]):
        vol_ax[12] += volumes[i] 

    elif(prices[i] >= prices_ax[13] and prices[i] < prices_ax[14]):
        vol_ax[13] += volumes[i] 

    elif(prices[i] >= prices_ax[14] and prices[i] < prices_ax[15]):
        vol_ax[14] += volumes[i]   
        
    elif(prices[i] >= prices_ax[15] and prices[i] < prices_ax[16]):
        vol_ax[15] += volumes[i] 
        
    elif(prices[i] >= prices_ax[16] and prices[i] < prices_ax[17]):
        vol_ax[16] += volumes[i]         
        
    elif(prices[i] >= prices_ax[17] and prices[i] < prices_ax[18]):
        vol_ax[17] += volumes[i]         
        
    elif(prices[i] >= prices_ax[18] and prices[i] < prices_ax[19]):
        vol_ax[18] += volumes[i] 
    
    else:
        vol_ax[19] += volumes[i]

fig = make_subplots(
        rows=1, cols=2,
        column_widths=[0.2, 0.8],
        specs=[[{}, {}]],
        horizontal_spacing = 0.01
    )

fig.add_trace(
        go.Bar(
                x = vol_ax, 
                y= prices_ax,
                text = np.around(prices_ax,2),
                textposition='auto',
                orientation = 'h'
            ),
        row = 1, col =1
    )

# Converting the index of the dataframe to string so that it can be used as x-axis
history_data.index = pd.to_datetime(history_data.index).strftime('%Y-%m-%d')    
dateStr = history_data.index

fig.add_trace(
    go.Candlestick(x=dateStr,
                open=history_data['Open'],
                high=history_data['High'],
                low=history_data['Low'],
                close=history_data['Close'],
                yaxis= "y2"  
            ),
        row = 1, col=2
    )
        
fig.update_layout(
    title_text='Market Profile Chart (VCP)', # title of plot
    bargap=0.01, # gap between bars of adjacent location coordinates,
    showlegend=False,
    
    xaxis = dict(
            showticklabels = False
        ),
    yaxis = dict(
            showticklabels = False
        ),
    
    yaxis2 = dict(
            title = "Price (USD)",
            side="right"
        )
)

fig.update_yaxes(nticks=20)
fig.update_yaxes(side="right")
fig.update_layout(height=800)

config={
        'modeBarButtonsToAdd': ['drawline']
    }

st.plotly_chart(fig, use_container_width=True, config=config)

