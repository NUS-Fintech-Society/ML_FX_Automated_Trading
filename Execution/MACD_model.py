import pandas as pd
import numpy as np
import requests
import json
from Model import Model

from Training_DF import get_df

class MACD(Model):
    def __init__(self,df):
        Model.__init__(self)
        self.df = df.copy(deep = True)
        self.prices = self.df['GBP_JPY']
        self.shortEMA = None # 12 period EMA
        self.longEMA = None # 26 period EMA
        self.signalLine = None # 9 period EMA
        
        self.MACD = None
        self.hist = None
        self.prevAction = None
        
        self.initiate()

    def initiate(self):
        self.shortEMA = self.calcEMA(12)
        self.longEMA = self.calcEMA(26)
        self.calc_MACD()
        self.signalLine = self.calcEMA(9, True)
        print("MACD Model Initialised")

    def calcEMA(self, period, MACD = False):
        if MACD == False:
            return self.prices.ewm(span = period, adjust = False).mean().to_list()
        else:
            return pd.Series(self.MACD).ewm(span = period, adjust = False).mean().to_list()

    def calc_MACD(self):
        MACD = list()
        
        for i in range(len(self.shortEMA)):
            value = self.shortEMA[i] - self.longEMA[i]
            MACD.append(value)
            
        self.MACD = MACD

    def update(self, currencyValue):
        if len(self.prices) > 60:
            self.prices = self.prices[-60:]
            self.prices.reset_index(drop=True)
            
        self.prices = self.prices.append(pd.Series(currencyValue))
        self.shortEMA = self.calcEMA(12)
        self.longEMA = self.calcEMA(26)
        self.signalLine = self.calcEMA(9, True)        
        self.calc_MACD()
        return self.produceSignal()

    # Simple crossover strategy, if MACD crosses above signal ("Buy"), if MACD crosses below signal ("sell")
    def produceSignal(self):
        diff = self.MACD[-1] - self.signalLine[-1]
        if self.prevAction == None:
            if diff > 0:
                self.prevAction = "Buy"
                return "Buy"
            elif diff < 0:
                self.prevAction = "Sell"
                return "Sell"
            else:              
                return "Hold"
            
        elif self.prevAction == "Buy":
            if diff > 0:
                return "Hold"
            elif diff < 0:
                self.prevAction = "Sell"
                return "Sell"
            else:
                return "Hold"

        elif self.prevAction == "Sell":
            if diff > 0:
                self.prevAction = "Buy"
                return "Buy"
            elif diff < 0:
                return "Hold"
            else:
                return "Hold"
        
        
    
