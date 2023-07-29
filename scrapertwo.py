import time
from selenium import webdriver
import selenium.common.exceptions as exceptions
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
driver.get("https://aitoptools.com")
time.sleep(5)
while True:
    height = driver.execute_script('return document.body.scrollHeight')    
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
    new_height = driver.execute_script('return document.body.scrollHeight')
    print(new_height)
    # if height == new_height:
    #     print(new_height)
    #     break

driver.quit()