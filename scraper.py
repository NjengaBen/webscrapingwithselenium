import time
from selenium import webdriver
import selenium.common.exceptions as exceptions
import requests
from bs4 import BeautifulSoup

website = "https://aitoptools.com/"
driver = webdriver.Chrome()
driver.get(website)
time.sleep(7)
page_source = driver.page_source
soup = BeautifulSoup(page_source, "html.parser")
toolnames = soup.find('div', class_="jet-listing")
for toolname in toolnames.find_all('div', class_="elementor-heading-title elementor-size-default"):
    tool = toolname.text.strip()
    print(tool)


driver.quit()