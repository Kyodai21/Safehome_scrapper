import urllib.request
from bs4 import BeautifulSoup
import datetime
import requests

LANDING_URL = "https://safehome.eu/webshop?k="
FILENAME = "safehome_data.csv"

# REQUIRED FOR ACCESSING WEBSITE
landingReq = urllib.request.Request(LANDING_URL)
landingReq.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0')
landingReq.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8')
landingReq.add_header('Accept-Language', 'en-US,en;q=0.5')

# GETTING LANDING HTML AND PARSING IT WITH BS4
landingPage = urllib.request.urlopen(landingReq).read().decode('utf-8')
landingSoup = BeautifulSoup(landingPage, 'html.parser')

# GETTING USABLE PAGE ELEMENTS
maxPageNumber = int(landingSoup.find("div", {"class": "oldalakra-tordeles"}).contents[-3].text)
products = []
stocks = []

# GETTING PRODUCTS FOR EACH PAGE
for pageNumber in range(maxPageNumber) :
    # SETTING UP WEBSITE ACCESS
    URL = "https://safehome.eu/webshop?k=&lap=" + str(pageNumber + 1)
    req = urllib.request.Request(URL)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0')
    req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8')
    req.add_header('Accept-Language', 'en-US,en;q=0.5')
    page = urllib.request.urlopen(req).read().decode('utf-8')
    soup = BeautifulSoup(page, 'html.parser')
    
    # PRODUCT NAME
    productsOnPage = soup.find_all("div", {"class": "termek_fejlec"})
    for product in productsOnPage :
        products.append(product.find("h2").text.strip())
    
    # STOCK
    stocksOnPage = soup.find_all("div", {"class": "db_info"})
    for stock in stocksOnPage :
        stocks.append(stock.text.replace("Raktáron:", "").replace("db", "").strip())

# WRITING DATA
previousData = requests.get("https://raw.githubusercontent.com/Kyodai21/safehome/main/safehome_data.csv").text
previousData = previousData.split("\n")

with open(FILENAME, "w") as file:
    file.write(previousData[0] + ";" + str(datetime.datetime.date(datetime.datetime.now())) + "\n")
    for i in range(len(products)) :
        file.write(previousData[i + 1] + ";" + str(stocks[i]) + "\n")