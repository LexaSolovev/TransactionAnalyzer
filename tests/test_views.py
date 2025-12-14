from unittest.mock import Mock

import src.utils
from src.views import get_response


def test_get_response():
    src.utils.greeting = Mock(return_value="Добрый день!")
    src.utils.get_cards = Mock(return_value=[{"cards_keys": "cards_values"}])
    src.utils.get_top_transactions = Mock(return_value=[{"top_keys": "top_values"}])
    src.utils.get_currencies_rates = Mock(return_value=[{"rate_keys": "rate_values"}])
    src.utils.get_stock_prices = Mock(return_value=[{"price_keys": "price_values"}])
    assert get_response("2021-12-30 00:00:00") == {
        "greeting": "Добрый день!",
        "cards": [{"cards_keys": "cards_values"}],
        "top_transactions": [{"top_keys": "top_values"}],
        "currency_rates": [{"rate_keys": "rate_values"}],
        "stock_prices": [{"price_keys": "price_values"}]
    }
