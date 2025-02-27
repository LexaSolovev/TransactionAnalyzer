import json
import os

import pandas as pd

from config import PATH_DATA, PATH_REPORTS
from src.reports import report_to_file, spending_by_category


def test_report_to_file():
    @report_to_file("test_decorator")
    def example_report():
        path_to_test_excel = os.path.join(PATH_DATA, "operations_for_test.xlsx")
        df = pd.read_excel(path_to_test_excel)
        return df

    test_df = example_report()
    path_to_test_report = os.path.join(PATH_REPORTS, "test_decorator.xlsx")
    df_from_test_decorator = pd.read_excel(path_to_test_report)
    assert test_df.to_json() == df_from_test_decorator.to_json()


def test_spending_by_category(dataframe_for_tests):
    result = spending_by_category(dataframe_for_tests, "Различные товары", "31.12.2021")
    result_str = result.to_json(orient="records", index=False, date_format="%d.%m.%Y %H:%M:%S", indent=4)
    result_json = json.loads(result_str)
    assert result_json == [{
                "Дата операции": "31.12.2021 01:23:42",
                "Дата платежа": "31.12.2021",
                "Номер карты": "*5091",
                "Статус": "OK",
                "Сумма операции": -564.00,
                "Валюта операции": "RUB",
                "Сумма платежа": -564.00,
                "Валюта платежа": "RUB",
                "Кэшбэк": 0,
                "Категория": "Различные товары",
                "MCC": 5399,
                "Описание": "Ozon.ru",
                "Бонусы(включая кэшбэк)": 5,
                "Округление на инвесткопилку": 0,
                "Сумма операции с округлением": 564.00
            }]
