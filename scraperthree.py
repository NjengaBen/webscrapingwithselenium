import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import selenium.common.exceptions as exceptions
import requests
from bs4 import BeautifulSoup
import json
import os

def download_image(url, save_path):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
    else:
        print(f"Failed to download image from {url}")

if not os.path.exists("Images2"):
    os.mkdir("Images2")

website = "https://aitoptools.com"


driver = webdriver.Chrome()
driver.get(website)
time.sleep(3)
SCROLL_PAUSE_TIME = 2 
# popup_iframe = driver.find_element(By.CLASS_NAME, "edialog-widget dialog-lightbox-widget dialog-type-buttons dialog-type-lightbox elementor-popup-modal")
# driver.switch_to.frame(popup_iframe)
# close_button = driver.find_element(By.CLASS_NAME, "eicon-close")
# close_button.click()
# driver.switch_to.default_content() 
last_height = driver.execute_script("return document.body.scrollHeight")

while True:                 
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
    time.sleep(SCROLL_PAUSE_TIME) 

    new_height = driver.execute_script("return document.body.scrollHeight")
    print(new_height)
    if new_height >= 150000:     
        break       
    last_height = new_height
    
page_source = driver.page_source
soup = BeautifulSoup(page_source, "html.parser")
toollist = soup.find_all('div', class_="elementor elementor-43")

wholelist=[]
toollink = []
toollink1=[]    


for tool in toollist:
    name = tool.find('h2', class_="elementor-heading-title elementor-size-default").text.strip()
    try:
        price_div= tool.find('div', attrs={"data-id":"600e028"})
        price = price_div.find('div', class_="jet-listing-dynamic-field__content").text.strip()
    except:
        price = None        
    try:
        category_div= tool.find('div', attrs={"data-id":"e33aa69"})
        category = category_div.find('div', class_="jet-listing-dynamic-field__content").text.strip()
    except:
        category = None        
    download_div=tool.find("div", attrs={"data-id":"a27d6a1"})
    download = download_div.find('div', class_="jet-listing-dynamic-field__content").text.strip()
    reviews = tool.find('div', class_='elementor-star-rating__title').text.strip("()")
    ratings = tool.find('div', class_='elementor-star-rating').span.text.strip()
                
    tags = []        
    tags_div = tool.find('div', attrs={"data-id":"5e0b612"})    
    tags_links = tags_div.find_all('a', class_='jet-listing-dynamic-terms__link')
    tags = [link.text for link in tags_links] 
    Description=tool.find('div', attrs={"data-id":"42010bf"})
    Desc = Description.find('div', class_="jet-listing-dynamic-field__content").text 
          
    img_element = tool.find('div', attrs={"data-id":"4771aec"}).img
    if img_element:
        Imgsrc = img_element.get('data-src') or img_element.get('src')
    else:
        Imgsrc = None
    
    
    scraped_data = {
        "Name": name,
        "price": price,
        "Category":category,
        "Download":download,
        "Reviews": reviews,
        "Ratings": ratings,
        "Tags": tags,
        "Imgsrc": Imgsrc,
        "Desc": Desc
    }
    wholelist.append(scraped_data)
    try:    
        filename = os.path.basename(Imgsrc)
        save_path = os.path.join("Images2", filename)
        download_image(Imgsrc, save_path)
    except:
        pass 
          
    
with open("data2.json", 'w') as json_file:
    json.dump(wholelist, json_file)
# print(wholelist) 

driver.quit()

