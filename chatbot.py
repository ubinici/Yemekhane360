from wit import Wit
from datetime import datetime, time, timedelta
import json

class Bot:
    """Bot class for interacting with wit.ai and handling different user intents"""
    def __init__(self, token):
        """Initialize the bot with a Wit.ai access token"""
        self.client = Wit(token)
        self.handlers = {
            'getMenu': self.handle_get_menu,
            'queryMeal': self.handle_query_meal,
            'getMenuForDate': self.handle_get_menu_for_date,
            'getLocation': self.handle_get_location,
            'getMealTimesForCampus': self.handle_get_meal_times_for_campus,
        }


    def get_meal_time(self):
        """Return the current meal time based on the current time of the day"""
        current_time = datetime.now().time()

        if time(7, 30) <= current_time <= time(9, 30):
            return 'kahvaltı'
        elif time(11, 30) <= current_time <= time(14, 30):
            return 'öğle yemeği'
        elif time(17, 0) <= current_time <= time(19, 0):
            return 'akşam yemeği'
        else:
            return None


    def handle_get_meal_times_for_campus(self, entities, context):
        """Handle the 'getMealTimesForCampus' intent by returning the meal times for a specific campus"""
        # Check if the campus name was provided in the entities
        if 'campus:campus' not in entities or 'value' not in entities['campus:campus'][0]:
            # If not, return an error message
            return {"text": "Kampüs bilgisi eksik veya hatalı. Lütfen tekrar deneyin."}

        # Define each campus with meal times for both weekdays and weekend
        CAMPUS_TIMES = {
                    'Kuzey': {
                        'Haftaiçi': {
                            'Kahvaltı': ['07:30', '09:30'],
                            'Öğle Yemeği': ['11:30', '14:30'],
                            'Akşam Yemeği': ['17:00', '19:00']
                        },
                        'Haftasonu': {
                            'Kahvaltı': ['08:30', '10:00'],
                            'Öğle Yemeği': ['12:00', '13:45'],
                            'Akşam Yemeği': ['17:30', '19:30']
                        }
                    },
                    'Güney': {
                        'Haftaiçi': {
                            'Kahvaltı': ['07:30', '09:30'],
                            'Öğle Yemeği': ['12:15', '14:30'],
                            'Akşam Yemeği': ['17:00', '19:00']
                        },
                        'Haftasonu': {
                            'Kahvaltı': ['08:30', '10:00'],
                            'Öğle Yemeği': ['12:00', '13:45'],
                            'Akşam Yemeği': ['17:30', '19:30']
                        }
                    },
                    'Kilyos': {
                        'Haftaiçi': {
                            'Kahvaltı': ['07:30', '10:00'],
                            'Öğle Yemeği': ['12:00', '15:00'],
                            'Akşam Yemeği': ['17:00', '19:00']
                        },
                        'Haftasonu': {
                            'Kahvaltı': ['08:30', '10:00'],
                            'Öğle Yemeği': ['12:00', '13:45'],
                            'Akşam Yemeği': ['17:30', '19:30']
                        }
                    },
                    'Kandilli': {
                        'Haftaiçi': {
                            'Kahvaltı': ['07:30', '09:30'],
                            'Öğle Yemeği': ['11:30', '14:30'],
                            'Akşam Yemeği': ['17:00', '19:00']
                        },
                        'Haftasonu': {
                            'Kahvaltı': ['08:30', '10:00'],
                            'Öğle Yemeği': ['12:00', '13:45'],
                            'Akşam Yemeği': ['17:30', '19:30']
                        }
                    },
                    'Hisar': {
                        'Haftaiçi': {
                            'Kahvaltı': None,
                            'Öğle Yemeği': ['11:30', '14:30'],
                            'Akşam Yemeği': None
                        },
                        'Haftasonu': {
                            'Kahvaltı': None,
                            'Öğle Yemeği': None,
                            'Akşam Yemeği': None
                        }
                    },
                }
        
        # Extract the campus name from the entities
        campus_name = entities['campus:campus'][0]['value']
        # Get the meal times for the specified campus
        campus_meal_times = CAMPUS_TIMES.get(campus_name)

        # If the campus name is not found in the CAMPUS_TIMES dictionary, return an error message
        if not campus_meal_times:
            return {"text": f"Kampüs bilgisi hatalı: {campus_name}. Lütfen tekrar deneyin."}

        # Prepare a response text
        response = f"{campus_name} kampüsü yemek saatleri:\n"
        # Iterate over the weekday/weekend categories, add the category name to the response
        for day_type, meals in campus_meal_times.items():
            response += f"\n{day_type.capitalize()}:\n"
            # Iterate over the meals in the category
            # Depending on whether the meals are served for that time frame, prepare the response accordingly
            for meal, times in meals.items():
                if times is None:
                    response += f"- {meal.capitalize()}: Bu öğün için yemek hizmeti verilmemektedir.\n"
                else:
                    response += f"- {meal.capitalize()}: {times[0]} - {times[1]}\n"
        return {"text": response}


    def handle_get_menu(self, entities=None, context=None):
        """Handle the 'getMenu' intent by returning the current or next day's meal menu"""
        
        # Open the menu data file
        with open('menu.json', 'r', encoding='utf-8') as f:
            menu = json.load(f)
        
        # Get the current date and time, format it as 'dd mm'
        current_time = datetime.now()
        current_date = current_time.strftime('%d %m')
        meal_time = self.get_meal_time()

        # If the current time is outside of meal times, get the menu for the next day
        if meal_time is None:
            # Calculate the date of the next day
            next_day = (current_time + timedelta(days=1)).strftime('%d %m')
            # If the menu for the next day is available, prepare the menu for the next day
            if next_day in menu:
                meal_menu = menu[next_day]
                menu_str = f"{next_day} Menüsü:\n"
                for meal_time, items in meal_menu.items():
                    menu_str += f"\n{meal_time.capitalize()}:\n"
                    for category, items in items.items():
                        menu_str += f"\n{category.capitalize()}:\n"
                        for item in items:
                            menu_str += f"- {item['name']}: {item['ingredients']}\n"
                return {"text": menu_str}
            else:
                return {"text": "Yarının menüsü mevcut değil."}
        
        # If the menu for the current date is not available, return an error message
        if current_date not in menu:
            return {"text": "Bugünün menüsü mevcut değil."}

        # If the menu for the current meal time is not available, return an error message
        if meal_time not in menu[current_date]:
            return {"text": f"{meal_time.capitalize()} menüsü mevcut değil."}

        # Prepare the string of the menu for the current meal time
        meal_menu = menu[current_date][meal_time]
        menu_str = f"{current_date} {meal_time.capitalize()} Menüsü:\n"
        for category, items in meal_menu.items():
            menu_str += f"\n{category.capitalize()}:\n"
            for item in items:
                menu_str += f"- {item['name']}: {item['ingredients']}\n"
        return {"text": menu_str}


    def handle_query_meal(self, entities, context):
        """Handle the 'queryMeal' intent by searching for a specific meal in the menu data"""
        
        # Extract the meal name from the entities, or set it to None if not provided
        meal_name = next(
            (
                entity[0]['value']
                for entity in entities.values()
                if 'value' in entity[0]
            ),
            None,
        )
        
        # If no meal name was provided, return an error message
        if meal_name is None:
            return {"text": "Yemek ismi belirtmediniz."}

        # Open the menu data file
        with open('menu.json', 'r', encoding='utf-8') as f:
            menu = json.load(f)

        # Get the current date, format it as 'dd mm'
        # Create a sorted list of the dates in the menu
        today = datetime.now().strftime('%d %m')
        sorted_dates = sorted(menu.keys())

        # Loop through each date in the sorted dates
        for date in sorted_dates:
            # Skip dates that are before today
            if date < today:
                continue

            # Get the meals for the current date
            meals = menu[date]
            
            # Loop through each meal time (e.g., breakfast, lunch, dinner)
            for meal_time, meal_items in meals.items():
                # Loop through each category of items (e.g., main, sides, dessert)
                for category, items in meal_items.items():
                    # Loop through each item in the category
                    for item in items:
                        # If the item's name matches the queried meal name
                        if item['name'] == meal_name:
                            return {"text": f"{meal_name}, {date} tarihinde {meal_time} menüsünde sunulacak."}

        return {"text": f"Maalesef {meal_name} ayın geri kalanı için menüde gözükmüyor."}


    def handle_get_menu_for_date(self, entities, context):
        """Handle the 'getMenuForDate' intent by returning the meal menu for a specific date"""
        
        # Check if the 'datetime' entity exists in the entities dictionary
        if 'wit$datetime:datetime' in entities:
            # Get the first 'datetime' entity
            datetime_entity = entities['wit$datetime:datetime'][0]

            # Check if the 'value' key exists in the datetime entity
            if 'value' in datetime_entity:
                # Extract the date from the 'value' key
                date_str = datetime_entity['value'][:10]

                # Load the menu data
                with open('menu.json', 'r', encoding='utf-8') as f:
                    menu = json.load(f)

                # Convert the date_str to a datetime object
                date_obj = datetime.strptime(datetime_entity['value'], '%Y-%m-%dT%H:%M:%S.%f%z')

                # Convert the datetime object to a string in the format used in the menu data
                menu_date_str = date_obj.strftime('%d %m').lstrip("0")

                # Check if the date exists in the menu data
                if menu_date_str in menu:
                    # Get the menu for the date
                    date_menu = menu[menu_date_str]

                    # Format the menu into a string
                    menu_str = f"{menu_date_str} Menüsü:\n"
                    for meal_time, meal_menu in date_menu.items():
                        menu_str += f"\n{meal_time}:\n"
                        for category, items in meal_menu.items():
                            menu_str += f"\n{category}:\n"
                            for item in items:
                                menu_str += f"- {item['name']}: {item['ingredients']}\n"

                    return {"text": menu_str}

                else:
                    return {"text": f"{menu_date_str} tarihli menü mevcut değil."}

        # If no 'datetime' entity was found or it doesn't contain a 'value', return a default response
        return {"text": "Tarih belirtmediniz."}


    def handle_get_location(self, entities, context):
        """Handle the 'getLocation' intent by returning the URL of a specific campus"""
        
        # Check if the 'campus' entity exists in the entities dictionary
        if 'campus:campus' in entities:
            # Get the first 'campus' entity
            campus_entity = entities['campus:campus'][0]

            # Check if the 'value' key exists in the campus entity
            if 'value' in campus_entity:
                # Get the campus name
                campus_name = campus_entity['value']

                # Define a dictionary mapping campus names to URLs
                campus_urls = {
                    'Kuzey': 'https://yemekhane.boun.edu.tr/yemekhaneler/kuzey-kampus-yemekhanesi',
                    'Güney': 'https://yemekhane.boun.edu.tr/yemekhaneler/guney-kampus-yemekhanesi',
                    'Kilyos': 'https://yemekhane.boun.edu.tr/yemekhaneler/saritepe-kampusu-yemekhanesi',
                    'Kandilli': 'https://yemekhane.boun.edu.tr/yemekhaneler/kandilli-kampusu-yemekhanesi',
                    'Hisar': 'https://yemekhane.boun.edu.tr/yemekhaneler/hisar-kampusu-yemekhanesi'
                }

                # Check if the campus name exists in the campus_urls dictionary
                if campus_name in campus_urls:
                    # Get the URL for the campus
                    campus_url = campus_urls[campus_name]

                    # Return the URL for the campus
                    return {"text": f"{campus_name.capitalize()} Kampüs yemekhanesi hakkında detaylı bilgiye buradan erişebilirsiniz: {campus_url}"}

        # If no 'campus' entity was found or it doesn't contain a 'value', return a default response
        return {"text": "Bu kampüste yemekhane bulunmamaktadır."}


    def handle_message(self, message):
        """Handle an incoming message by passing it to Wit.ai and executing the appropriate intent handler"""
        try:
            # Pass the message to Wit.ai and receive the response
            reply = self.client.message(message)
            
            # Get the intent name from the response, if there is any
            intent = reply['intents'][0]['name'] if reply['intents'] else None
            
            # Get the entities from the response
            entities = reply['entities']
                
            # If the intent is "killProcess", return "exit" to stop the bot
            if intent == "killProcess":
                return "exit"

            # If there is a handler for the intent
            if intent in self.handlers:
                # Call the handler and get its response
                handler_response = self.handlers[intent](entities, {})
                
                # Return the text from the handler's response
                return handler_response["text"]
            else:
                # If there is no handler for the intent, return a default error message
                return "Anladığım bir komut değil."
        except Exception as e:
            # If an error occurred, return a message with the error
            return f"Bir hata oluştu: {str(e)}"

bot = Bot('RUVCQ222IJJWFZ72SAJXV7DX4GXCYVVX')

while True:
    user_input = input("Sormak istediğiniz bir şey var mı: ")
    
    
    onse = bot.handle_message(user_input)
    if response == "exit":
        print("Pekala, görüşmek üzere!")
        break
    print(response)
