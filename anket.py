import random
import json
def anket():
  with open('foodlist.json', 'r', encoding='utf-8') as f:
            foodlist = json.load(f)
    # Select random food from the list
  selected_food = random.choice(list(foodlist.keys()))
  if "Bileşen bilgisi bulunamadı" in foodlist[selected_food]["ingredients"]:
      print(f"Some information is missing for {selected_food}.")

      # Ask questions to fill in the missing information
      vegan = input(f"Is {selected_food} vegan? (True/False): ")
      vegetarian = input(f"Is {selected_food} vegetarian? (True/False): ")
      glutenfree = input(f"Is {selected_food} gluten free? (True/False): ")
      rating = int(input(f"Rate {selected_food} from 1 to 5: "))

    # Update the food information in the list
      foodlist[selected_food]["vegan"] = bool(vegan)
      foodlist[selected_food]["vegetarian"] = bool(vegetarian)
      foodlist[selected_food]["glutenfree"] = bool(glutenfree)
      if (0 < rating) and (rating < 10):
        foodlist[selected_food]["totalscore"] += rating
        foodlist[selected_food]["totalrated"] += 1
      

      print(f"{selected_food} has been updated with the following information:")
      print(foodlist[selected_food])
  else:
      # Select random food from the list

      # Ask user to rate the selected food
      print(foodlist[selected_food]["ingredients"])
      rating = int(input(f"Rate {selected_food} from 1 to 10: "))
      
      # Update the food's rating information
      foodlist[selected_food]["totalscore"] += rating
      foodlist[selected_food]["totalrated"] += 1

      # Print the updated information for the selected food
      print(f"{selected_food} has been updated with the following information:")
      print(foodlist[selected_food])
  with open('foodlist.json', 'w', encoding='utf-8') as f:
      json.dump(foodlist, f, ensure_ascii=False, indent=4)
while True:
  anket()