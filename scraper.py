import time
from selenium import webdriver
import selenium.common.exceptions as exceptions
import requests
from bs4 import BeautifulSoup

website = "https://aitoptools.com"

try:
    driver = webdriver.Chrome()
    driver.get(website)
    time.sleep(3)     

    while True: 
        last_height = driver.execute_script("return document.body.scrollHeight")          
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')                    
        new_height = driver.execute_script("return document.body.scrollHeight")   
        
        if new_height != last_height:     
            break       
        # last_height = new_height

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")
    responses = soup.find('div', class_='jet-listing')
    for response in responses:
        getTitles = response.find_all('h2', class_='elementor-heading-title elementor-size-default')
        misc = response.find_all('div', class_="jet-listing-dynamic-field__content")
        for titles, info in zip(getTitles, misc):
            datalist=[]
            title = titles.text.strip()
            for infoName in info:
                info = infoName.text.strip()
                if info == "":
                    pass
                if info == "true":
                    pass
                else:                
                    datalist.append(info)
            
            print(datalist)
        misc_key = ["Price", "Downloads", "Category", "Desc", "Data"]
        misc_dict = {key:datalist[i] for i, key in enumerate(misc_key)}
        data_dict = {
            "Tool": title,
            "Misc": misc_dict
        }

        # print(data_dict)
        

except exceptions.WebDriverException as e:
    print("Error", str(e))

finally:
    driver.quit()

    