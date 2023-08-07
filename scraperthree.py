import time
from selenium import webdriver
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

if not os.path.exists("Images"):
    os.mkdir("Images")

website = "https://aitoptools.com"

try:
    driver = webdriver.Chrome()
    driver.get(website)
    time.sleep(3)
    SCROLL_PAUSE_TIME = 2  
    last_height = driver.execute_script("return document.body.scrollHeight")   

    while True:                 
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        time.sleep(SCROLL_PAUSE_TIME)                    
        new_height = driver.execute_script("return document.body.scrollHeight")   
        
        if new_height == last_height:     
            break       
        last_height = new_height

    records = []
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
        for link in tool.find_all('a', href=True):                               
            toollink.append(link['href'])
        toollink1.append(link['href'])
        for url in toollink1:
            r=requests.get(url)
            soup = BeautifulSoup(r.content, 'html.parser')       
            
            imgSrc = soup.find('div', class_='jet-listing jet-listing-dynamic-image').img['data-src'] 
        scraped_data = {
            "Name": name,
            "price": price,
            "Category":category,
            "Download":download,
            "Links":link['href'],
            "ImgSrc": imgSrc
        }
        wholelist.append(scraped_data)
              
        # wholelist.append(scraped_data)
    # with open("data_json", 'w') as json_file:
    #     json.dump(wholelist, json_file)
    print(wholelist)   
        # filename = os.path.basename(imgSrc)
        # save_path = os.path.join("Images", filename)
        # download_image(imgSrc, save_path)  

except exceptions.WebDriverException as e:
    print("Error", str(e))

finally:
    driver.quit()

