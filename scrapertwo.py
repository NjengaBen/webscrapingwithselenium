import time
from selenium import webdriver
import selenium.common.exceptions as exceptions
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup

driver = webdriver.Chrome()
driver.get("https://aitoptools.com/tool/sidekick-by-jigso")
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
section_tags = soup.find_all('section', class_='ob-is-breaking-bad')

tags = []
features = []

tags_div = soup.find('div', attrs={"data-id":"d100745"})
tags_links = tags_div.find_all('a', class_='jet-listing-dynamic-terms__link')
tags = [link.text.strip() for link in tags_links]

features_div = soup.find('div', attrs={"data-id":"5217d73"})
features_links = features_div.find_all('a', class_='jet-listing-dynamic-terms__link')
features = [link.text.strip() for link in features_links]
# if features == []:
#     features = ["No features"]
# else:
#     features = [link.text.strip() for link in features_links]

print("Tags:", tags)
print("Features:", features)


driver.quit()

