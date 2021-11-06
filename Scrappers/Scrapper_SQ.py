from __future__ import division
from pandas_datareader.data import DataReader
import numpy as np
import pandas as pd
import requests_cache
from datetime import date
import bs4
import requests
from bs4 import BeautifulSoup

url = 'https://e6hx5erhc6.execute-api.ap-southeast-1.amazonaws.com/Fintech/fintech_data_pipe'

session = requests_cache.CachedSession(cache_name='cache', backend='sqlite')

# add header to session and provide it to the reader
session.headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0',
                   'Accept': 'application/json;charset=utf-8'}

def get_data_for_multiple_stocks(tickers,start_date,end_date):
    stocks = dict()
    # loop through all the tickers
    for ticker in tickers:
        # get the data for the specific ticker
        s = DataReader(ticker, 'yahoo', start_date, end_date, session=session)
      
        s.insert(0, "Ticker", ticker)  #insert ticker column so you can reference better later
        
        s['Prev Close'] = s['Adj Close'].shift(1)
        s['perc_return'] = (s['Adj Close']/s['Prev Close']) - 1
        # add it to the dictionary
        stocks[ticker] = s
    # return the dictionary
    return stocks

#scrap stock price for brent crude oil from yahoo finance
def scrapper_sq():
    today = date.today() #get today's date
    enddate = str(today.strftime("%Y-%m-%d"))
    tickers = ['BZ=F']
    bc_oil_2021 = get_data_for_multiple_stocks(tickers,start_date='2021-01-01',end_date=enddate)
    BCO= bc_oil_2021['BZ=F']

    cur = BCO.tail(1)
    adjClose = float(cur['Adj Close'])
    percReturn = float(cur['perc_return'])

    #prepare key-value dictionary
    result = {'BrentCrudeOil_adjClose': adjClose}

    body = {
        "values": result
    }
    resp = requests.post(url, json = body)
    print(resp.text)
