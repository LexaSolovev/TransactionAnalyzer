import json
from itertools import islice

import pandas as pd
from datetime import datetime

import os
from pandas.core.interchange.dataframe_protocol import DataFrame

from config import PATH_DATA


def greeting(date: str) -> str:
    """
    Функция принимает дату в формате строки YYYY-MM-DD HH-MM-SS
    Возвращает строку приветствия в зависимости от времени:
    22.00 - 04.00 - Доброй ночи
    04.00 - 10.00 - Доброе утро
    10.00 - 16.00 - Добрый день
    16.00 - 22.00 - Добрый вечер
    """
    date_obj = datetime.strptime(date, "%Y-%m-d %H-%M-%S")
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

    transactions_df = pd.read_excel(path_to_excel)
    return transactions_df


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
    grouped_by_cards = filtered_status_ok.groupby("Номер карты", as_index=False).sum()

    cards = []
    for index, row in grouped_by_cards.iterrows():
        cards.append(
            {
                "last_digits": row['Номер карты'][1:],
                "total_spent": round(float(row['Сумма операции с округлением']),2),
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
    """
    filtered_status_ok = transactions_df[transactions_df["Статус"] == "OK"]
    sorted_by_amount = filtered_status_ok.sort_values("Сумма операции с округлением", ascending=False)
    top = []
    for index, row in islice(sorted_by_amount.iterrows(), count):
        top.append(
            {
                "date": row["Дата платежа"],
                "amount": round(float(row['Сумма операции с округлением']),2),
                "category": row["Категория"],
                "description": row["Описание"]
            }
        )
    return top


if __name__ == "__main__":
     path_to_excel = os.path.join(PATH_DATA, "operations.xlsx")
     df = get_transactions_df_from_excel(path_to_excel)
     # cards = get_cards(get_transactions_df_from_excel(path_to_excel))
     # print(cards)
     top = get_top_transactions(df)
     print(top)

