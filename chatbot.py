from wit import Wit
from datetime import datetime, time, timedelta
import json

class Bot:
    """Bot class for interacting with wit.ai and handling different user intents"""
    def __init__(self, token):
        self.client = Wit(token)
        self.handlers = {
            'getMenu': self.handle_get_menu,
            'queryMeal': self.handle_query_meal,
            'getMenuForDate': self.handle_get_menu_for_date,
            'getLocation': self.handle_get_location,
            'getMealTimesForCampus': self.handle_get_meal_times_for_campus,
        }


    def get_meal_time(self):
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
        if 'campus:campus' not in entities or 'value' not in entities['campus:campus'][0]:
            return {"text": "Kampüs bilgisi eksik veya hatalı. Lütfen tekrar deneyin."}

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
        
        campus_name = entities['campus:campus'][0]['value']
        campus_meal_times = CAMPUS_TIMES.get(campus_name)

        if not campus_meal_times:
            return {"text": f"Kampüs bilgisi hatalı: {campus_name}. Lütfen tekrar deneyin."}

        response = f"{campus_name} kampüsü yemek saatleri:\n"
        for day_type, meals in campus_meal_times.items():
            response += f"\n{day_type.capitalize()}:\n"
            for meal, times in meals.items():
                if times is None:
                    response += f"- {meal.capitalize()}: Bu öğün için yemek hizmeti verilmemektedir.\n"
                else:
                    response += f"- {meal.capitalize()}: {times[0]} - {times[1]}\n"
        return {"text": response}


    def handle_get_menu(self, entities=None, context=None):
        with open('menu.json', 'r', encoding='utf-8') as f:
            menu = json.load(f)

        current_time = datetime.now()
        current_date = current_time.strftime('%d %m')

        meal_time = self.get_meal_time()

        if meal_time is None:
            # If the current time is outside of meal times, get the menu for the next day
            next_day = (current_time + timedelta(days=1)).strftime('%d %m')
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

        if current_date not in menu:
            return {"text": "Bugünün menüsü mevcut değil."}

        if meal_time not in menu[current_date]:
            return {"text": f"{meal_time.capitalize()} menüsü mevcut değil."}

        meal_menu = menu[current_date][meal_time]

        menu_str = f"{current_date} {meal_time.capitalize()} Menüsü:\n"
        for category, items in meal_menu.items():
            menu_str += f"\n{category.capitalize()}:\n"
            for item in items:
                menu_str += f"- {item['name']}: {item['ingredients']}\n"
        return {"text": menu_str}


    def handle_query_meal(self, entities, context):
        meal_name = next(
            (
                entity[0]['value']
                for entity in entities.values()
                if 'value' in entity[0]
            ),
            None,
        )
        if meal_name is None:
            return {"text": "Yemek ismi belirtmediniz."}

        with open('menu.json', 'r', encoding='utf-8') as f:
            menu = json.load(f)

        # Get today's date
        today = datetime.now().strftime('%d %m')

        # Sort the dates in ascending order
        sorted_dates = sorted(menu.keys())

        for date in sorted_dates:
            # Skip past dates
            if date < today:
                continue

            meals = menu[date]
            for meal_time, meal_items in meals.items():
                for category, items in meal_items.items():
                    for item in items:
                        if item['name'] == meal_name:
                            return {"text": f"{meal_name}, {date} tarihinde {meal_time} menüsünde sunulacak."}

        return {"text": f"Maalesef {meal_name} ayın geri kalanı için menüde gözükmüyor."}


    def handle_get_menu_for_date(self, entities, context):
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
        try:
            resp = self.client.message(message)
            intent = resp['intents'][0]['name'] if resp['intents'] else None
            entities = resp['entities']
                
            if intent == "killProcess":
                return "exit"

            if intent in self.handlers:
                handler_response = self.handlers[intent](entities, {})
                return handler_response["text"]
            else:
                return "Anladığım bir komut değil."
        except Exception as e:
            return f"Bir hata oluştu: {str(e)}"

bot = Bot('RUVCQ222IJJWFZ72SAJXV7DX4GXCYVVX')

while True:
    user_input = input("Sormak istediğiniz bir şey var mı: ")
    response = bot.handle_message(user_input)
    if response == "exit":
        print("Pekala, görüşmek üzere!")
        break
    print(response)