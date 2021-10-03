from Scrapper_GG import scrapper_gg
from Scrapper_HP import scrapper_hp
from Scrapper_JX import scrapper_jx
from Scrapper_SQ import scrapper_sq
import time
import datetime
import schedule
import requests
import logging
from telebot import types
import telebot
from Credentials import * 
bot = telebot.TeleBot(token)

logger = logging.getLogger()
logging.basicConfig(filename="logs/"+datetime.datetime.now().strftime("%Y%m%d%H%M%S")+".log",
                    format='%(asctime)s %(message)s',
                    filemode='w',
                    level=logging.DEBUG)

def scrapper_scheduler():
    schedule.every(5).minutes.do(processes)
    while True:
        schedule.run_pending()
        time.sleep(1)

def DTF():
    body = {
      "signal": 0
    }
    resp = requests.post("https://e6hx5erhc6.execute-api.ap-southeast-1.amazonaws.com/Fintech/dtl", json = body)
    
def processes():
    try:
        scrapper_sq()
        scrapper_jx()
        scrapper_hp()
        scrapper_gg()
        DTF()
        logger.info("Scrapped successfully at " + datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
    except Exception as e:
        logging.debug("Scrapping failed at " + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ", with message\n" + str(e))
        try:
            bot.send_message("497602206", "Scrapper has encountered an error: " + str(e))
        except:
            print("Unable to send telebot message")
    ##Add scrapper methods from here onwards

#processes()
#DTF()
bot.send_message("497602206", "Scrappers launched")
scrapper_scheduler()
