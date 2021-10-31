import pandas as pd
import numpy as np
import requests
import json
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
import math
import itertools
from pandas.api.types import is_numeric_dtype
from sklearn.preprocessing import StandardScaler
from Model import Model
from Training_DF import get_df


class LogisticRegression_HA(Model):
    
    def __init__(self, df):
        Model.__init__(self)
        self.df = df.copy()
        self.start_training(self.df)
        pass

    def start_training(self, df):
        df = df.copy()
        df = df[df["GBP_JPY_Labels"] != 0]
        df['GBP_JPY_Labels'] = df['GBP_JPY_Labels'].map({20.0:1,-20.0:-1,0.0:0})
        x_df = df.drop(['GBP_JPY_Labels', 'timestamp', 'item_index'], axis=1)
        y_df = df['GBP_JPY_Labels']
        X_train, X_test, y_train, y_test = train_test_split(x_df, y_df, random_state=1)
        stdScaler = StandardScaler()
        X_train = stdScaler.fit_transform(X_train)
        X_test = stdScaler.transform(X_test)
        model = LogisticRegression()
        model.fit(X_train, y_train)
        cm = confusion_matrix(y_test, model.predict(X_test))
        accuracy = (cm[0][0] + cm[1][1])/(cm[0][0] + cm[1][0] + cm[0][1] + cm[1][1])
        self.accuracy = accuracy
        self.model = model
        self.columns = x_df.columns.to_numpy()

    def produce_signal(self, currency_value, currency_name):
        latest_values = self.universal_fetch()
        target_currency_index = list(self.columns).index(currency_name)
        currency_compare_value = latest_values[0][target_currency_index]
        prediction = list(self.model.predict(latest_values))[0]
        prediction_proba = max(list(self.model.predict_proba(latest_values)[0]))
        return (currency_compare_value - currency_value), prediction, prediction_proba
        

