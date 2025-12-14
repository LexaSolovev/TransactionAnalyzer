import json
import os
from datetime import datetime

import src.utils
from config import PATH_DATA


def get_response(date: str) -> dict:
    """
    Функция главной страницы, принимает дату в виде строки формата YYYY-MM-DD HH:MM:SS
    Возвращает ответ в виде словаря
    """
    date_obj = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

    path_to_excel = os.path.join(PATH_DATA, "operations.xlsx")
    path_to_user_settings = os.path.join(PATH_DATA, "user_settings.json")
    transactions_df = src.utils.get_transactions_df_from_excel(path_to_excel)
    filtered_trs_by_date = src.utils.filter_transactions_by_date(transactions_df, date_obj.strftime("%d.%m.%Y"))

    current_date = datetime.now()
    with open(path_to_user_settings) as f:
        user_settings = json.load(f)
        user_currencies = user_settings.get("user_currencies")
        user_stocks = user_settings.get("user_stocks")

    result = {
        "greeting": src.utils.greeting(current_date.strftime("%Y-%m-%d %H:%M:%S")),
        "cards": src.utils.get_cards(filtered_trs_by_date),
        "top_transactions": src.utils.get_top_transactions(filtered_trs_by_date),
        "currency_rates": src.utils.get_currencies_rates(user_currencies),
        "stock_prices": src.utils.get_stock_prices(user_stocks)
    }
    return result


if __name__ == "__main__":
    print(get_response("2021-12-30 00:00:00"))
