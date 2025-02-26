import os
from datetime import datetime
from typing import Optional

import pandas as pd
from dateutil.relativedelta import relativedelta

from config import PATH_DATA
from src.utils import filter_transactions_by_date


def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """
    Функция принимает список транзакций в виде DataFrame, Категорию и дату в формате DD.MM.YYYY
    Возвращает траты по заданной категории за последние три месяца (от переданной даты), если дата не передана
    то последние три месяца от текущей даты
    """
    if not date:
        date_end = datetime.now()
    else:
        date_end = datetime.strptime(date, "%d.%m.%Y")

    date_begin = date_end + relativedelta(months=-3)

    filtered_by_date = filter_transactions_by_date(
        transactions,
        date_end.strftime("%d.%m.%Y"),
        date_begin.strftime("%d.%m.%Y")
    )
    filter_by_category = filtered_by_date[filtered_by_date["Категория"] == category]

    return filter_by_category



if __name__ == "__main__":
    path_to_excel = os.path.join(PATH_DATA, "operations.xlsx")
    transactions = pd.read_excel(path_to_excel, parse_dates=True, date_format='%d.%m.%Y %H:%M:%S')
    result = spending_by_category(transactions, "Супермаркеты", "31.12.2021")
    print(result)
