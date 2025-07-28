import json
import logging
import pathlib
from datetime import timedelta
from typing import Any

import pandas as pd
from dateutil.relativedelta import relativedelta

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

logger = logging.getLogger(__name__)
projectdir = pathlib.Path(__file__).parent.parent
logfilename = projectdir / "log.log"

file_handler = logging.FileHandler(logfilename, "w")
logger.addHandler(file_handler)
file_formatter = logging.Formatter("%(asctime)s %(filename)s %(levelname)s %(funcName)s %(message)s")
file_handler.setFormatter(file_formatter)
logger.setLevel(logging.DEBUG)


def reading_excel(transactions_file: pathlib.Path) -> Any:
    """excel-файл -> список словарей"""
    logger.debug("")
    try:
        result_df = pd.read_excel(transactions_file)
        result_df.columns = [
            "date",
            "date_payment",
            "card_num",
            "status",
            "sum",
            "curency",
            "sum_payment",
            "curency_payment",
            "cashback",
            "category",
            "mcc",
            "descript",
            "bonus",
            "rounding",
            "sum_rounding",
        ]
        result_df["date"] = pd.to_datetime(result_df["date"], format="%d.%m.%Y %H:%M:%S")
        return result_df
    except FileNotFoundError:
        return []


def reading_json(operations_file: pathlib.Path) -> Any:
    """JSON-файл -> список словарей"""
    logger.debug("")
    try:
        with open(operations_file, "r", encoding="utf-8", errors="replace") as f:
            result_dict = json.load(f)
        return result_dict
    except FileNotFoundError:
        return []


def output(dict_: dict) -> None:
    """список словарей -> JSON"""
    logger.debug("")
    for k, v in dict_.items():
        print(k, v)
    with open("report.json", "w", encoding="utf-8") as f:
        json.dump(dict_, f, ensure_ascii=False, indent=True)


def time_period(begin_t: Any, time_t: Any, df: pd.DataFrame) -> pd.DataFrame:
    """Выбор строк из DataFrame попадающих в период времени"""
    logger.debug("")
    return df[(df["date"] >= begin_t) & (df["date"] <= time_t)]


def beginin_period(time_t: Any, n: int) -> Any:
    """определение начальной даты"""
    logger.debug("")
    if n == 1:
        return time_t - timedelta(days=time_t.weekday())  # начало недели
    elif n == 2:
        return time_t.replace(day=1)  # начало месяца
    elif n == 3:
        return time_t.replace(month=1, day=1)  # начало года
    elif n == 4:
        return time_t - relativedelta(months=1)  # месяц назад
    elif n == 5:
        return time_t - relativedelta(months=3)  # три месяца назад
    elif n == 6:
        return time_t - relativedelta(years=1)  # год назад
    else:
        return time_t - relativedelta(years=30)  # все


def greeting(time_t: Any) -> str:
    """тип приветствия по дате"""
    logger.debug("")
    if time_t.hour <= 0 and time_t.hour < 6:
        return "Доброе утро"
    elif time_t.hour <= 6 and time_t.hour < 12:
        return "Добрый день"
    elif time_t.hour <= 12 and time_t.hour < 18:
        return "Добрый вечер"
    elif time_t.hour <= 18:
        return "Доброй ночи"
    else:
        return "Добрый день"


def main_page(df: pd.DataFrame, time_t: Any) -> dict:
    """главная страница"""
    logger.debug("")
    projectdir_ = pathlib.Path(__file__).parent.parent
    filename_ = projectdir_ / "data/user_settings.json"
    user_settings = reading_json(filename_)
    res_dict = {
        "greeting": greeting(time_t),
        "cards": card_expenses(df),
        "top_transactions": top_transactions(df),
        "currency_rates": get_currency_rate(user_settings["user_currencies"]),
        "stock_prices": get_stoks_rate(user_settings["user_stocks"]),
    }
    return res_dict


def events(df: pd.DataFrame) -> dict:
    """Страница событий"""
    logger.debug("")
    projectdir_ = pathlib.Path(__file__).parent.parent
    filename_ = projectdir_ / "data/user_settings.json"
    user_settings = reading_json(filename_)
    res_dict = {
        "expenses": {
            "total_amount": expenses_total(df),
            "main": expenses_main(df),
            "transfers_and_cash": transfers_and_cash(df),
        },
        "income": {"total_amount": income_total(df), "main": income_main(df)},
        "currency_rates": get_currency_rate(user_settings["user_currencies"]),
        "stock_prices": get_stoks_rate(user_settings["user_stocks"]),
    }
    return res_dict


# Дата операции	Дата платежа	Номер карты	Статус	Сумма операции	Валюта операции	Сумма платежа	Валюта платежа	Кэшбэк	Категория	MCC	Описание	Бонусы (включая кэшбэк)	Округление на инвесткопилку	Сумма операции с округлением

"""df.columns=["date","date_payment","card_num","status", "sum","curency", "sum_payment", "curency_payment","cashback","category","mcc","descript","bonus", "rounding","sum_rounding"]
for i in df.card_num.unique():
    print(i)"""
