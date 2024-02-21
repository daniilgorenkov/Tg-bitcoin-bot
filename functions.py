import requests
from coinmarketcapapi import CoinMarketCapAPI
import pandas as pd
import datetime
import pickle as pkl
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

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


def split_dates(data:pd.DataFrame) -> pd.DataFrame:
    copy = data.copy()

    copy["day"] = copy["Date"].dt.day
    copy["month"] = copy["Date"].dt.month
    copy["year"] = copy["Date"].dt.year
    copy["day_of_week"] = copy["Date"].dt.day_of_week

    copy = copy.drop("Date", axis=1)

    return copy

# date = pd.to_datetime("19-02-2024")

def add_day_of_week_cols(data:pd.DataFrame):

    d = {"day_of_week_1":1,
         "day_of_week_2":2,
         "day_of_week_3":3,
         "day_of_week_4":4,
         "day_of_week_5":5,
         "day_of_week_6":6,}

    copy = data.copy()

    for i in range(1,7):
        copy[f"day_of_week_{i}"] = 0
    
    # print(copy["day_of_week"])

    for i in copy["day_of_week"]:
        if i != 0:
            for k in d.keys():
                if d[k] == i:
                    copy[k] = 1
    
    copy = copy.drop("day_of_week", axis=1)

    return copy

def load_volume_model():
    with open('xgb_volume.pkl', 'rb') as f:
        volume_model = pkl.load(f)
        return volume_model


def load_price_model():
    with open('xgb_price.pkl', 'rb') as f:
        price_model = pkl.load(f)
        return price_model

a = datetime.datetime.now()

a + datetime.timedelta(1)

def predict(volume_model,
            price_model,
            volume_cols:list,
            price_cols:list):

    pred_dates = {"Date":[]}

    for d in range(0,6):
        date = datetime.datetime.now() + datetime.timedelta(d)
        
        day = date.day
        month = date.month
        year = date.year

        timestamp = f"{day}-{month}-{year}"
        pred_dates["Date"].append(pd.to_datetime(timestamp))
    
    X = pd.DataFrame(pred_dates)
    X = split_dates(X)
    # print(X)
    X = add_day_of_week_cols(X)
    X["is_covid"] = True
    X["is_war"] = True

    X_volume = X
    X_volume = X_volume[volume_cols]
    volume_preds = volume_model.predict(X_volume)

    X["Vol."] = volume_preds
    X_price = X[price_cols]
    price_prediction = np.exp(price_model.predict(X_price))

    plt.title("График предсказаний цены BTC на 5 дней")
    plt.figure().set_size_inches(12,8)
    sns.lineplot(price_prediction)
    plt.xlabel("Дни")
    plt.ylabel("Цена, USD")

    plt.savefig("pred_graph.png")