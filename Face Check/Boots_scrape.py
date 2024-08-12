from bs4 import BeautifulSoup
import requests

url = "https://www.boots.com/beauty/skincare/skincare-all-skincare"
response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')

print(soup.prettify())

items = soup.find('div', {'data_insights-index': 'prod_live_products_uk'})
if items:
    first_child = items.contents[0]
    first_data_obj_id = first_child['data-insights-object-id']
    print(first_data_obj_id)
else:
    print("not found")
