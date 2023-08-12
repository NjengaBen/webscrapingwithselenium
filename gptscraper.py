import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import selenium.common.exceptions as exceptions
import requests
from bs4 import BeautifulSoup
import json
import os

def tool_data(tool):
    data={}
    data["Name"] = tool.find('h2', class_="elementor-heading-title elementor-size-default").text.strip()
    try:
        price = tool.find('div', attrs={"data-id":"600e028"})
        data["Price"]=price.find('div', class_="jet-listing-dynamic-field__content").text.strip()
    except:
        data["Price"]=None
    try:
        category_div= tool.find('div', attrs={"data-id":"e33aa69"})
        data["Category"] = category_div.find('div', class_="jet-listing-dynamic-field__content").text.strip()
    except:
        data["category"] = None
    download =tool.find("div", attrs={"data-id":"a27d6a1"})
    data["Downloads"]=download.find('div', class_="jet-listing-dynamic-field__content").text.strip()
    # data["Website"]=tool.find('a', href=True)['href']
    data["Review"]=tool.find('div', class_='elementor-star-rating__title').text.strip("()")
    data["Rating"]=tool.find('div', class_='elementor-star-rating').span.text.strip()
    # data["Tags"]=tool.find('div', attrs={"data-id":"d100745"})
    # data["Features"]=tool.find('div', attrs={"data-id":"5217d73"})
    # data["ImgSrc"]=tool.find('div', class_='jet-listing jet-listing-dynamic-image').img['data-src']
    # data["Desc"]=tool.find_all('p')[2].text.strip()
    return tool_data

driver = webdriver.Chrome()
driver.get("https://aitoptools.com/")

scroll_pause_time = 2
tools_per_batch = 10  # Number of tools to scrape in each batch

scraped_data = []
batch_count = 0

while True:
    batch_count += 1
    tools_in_view = driver.find_elements(By.CLASS_NAME, "elementor elementor-43")

    for tool_element in tools_in_view:
        tool_data = tool_data(BeautifulSoup(tool_element.get_attribute("outerHTML"), "html.parser"))
        scraped_data.append(tool_data)

    if batch_count >= tools_per_batch:
        break

    driver.execute_script("arguments[0].scrollIntoView();", tools_in_view[-1])
    time.sleep(scroll_pause_time)

# At this point, scraped_data contains the data from the first batch of tools

# Now, let's scroll for the next batch of tools
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(scroll_pause_time)

# Reset batch_count for the next batch
batch_count = 0

# Continue the process for the next batch of tools...

driver.quit()
