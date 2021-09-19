import bs4
import requests
from bs4 import BeautifulSoup

url = 'https://e6hx5erhc6.execute-api.ap-southeast-1.amazonaws.com/Fintech/fintech_data_pipe'


#get the website for 10 year daily brent crude oil prices
oil_web = requests.get("https://www.macrotrends.net/2480/brent-crude-oil-prices-10-year-daily-chart")
soup = BeautifulSoup(oil_web.text, "html.parser")

#prepare chart
content = soup.find_all('td')
#prepare values
AverageClosing = float(content[1].contents[0][1:])
YearOpen = float(content[2].contents[0][1:])
YearHigh = float(content[3].contents[0][1:])
YearLow = float(content[4].contents[0][1:])
YearClose = float(content[5].contents[0][1:])
AnnualChange = float(content[6].contents[0][:-1])/100

#prepare key-value dictionary
result = {"AverageClosing2021-USD": AverageClosing, "YearOpen2021-USD": YearOpen, "YearHigh2021-USD": YearHigh, "YearLow2021-USD": YearLow, "YearClose2021-USD": YearClose, "AnnualChange2021-USD": AnnualChange}

body = {
    "values": result
}
resp = requests.post(url, json = body)
print(resp.text)