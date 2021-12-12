import pandas as pd
import numpy as np
import requests
import json
import sklearn
import sklearn.metrics as metrics
import sklearn.utils as utils
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import BaggingClassifier
from sklearn.neighbors import KNeighborsClassifier
from pandas.api.types import is_numeric_dtype
from Model import Model

from Training_DF import get_df
class Bagging(Model):
    
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
        bagging = BaggingClassifier(max_samples=0.5, max_features=0.5, base_estimator = DecisionTreeClassifier(criterion = "entropy", max_depth = 4), n_estimators = 700)
        bagging.fit(X_train,y_train)
        bagging_pred_class = bagging.predict(X_test)
        accuracy = metrics.accuracy_score(y_test, bagging_pred_class)
        self.stdScaler = stdScaler
        self.accuracy = accuracy
        self.model = bagging
        self.columns = x_df.columns.to_numpy()
        
    def predict(self, x):
        prediction = self.model.predict(x)
        probability = self.model.predict_proba(x)
        return list(self.model.predict(x))[0] , max(list(self.model.predict_proba(x)[0]))

    def produce_signal(self, currency_value, currency_name):
        latest_values = self.universal_fetch()      #Predict based on latest value
        target_currency_index = list(self.columns).index(currency_name)                   #Get latest target value index
        currency_compare_value = latest_values[0][target_currency_index]    #Get latest target value
        latest_values = self.stdScaler.transform(self.make_df(latest_values, self.columns))             #Scaling the latest values
        prediction, prediction_proba = self.predict(latest_values)
        return (currency_compare_value - currency_value), prediction, prediction_proba  ##Difference in currency value as of time at training vs live, predicted currency movement, probability of the movement
        
