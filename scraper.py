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
    time.sleep(5)
    SCROLL_PAUSE_TIME = 3  
   
    try:
        with open('last_scroll_position.txt', 'r') as f:
            last_scroll_position = int(f.read())
    except FileNotFoundError:
        last_scroll_position = 0
    
    last_height = driver.execute_script("return document.body.scrollHeight")
    wholelist=[]   

    while True:       
        driver.execute_script(f'window.scrollTo({last_scroll_position}, document.body.scrollHeight)')
        time.sleep(SCROLL_PAUSE_TIME) 

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")
        toollist = soup.find_all('div', class_="elementor elementor-43")
        
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
            
            wholelist.append(data)
            filename = os.path.basename(imgSrc)
            save_path = os.path.join("Images", filename)
            download_image(imgSrc, save_path)
        with open("data.json", 'w') as json_file:
            json.dump(wholelist, json_file)

            new_height = driver.execute_script("return document.body.scrollHeight")   
            print(new_height)
            if new_height == last_height:     
                break       
            last_height = new_height
            last_scroll_position= new_height

            with open('last_scroll_position.txt', 'w') as f:
                f.write(str(last_scroll_position))
   

except exceptions.WebDriverException as e:
    print("Error", str(e))

finally:
    driver.quit()

