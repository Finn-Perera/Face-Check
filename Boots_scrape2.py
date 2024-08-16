from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC7
import mysql.connector
from mysql.connector import Error


options = webdriver.ChromeOptions() 
options.add_argument("--headless") # set headless mode
options.add_argument("--window-size=1920x1080")  # Set browser window size to standard resolution
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
driver = webdriver.Chrome(options=options)

url = "https://www.boots.com/beauty/skincare/skincare-all-skincare" 
driver.get(url)

#search_box = driver.find_element(By.CSS_SELECTOR, "input.cdx-text-input__input") 
#search_box.click() 
#search_box.send_keys("CSS Baltic")

#try: 
	# wait for 10 seconds for content to load. 
#	search_suggestions = WebDriverWait(driver, 10).until( 
#		EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.cdx-menu-item__content")) 
#	) 
	# click to the first suggestion 
#	search_suggestions[0].click() 
	 
	# extract the data using same selectors as in beautiful soup. 
#	main_div = driver.find_element(By.CSS_SELECTOR, "div.mw-body-content") 
#	content_div = main_div.find_element(By.CSS_SELECTOR, "div.mw-parser-output") 
#	paragraphs = content_div.find_elements(By.TAG_NAME, "p") 
	 
	# we need the second paragraph 
#	intro = paragraphs[1].text 
	 
#	print(intro) 
#except Exception as error: 
#	print(error)

try:
    # Locate the div with the specific data-insights-index attribute
    div = driver.find_element(By.CSS_SELECTOR, 'div[data-insights-index="prod_live_products_uk"]')
    print("Div found:")
    #print(div.get_attribute('outerHTML'))  # Print the outer HTML of the div for debugging

    # Get the first child element of the div
    first_child = div.find_element(By.XPATH, './*')  # Locate the first child using XPath

    print("First child found:")
    #print(first_child.get_attribute('outerHTML'))  # Print the outer HTML of the first child for debugging

    # Find all <p> and <a> elements that are descendants of the first child (nested elements included)
    paragraphs_and_links = first_child.find_elements(By.XPATH, './/p | .//a')

    # Iterate over the found elements and print their attributes
    for element in paragraphs_and_links:
        print(f"\nTag: {element.tag_name}")
        for attribute_name in element.get_property('attributes'):
            attribute = attribute_name['name']
            value = element.get_attribute(attribute)
            print(f"{attribute}: {value}")
except Exception as e:
    print("An error occurred:", e)

# Close the WebDriver
driver.quit()


