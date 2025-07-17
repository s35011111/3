from typing import Any
from unittest.mock import patch

import pandas as pd

from src.views1 import (
    card_expenses,
    expenses_main,
    expenses_total,
    get_currency_rate,
    get_stoks_rate,
    income_main,
    income_total,
    top_transactions,
    transfers_and_cash,
)
from tests.conftest import data_list, data_list_empty


def test_card_expenses(data_list: pd.DataFrame) -> Any:
    assert card_expenses(data_list) == [
        {"last_digits": "", "total_spent": 31431.19, "cashback": 8},
        {"last_digits": "5091", "total_spent": 92.92, "cashback": 0},
        {"last_digits": "7197", "total_spent": 4033.31, "cashback": 5},
    ]


def test_card_expenses_empty(data_list_empty: pd.DataFrame) -> Any:
    assert card_expenses(data_list_empty) == []


def test_top_transactions(data_list: pd.DataFrame) -> Any:
    assert top_transactions(data_list) == [
        {"date": "31.12.2021", "amount": 20000.0, "category": "Переводы", "description": "Константин Л."},
        {"date": "25.12.2021", "amount": 3400.0, "category": "Развлечения", "description": "sevs.eduerp.ru"},
        {
            "date": "17.12.2021",
            "amount": 232.96,
            "category": "Услуги банка",
            "description": "Плата за Программу страховой защиты",
        },
        {"date": "23.12.2021", "amount": 201.0, "category": "Канцтовары", "description": "IP Mitrankov M V"},
        {"date": "06.12.2021", "amount": 179.77, "category": "Супермаркеты", "description": "Дикси"},
    ]


def test_top_transactions_empty(data_list_empty: pd.DataFrame) -> Any:
    assert top_transactions(data_list_empty) == []


def test_expenses_total(data_list: pd.DataFrame) -> Any:
    assert expenses_total(data_list) == 35557.42


def test_expenses_total_empty(data_list_empty: pd.DataFrame) -> Any:
    assert expenses_total(data_list_empty) == 0


def test_income_main(data_list: pd.DataFrame) -> Any:
    assert income_main(data_list) == 1100.0


def test_income_main_empty(data_list_empty: pd.DataFrame) -> Any:
    assert income_main(data_list_empty) == 0


def test_transfers_and_cash(data_list: pd.DataFrame) -> Any:
    assert transfers_and_cash(data_list) == {"Переводы": -31198.23}


def test_transfers_and_cash_empty(data_list_empty: pd.DataFrame) -> Any:
    assert transfers_and_cash(data_list_empty) == {}


def test_expenses_main(data_list: pd.DataFrame) -> Any:
    assert expenses_main(data_list) == [
        {"category": "Переводы", "amount": 20000.0},
        {"category": "Развлечения", "amount": 3400.0},
        {"category": "Услуги банка", "amount": 232.96},
        {"category": "Канцтовары", "amount": 201.0},
        {"category": "Супермаркеты", "amount": 179.77},
    ]


def test_expenses_main_empty(data_list_empty: pd.DataFrame) -> Any:
    assert expenses_main(data_list_empty) == []


def test_income_total(data_list: pd.DataFrame) -> Any:
    assert income_total(data_list) == [
        {"category": "Пополнения", "amount": 1100.0},
        {"category": "cashback", "amount": 13},
        {"category": "bonus", "amount": 78.0},
    ]


def test_income_total_empty(data_list_empty: pd.DataFrame) -> Any:
    assert income_total(data_list_empty) == []


@patch("requests.get")
def test_get_currency_rate(mock_requests: Any) -> Any:
    mock_requests.return_value.text = '{"rates":{"USD":0.0128221566868,"EUR":0.0109721307878}}'
    assert get_currency_rate(["USD", "EUR"]) == [
        {"currency": "USD", "rate": 77.99},
        {"currency": "EUR", "rate": 91.14},
    ]


@patch("requests.get")
def test_get_stoks_rate(mock_requests: Any) -> Any:
    mock_requests.return_value.text = (
        '[{"close":208.62},{"close": 225.69},{"close":181.56},{"close":503.02},{"close":316.9}]'
    )
    assert get_stoks_rate(["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]) == [
        {"stock": "AAPL", "price": 208.62},
        {"stock": "AMZN", "price": 225.69},
        {"stock": "GOOGL", "price": 181.56},
        {"stock": "MSFT", "price": 503.02},
        {"stock": "TSLA", "price": 316.9},
    ]
