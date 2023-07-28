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

website = "https://aitoptools.com"

try:
    driver = webdriver.Chrome(options=options) 

    driver.get(website)
    time.sleep(3)
    footerElement = driver.find_element(By.CLASS_NAME, "elementor.elementor-134.elementor-location-footer")
    SCROLL_PAUSE_TIME = 2
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:    
        driver.execute_script("arguments[0].scrollIntoView();", footerElement)    
        time.sleep(SCROLL_PAUSE_TIME)    
        new_height = driver.execute_script("return document.body.scrollHeight")   
        
        if new_height == last_height:
            break
        
        last_height = new_height

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")
    responses = soup.find('div', class_='jet-listing')
    for response in responses:
        getTitles = response.find_all('h2', class_='elementor-heading-title elementor-size-default')
        for titles in getTitles:
            title = titles.text.strip()
            print(title)

except exceptions.WebDriverException as e:
    print("Error", str(e))

finally:
    driver.quit()