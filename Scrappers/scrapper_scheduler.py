from scrapper_template import *
from XAU_JPY_GBP_BCO import *
from scrapper_template_gg import *
import time
import schedule

def scrapper_scheduler():
    processes()
    ##schedule.every(10).seconds.do(processes)
    ##while True:
    ##    schedule.run_pending()
    ##    time.sleep(1)

def processes():
    scrapper_template()
    scrapper_template_gg()
    
    ##Add scrapper methods from here onwards

scrapper_scheduler()
