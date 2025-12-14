import json
import os

import pandas as pd

from config import PATH_DATA
from src.reports import spending_by_category
from src.services import get_best_categories
from src.views import get_response


def main():
    """
    Функция демонстрирующая основные возможности проекта.
    """
    path_to_excel = os.path.join(PATH_DATA, "operations.xlsx")
    df = pd.read_excel(path_to_excel, parse_dates=True, date_format='%d.%m.%Y %H:%M:%S')
    data_json = json.loads(df.to_json(orient="records"))
    best_categories = get_best_categories(data_json, 2021, 12)
    print(json.dumps(best_categories, indent=4, ensure_ascii=False))
    print(json.dumps(get_response("2021-12-30 00:00:00"), indent=4))
    spending_by_category(df, "Супермаркеты", "31.12.2021")


if __name__ == "__main__":
    main()
