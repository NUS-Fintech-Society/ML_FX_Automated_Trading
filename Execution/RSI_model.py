import pandas as pd
import numpy as np
import requests
import json
from Model import Model

from Training_DF import get_df

class RSI(Model):
    def __init__(self, df):
        Model.__init__(self)
        self.df = df.copy(deep = True)
        self.RSI = list()
        self.prices = self.df['GBP_JPY'].to_list()
        
        self.lastestUp = None
        self.lastestDown = None
        self.latestPx = None
        
        self.initiate(self.df)
        
    def initiate(self,df):
        avgGain, avgLoss = self.avg_gain_loss()
        self.RSI = self.calc_RSI(avgGain, avgLoss)
        print("RSI Model initialised")
        
    def avg_gain_loss(self):
        duration = 14
        i = 0
        j = 0
        up = list()
        down = list()
        avgGain = list()
        avgLoss = list()
        lastPx = None

        while i < len(self.df):
            if i == 0:
                up.append(0)
                down.append(0)
                lastPx = self.prices[i]
                currPx = self.prices[i]
            else:
                currPx = self.prices[i]
                diff = currPx - lastPx
                if diff > 0:
                    up.append(diff)
                    down.append(0)
                elif diff < 0:
                    up.append(0)
                    down.append(diff)
                else:
                    up.append(0)
                    down.append(0)
                    
            i += 1
            lastPx = currPx

        # keep the last 14 elements in the list and store it
        self.latestUp = up[-14:]
        self.latestDown = down[-14:]
        self.latestPx = lastPx

        while j < len(self.df):
            if j < duration:
                avgGain.append(0)
                avgLoss.append(0)
            else:
                sum_gain = 0
                sum_loss = 0
                count = j - duration
                while count <= j:
                    sum_gain += up[count]
                    sum_loss += down[count]
                    count += 1
                avgGain.append(sum_gain/duration)
                avgLoss.append(abs(sum_loss/duration))
            
            j += 1

        return avgGain, avgLoss

    def calc_RSI(self, avgGain, avgLoss):
        RSI = list()
        duration = 14
        i = 0

        while i < len(avgGain):
            if i < duration:
                RSI.append(0)
            else:
                RS_value = avgGain[i] / avgLoss[i]
                RSI.append(100 - (100/(1+RS_value)))
            i += 1
            
        return RSI

    def update(self, currencyValue):
        duration = 14
        diff = currencyValue - self.latestPx
        self.latestUp.pop(0)
        self.latestDown.pop(0)
        
        if diff > 0:
            self.latestUp.append(diff)
            self.latestDown.append(0)
        else:
            self.latestUp.append(0)
            self.latestDown.append(diff)

        avgGain = sum(self.latestUp)/duration
        avgLoss = abs(sum(self.latestDown)/duration)

        RS_value = avgGain / avgLoss

        # Ensure that list is not too long
        if len(self.RSI) > 60:
            self.RSI = self.RSI[-60:]
            
        self.RSI.append(100-(100/(1+RS_value)))
        return self.produceSignal()

    def produceSignal(self):
        if self.RSI[-1] < 30:
            return "Buy"
        elif self.RSI[-1] > 70:
            return "Sell"
        else:
            return "Hold"
           
##a = RSI(get_df(100))
##print("### Test 1 ###")
##print(f"Latest RSI: {a.RSI[-1]}")
##print("Add Price: 149.95")
##signal = a.update(149.95)
##print("Signal: ", signal)




            
