
from src.services import get_best_categories


def test_get_best_categories(json_for_tests):
    assert get_best_categories(json_for_tests, 2021, 12) == {
        "Различные товары": 564.00,
        "Супермаркеты": 224.89,
        "Каршеринг": 7.07
    }