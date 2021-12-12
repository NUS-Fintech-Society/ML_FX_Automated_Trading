import pandas as pd
import numpy as np
import requests
import json
from pandas.api.types import is_numeric_dtype

def fetch(MYSQL_QUERY):
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
    t = calculate_label(GBP_JPY, 20, 0.01)   ##Get labels
    json_data.insert(target_feature_index, t)
    json_data_columns.insert(target_feature_index, "GBP_JPY_Labels")
    json_data = list(map(list, zip(*json_data))) ##Transpose matrix back
    df = pd.DataFrame(json_data)
    df.columns = json_data_columns
    df = df.dropna(axis=1, how='all') ##Drop columns with all NA values
    return df.apply(lambda x: 0 if x.isnull().all() else x.fillna(x.mean()) if is_numeric_dtype(x) else x.fillna(x.mode().iloc[0]))

def calculate_label(arr, pip, pip_ratio):
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

def get_df(size):
    df = fetch('select * from (SELECT * FROM dataframe where dayofweek(timestamp) <= 5 order by timestamp desc limit %s) as a order by a.timestamp' % (str(size),))
    return df

