import calendar
import logging
import os
from datetime import datetime

import pandas as pd

from config import PATH_LOGS
from src.utils import filter_transactions_by_date

services_logger = logging.getLogger("services")
file_handler = logging.FileHandler(os.path.join(PATH_LOGS, "services.log"))
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
services_logger.addHandler(file_handler)
services_logger.setLevel(logging.INFO)


def get_best_categories(data: list[dict], year: int, month: int) -> dict:
    """
    Функция для подсчета лучших категорий для кэшбэка
    :param data: Транзакции
    :param year: Год для выборки
    :param month: Месяц для выборки
    Возвращает словарь в виде:
        {
            "Категория 1": 1000,
            "Категория 2": 2000,
            "Категория 3": 500
        }
    """
    first_day, last_day = calendar.monthrange(year, month)
    date_begin = datetime(year=year, month=month, day=first_day)
    date_end = datetime(year=year, month=month, day=last_day, hour=23, minute=59, second=59)

    filtered_data = []
    for transaction in data:
        operation_date = datetime.strptime(transaction['Дата операции'], '%d.%m.%Y %H:%M:%S')
        if (date_begin <= operation_date <= date_end
                and transaction['Бонусы (включая кэшбэк)'] > 0
                and transaction['Статус'] == "OK"
        ):
            filtered_data.append(transaction)

    best_categories = {}
    for transaction in filtered_data:
        category = transaction['Категория']
        bonus = transaction['Бонусы (включая кэшбэк)']
        if category in best_categories:
            best_categories[category] += bonus
        else:
            best_categories[category] = bonus

    best_categories = dict(sorted(best_categories.items(), key=lambda x: x[1], reverse=True))

    # df = pd.DataFrame(data)
    # _, last_day_month = calendar.monthrange(year, month)
    # date_str = datetime(year=year, month=month, day=last_day_month).strftime("%d.%m.%Y")
    # df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)
    #
    # services_logger.info("Запущена фильтрация данных по дате filter_transactions_by_date")
    # filtered = filter_transactions_by_date(df, date_str)
    # services_logger.info("Фильтрация закончена.")
    # grouped_by_categories = filtered[
    #     [
    #         "Категория",
    #         "Сумма операции с округлением"
    #     ]
    # ].groupby("Категория", as_index=False).sum()
    #
    # sorted_categories = grouped_by_categories.sort_values("Сумма операции с округлением", ascending=False)
    # best_categories = {}
    # for index, row in sorted_categories.iterrows():
    #     best_categories[row["Категория"]] = row["Сумма операции с округлением"]

    return best_categories
