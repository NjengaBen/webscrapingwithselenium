import time
from selenium import webdriver
import selenium.common.exceptions as exceptions
from selenium.webdriver.chrome.options import Options
import requests
from bs4 import BeautifulSoup

options = Options()
options.page_load_strategy = 'none'
options.add_argument('--ignore-certificate-errors')
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_experimental_option('detach', True)
options.add_experimental_option('useAutomationExtension', False)
# website = "http://www.google.com"

try:
    driver = webdriver.Chrome(options=options)    

    website = "https://aitoptools.com"
    driver.get(website)
    time.sleep(7)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")
    toolnames = soup.find('div', class_="jet-listing")
    for toolname in toolnames.find_all('div', class_="elementor-heading-title elementor-size-default"):
        tool = toolname.text.strip()
        print(tool)

except exceptions.WebDriverException:
    print("You need to download a new version of chromedriver")



driver.quit()