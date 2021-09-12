from scrapper_template import *
import time
import schedule

def scrapper_scheduler():
    schedule.every(10).seconds.do(processes)
    while True:
        schedule.run_pending()
        time.sleep(1)

def processes():
    scrapper_template()
    ##Add scrapper methods from here onwards

scrapper_scheduler()
