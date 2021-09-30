import oandapyV20
from oandapyV20 import API
import oandapyV20.endpoints.pricing as pricing
import json
import requests
from Credentials import *

url = 'https://e6hx5erhc6.execute-api.ap-southeast-1.amazonaws.com/Fintech/fintech_data_pipe'

api = API(access_token= oanda_token)
accountID = oanda_acc_id

# GBP_JPY pair
close_bid_GBP_JPY = []
close_ask_GBP_JPY = []
time_GBP_JPY = []

# Brent Crude Oil_GBP pair
close_bid_BCO_GBP = []
close_ask_BCO_GBP = []
time_BCO_GBP = []

# Gold_JPY pair
close_bid_XAU_JPY = []
close_ask_XAU_JPY = []
time_XAU_JPY = []

def scrapper_jx():
    params_XAU_JPY = {
              "instruments": {"XAU_JPY"}
            }

    r_XAU_JPY = pricing.PricingStream(accountID=accountID, params=params_XAU_JPY)
    rv_XAU_JPY = api.request(r_XAU_JPY)
    for ticks in rv_XAU_JPY:
        time_XAU_JPY.append(ticks['time'])
        if ('closeoutBid' in ticks.keys()):
            close_bid_XAU_JPY.append(ticks['closeoutBid'])
            close_ask_XAU_JPY.append(ticks['closeoutAsk'])
        else:
            break
        '''

    params_GBP_JPY = {
              "instruments": "GBP_JPY"
            }

    r_GBP_JPY = pricing.PricingStream(accountID=accountID, params=params_GBP_JPY)
    rv_GBP_JPY = api.request(r_GBP_JPY)
    for ticks in rv_GBP_JPY:
        time_GBP_JPY.append(ticks['time'])
        if ('closeoutBid' in ticks.keys()):
            close_bid_GBP_JPY.append(ticks['closeoutBid'])
            close_ask_GBP_JPY.append(ticks['closeoutAsk'])
        else:
            break
    '''

    params_BCO_GBP = {
              "instruments": "BCO_GBP"
            }

    r_BCO_GBP = pricing.PricingStream(accountID=accountID, params=params_BCO_GBP)
    rv_BCO_GBP = api.request(r_BCO_GBP)
    for ticks in rv_BCO_GBP:
        time_BCO_GBP.append(ticks['time'])
        if ('closeoutBid' in ticks.keys()):
            close_bid_BCO_GBP.append(ticks['closeoutBid'])
            close_ask_BCO_GBP.append(ticks['closeoutAsk'])
        else:
            break
    body = {"values":{"XAU_JPY" : float(close_bid_XAU_JPY[0]), "BCO_GBP":float(close_bid_BCO_GBP[0])}}
    resp = requests.post(url, json = body)
