import os

import pytest

from config import PATH_DATA, PATH_REPORTS
from src.reports import report_to_file
import pandas as pd

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