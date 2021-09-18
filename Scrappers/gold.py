import oandapyV20
from oandapyV20 import API
import oandapyV20.endpoints.pricing as pricing
import json

api = API(access_token= "6d3f41bece536ad3f426dce6b221a936-d0dc087ffefd07412308ec16e169b685")
accountID = "101-003-9162148-001"

closeoutBid = []
closeoutAsk = []
time = []

params = {
          "instruments": "XAU_JPY"
        }

r = pricing.PricingStream(accountID=accountID, params=params)
rv = api.request(r)
for ticks in rv:
    time.append(ticks['time'])
    closeoutBid.append(ticks['closeoutBid'])
    closeoutAsk.append(ticks['clouseoutAsk'])



