import oandapyV20
from oandapyV20 import API
import oandapyV20.endpoints.pricing as pricing
import json

api = API(access_token= "6d3f41bece536ad3f426dce6b221a936-d0dc087ffefd07412308ec16e169b685")
accountID = "101-003-9162148-001"

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

def XAU_JPY_GBP_BCO():
    params_XAU_JPY = {
              "instruments": "XAU_JPY"
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
    print(close_bid_BCO_GBP)
    print(close_bid_XAU_JPY)
    print(close_ask_GBP_JPY)
    return 
XAU_JPY_GBP_BCO()
