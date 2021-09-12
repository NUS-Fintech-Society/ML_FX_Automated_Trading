import requests

url = 'https://e6hx5erhc6.execute-api.ap-southeast-1.amazonaws.com/Fintech/fintech_data_pipe'

def scrapper_template():
    body = {
      "values": {
        "test3": 999
      }
    }
    resp = requests.post(url, json = body)
    print(resp.text)
