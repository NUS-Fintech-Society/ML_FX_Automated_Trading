from Scrapper_GG import scrapper_gg
from Scrapper_HP import scrapper_hp
from Scrapper_JX import scrapper_jx
from Scrapper_SQ import scrapper_sq
import time
import schedule

def scrapper_scheduler():
    processes()
    ##schedule.every(10).seconds.do(processes)
    ##while True:
    ##    schedule.run_pending()
    ##    time.sleep(1)

def processes():
    scrapper_sq()
    scrapper_jx()
    scrapper_hp()
    scrapper_gg()
    ##Add scrapper methods from here onwards

scrapper_scheduler()
