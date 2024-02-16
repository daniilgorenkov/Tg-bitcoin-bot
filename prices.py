import requests
from coinmarketcapapi import CoinMarketCapAPI

def get_BTC_price() -> str:
    """Получение актуального курса BTC  к USD"""

    cmc = CoinMarketCapAPI(api_key="50cded87-a8c5-4828-8e30-50462cb35104")

    rep = cmc.cryptocurrency_info(symbol="BTC")

    BTC_description = rep.data["BTC"][0]["description"].split(" ")

    for i in range(len(BTC_description)):
        if BTC_description[i] == "USD":
            price = BTC_description[i-1]
            
    return price

def get_USDT_price() -> str:
    """Получение актуального курса USDT к USD"""
    cmc = CoinMarketCapAPI(api_key="50cded87-a8c5-4828-8e30-50462cb35104")

    rep = cmc.cryptocurrency_info(symbol="USDT")

    USDT_description = rep.data["USDT"][0]["description"].split(" ")

    for i in range(len(USDT_description)):
        if USDT_description[i] == "USD":
            price = USDT_description[i-1]

    return price

def get_RUB_price() -> float:
    """Получение актуального курса рубля к доллару"""

    url = 'https://www.cbr.ru/scripts/XML_daily.asp'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.text
        data
        # Найдем курс доллара в XML-данных

        lines = data.split('</Valute>')
        lines
        for line in lines:
            if 'Доллар США' in line:
                RUB = line.split("<Value>")[1][:7]
                break
    return float(RUB.replace(",","."))