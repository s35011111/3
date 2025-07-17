import json
from typing import Any

import pandas as pd

from src.reports import expenses_dotw, report_noparam, report_param, spending_by_workday
from src.utils import output
from tests.conftest import data_list, data_list_empty


def test_expenses_dotw(data_list: pd.DataFrame) -> Any:
    assert expenses_dotw(data_list) == {
        "Friday": -133.48,
        "Monday": -179.77,
        "Saturday": -1761.77,
        "Sunday": -42.92,
        "Thursday": -10067.0,
        "Tuesday": -646.62,
        "Wednesday": -50.0,
    }


def test_expenses_dotw_empty(data_list_empty: pd.DataFrame) -> Any:
    assert expenses_dotw(data_list_empty) == {}


def test_spending_by_workday(data_list: pd.DataFrame) -> Any:
    assert spending_by_workday(data_list) == {"Workday": -3555, "Weekend": -1189}


def test_spending_by_workday_empty(data_list_empty: pd.DataFrame) -> Any:
    assert spending_by_workday(data_list_empty) == {}


def test_report_noparam(data_list: pd.DataFrame) -> Any:
    @report_noparam
    def json_test(df: pd.DataFrame) -> Any:
        df = df["card_num"].unique()
        res = {"1": df[0], "2": df[1], "3": df[2]}
        return res

    json_test(data_list)
    with open("report.json") as f:
        data = json.load(f)
    assert data == {"1": "", "2": "*7197", "3": "*5091"}


def test_report_param(data_list: pd.DataFrame) -> Any:
    @report_param("report_.json")
    def json_test(df: pd.DataFrame) -> Any:
        df = df["card_num"].unique()
        res = {"1": df[0], "2": df[1], "3": df[2]}
        return res

    json_test(data_list)
    with open("report_.json") as f:
        data = json.load(f)
    assert data == {"1": "", "2": "*7197", "3": "*5091"}
