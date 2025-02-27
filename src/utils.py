import logging
import os
from datetime import datetime
from itertools import islice

import pandas as pd
import requests
from dotenv import load_dotenv
from pandas import DataFrame
from config import PATH_LOGS, PATH_DATA

load_dotenv()
EXCHANGE_RATE_API_KEY = os.getenv('EXCHANGE_RATE_API_KEY')
MARKET_STACK_API_KEY = os.getenv('MARKET_STACK_API_KEY')

api_logger = logging.getLogger("api_loger")
file_handler = logging.FileHandler(os.path.join(PATH_LOGS, "api_logs.log"))
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
api_logger.addHandler(file_handler)
api_logger.setLevel(logging.INFO)


def greeting(date: str) -> str:
    """
    Функция принимает дату в формате строки YYYY-MM-DD HH:MM:SS
    Возвращает строку приветствия в зависимости от времени:
    22.00 - 04.00 - Доброй ночи
    04.00 - 10.00 - Доброе утро
    10.00 - 16.00 - Добрый день
    16.00 - 22.00 - Добрый вечер
    """
    date_obj = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    hour = date_obj.hour
    if hour > 21 or hour < 4:
        return "Доброй ночи!"
    elif 3 < hour < 10:
        return "Доброе утро!"
    elif 9 < hour < 16:
        return "Добрый день!"
    else:
        return "Добрый вечер!"


def get_transactions_df_from_excel(path_to_excel: str) -> DataFrame:
    """Функция принимает путь до EXCEL файла и возвращает данные о транзакциях в виде списка словарей"""

    transactions_df = pd.read_excel(path_to_excel, parse_dates=["Дата операции"], date_format='%d.%m.%Y %H:%M:%S')
    return transactions_df


def filter_transactions_by_date(transactions: DataFrame, date_str: str, date_begin: str = None) -> DataFrame:
    """
    Функция фильтрует transactions: DateFrame по полю "Дата операции" в интервале
    от начало месяца до date_str в формате DD.MM.YYYY
    """
    date_end = datetime.strptime(date_str, "%d.%m.%Y")
    date_end = date_end.replace(hour=23, minute=59, second=59)
    if not date_begin:
        date_begin = datetime(date_end.year, date_end.month, 1)
    else:
        date_begin = datetime.strptime(date_begin, "%d.%m.%Y")
    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], dayfirst=True)
    filtered = transactions[
        (transactions["Дата операции"] >= date_begin) &
        (transactions["Дата операции"] <= date_end)
    ]
    return filtered


def get_cards(transactions_df: DataFrame) -> list[dict]:
    """
    Функция принимает список транзакций DataFrame и возвращает список карт в формате:
    [
        {
          "last_digits": "5814",
          "total_spent": 1262.00,
          "cashback": 12.62
        },
        {
          "last_digits": "7512",
          "total_spent": 7.94,
          "cashback": 0.08
        }
    ]
    """
    filtered_status_ok = transactions_df[transactions_df["Статус"] == "OK"]
    grouped_by_cards = filtered_status_ok[["Номер карты", "Кэшбэк", "Сумма операции с округлением"]].groupby(
        "Номер карты", as_index=False).sum()

    cards = []
    for index, row in grouped_by_cards.iterrows():
        cards.append(
            {
                "last_digits": row['Номер карты'][1:],
                "total_spent": round(float(row['Сумма операции с округлением']), 2),
                "cashback": row["Кэшбэк"]
            }
        )

    return cards


def get_top_transactions(transactions_df: DataFrame, count: int = 5) -> list[dict]:
    """
    Функция принимает список транзакций DataFrame и возвращает список из count транзакций вида:
    [
        {
          "date": "21.12.2021",
          "amount": 1198.23,
          "category": "Переводы",
          "description": "Перевод Кредитная карта. ТП 10.2 RUR"
        },
        {
          "date": "20.12.2021",
          "amount": 829.00,
          "category": "Супермаркеты",
          "description": "Лента"
        }
        ...
    ]
    При этом учитываются только транзакции, завершенные успешно (Статус=ОК)
    """
    filtered_status_ok = transactions_df[transactions_df["Статус"] == "OK"]
    sorted_by_amount = filtered_status_ok.sort_values("Сумма операции с округлением", ascending=False)
    top = []
    for index, row in islice(sorted_by_amount.iterrows(), count):
        top.append(
            {
                "date": row["Дата платежа"],
                "amount": round(float(row['Сумма операции с округлением']), 2),
                "category": row["Категория"],
                "description": row["Описание"]
            }
        )
    return top


def get_currency_rate(currency: str) -> float:
    """Получает курс валюты от API и возвращает его в виде float"""

    url = f"https://api.apilayer.com/exchangerates_data/latest?base={currency}"
    api_logger.info(f"Вызов метода GET по url = {url}")
    try:
        response = requests.get(url, headers={'apikey': EXCHANGE_RATE_API_KEY}).json()
    except Exception as ex:
        api_logger.error(f"При выполнения запроса возникла ошибка: {ex}", exc_info=True)

    rate = response["rates"]["RUB"]
    return float(rate)


def get_currencies_rates(currencies: list) -> list[dict]:
    """
    Получает курсы валют в виде списка словарей вида:
    [
        {
          "currency": "USD",
          "rate": 73.21
        },
        {
          "currency": "EUR",
          "rate": 87.08
        }
    ]
    """

    result = []
    for currency in currencies:
        result.append(
            {
                "currency": currency,
                "rate": round(get_currency_rate(currency), 2)
            }
        )
    return result


def get_stock_price(ticker: str) -> float:
    """Получает последнюю цену закрытия цены акции по API и возвращает его в виде float"""
    url = "https://api.marketstack.com/v1/eod/latest"

    params = {
        "access_key": MARKET_STACK_API_KEY,
        "symbols": ticker
    }
    api_logger.info(f"Вызов метода GET по url = {url}")
    try:
        response = requests.get(url, params=params)
    except Exception as ex:
        api_logger.error(f"При выполнения запроса возникла ошибка: {ex}", exc_info=True)

    if response.status_code == 200:
        return response.json().get('data', [{}])[0].get('close')
    else:
        return 0


def get_stock_prices(tickers: list[str]) -> list[dict]:
    """
    Получает список тикеров, возвращает список словарей в формате:
    [
        {
          "stock": "AAPL",
          "price": 150.12
        },
        {
          "stock": "AMZN",
          "price": 3173.18
        }
        ...
    ]
    """
    stock_prices = []
    for ticker in tickers:
        stock_prices.append(
            {
                "stock": ticker,
                "price": get_stock_price(ticker)
            }
        )
    return stock_prices


if __name__ == "__main__":
    path_to_excel = os.path.join(PATH_DATA, "operations.xlsx")
    df = get_transactions_df_from_excel(path_to_excel)
    cards = get_cards(get_transactions_df_from_excel(path_to_excel))
    print(cards)
    top = get_top_transactions(df)
    print(top)
    print(get_currencies_rates(['USD', 'EUR']))
    filtered = filter_transactions_by_date(df, "28.12.2021")
    print(filtered)
    print(get_stock_price("AAPL"))
