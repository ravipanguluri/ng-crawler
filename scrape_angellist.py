
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd

driver = webdriver.Chrome('/Users/aidanmelvin/Downloads/chromedriver_mac_arm64/chromedriver')

driver.get('https://angel.co/startups?page=5')
