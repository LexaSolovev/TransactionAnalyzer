import os
from datetime import datetime
from functools import wraps
from typing import Optional

import pandas as pd
from dateutil.relativedelta import relativedelta


from config import PATH_DATA, PATH_REPORTS
from src.utils import filter_transactions_by_date

def report_to_file(file_name :str="default_report"):
    def inner(func):
        @wraps(func)
        def wrapper(*args,**kwargs):
            result = func(*args, **kwargs)
            path_to_report = os.path.join(PATH_REPORTS, file_name + ".xlsx")
            result.to_excel(path_to_report, index=False)
            return result
        return wrapper
    return inner


@report_to_file("spending_by_category")
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
    filter_by_category["Дата операции"] = filter_by_category["Дата операции"].dt.strftime('%d.%m.%Y %H:%M:%S')
    return filter_by_category



if __name__ == "__main__":
    path_to_excel = os.path.join(PATH_DATA, "operations.xlsx")
    transactions_df = pd.read_excel(path_to_excel, parse_dates=True, date_format='%d.%m.%Y %H:%M:%S')
    spent = spending_by_category(transactions_df, "Супермаркеты", "31.12.2021")
    print(spent)
