import time
from selenium import webdriver
import selenium.common.exceptions as exceptions
import requests
from bs4 import BeautifulSoup
import json



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
        for link in tool.find_all('a', href=True):               
            toollink.append(link['href'])   
        toollink1.append(link['href'])

    for url in toollink1:
        r=requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')

        name = soup.find('h2', class_="elementor-heading-title elementor-size-default").text.strip("About ")
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
    
        misc = soup.find_all('div', class_="jet-listing-dynamic-field__content")
        datalist=[]
        for infoName in misc:
            info = infoName.text.strip()
            if info == "":
                pass
            if info == "true":
                pass
            else:
                datalist.append(info)
    
        misc_key = ["Price", "Downloads", "Category", "Desc", "Data"]
        misc_dict = {key:datalist[i] for i, key in enumerate(misc_key)}
        data = {
            "Name": name,
            "Website": url,
            "Review": reviews,
            "Rating": ratings,
            "Tags": tags,
            "Features": features,
            "ImgSrc": imgSrc,
            "Desc":desc,
            "Misc":misc_dict
        }
       
        wholelist.append(data)
    with open("data_json", 'w') as json_file:
        json.dump(wholelist, json_file)
    # print(wholelist)   
        

except exceptions.WebDriverException as e:
    print("Error", str(e))

finally:
    driver.quit()

