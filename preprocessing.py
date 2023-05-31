import requests
from bs4 import BeautifulSoup
import json

response = requests.get("https://yemekhane.boun.edu.tr/aylik-menu/2023-06")
soup = BeautifulSoup(response.text, 'html.parser')
menu = {}
days = soup.find_all('div', class_="item")

def get_ingredients(url):
    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        print(f"Bileşen bilgisi bulunamadı: {e}")
        return ["Bileşen bilgisi bulunamadı"]

    soup = BeautifulSoup(response.text, 'html.parser')

    ingredients_section = soup.find('div', class_='field-name-field-i-indekiler2')
    if ingredients_section is not None:
        ingredient_divs = ingredients_section.find_all('div', class_='field-item')
        ingredients = [div.text.strip() for div in ingredient_divs]
        ingredients = [i for i in ingredients if i and i != 'İçindeki Malzemeler (Çiğ )']
    else:
        ingredients = ["Bileşen bilgisi bulunamadı"]

    return ingredients


for day in days:
    date = day.find('span', class_='date-display-single').text.strip()
    date = date.split(' ')[0] + ' 06'

    meal_times = day.find_all('div', class_='views-field views-field-field-yemek-saati')

    for meal_time in meal_times:
        meal_name = meal_time.text.strip()
        meal = {}
        categories = [('ccorba', 'Çorba'), ('anaa-yemek', 'Ana Yemek'), ('vejetarien', 'Vegan Yemek'), ('yardimciyemek', 'Yan Yemek'), ('aperatiff', 'Seçmeliler')]
        base_url = 'https://yemekhane.boun.edu.tr'

        for cat, cat_name in categories:
            cat_div = day.find('div', class_=f'views-field views-field-field-{cat}')
            items = cat_div.find_all('a')

            meal[cat_name] = []

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

with open('menu.json', 'w', encoding='utf-8') as f:
    json.dump(menu, f, ensure_ascii=False, indent=4)
