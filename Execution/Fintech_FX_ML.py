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
from threading import Thread
import telebot
from Credentials import *
from RandomForest import RandomForest
from AdaBoost import AdaBoost
from Bagging import Bagging
from LogisticRegression import LogisticRegression_HA
import schedule
from Training_DF import get_df

############################Access MySQL Database#########################
MYSQL_CONNECTOR_URL = 'https://e6hx5erhc6.execute-api.ap-southeast-1.amazonaws.com/Fintech/fintech'

def query(type, statement):
    #print(statement, flush = True)
    payload = {
      'statement': statement,
      'type': type
      }
    if(type == "query"):
        response = requests.post(MYSQL_CONNECTOR_URL, data=json.dumps(payload))
        print(response.text)
        return None
        data = json.loads(response.json()['body'])
        json_data = data['result']
        return json_data
    if(type == "update"):
        response = requests.post(MYSQL_CONNECTOR_URL, data=json.dumps(payload))
        return "True"
    return "False";
############################Account Set Up################################
accountID=oanda_acc_id
token=oanda_token
api=API(access_token=token,environment="practice")
chat_id = tele_chat_id
bot = telebot.TeleBot(bot_token)
currencyList =  ['GBP_JPY']
###########################End of set up##################################

##############################Parameters################################
currency_diff_threshold = 2 ##unit is pips
accuracy_threshold_ada = 0.95
accuracy_threshold_rf = 0.95
probability_threshold = 0.90
purchase_units = 5000
interval = 20 #in seconds
#############################End of parameters#########################
##Note that the code in this file was written for multiple currency pairs as target. However, our ML model only use GBPJPY as target. 
def get_pip_ratio(currency):
    if "JPY" in str(currency):
        return 0.01
    else:
        return 0.0001
    
def getCurrencyValue(rv, currencyIndex):
    if get_pip_ratio(currencyList[currencyIndex]) == 0.01:
        return round((float((((rv["prices"][currencyIndex])["asks"])[0])["price"]) + float((((rv["prices"][currencyIndex])["bids"])[0])["price"]))/2,3)
    else:
        return round((float((((rv["prices"][currencyIndex])["asks"])[0])["price"]) + float((((rv["prices"][currencyIndex])["bids"])[0])["price"]))/2,5)

def getAskPrice(rv, currencyIndex):
    return float((((rv["prices"][currencyIndex])["asks"])[0])["price"])

def getBidPrice(rv, currencyIndex):
    return float((((rv["prices"][currencyIndex])["bids"])[0])["price"])

def requestRate():  ##Request parameters from Oanda
    r = pricing.PricingInfo(accountID=accountID, params=params)
    rv = api.request(r)
    return rv

def currencyConcate(currencies):  ##Concatenate currencies from array to a format that Oanda can read
    param = ""
    for currency in currencies:
        param = param + currency + ","
    return param[0:len(param)-1]
    
def createBuyOrder(instru, unit, tp, sl, model_name,currencyValue, pip_ratio): ##Creating a buy(or long) order
    stopLoss = currencyValue - sl * pip_ratio
    takeProfit = currencyValue + tp * pip_ratio
    takeProfit = TakeProfitDetails(takeProfit).data
    stopLoss = StopLossDetails(stopLoss).data
    data = MarketOrderRequest(instrument = instru, units = unit,
           takeProfitOnFill = takeProfit, stopLossOnFill = stopLoss).data
    o = order.OrderCreate(accountID, data)
    api.request(o)
    rsp = o.response
    print(rsp)
    upload_order(str(rsp), rsp["orderCreateTransaction"]["id"], instru, unit, 20, 20, currencyValue, model_name)


def createSellOrder(instru, unit, tp, sl, model_name,currencyValue, pip_ratio): ##Creating a sell(or short) order
    stopLoss = currencyValue + sl * pip_ratio
    takeProfit = currencyValue - tp * pip_ratio
    takeProfit = TakeProfitDetails(takeProfit).data
    stopLoss = StopLossDetails(stopLoss).data
    data = MarketOrderRequest(instrument = instru, units = -unit,
           takeProfitOnFill = takeProfit, stopLossOnFill = stopLoss).data
    o = order.OrderCreate(accountID, data)
    api.request(o)
    rsp = o.response
    upload_order(str(rsp), rsp["orderCreateTransaction"]["id"], instru, unit, 20, 20, currencyValue, model_name)

def upload_order(raw, oanda_order_id, instrument, units, take_profit, stop_loss, currency_value, model_name):
    print("inserting trade")
    statement = 'insert into trades (raw, oanda_order_id, instrument, units, take_profit, stop_loss, currency_value,  model_name) values ("%s", "%s", "%s", %s, %s, %s, %s, "%s")'
    statement = statement % (raw, oanda_order_id, instrument, units, take_profit, stop_loss, currency_value, model_name)
    query("update", statement)
    
###################Set up ML Models
df = get_df()
rf = RandomForest(df)
ada = AdaBoost(df)
bagging = Bagging(df)
lg_ha = LogisticRegression_HA(df)
def model_trainer():
    global rf
    global ada
    global bagging
    global lg_ha
    df = get_df()
    rf = RandomForest(df)
    ada = AdaBoost(df)
    bagging = Bagging(df)
    lg_ha = LogisticRegression_HA(df)
    
def model_training_scheduler():
    schedule.every(interval).seconds.do(model_trainer)
    while True:
        if datetime.datetime.today().weekday() <= 4:
            schedule.run_pending()
        time.sleep(1)
###################End 

##################Running trading algo
def fintech_fx():
    rv = requestRate()
    for i in range(len(currencyList)):
        currency = currencyList[i]
        pip_ratio = get_pip_ratio(currency)
        currencyValue = getCurrencyValue(rv, i)
        ###Random Forest
        rf_signal = rf.produce_signal(currencyValue, currency)
        rf_signal_value_diff = rf_signal[0]
        rf_prediction = rf_signal[1]
        rf_prediction_proba = rf_signal[2]
        model_accuracy = rf.accuracy
        print(rf_signal)
        if rf_signal_value_diff/pip_ratio < currency_diff_threshold and rf_prediction_proba > probability_threshold and model_accuracy > accuracy_threshold_rf:
            if rf_prediction > 0:
                ##Execute buy order
                createBuyOrder(currency, purchase_units, 20, 20, "RandomForest_V1", currencyValue, pip_ratio)
            if rf_prediction < 0:
                ##Execute sell order
                createSellOrder(currency, purchase_units, 20, 20, "RandomForest_V1", currencyValue, pip_ratio)
        ###Ada boost
        ada_signal = ada.produce_signal(currencyValue, currency)
        ada_signal_value_diff = ada_signal[0]
        ada_prediction = ada_signal[1]
        ada_prediction_proba = ada_signal[2]
        model_accuracy = ada.accuracy
        print(ada_signal)
        if ada_signal_value_diff/pip_ratio < currency_diff_threshold and ada_prediction_proba > probability_threshold and model_accuracy > accuracy_threshold_ada:
            if ada_prediction > 0:
                ##Execute buy order
                createBuyOrder(currency, purchase_units - 1, 20, 20, "AdaBoost_V1", currencyValue, pip_ratio)
            if ada_prediction < 0:
                ##Execute sell order
                createSellOrder(currency, purchase_units - 1, 20, 20, "AdaBoost_V1", currencyValue, pip_ratio)
        '''
        ###Bagging boost
        bagging_signal = bagging.produce_signal(currencyValue, currency)
        bagging_signal_value_diff = bagging_signal[0]
        bagging_prediction = bagging_signal[1]
        bagging_prediction_proba = bagging_signal[2]
        model_accuracy = bagging.accuracy
        print(bagging_signal)
        if bagging_signal_value_diff/pip_ratio < currency_diff_threshold and bagging_prediction_proba > probability_threshold and model_accuracy > accuracy_threshold_ada:
            if bagging_prediction > 0:
                ##Execute buy order
                createBuyOrder(currency, purchase_units - 1, 20, 20, "BaggingBoost_V1", currencyValue, pip_ratio)
            if bagging_prediction < 0:
                ##Execute sell order
                createSellOrder(currency, purchase_units - 1, 20, 20, "BaggingBoost_V1", currencyValue, pip_ratio)
        '''
        
        '''
        ###LG Regression
        lg_ha_signal = lg_ha.produce_signal(currencyValue, currency)
        lg_ha_signal_value_diff = lg_ha_signal[0]
        lg_ha_prediction = lg_ha_signal[1]
        lg_ha_prediction_proba = lg_ha_signal[2]
        model_accuracy = lg_ha.accuracy
        print(lg_ha_signal)
        if lg_ha_signal_value_diff/pip_ratio < currency_diff_threshold and lg_ha_prediction_proba > probability_threshold and model_accuracy > accuracy_threshold_ada: ##Follow adaboost setting
            if lg_ha_prediction > 0:
                ##Execute buy order
                createBuyOrder(currency, purchase_units + 1, 20, 20, "LogisticRegression_HA", currencyValue, pip_ratio)
                pass
            if lg_ha_prediction < 0:
                ##Execute sell order
                createSellOrder(currency, purchase_units + 1, 20, 20, "LogisticRegression_HA", currencyValue, pip_ratio)
                pass
            '''
model_mapping = {4999: "RandomForest_V1", 5000: "AdaBoost_V1", 5001: "Bagging_V1", 5002: "LogisticRegression_HA"}
##################End
    
###########Initialize variables.....###########
params ={"instruments": currencyConcate(currencyList)}
rv = requestRate()
##########Here we go!!##############
print("Launch Success!")
#bot.send_message(chat_id, "Launched")

Thread(target = model_training_scheduler).start()  ##Running model training on separate thread
while True:
    if datetime.datetime.today().weekday() <= 4:
        fintech_fx()
    time.sleep(interval + 5)
    