from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import mysql.connector
from mysql.connector import Error
import requests
import json
import time

def gather_items():
    options = webdriver.ChromeOptions() 
    #options.add_argument("--headless") # set headless mode, so it doesn't appear
    options.add_argument("--window-size=1920x1080")  # Set browser window size to standard resolution
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    driver = webdriver.Chrome(options=options)

    url = "https://theordinary.com/en-gb/category/skincare/skincare-products" 
    driver.get(url)
    items = []

    try:
        #time.sleep(10)
        div = driver.find_element(By.CSS_SELECTOR, 'div[itemid="#product"]')
        print("Div found:")
        
        all_children = div.find_elements(By.CSS_SELECTOR, 'div[class="product"]')

        name = ""
        stars = 0
        reviewNum = 0
        price = 0
        href = ""
        image = ""

        print("All children found")

        for element in all_children:
            driver.execute_script("arguments[0].scrollIntoView(true);", element)
            # Get Name and Price data
            price_element = element.find_element(By.CSS_SELECTOR, 'span[class="value"]')
            price = float(price_element.get_attribute("content"))

            name_element = element.find_element(By.CSS_SELECTOR, 'a.link.product-link')
            name = name_element.text

            # Get size
            size_element = element.find_elements(By.CSS_SELECTOR, 'span.size-value')[0]
            size = size_element.get_attribute('data-attr-value')

            # Get rating Data
            review_elem = element.find_element(By.CSS_SELECTOR, 'a.bv_main_container.bv_hover.bv_inline_rating_container_left')
            label = review_elem.get_attribute('aria-label')
            label = label.split()
            stars = float(label[0])
            reviewNum = int(label[-2])

            # Get href
            href_element = element.find_element(By.CSS_SELECTOR, 'a.bv_main_container')
            href = href_element.get_attribute('href')

            image_element = element.find_element(By.CSS_SELECTOR, 'source[media="(min-width: 1024px)"]')
            srcset = image_element.get_attribute('data-srcset')
            image_split = srcset.split()
            image = image_split[0]

            name = f"The Ordinary {name} {size}"
            
            items.append((name, price, stars, reviewNum, href, "The Ordinary", image))
            #items.append((name, price, stars, reviewNum, link, "Boots", image_data))
    except Exception as e:
        print("An error occurred:", e)

    # Close the WebDriver
    driver.quit()
    if items == []:
        return None
    else:
        return items