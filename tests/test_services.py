from typing import Any

import pandas as pd

from src.services import investment_bank, names_search, phone_search, simple_search, top_cashback
from tests.conftest import data_list, data_list_empty


def test_top_cashback(data_list: pd.DataFrame) -> Any:
    assert top_cashback(data_list) == {"Канцтовары": 5, "Услуги банка": 8}


def test_top_cashback_empty(data_list_empty: pd.DataFrame) -> Any:
    assert top_cashback(data_list_empty) == {}


def test_investment_bank(data_list: pd.DataFrame) -> Any:
    assert investment_bank(data_list, 10) == 122.58
    assert investment_bank(data_list, 50) == 542.58


def test_investment_bank_empty(data_list_empty: pd.DataFrame) -> Any:
    assert investment_bank(data_list_empty, 10) == 0
    assert investment_bank(data_list_empty, 50) == 0


def test_simple_search(data_list: pd.DataFrame) -> Any:
    assert simple_search(data_list, "фастф").iloc[0, 6] == "Rumyanyj Khleb"
    assert simple_search(data_list, "Супермарк").iloc[0, 6] == "Дикси"


def test_simple_search_empty(data_list_empty: pd.DataFrame) -> Any:
    assert simple_search(data_list_empty, "фастф") == ""
    assert simple_search(data_list_empty, "Супермарк") == ""


def test_phone_search(data_list: pd.DataFrame) -> Any:
    assert phone_search(data_list).iloc[0, 6] == "IP Nelikaev +7 911 198-78-58"


def test_phone_search_empty(data_list_empty: pd.DataFrame) -> Any:
    assert phone_search(data_list_empty) == ""


def test_names_search(data_list: pd.DataFrame) -> Any:
    assert names_search(data_list).iloc[0, 6] == "Константин Л."


def test_names_search_empty(data_list_empty: pd.DataFrame) -> Any:
    assert names_search(data_list_empty) == ""
