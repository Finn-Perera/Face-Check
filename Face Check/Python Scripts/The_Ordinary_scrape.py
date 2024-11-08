from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from bs4 import BeautifulSoup
import mysql.connector
from mysql.connector import Error
import requests
import json
import time

def load_all_content(driver, load_button_locator):
    maxCount = 100
    count = 0
    while count <= maxCount:
        try:
            load_more_button = driver.find_element(*load_button_locator)
            driver.execute_script("arguments[0].scrollIntoView(true);", load_more_button)
            driver.execute_script("arguments[0].click();", load_more_button)
            count += 1
            time.sleep(1)
        except NoSuchElementException:
            print("Load More button not found. Loaded all content.")
            break
        except ElementNotInteractableException:
            print("Load More button is not interactable. Loaded all content.")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            break

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
        load_all_content(driver, (By.CSS_SELECTOR, '.btn-load.more'))

        div = driver.find_element(By.CSS_SELECTOR, 'div[itemid="#product"]')
        print("Div found:")
        #print(div.get_attribute("data-total-count"))
        
        all_children = div.find_elements(By.CSS_SELECTOR, 'div[class="product-grid-item"]')
        #print(len(all_children))

        name = ""
        stars = 0
        reviewNum = 0
        price = 0
        href = ""
        image = ""
        id_set = set()
        count = 0

        print("All children found")

        for element in all_children:
            try:
                count += 1
                driver.execute_script("arguments[0].scrollIntoView(true);", element)
                # Get Name and Price data
                detail_element = element.find_element(By.CSS_SELECTOR, '.product-detail')
                if detail_element.get_attribute('data-available') != 'true' or detail_element.get_attribute('data-gtm-enhanced-ecommerce') == "null":
                    continue
                
                item_data = json.loads(detail_element.get_attribute('data-gtm-enhanced-ecommerce'))      
                
                id = str(item_data["id"])
                
                if id in id_set:
                    print("Already retrieved item")
                    continue
                else:
                    id_set.add(id)

                name = item_data["name"]
                brand = item_data["brand"]
                price = float(item_data["price"])
                size = item_data["variant"]
                
                

                # Get size
                #size_element = element.find_elements(By.CSS_SELECTOR, 'span.size-value')[0]
                #size = size_element.text
                
                # Get rating Data
                review_elem = element.find_element(By.CSS_SELECTOR, 'a.bv_main_container.bv_hover.bv_inline_rating_container_left')
                label = review_elem.get_attribute('aria-label')
                label = label.split()
                stars = float(label[0])
                reviewNum = int(label[-2])

                #Get href
                href_element = element.find_element(By.CSS_SELECTOR, 'a.bv_main_container') 
                href = href_element.get_attribute('href')

                image_element = element.find_element(By.CSS_SELECTOR, 'source[media="(min-width: 1024px)"]')
                srcset = image_element.get_attribute('data-srcset')
                image_split = srcset.split()
                image = image_split[0]
                name.strip()
                size.strip()
                name = f"{brand} {name}" # {size}
                
                items.append((name, price, stars, reviewNum, href, "The Ordinary", image))
            except Exception as e:
                print("An error occured:", e)
                print("At element: ", count)
                soup = BeautifulSoup(element.get_attribute('outerHTML'), 'html.parser')
                print(soup.prettify())
                continue
    except Exception as e:
        print("An error occurred:", e)
    
    # Close the WebDriver
    driver.quit()
    if items == []:
        return None
    else:
        print("Number of items: " + str(len(items)))
        return items