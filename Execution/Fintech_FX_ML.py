#!/usr/bin/python3.6
from oandapyV20.contrib.requests import TakeProfitDetails, StopLossDetails
from oandapyV20.contrib.requests import MarketOrderRequest
import oandapyV20.endpoints.pricing as pricing
import oandapyV20.endpoints.orders as order
from oandapyV20 import API
import datetime
import time
import requests
import json
import threading
import telebot
from Credentials import *
from ml_model import *
############################Access MySQL Database#########################
url = 'https://owuq9doad0.execute-api.ap-southeast-1.amazonaws.com/ShopPal_Telebot_Agent/'
def query(type, statement):
    #print(statement, flush = True)
    param = {"statusCode": 200,\
    "Body":{\
    "type" : type,\
    "statement" : statement}}
    if(type == "select"):
        x = requests.post(url, data = json.dumps(param))
        statusCode = x.status_code
        if(str(statusCode) != '200'):
            print(x.text)
            return False
        lst = json.loads(x.text)["body"]
        lst = json.loads(lst)
        return lst
    if(type == "other"):
        y = requests.post(url, data = json.dumps(param))
        statusCode = y.status_code
        if(str(statusCode) != '200'):
            return "False"
        return "True"
    return "False";
############################Account Set Up################################
accountID=oanda_acc_id
token=oanda_token
api=API(access_token=token,environment="practice")
chat_id = tele_chat_id
bot = telebot.TeleBot(bot_token)
currencyList =  ['GBP/JPY']
pipRatio = 0.01
###########################End of set up##################################
def getCurrencyValue(rv): ##Return the price of currency(as average of bid and ask)
    return round((getAskPrice(rv) + getBidPrice(rv))/2,3)

def getAskPrice(rv): ##Get ask price
    return float((((rv["prices"][0])["asks"])[0])["price"])

def getBidPrice(rv):  ##Get bid price
    return float((((rv["prices"][0])["bids"])[0])["price"])

def requestRate():  ##Request parameters from Oanda
    r = pricing.PricingInfo(accountID=accountID, params=params)
    rv = api.request(r)
    return rv

def currencyConcate(currencies):  ##Concatenate currencies from array to a format that Oanda can read
    param = ""
    for currency in currencies:
        param = param + currency + ","
    return param[0:len(param)-1]
    
def createBuyOrder(instru, unit, tp, sl): ##Creating a buy(or long) order
    takeProfit = TakeProfitDetails(tp).data
    stopLoss = StopLossDetails(sl).data
    data = MarketOrderRequest(instrument = instru, units = unit,
           takeProfitOnFill = takeProfit, stopLossOnFill = stopLoss).data
    o = order.OrderCreate(accountID, data)
    api.request(o)

def createSellOrder(instru, unit, tp, sl): ##Creating a sell(or short) order
    takeProfit = TakeProfitDetails(tp).data
    stopLoss = StopLossDetails(sl).data
    data = MarketOrderRequest(instrument = instru, units = -unit,
           takeProfitOnFill = takeProfit, stopLossOnFill = stopLoss).data
    o = order.OrderCreate(accountID, data)
    api.request(o)

def fintech_fx():
    ##Method body
    signal = createSignal()
    if signal.execute:
        if signal.unit > 0:
            createBuyOrder(signal.instru, signal.unit, signal.tp, signal.sl)
        if signal.unit < 0:
            createSellOrder(signal.instru, signal.unit, signal.tp, signal.sl)

###########Initialize variables.....###########
params ={"instruments": currencyConcate(currencyList)}
rv = requestRate()
print(rv)
##########Here we go!!##############
print("Success!",flush = True)
bot.send_message(chat_id, "Launched")
#fintech_fx()

while True:
    try:
        fintech_fx()
    
    
