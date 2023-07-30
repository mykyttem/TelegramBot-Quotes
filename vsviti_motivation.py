import requests
from bs4 import BeautifulSoup
import json

""" Parse site, 
    getting quotes,
    save file, and read """


URL = "https://vsviti.com.ua/society/81550"

response = requests.get(URL)
soup = BeautifulSoup(response.text, "lxml")

quotes = soup.find_all("p")[::-2]
quote_list = []

for q in quotes:
    qoute = q.get_text()
    quote_list.append(qoute[3:])


# save quotes in file
with open("result_quotes.json", "w", encoding="utf-8") as json_file:
    json.dump(quote_list, json_file, ensure_ascii=False)


# read file
file_name = "result_quotes.json"
with open(file_name, 'r', encoding='utf-8') as file:
    quotes = json.load(file)