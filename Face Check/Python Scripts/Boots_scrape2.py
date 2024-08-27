from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
import mysql.connector
from mysql.connector import Error
import requests

# How to do searching
#search_box = driver.find_element(By.CSS_SELECTOR, "input.cdx-text-input__input") 
#search_box.click() 
#search_box.send_keys("CSS Baltic")

#def get_img(component):
    
            # if img_url.startswith('data:image'):
            #     return img_url
            # else:
            #     try :
            #         img_data = requests.get(img_url).content
            #     except Exception as e:
            #         print("Error occured gathering img data: ", e)

            # return img_data

def gather_items():
    options = webdriver.ChromeOptions() 
    options.add_argument("--headless") # set headless mode, so it doesn't appear
    options.add_argument("--window-size=1920x1080")  # Set browser window size to standard resolution
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    driver = webdriver.Chrome(options=options)

    url = "https://www.boots.com/beauty/skincare/skincare-all-skincare" 
    driver.get(url)
    items = []
    try:
        div = driver.find_element(By.CSS_SELECTOR, 'div[data-insights-index="prod_live_products_uk"]')
        print("Div found:")
        
        all_children = div.find_elements(By.XPATH, './*')
        filtered_children = []

        for element in all_children:
            if element.get_attribute('data-productid') is not None:
                filtered_children.append(element)

        print("All children found:")

        # Find all <p>, <a>, <h3>, <img> elements that are descendants of the first child (nested elements included)
        for element in filtered_children:
            name = ""
            stars = 0
            reviewNum = 0
            hrefs = []
            text = []

            driver.execute_script("arguments[0].scrollIntoView(true);", element)


            paragraphs_and_links = element.find_elements(By.XPATH, './/p | .//a | .//h3 |.//img')
            for component in paragraphs_and_links:
                #print(f"\nTag: {component.tag_name}")
                if component.tag_name == "img" :
                    temp_src = component.get_attribute('src')
                    if temp_src.startswith('data:image/svg+xml;base64,'):
                        continue
                    image_data = temp_src

                if component.tag_name == "h3" :
                    name = component.text
                elif component.text != None:
                    text.append(component.text)
                for attribute_name in component.get_property('attributes'):
                    attribute = attribute_name['name']
                    if attribute == "href":
                        hrefs.append(component.get_attribute(attribute))

                    if attribute == "aria-label":
                        parts = component.get_attribute(attribute).split()
                        if "stars" in parts and "reviews" in parts: # gather reviews
                            stars_index = parts.index("stars") - 1
                            stars = parts[stars_index] if stars_index >= 0 else None
                            reviews_index = parts.index("reviews") - 1
                            reviewNum = parts[reviews_index] if reviews_index >= 0 else None
                    
                    value = component.get_attribute(attribute)
                    #print(f"{attribute}: {value}")
            price = text[2] # select price str
            price = price[1:] # strip £
            link = hrefs[0]
            name = name.strip()
            # ['No7 Future Renew Day Cream SPF40 50ml', '(1165)', '£34.95', '50ML | £69.90 per 100ML', '', '', '', '']
            # ['No7 HydraLuminous+ Day Gel 50ml', '(57)', '£14.36', 'Save £3.59', 'Was £17.95', '50ML | £28.72 per 100ML', '', '', '', '']
            # Can also use text here to find discounts and price per unit?
            #print(image_data)
            items.append((name, price, stars, reviewNum, link, image_data, "Boots"))
            
            #print(f"{name}\nstars: {stars} reviews {reviewNum}\nprice: {price}\nhref: {link}\n")
    except Exception as e:
        print("An error occurred:", e)

    # Close the WebDriver
    driver.quit()
    if items == []:
        return None
    else:
        return items

