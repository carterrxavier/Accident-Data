import pandas as pd
import numpy as np
import re
import requests 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import selenium.webdriver.support.ui as ui
import selenium.webdriver.support.expected_conditions as EC
import os
import time
import datetime

#### Selenium Webscraping Settings and configurations
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
#Using google chrome as our browser of choice, needs chromedriver installed
dir_path = os.path.dirname(os.path.realpath('chromedriver'))
chromedriver = dir_path + '/chromedriver'
os.environ['webdriver.chrome.driver'] = chromedriver


######## The data on the website will be scrapped 6 months back from today(188 days), initial scrape done 8/8/2021 ######
numdays = 60
base = datetime.datetime.today()
date_list = [base - datetime.timedelta(days=x) for x in range(numdays)]
#reverse list to get older accidents first
date_list.sort(reverse=False)

###only store after date after itterating about 30 days, here we're getting a rough estimate of month increments, 29 day increments creates list of 20 dates, easier number to work with in the next step. we're scraping 1 month at a time from the website.
date = 0
month_periods = []
for i in range(3):
    month_periods.append(str(date_list[date].year) + '-'+  str(date_list[date].month) + '-' + str(date_list[date].day))
    date += 29
    

accident_list = [] # the list in which the accident links will be stored
#looking at two indexes, look at index accidents between index 0 and index 1, then index 2 and index 3
for i in range(int(len(month_periods))-1):
    #open webscrapper
    driver = webdriver.Chrome(executable_path=chromedriver)
    #set url to month start date and end date specified in previous step
    url = f'https://app.myaccident.org/results?startDate={month_periods[i]}&endDate={month_periods[i+1]}&lat=29.410489385788157&lng=-98.47068431884783&radius=16903'
    driver.get(url)
    #Wait for page to load, timeout after 60 seconds
    ui.WebDriverWait(driver, 60).until(EC.visibility_of_all_elements_located((By.ID, 'root')))
    #to avoid possible suspicion from website, wait 5 seconds after loading before doing anything else
    time.sleep(5)
    #find url links in html
    elems = driver.find_elements_by_xpath("//a[@href]")
    for elem in elems:
        if '/accident/' in elem.get_attribute("href") and 'undefined' not in elem.get_attribute("href"):
            print('grabbing:{}'.format(elem.get_attribute("href")))
            dictionary = {'link': elem.get_attribute("href")}
            accident_list.append(dictionary)
    #close webscrapper
    driver.close()
#create list of website urls for the next step, grabbing the contents off of each page
all_links = pd.DataFrame(accident_list)
all_links.to_csv('accident_links.csv', index = False)
