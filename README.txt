==========================================================
README: Yemekhane360°
==========================================================

Yemekhane360° provides information about the campus meal 
menus of Boğaziçi University in Turkey. The bot uses wit.ai 
for intent classification.

==========================================================
Scripts:
==========================================================

There are two main scripts in this application:

1. preprocessing.py
2. chatbot.py

==========================================================
preprocessing.py
==========================================================

This script scrapes the Boğaziçi University cafeteria 
website for meal data, including meal names and ingredients 
for different categories of meals, such as soups, main 
dishes, vegan meals, side dishes, and additional choices. 

The meal data is organized by date and meal time 
(breakfast, lunch, and dinner), and is saved in a JSON 
file named 'menu.json'.

To run the preprocessing script:

$ python preprocessing.py

This will generate the 'menu.json' file with the scraped 
meal data.

==========================================================
chatbot.py
==========================================================

This script is the main application script. It uses the 
wit.ai API to understand user queries about campus meals.

The Bot class in this script interacts with wit.ai to 
handle different user intents, such as getting the menu 
for a specific date or meal, querying a specific meal, 
getting the location of the meal, and getting the meal 
times for a specific campus. Meal times are specific to 
each campus and vary for weekdays and weekends.

The chatbot comes with its pre-trained wit.ai application,
hence you do not need to change its token.

In order to run the chatbot script with your own wit.ai 
application, you will first need to set your wit.ai token. 
You can do this in the following way:

$ python chatbot.py --token YOUR_WIT_AI_TOKEN

Replace 'YOUR_WIT_AI_TOKEN' with your actual wit.ai token.

==========================================================
Dependencies:
==========================================================

The following Python packages are needed to run the 
application:

1. requests
2. BeautifulSoup4
3. wit
4. json
5. datetime

You can install these packages using pip:

$ pip install requests beautifulsoup4 wit

Python 3.6 or later is required to run this application.

==========================================================
Support:
==========================================================

For any issues, please reach out to the developer at:

Ümit Altar Binici - umit.binici@boun.edu.tr
Ardıl Acar - ardil.acar@boun.edu.tr
Ömer Çağlayan - omer.caglayan@boun.edu.tr
