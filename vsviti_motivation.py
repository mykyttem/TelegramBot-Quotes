import requests
from bs4 import BeautifulSoup

URL = "https://vsviti.com.ua/society/81550"

response = requests.get(URL)
soup = BeautifulSoup(response.text, "lxml")

block_quotes = soup.find("div", class_="td-post-content")
for quotes in block_quotes:
    quotes = quotes.get_text(strip=True)

    print(quotes)