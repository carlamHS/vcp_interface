#!/usr/bin/env python
# coding: utf-8

# In[1]:

import pandas as pd
import streamlit as st
import datetime as dt
import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import math
import os
from pandas_datareader import data as pdr
import yfinance as yf
from datetime import date, time,timedelta, datetime
import gspread
import json
import streamlit as st
import streamlit.components.v1 as components
from streamlit.components.v1 import html




yf.pdr_override()

def get_credentials():
    from oauth2client.service_account import ServiceAccountCredentials
    credentials = {
  "type": "service_account",
  "project_id": "web-application-358408",
  "private_key_id": "ca0e336e01e1cd5b194da82fc4205a71c61d010f",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCtnR14yAkmUBxT\nQE6Ects3apMiZjuCbbtecrt1cw40a2Zk+3EV23MHMx6xPO4LjiWwBA7gAB7bcwvr\n5xOkHQpOiCS3dBZEGOkI09uVhqilZzZ5svLQ3Lvtt22wPN7mWKQ5dN7Zg04nkVIP\nOn0nXwUkL4H3QYUjQX8AUlr1N31sLAZOjwq8hSdpw2+9+k3mQ6LnmBz3JqhD2EW6\n7X/U3udr7/Y31PAqQPDbTUkrNqC9dKB3WfohmSv+U/V6pOXw8m1nOF7szUOSaiR1\nnnMdRMa25PvAJ8fO1FwPbQ1vxDGdAdO7QOagkDT293f/ODY7H7BJscGcCeEc0zCu\nrxwXUkdLAgMBAAECggEAOgf0W/TxKf9JGIK8PAVwRPu4ppzpc1Veddl/02hb7SWh\nGkv5psatklCCB9hH8VDYRBd3KWSg69VuvLGGnSqf0VQsga2p66Uv76VxFm/mWzM+\nwDsScsH1hyXy4h/WmcQzUIlCHA6JxywJ89EnGEvomgnPNWiPKhOwcdkVUjX0FH2s\nXIU4qCQqdpoR5dCCk5IYhegJBGRzL38ggTF00JcSr6gwrOwIpaz9+9u3msRoU60g\nRejAXDdwXTVZKRk7w5hCE4AIiOnE4hPme/XprT6jkgcomTHf10Xsl+e28sFPdQdd\n7Y9r6n4f556r9dXOvJjcTNIdbHQH7z0gQbxiXyxMgQKBgQDy2voGpVVectkuWEop\nO0MDoHivGg9ncAFytpDrEDNHK3O4ubPHhFIirVPOnf+1MYGNOL8Jp20egUaaPbBv\nFUJpjiK3KhWPltb02mEH8BFP2SB8H99AOWR8sJ53i8F402L23PrxRia0Gm5BRPIm\npQ+UjIqi35e/SKHWNVkq2r89awKBgQC3AriBVBAJuJL58tSTl+YvymBw36sFCoEG\nAyWP3AVcoF9w+DI/yln+/rf4vA2VpsOnHGAzbauLG81boVXq/KSFAfw/t9iFQz/h\nJW/6UfZh2LXoHu8SE4jt9PLrf707jaMJCBgteMXMDdhtq7EfwVqKIaBxv7lv+NQg\nRCHX8+C1oQKBgEOxvlfz5iP5p4g/nAx6NGfiZ0GH5htTIVQ0h5i+X0zLU+p9+Rr4\nS1zXK7FAYXLEZfRTiQzL2qLSLjf4UiHkryp1MEAWPwRTa3+9D6cCyBCV2XQ//h8M\n4HHRWZrBHiDr634cguaWQ1uYsnsHGOikwf8KXeqgoM/1Ewd+v2guqXgZAoGACAf6\niNJjkcmjyYw6f++ejmJXMRzfqGz5lIX21AVXxuTSy2ZY7iu3H1WWRTgbcIHM/Dxm\njFs3t/cUX/0IhDNqFNwtca5jthVpbDv0WgvWwBx+fx08aJKq46ZoMqV8bGyexvqv\n9O7j3zyMTuPF9hrKGl23aMZ9IMjOpkvXIF73cYECgYAW+yx/pBtz5p40EtTOl7AK\nNI8oF9IDMy+Wt0Yv/AzKyqFKvjX03dpU0vU/xNpStseW/btaCmoO9s6b+77Mckqk\nVeLI81krPkD4ff2KNSzFM/o58jCMjtS14TDZGpYc3+3gE+sS1BjvXgTTikrgmTsy\npk85IKHWX4xAUc2PkWozZQ==\n-----END PRIVATE KEY-----\n",
  "client_email": "vcp-for-streamlit@web-application-358408.iam.gserviceaccount.com",
  "client_id": "109364290400051661215",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/vcp-for-streamlit%40web-application-358408.iam.gserviceaccount.com"
}
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials, scope)
    client = gspread.authorize(creds)
    return client

#Now will can access our google sheets we call client.open on StartupName
sheet = get_credentials().open('VCP_info').sheet1
results = sheet.get_all_records()
df = pd.json_normalize(results)

st.set_page_config(
    page_title="VCP Profile Chart",
    layout="wide")

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


# Initialization
if 'key' not in st.session_state:
    st.session_state['key'] = ''

# Session State also supports attribute based syntax
if 'key' not in st.session_state:
    st.session_state.key = ''

# Read
st.write(st.session_state.key)

symbols = df.loc[date]['Tickers']
symbols = [i.replace("'", "") for i in symbols]

ticker = st.sidebar.selectbox(
    'Choose a Stock',
     symbols)

p = st.sidebar.number_input("How many days (10-260)",min_value=10, max_value=260, step=1)

risk_input = st.sidebar.text_input('Enter your risk($)', '100')

buy_at = st.sidebar.text_input('Enter your buy at price', '100')

stop_loss = st.sidebar.text_input('Enter your stop loss','99')

st.sidebar.write(f'''
    <a target="_self" href="https://carlam.net">
        <button>
            Find the latest info in csv here
        </button>
    </a>
    ''',
    unsafe_allow_html=True
)

result = st.subheader(ticker + "------- Amt: " + str(math.floor(eval(risk_input)/(eval(buy_at) - eval(stop_loss)))) +", buy at: "+buy_at+ ",    stop Loss at: " + stop_loss +  ",  Risk(%):  " + str(round((eval(buy_at) - eval(stop_loss))/eval(buy_at)*100,2))+"%" )
earning_date = st.caption("Next earning date: "+str(get_next_earnings_date(ticker)))

# download dataframe
start = date - timedelta(days = p)

history_data = pdr.get_data_yahoo(ticker, start=start, end=date+timedelta(days = 1))

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

# Define your javascript
my_js = '''
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-2153021198707711"
     crossorigin="anonymous"></script>
<!-- stream lit -->
<ins class="adsbygoogle"
     style="display:block"
     data-ad-client="ca-pub-2153021198707711"
     data-ad-slot="8965125538"
     data-ad-format="auto"
     data-full-width-responsive="true"></ins>
<script>
     (adsbygoogle = window.adsbygoogle || []).push({});
</script>;
'''


components.html(my_js)  # JavaScript works

