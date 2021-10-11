import requests
from oandapyV20 import API
import oandapyV20.endpoints.pricing as pricing
import oandapyV20.endpoints.orders as orders
import oandapyV20.endpoints.trades as trades
import oandapyV20.endpoints.accounts as accounts
from Credentials import *
from prettytable import PrettyTable
import oandapyV20.endpoints.transactions as trans


accountID=oanda_acc_id
token=oanda_token
api=API(access_token=token,environment="practice")

def requestTrades():
    r = trades.TradesList(accountID)
    r = api.request(r)
    return formatTrades(r)

def requestAccountSummary():
    r =accounts.AccountSummary(accountID)
    r = api.request(r)
    return r

def formatAccountSummary():
    rv = requestAccountSummary()
    NAV = rv["account"]["NAV"]
    openTradeCount = rv["account"]["openTradeCount"]
    profit_loss = rv["account"]["pl"]
    margin_used = rv["account"]["marginUsed"]
    margin_available = rv["account"]["marginAvailable"]
    positionValue = rv["account"]["positionValue"]
    s = '**********************************\n'
    s = s + "NAV: %s\n$" % (NAV, )
    s = s + "Trade Count: %s\n" % (openTradeCount, )
    s = s + "P/L: %s\n$" % (profit_loss, )
    s = s + "Margin Used: %s\n$" % (margin_used, )
    s = s + "Margin Available: %s\n$" % (margin_available, )
    s = s + "Position Value: %s\n$" % (positionValue, )
    return s

def formatTrades(rv):
    s= ""
    for trade in rv["trades"][:10]:
        s = s + trade["id"] + ": "  "Instrument: " +trade["instrument"] +  ", price: " + trade["price"] + ", P/L: " + trade["unrealizedPL"] + "\n"
    return s
