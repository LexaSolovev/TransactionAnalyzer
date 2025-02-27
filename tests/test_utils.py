from unittest.mock import Mock, patch

import pytest

import src
from src.utils import (get_cards, get_currencies_rates, get_currency_rate, get_stock_price, get_stock_prices,
                       get_top_transactions, greeting)


@pytest.mark.parametrize("date, expected", [
    ("2025-02-01 01:02:00", "Доброй ночи!"),
    ("2025-02-01 09:02:00", "Доброе утро!"),
    ("2025-02-01 11:00:00", "Добрый день!"),
    ("2025-02-01 17:02:00", "Добрый вечер!")
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


@patch("requests.get")
def test_get_currency_rate(mock_request):
    mock_response = mock_request.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = {"rates": {"RUB": 100}}
    assert get_currency_rate("USD") == 100


def test_get_currencies_rates():
    src.utils.get_currency_rate = Mock(return_value=100)
    assert get_currencies_rates(["USD", "EUR"]) == [
        {
          "currency": "USD",
          "rate": 100
        },
        {
          "currency": "EUR",
          "rate": 100
        }
    ]


@patch("requests.get")
def test_get_stock_price(mock_request):
    mock_response = mock_request.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": [{"close": 100}]}
    assert get_stock_price("AAPL") == 100


def test_get_stock_prices():
    src.utils.get_stock_price = Mock(return_value=100)
    assert get_stock_prices(["AAPL", "AMZN"]) == [
        {
            "stock": "AAPL",
            "price": 100
        },
        {
            "stock": "AMZN",
            "price": 100
        }
    ]
