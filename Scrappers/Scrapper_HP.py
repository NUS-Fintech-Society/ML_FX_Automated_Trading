from logging import error
import urllib.request
import urllib.response
import urllib.error
import json
from bs4 import BeautifulSoup 
import urllib.request as rq
import requests
import datetime
from oandapyV20 import API
import oandapyV20.endpoints.pricing as pricing
from constants_hp import POSITIVE_CORRELATION, YAHOO_OPTION, YAHOO_STOCK, EPOCH_WEEK, VOLAFY_URL, IVR_LST, ACCOUNT_ID


url = 'https://e6hx5erhc6.execute-api.ap-southeast-1.amazonaws.com/Fintech/fintech_data_pipe'
api = API(access_token="6d3f41bece536ad3f426dce6b221a936-d0dc087ffefd07412308ec16e169b685")
    
# calls to oanda for commodities/pairs with positive correlation
def get_positive_correlation_query_oanda():

    instruments = "GBP_JPY"

    for pairs in POSITIVE_CORRELATION:
        instruments += f",{pairs}"

    params = {
        "instruments" : instruments
    }

    r = pricing.PricingInfo(accountID=ACCOUNT_ID, params=params)
    rv = api.request(r) 

    body = {}
    prices = rv["prices"]

    gbpjpy_price = get_price(prices[0]["bids"], prices[0]["asks"])
    body["GBP_JPY"] = gbpjpy_price

    for i in range(len(POSITIVE_CORRELATION)):
        price = get_price(prices[i + 1]["bids"], prices[i + 1]["asks"])
        price_spread = gbpjpy_price - price
        price_ratio = gbpjpy_price / price

    body[f"{POSITIVE_CORRELATION[i]}"] = price_spread
    body[f"{POSITIVE_CORRELATION[i]}_spread"] = price_spread
    body[f"{POSITIVE_CORRELATION[i]}_ratio"] = price_ratio
    return body

# calculate mid price from bid ask spread
def get_price(bids, asks):
    bid_price = float(max(bids, key = lambda x:x["liquidity"])["price"])
    ask_price = float(max(asks, key = lambda x:x["liquidity"])["price"])

    return (bid_price + ask_price) / 2

# returns yfinance stock data on ticker
def query_y_finance_stock(ticker):
    url = f"{YAHOO_STOCK}{ticker}?modules=price%2CsummaryDetail"

    response = urllib.request.urlopen(url)
    data = json.loads(response.read())
    result = data["quoteSummary"]["result"][0]

    price = float(result["price"]["regularMarketPrice"]["fmt"].replace(",", ""))
    return price

# returns yfinance options data on ticker base on weeks to expiry
def query_y_finance_options(ticker, week = 0):
    epoch = coming_friday_epoch() + week * EPOCH_WEEK

    url = f"{YAHOO_OPTION}{ticker}?date={epoch}" 

# calculate coming friday epoch time for yfinance
def coming_friday_epoch():
    today = datetime.date.today()
    friday =  today + datetime.timedelta( (4 - today.weekday()) % 7 )
    epoch = int(datetime.datetime(friday.year, friday.month, friday.day, tzinfo=datetime.timezone.utc) \
    .timestamp()) 

    return epoch

# type: equity or future(commodities and FX index)
def iv_volafy(type, ticker):
    url = f"{VOLAFY_URL}{type}/{ticker}"
    request = rq.urlopen(url)
    soup = BeautifulSoup(request.read(), 'html.parser')

    tr_ivr = float(soup.find(text="Implied Volatility Percentile (IVP) 1y") \
        .find_parent('tr').find('td').find('div').get_text())

    tr_iv = float(soup.find(text="Implied Volatility (IV) 30d") \
        .find_parent('tr').find('td').find('div').get_text())

    tr_hv = float(soup.find(text="Implied Volatility (IV) 30d") \
        .find_parent('tr').find('td').find('div').get_text())    


    return {
        f"{ticker}_ivr" : tr_ivr
    }

# calls to volafy for ivr of interested tickers       
def get_ivr_equity_query_volafy():
    body = {}
    for ticker in IVR_LST:
        try:
            body.update(iv_volafy("equity", ticker))
        except:
            pass
    return body

# main function calling helper functions to scrape from the various sources
def scrapper_hp():
    body = {}
    value = {}

    value.update(get_positive_correlation_query_oanda())
    value.update(get_ivr_equity_query_volafy())
 
    body["values"] = value
    resp = requests.post(url, json = body)
    print(body)
    print(resp.text)

#positive_correlation_query_oanda()
#scrape_main()
