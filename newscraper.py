import time
from selenium import webdriver
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

driver = webdriver.Chrome()
driver.get("https://aitoptools.com/")

scroll_pause_time = 2
tools_per_batch = 12  

scraped_data = []
batch_count = 0
scraped_tools_urls=set()

while True:
    batch_count += 1    
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")
    tools_in_view = soup.find_all('div', class_="elementor elementor-43")
    
    for tool in tools_in_view:
        tool_name = tool.find('h2', class_="elementor-heading-title elementor-size-default").text.strip()
        if tool_name in scraped_tools_urls:
            continue
        scraped_tools_urls.add(tool_name)  
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
        toollink=[]
        toollink1=[]
        for link in tool.find_all('a', href=True):               
            toollink.append(link['href'])   
        toollink1.append(link['href'])
        print("Hurray onto the next...", {len(toollink1)})
        for url in toollink1:
            r=requests.get(url)
            soup = BeautifulSoup(r.content, 'html.parser')

            website_div = soup.find('div', attrs={"data-id":"7bcc280"})
            try:
                website = website_div.find('a', href=True)['href']
            except:
                website = None
            reviews = soup.find('div', class_='elementor-star-rating__title').text.strip("()")
            ratings = soup.find('div', class_='elementor-star-rating').span.text.strip()
            
            tags = []        
            tags_div = soup.find('div', attrs={"data-id":"d100745"})
            tags_links = tags_div.find_all('a', class_='jet-listing-dynamic-terms__link')
            tags = [link.text.strip() for link in tags_links]

            features = []
            features_div = soup.find('div', attrs={"data-id":"5217d73"})
            features_links = features_div.find_all('a', class_='jet-listing-dynamic-terms__link')
            features = [link.text.strip() for link in features_links]
            
            imgSrc = soup.find('div', class_='jet-listing jet-listing-dynamic-image').img['data-src']        
            desc = soup.find_all('p')[2].text.strip()   
        
            data = {
                "Name": name,
                "Price": price,
                "Category": category,
                "Downloads": download,
                "Website": website,
                "Review": reviews,
                "Rating": ratings,
                "Tags": tags,
                "Features": features,
                "ImgSrc": imgSrc,
                "Desc":desc,            
            }
            scraped_data.append(data)
            filename = os.path.basename(imgSrc)
            save_path = os.path.join("Images", filename)
            download_image(imgSrc, save_path)
        with open("data.json", 'w') as json_file:
            json.dump(scraped_data, json_file)
           
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(scroll_pause_time)
    

    if len(scraped_tools_urls)==5108:
        break    

driver.quit()