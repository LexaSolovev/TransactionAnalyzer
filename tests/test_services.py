
from src.services import get_best_categories


def test_get_best_categories(json_for_tests):
    assert get_best_categories(json_for_tests, 2021, 12) == {
        "Различные товары": 5,
        "Супермаркеты": 4,
    }
