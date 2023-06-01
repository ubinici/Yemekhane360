import json 

def foodbase():
  with open('foodlist.json', 'r', encoding='utf-8') as f:
      foods = json.load(f)
  meat_keywords = ["Dana", "Et", "Eti", "Kıyma", "Kuzu", "Tavuk", "Fileto", "Balık", "But", "Bonfile", "Göğüs", "Pane", "Mezgit", "Ciğer"]
  vegan_keywords = ["Yumurta", "Tereyağı", "Yoğurt", "Süt", "Dana", "Et", "Eti", "Kıyma", "Kuzu", "Tavuk", "Fileto", "Balık", "Peynir", "yumurta" "Krema", "Kaşar"]
  gluten_keywords = ["Pirinç", "Makarna", "Erişte", "Kadayıf", "Şehriye", "Bulgur", "Kuskus", "Mantı", "Yufka", "Un", "Makarna", "Nişasta", "Mantı", "Ekmek", "Yufka", "Unu", "Galeta"]
  global listingredients
  listingredients = []
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
                  "type" : type,
                  "ingredients" : ingredients,
                  "vegan" : not(any([s for s in ingredients if any(xs in s for xs in vegan_keywords)])),
                  "vegetarian" : not(any([s for s in ingredients if any(xs in s for xs in meat_keywords)])),
                  "glutenfree" : not(any([s for s in ingredients if any(xs in s for xs in gluten_keywords)])),
                  "totalscore" : 0,
                  "totalrated" : 0,
                }
                for i in range(len(ingredients)):
                  listingredients.append(ingredients[i]) if ingredients not in listingredients else None
  listingredients = set(listingredients)
  print(listingredients)
  with open('foodlist.json', 'w', encoding='utf-8') as f:
    json.dump(foods, f, ensure_ascii=False, indent=4)
foodbase()
