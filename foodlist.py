import json 
foods = {}

def isVegetarian(food):
    return True
def glutenFree(food):
    return True
def foodbase():
    meat_keywords = ["Dana", "Et", "Eti", "Kıyma", "Kuzu", "Tavuk", "Fileto", "Balık", ]
    vegan_keywords = ["Yumurta", "Tereyağı", "Yoğurt", "Süt", "Dana", "Et", "Eti", "Kıyma", "Kuzu", "Tavuk", "Fileto", "Balık", "Peynir"]
    gluten_keywords = ["Pirinç", "Makarna", "Erişte", "Kadayıf", "Şehriye", "Bulgur", "Kuskus", "Mantı", "Yufka", "Un", "Makarna"]
    global list_ingredients
    list_ingredients = []
    with open('menu.json', 'r', encoding='utf-8') as f:
        menu = json.load(f)
    for day in menu.keys():
        # Loop through each meal in the day
        for meal_type in ['Öğle Yemeği', 'Akşam Yemeği']:
            for type, meal in menu[day][meal_type].items():
                for dish in meal:
                    #print(menu[day][meal_type].keys())
                    name = dish['name']
                    ingredients = dish['ingredients']
                    if name not in foods:
                        foods[name] = {
                            "type": type,
                            "ingredients": ingredients,
                            "vegan": not any(
                                s
                                for s in ingredients
                                if any(xs in s for xs in vegan_keywords)
                            ),
                            "vegetarian": not any(
                                s
                                for s in ingredients
                                if any(xs in s for xs in meat_keywords)
                            ),
                            "gluten_free": not any(
                                s
                                for s in ingredients
                                if any(xs in s for xs in gluten_keywords)
                            ),
                            "total_score": 0,
                            "total_rated": 0,
                        }
                    for i in range(len(ingredients)):
                        list_ingredients.append(ingredients[i]) if ingredients not in list_ingredients else None
    list_ingredients = set(list_ingredients)

    with open('foodlist.json', 'w', encoding='utf-8') as f:
        json.dump(foods, f, ensure_ascii=False, indent=4)
        
foodbase()