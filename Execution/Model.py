import pandas as pd
import numpy as np
import requests
import json


class Model:
    model = None
    accuracy = None
    columns = None
    df = None
    stdScaler = None
    
    def __init__(self):
        pass

    def universal_fetch(self):
        MYSQL_CONNECTOR_URL = 'https://e6hx5erhc6.execute-api.ap-southeast-1.amazonaws.com/Fintech/fintech'  
        payload = {
          'statement': self.arr_to_statement(self.columns),
          'type': 'query'
        }
        response = requests.post(MYSQL_CONNECTOR_URL, data=json.dumps(payload))
        data = json.loads(response.json()['body'])
        json_data = data['result']
        json_data[0] = [0 if pd.isna(x)  else x for x in json_data[0]]
        return json_data
    
    def arr_to_statement(self, arr):
        s = ''
        for a in arr:
            s = s + a + ", "
        s = s[:-2]
        return "select " + s + " from dataframe order by timestamp desc limit 1"

    def make_df(self, latest_values, columns):
        df = pd.DataFrame(latest_values)
        df.columns = columns
        return df
