# Web scraping of car related data from carwale.com

# importing necessary libraries
import time
from selenium import webdriver
from selenium.common import ElementClickInterceptedException, StaleElementReferenceException, \
    ElementNotInteractableException
from selenium.webdriver.common.by import By
import json

car_url = 'https://www.carwale.com/maruti-suzuki-cars/fronx/'
driver = webdriver.Chrome()

driver.get(car_url)

varient_ele = driver.find_elements(by=By.XPATH, value='//*[@id="root"]/div[2]/div[1]/div[5]/div[1]/div[1]/div[1]/div[1]/section/div/div[2]/table/tbody')
for var in varient_ele:
    print(var.text)