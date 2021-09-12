import requests

url = 'https://e6hx5erhc6.execute-api.ap-southeast-1.amazonaws.com/Fintech/fintech_data_pipe'

##
def scrapper_template():
    body = scrap_data()
    print(body)
    resp = requests.post(url, json = body)
    print(resp.text)

def scrap_data():
    ##Scrapping function
    return {"values": {"interest_cn":0.02, "interest_aus":0.03}} ##example output format

