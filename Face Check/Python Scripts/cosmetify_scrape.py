from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
import mysql.connector
from mysql.connector import Error
import time
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException

def gather_items():
    options = webdriver.ChromeOptions() 
    #options.add_argument("--headless") # set headless mode, so it doesn't appear
    options.add_argument("--window-size=1920x1080")  # Set browser window size to standard resolution
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    driver = webdriver.Chrome(options=options)

    count = 1
    items = []
    try:
        while (count <= 5):
            url = f"https://www.cosmetify.com/skin-care/?page_no={count}" 
            driver.get(url)
            time.sleep(2)
            scrape_items(driver, items)
            count += 1
    except Exception as e:
        print("An error occurred:", e)

    # Close the WebDriver
    driver.quit()
    if items == []:
        return None
    else:
        print("Number of items: " + str(len(items)))
        return items

def scrape_items(driver, items):
    try:
        all_children = driver.find_elements(By.CSS_SELECTOR, 'div[class="items grid"]>div')
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
            price_element = element.find_element(By.CLASS_NAME, 'price')
            price_string = price_element.text.split(" ")[0]
            price = float(price_string[1:].strip())
            
            name_element = element.find_element(By.CSS_SELECTOR, 'span[class="name"]')
            name = name_element.text.strip()

            brand_element = element.find_element(By.CSS_SELECTOR, 'span[class="brand"]')
            brand = brand_element.text.strip()

            # Can't get size not sure how to work from here!
            #size_element = element.find_elements(By.CSS_SELECTOR, 'span.size-value')[0]
            #size = size_element.text
            
            # Get rating Data
            review_elem = element.find_element(By.CSS_SELECTOR, 'div.review.f.nw.ac')
            reviews_text = review_elem.find_element(By.CSS_SELECTOR, '.review>span').text.split()
            if reviews_text[0] == 'No':
                reviewNum = 0
            else:
                reviewNum = int(reviews_text[0])
            star_elem = element.find_element(By.CSS_SELECTOR, '.stars>.starRating>span')
            star_elem_style = star_elem.get_attribute("style").split()[1].split('%')[0]
            stars = round(float(star_elem_style) / 100 * 5, 2)

            # Get href
            href_element = element.find_element(By.CSS_SELECTOR, 'a')
            href = href_element.get_attribute('href')

            image_element = element.find_element(By.CSS_SELECTOR, 'img')
            image = image_element.get_attribute('src')

            name = f"{brand} {name}" # can't find size? {size}
            
            items.append((name, price, stars, reviewNum, href, "Cosmetify", image))
            #items.append((name, price, stars, reviewNum, link, "Boots", image_data))    
    except Exception as e:
        print("An error occurred:", e)