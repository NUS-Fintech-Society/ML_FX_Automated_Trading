import bs4
import requests

url = 'https://e6hx5erhc6.execute-api.ap-southeast-1.amazonaws.com/Fintech/fintech_data_pipe'


def get_data():
  # web for US Daily Treasury Real Yield Curve Rates
  web = requests.get("https://www.treasury.gov/resource-center/data-chart-center/interest-rates/Pages/TextView.aspx?data=realyield")
  soup = bs4.BeautifulSoup(web.text, "lxml")

  # locate and process data 
  last_row = soup.select(".evenrow")[-1]
  data = last_row.select('td')
  data.pop(0)
  values = [float(ele.getText()) for ele in data]

  # format into wanted data structure
  keys = ["5years", "7years", "10years", "20years", "30years"]
  result = dict(zip(keys, values))
  return result

def scrapper_template():
    body = {
      "values": get_data()
    }
    resp = requests.post(url, json = body)
    print(resp.text)
