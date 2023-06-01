# Yemekhane360°

Yemekhane360° is an NLP bot project aimed at providing real-time information about the campus meal menus of Boğaziçi University in Turkey. The bot leverages the power of wit.ai for intent classification.

## Problem Statement
The primary task or problem this project intends to solve is to scrape meal data from the university cafeteria's website and use this data to construct a bot capable of responding accurately to various user inquiries about meal schedules and meal contents.

## Contributors
This project is developed by:
- **Ümit Altar Binici**: Lead Developer and Data Processing
- **Ardıl Acar**: Data Scraping, Dietary Considerations, Polling
- **Ömer Çağlayan**: Bot Interaction Design

## Project Structure
The project consists of three main Python scripts:

1. `preprocessing.py`
2. `chatbot.py`
3. `foodlist.py`
4. `anket.py`

Each script performs a specific function and should be executed in the specified order (1-3-2).

### preprocessing.py
This script scrapes the university's cafeteria website for meal data, including meal names and ingredients for different meal categories. The data is sorted by date and mealtime (breakfast, lunch, and dinner), and is saved in a JSON file named 'menu.json'.
To run the preprocessing script, use the command:

```shell
$ python preprocessing.py
```

### chatbot.py
This is the main application script. It interacts with the wit.ai API to understand user queries about campus meals. It leverages the Bot class to handle different user intents. To run the chatbot script with your own wit.ai application, set your wit.ai token:

```shell
$ python chatbot.py --token YOUR_WIT_AI_TOKEN
```

Replace `YOUR_WIT_AI_TOKEN` with your actual wit.ai token. The script uses a pre-trained wit.ai application by default.

### foodlist.py
This script processes the 'menu.json' file created by the `preprocessing.py` script. It generates a `foodlist.json` file that contains detailed information about each food item, including type, ingredients, dietary considerations, and user ratings. 

To run the foodlist script:

```shell
$ python foodlist.py
```

Note: This script should be executed after `preprocessing.py` and before `chatbot.py`.

### anket.py
This script provides the backbone of the user polling function to ask the user for the ratings of a randomly selected meal. Additionally, some of the meals do not have any ingredient listing under the school website, and this script will ask the user whether such a meal is vegan, vegetarian or gluten-free. The ratings are not yet implemented into the main application, but will be done so in a future release.

To run the foodlist script:

```shell
$ python anket.py
```

Note: This script should be executed after `preprocessing.py`.


## Dependencies
The application requires Python 3.6 or later and the following Python packages:

1. `requests`
2. `BeautifulSoup4`
3. `wit`
4. `json`
5. `datetime`
6. `re`
7. `random`

To install the necessary packages:

```shell
$ pip install requests beautifulsoup4 wit
```

## Support
For any questions, suggestions or issues, please contact:

- Ümit Altar Binici - [umit.binici@boun.edu.tr](mailto:umit.binici@boun.edu.tr)
- Ardıl Acar - [ardil.acar@boun.edu.tr](mailto:ardil.acar@boun.edu.tr)
- Ömer Çağlayan - [omer.caglayan@boun.edu.tr](mailto:omer.caglayan@boun.edu.tr)
