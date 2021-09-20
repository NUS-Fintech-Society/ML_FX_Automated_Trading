from Scrapper_GG import scrapper_gg
from Scrapper_HP import scrapper_hp
from Scrapper_JX import scrapper_jx
from Scrapper_SQ import scrapper_sq
import time
import schedule
import requests

def scrapper_scheduler():
    schedule.every(20).minutes.do(processes)
    while True:
        schedule.run_pending()
        time.sleep(1)

def DTF():
    body = {
      "signal": 0
    }
    resp = requests.post("https://e6hx5erhc6.execute-api.ap-southeast-1.amazonaws.com/Fintech/dtl", json = body)
    print(resp.text)
    
def processes():
    scrapper_sq()
    scrapper_jx()
    scrapper_hp()
    scrapper_gg()
    DTF()
    ##Add scrapper methods from here onwards

scrapper_scheduler()
#processes()
#DTF()
