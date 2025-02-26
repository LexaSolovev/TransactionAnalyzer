import os.path
from datetime import datetime

import pytest
from pandas import DataFrame

from config import PATH_DATA
from src.utils import greeting, get_transactions_df_from_excel, get_cards, get_top_transactions


@pytest.mark.parametrize("date, expected", [
    ("2025-02-01 01:02:00","Доброй ночи!"),
    ("2025-02-01 09:02:00","Доброе утро!"),
    ("2025-02-01 11:00:00","Добрый день!"),
    ("2025-02-01 17:02:00","Добрый вечер!")
])
def test_greeting(date, expected):
    assert greeting(date) == expected


def test_get_cards(dataframe_for_tests):
    assert get_cards(dataframe_for_tests) == [
        {
            "last_digits": "5091",
            "total_spent": 564.00,
            "cashback": 0
        },
        {
          "last_digits": "7197",
          "total_spent": 224.89,
          "cashback": 0
        }

    ]


def test_get_top_transactions(dataframe_for_tests):
    assert get_top_transactions(dataframe_for_tests) == [
        {
          "date": "31.12.2021",
          "amount": 564.00,
          "category": "Различные товары",
          "description": "Ozon.ru"
        },
        {
          "date": "31.12.2021",
          "amount": 160.89,
          "category": "Супермаркеты",
          "description": "Колхоз"
        },
        {
            "date": "31.12.2021",
            "amount": 64.00,
            "category": "Супермаркеты",
            "description": "Колхоз"
        }
    ]


def