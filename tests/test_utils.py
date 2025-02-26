import pytest

from src.utils import greeting


@pytest.mark.parametrize("date, expected", [
    ("2025-02-01 01:02:00","Доброй ночи!"),
    ("2025-02-01 09:02:00","Доброе утро!"),
    ("2025-02-01 11:00:00","Добрый день!"),
    ("2025-02-01 17:02:00","Добрый вечер!")
])
def test_greeting(date, expected):
    assert greeting(date) == expected


