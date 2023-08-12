from bs4 import BeautifulSoup
from selenium import webdriver
import time
import requests
import json
from concurrent.futures import ThreadPoolExecutor

def scrape_tool(tool_url):
    r = requests.get(tool_url)
    soup = BeautifulSoup(r.content, 'html.parser')
    
    # Extract tool details and return the data

driver = webdriver.Chrome()
driver.get("https://aitoptools.com")

scroll_pause_time = 2
tools_per_batch = 10

scraped_data = []
scraped_tool_urls = set()

# Collect all tool URLs first
all_tool_urls = []
while len(all_tool_urls) < tools_per_batch:
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")
    tools_in_view = soup.find_all('div', class_="elementor elementor-43")
    
    for tool in tools_in_view:
        tool_link = tool.find('a', href=True)['href']
        if tool_link not in scraped_tool_urls:
            all_tool_urls.append(tool_link)
            scraped_tool_urls.add(tool_link)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(scroll_pause_time)

# Scrape tool details using ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=10) as executor:
    for tool_data in executor.map(scrape_tool, all_tool_urls):
        scraped_data.append(tool_data)

# Save the scraped_data to a JSON file
with open("data.json", 'w') as json_file:
    json.dump(scraped_data, json_file)

driver.quit()
