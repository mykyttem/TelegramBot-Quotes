import requests
from bs4 import BeautifulSoup
import json

URL = "https://vsviti.com.ua/society/81550"

response = requests.get(URL)
soup = BeautifulSoup(response.text, "lxml")

quotes = soup.find_all("p")
quote_list = []

for q in quotes:
    qoute = q.get_text()

    dict_qoutes = {
        qoute[:2]: qoute[2:]
    }

    quote_list.append(dict_qoutes)


with open("result_quotes.json", "w", encoding="utf-8") as json_file:
    json.dump(quote_list, json_file, ensure_ascii=False)