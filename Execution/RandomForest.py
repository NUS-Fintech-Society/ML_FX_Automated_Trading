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
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier


class RandomForest:
    model = None
    accuracy = None
    columns = None
    
    def __init__(self):
        self.start_training()
        pass

    def calculate_label(self, arr, pip, pip_ratio):
        pivot = arr[0]
        result = []
        for i in range(len(arr)):
            current_value = arr[i]
            if not current_value:
                continue
            for j in range(i, len(arr)):
                compare_value = arr[j]
                if not compare_value:
                    continue
                if (current_value - compare_value) != 0 and abs(current_value - compare_value)/pip_ratio > pip:
                    result.append( -pip * (current_value - compare_value)/abs(current_value-compare_value))
                    break
        result = result + [0] * (len(arr) - len(result))
        return result

    def fetch(self, MYSQL_QUERY):
        MYSQL_CONNECTOR_URL = 'https://e6hx5erhc6.execute-api.ap-southeast-1.amazonaws.com/Fintech/fintech'  
        payload = {
          'statement': MYSQL_QUERY,
          'type': 'query'
        }
        response = requests.post(MYSQL_CONNECTOR_URL, data=json.dumps(payload))
        data = json.loads(response.json()['body'])
        json_data = data['result']
        json_data_columns = data['columns']
        target_feature_index = json_data_columns.index("GBP_JPY")  ##Getting index of GBP JPY
        json_data = list(map(list, zip(*json_data)))   ##Transpose matrix
        GBP_JPY = json_data[target_feature_index]   ##get GBP_JPY values
        t = self.calculate_label(GBP_JPY, 20, 0.01)   ##Get labels
        json_data.insert(target_feature_index, t)
        json_data_columns.insert(target_feature_index, "GBP_JPY_Labels")
        json_data = list(map(list, zip(*json_data))) ##Transpose matrix back
        df = pd.DataFrame(json_data)
        df.columns = json_data_columns
        return df.dropna()

    def universal_fetch(self):
        MYSQL_CONNECTOR_URL = 'https://e6hx5erhc6.execute-api.ap-southeast-1.amazonaws.com/Fintech/fintech'  
        payload = {
          'statement': self.arr_to_statement(self.columns),
          'type': 'query'
        }
        response = requests.post(MYSQL_CONNECTOR_URL, data=json.dumps(payload))
        data = json.loads(response.json()['body'])
        json_data = data['result']
        return json_data

    def start_training(self):
        df = self.fetch('SELECT * FROM dataframe where dayofweek(timestamp) <= 5 limit 3000')
        df = df[df["GBP_JPY_Labels"] != 0]
        df['GBP_JPY_Labels'] = df['GBP_JPY_Labels'].map({20.0:1,-20.0:-1,0.0:0})
        x_df = df.drop(['GBP_JPY_Labels', 'timestamp', 'item_index'], axis=1)
        y_df = df['GBP_JPY_Labels']
        X_train, X_test, y_train, y_test = train_test_split(x_df, y_df, random_state=1)
        stdScaler = StandardScaler()
        X_train = stdScaler.fit_transform(X_train)
        X_test = stdScaler.transform(X_test)
        rf = RandomForestClassifier(max_depth=5, n_estimators=10)
        rf.fit(X_train,y_train)
        rf_pred_class = rf.predict(X_test)
        accuracy = metrics.accuracy_score(y_test, rf_pred_class)
        self.accuracy = accuracy
        self.model = rf
        self.columns = x_df.columns.to_numpy()
        
    def predict(self, x):
        prediction = self.model.predict(x)
        probability = self.model.predict_proba(x)
        return prediction, probability

    def arr_to_statement(self, arr):
        s = ''
        for a in arr:
            s = s + a + ", "
        s = s[:-2]
        return "select " + s + " from dataframe order by timestamp desc limit 1"

    def produce_signal(self, currency_value, currency_name):
        latest_values = self.universal_fetch()
        target_currency_index = list(self.columns).index(currency_name)
        currency_compare_value = latest_values[0][target_currency_index]
        prediction = list(self.model.predict(latest_values))[0]
        prediction_proba = max(list(self.model.predict_proba(latest_values)[0]))
        return (currency_compare_value - currency_value), prediction, prediction_proba
        

