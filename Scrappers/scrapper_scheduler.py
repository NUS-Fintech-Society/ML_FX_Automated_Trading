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
    schedule.every(20).seconds.do(processes)
    while True:
        if datetime.datetime.today().weekday() <= 4:
            schedule.run_pending()
        time.sleep(1)

def DTF():
    body = {
      "signal": 0
    }
    resp = requests.post("https://e6hx5erhc6.execute-api.ap-southeast-1.amazonaws.com/Fintech/dtl", json = body)

def error_notifier(chat_id, name, e):
    try:
        bot.send_message(chat_id, name + "Scrapper has encountered an error: " + str(e))
    except:
        print("Unable to send telebot message")
        
def processes():
    try:
        scrapper_sq()
    except Exception as e:
        error_notifier("497602206", "SQ", e)
        logging.debug("Scrapping failed at " + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ", with message\n" + str(e))
        
    try:
        scrapper_jx()
    except Exception as e:
        error_notifier("497602206", "JX", e)
        logging.debug("Scrapping failed at " + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ", with message\n" + str(e))
        
    try:
        scrapper_hp()
    except Exception as e:
        error_notifier("497602206", "HP", e)
        logging.debug("Scrapping failed at " + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ", with message\n" + str(e))
        
    try:
        scrapper_gg()
    except Exception as e:
        error_notifier("497602206", "GG", e)
        logging.debug("Scrapping failed at " + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ", with message\n" + str(e))
        
    DTF()

#processes()
#DTF()
bot.send_message("497602206", "Scrappers launched")
scrapper_scheduler()
