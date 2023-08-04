import time
from selenium import webdriver
import selenium.common.exceptions as exceptions
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup

driver = webdriver.Chrome()
driver.get("https://aitoptools.com/tool/synthesia/")
time.sleep(5)
# while True:
#     height = driver.execute_script('return document.body.scrollHeight')    
#     driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
#     new_height = driver.execute_script('return document.body.scrollHeight')
#     print(new_height)
    # if height == new_height:
    #     print(new_height)
    #     break

page_source = driver.page_source
soup = BeautifulSoup(page_source, "html.parser")
toollist = soup.find('section', class_="ob-is-breaking-bad elementor-section elementor-top-section elementor-element elementor-element-b3035da elementor-section-stretched elementor-section-boxed elementor-section-height-default elementor-section-height-default")[0]
print(toollist)


driver.quit()

