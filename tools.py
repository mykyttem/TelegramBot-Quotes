from googletrans import Translator

import os
import json

from locales import dict_string


""" that for speed bot, we using google translate only quotes,
    translate only quotes, everything else through the locale 
"""

# translate locales
""" term translation, term key, and to which to translate """
def l_trans(text_key, language) -> dict:
    return dict_string[text_key].get(language, '')


# translate google
trans_google = Translator().translate


# read file
folder_path = "results_scrapy"

# path file
file_path = os.path.join(folder_path, "quotes.json")

with open(file_path, 'r', encoding='utf-8') as file:
    quotes = json.load(file)