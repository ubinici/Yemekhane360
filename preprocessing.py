import requests
from bs4 import BeautifulSoup
import json
import re

# Send a GET request to the website
response = requests.get("https://yemekhane.boun.edu.tr/aylik-menu/2023-06")
# Parse the content of the request with BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')
menu = {}
days = soup.find_all('div', class_="item")

# Function to scrape the ingredients of each dish
def get_ingredients(url):
    try:
        # Send a GET request to the url
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        print(f"Bir hata oluştu: {e}")
        return ["Bileşen bilgisi bulunamadı."]

    # Parse the content of the request with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    ingredients_section = soup.find('div', class_='field-name-field-i-indekiler2')
    if ingredients_section is not None:
        return format_ingredients(ingredients_section)
    else:
        return ["Bileşen bilgisi bulunamadı."]


# Function to format ingredients in the required format
def format_ingredients(ingredients_section):
    ingredient_divs = ingredients_section.find_all('div', class_='field-item')
    ingredients = [div.text.strip() for div in ingredient_divs]
    pattern = re.compile('İçindeki\\s*Malzemeler\\s*\\(\\s*Çiğ\\s*\\)')
    pattern2 = re.compile('\d*\s*gr.?|\d*\.\d*\s*g\s*r.?|\\s*\\d/\\d*|demet|dmt')
    result = []
    for i in ingredients:
        i = re.sub(pattern, "", i)
        if i := re.sub(pattern2, "", i):
            result.append(i.strip())

    return result

# Iterating over each day in the menu
for day in days:
    date = day.find('span', class_='date-display-single').text.strip()
    date = date.split(' ')[0] + ' 06'

    meal_times = day.find_all('div', class_='views-field views-field-field-yemek-saati')

    # Iterating over each meal time
    for meal_time in meal_times:
        meal_name = meal_time.text.strip()
        meal = {}
        categories = [('ccorba', 'Çorba'), ('anaa-yemek', 'Ana Yemek'), ('vejetarien', 'Vegan Yemek'), ('yardimciyemek', 'Yan Yemek'), ('aperatiff', 'Seçmeliler')]
        base_url = 'https://yemekhane.boun.edu.tr'

        # Iterating over each category of food
        for cat, cat_name in categories:
            cat_div = day.find('div', class_=f'views-field views-field-field-{cat}')
            items = cat_div.find_all('a')

            meal[cat_name] = []

            # Iterating over each item in the category
            for item in items:
                item_name = item.text.strip()
                url_suffix = item['href']
                item_url = f"{base_url}{url_suffix}"
                ingredients = get_ingredients(item_url)

                meal[cat_name].append({
                    'name': item_name,
                    'ingredients': ingredients
                })

        if date not in menu:
            menu[date] = {}
        menu[date][meal_name] = meal

# Write the scraped data into a JSON file
with open('menu.json', 'w', encoding='utf-8') as f:
    json.dump(menu, f, ensure_ascii=False, indent=4)
