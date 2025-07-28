import json
import logging
import os
import pathlib
from typing import Any, List, Union

import numpy as np
import pandas as pd
import requests
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
projectdir = pathlib.Path(__file__).parent.parent
logfilename = projectdir / "log.log"

file_handler = logging.FileHandler(logfilename, "w")
logger.addHandler(file_handler)
file_formatter = logging.Formatter("%(asctime)s %(filename)s %(levelname)s %(funcName)s %(message)s")
file_handler.setFormatter(file_formatter)
logger.setLevel(logging.DEBUG)


def card_expenses(df: pd.DataFrame) -> List:
    """Потрачено по картам"""
    logger.debug("")
    if df.empty:
        return []
    df = df[df["sum"] < 0]
    sum_df = df.groupby("card_num")[["sum", "cashback"]].sum()
    sum_df = sum_df.replace({np.nan: None}).astype(object)
    sum_dict = sum_df.to_dict("index")  # "records"keys_=["last_digits","total_spent","cashback"]
    lst_res = []
    for k, v in sum_dict.items():
        res = {"last_digits": k[1:], "total_spent": v["sum"] * (-1), "cashback": v["cashback"]}
        lst_res.append(res)
    return lst_res


def top_transactions(df: pd.DataFrame) -> List:  #
    """Наибольшие транзакции"""
    logger.debug("")
    if df.empty:
        return []
    top_df = df.sort_values("sum", ascending=True).groupby("category").head(1).reset_index(drop=True)
    top_df = top_df.loc[:, ["date_payment", "category", "sum", "descript"]]
    sum_df = top_df.replace({np.nan: None}).astype(object)
    sum_dict = sum_df.to_dict("index")

    lst_res = []
    for k, v in sum_dict.items():  # "date" "amount" "category" "description"
        res = {
            "date": v["date_payment"],
            "amount": v["sum"] * (-1),
            "category": v["category"],
            "description": v["descript"],
        }
        lst_res.append(res)
        if k > 3:
            break
    return lst_res


def expenses_total(df: pd.DataFrame) -> Union[float, int, Any]:
    """Расходов всего"""
    logger.debug("")
    if df.empty:
        return 0
    expenses_df = df[df["sum"] < 0]
    res = expenses_df["sum"].sum() * (-1)
    return round(res, 2)


def income_main(df: pd.DataFrame) -> Union[float, int, Any]:
    """Основной доход"""
    logger.debug("")

    if df.empty:
        return 0
    income_df = df[df["sum"] > 0]
    res = income_df["sum"].sum()
    return res


def transfers_and_cash(df: pd.DataFrame) -> Union[dict, Any]:
    """Переводы и наличные"""
    logger.debug("")
    if df.empty:
        return {}
    transfers_df = df[(df["category"] == "Наличные") | (df["category"] == "Переводы")]
    sum_df = transfers_df.groupby("category")["sum"].sum()
    sum_df = sum_df.replace({np.nan: None}).astype(object)
    sum_dict = sum_df.to_dict()

    return sum_dict


def expenses_main(df: pd.DataFrame) -> List:
    """Основные расходы"""
    logger.debug("")
    if df.empty:
        return []
    expenses_df = df[df["sum"] < 0]
    top_df = expenses_df.sort_values("sum", ascending=True).groupby("category").head(1).reset_index(drop=True)
    top_df = top_df.loc[:, ["category", "sum"]]
    sum_df = top_df.replace({np.nan: None}).astype(object)
    sum_dict = sum_df.to_dict("index")

    lst_res = []
    for k, v in sum_dict.items():

        res = {"category": v["category"], "amount": v["sum"] * (-1)}
        lst_res.append(res)
        if k > 3:
            break
    return lst_res


def income_total(df: pd.DataFrame) -> List:
    """Доход всего"""
    logger.debug("")
    if df.empty:
        return []
    income_df = df[df["sum"] > 0]
    top_df = income_df.groupby("category")["sum"].sum()
    sum_df = top_df.replace({np.nan: None}).astype(object)
    sum_dict = sum_df.to_dict()
    cashback = df["cashback"].sum()
    bonus_df = df[(df["bonus"] > 0) & (df["cashback"] == 0)]  # np.nan
    bonus = bonus_df["bonus"].sum()
    lst_res = []
    counter = 0
    for k, v in sum_dict.items():
        res = {"category": k, "amount": v}
        lst_res.append(res)
        if counter > 3:
            break
        counter += 1
    if cashback != 0:
        lst_res.append({"category": "cashback", "amount": int(cashback)})
    if bonus != 0:
        lst_res.append({"category": "bonus", "amount": float(bonus)})

    return lst_res


def get_currency_rate(currencies_lst: List) -> list[dict[str, str | Any]]:
    """Курсы валют"""
    logger.debug("")
    try:
        load_dotenv()
        api_token = os.getenv("API_KEY")
        headers_ = {"apikey": f"{api_token}"}
        url = f"https://api.apilayer.com/exchangerates_data/latest?base=RUB"
        response = requests.get(url, headers=headers_)
        response_data = json.loads(response.text)

        rate_0 = 1 / response_data["rates"][currencies_lst[0]]
        rate_1 = 1 / response_data["rates"][currencies_lst[1]]
        res_0 = {"currency": currencies_lst[0], "rate": round(rate_0, 2)}
        res_1 = {"currency": currencies_lst[1], "rate": round(rate_1, 2)}
        res = [res_0, res_1]
        return res  ## [{'currency': 'USD', 'rate': 77.99}, {'currency': 'EUR', 'rate': 91.14}]
    except Exception:
        return [
            {"currency": currencies_lst[0], "rate": "нет данных"},
            {"currency": currencies_lst[1], "rate": "нет данных"},
        ]


def get_stoks_rate(stoks_lst: List) -> Union[list[dict[str, str | Any]], list[str]]:
    """Курсы акций"""
    logger.debug("")
    try:
        load_dotenv()
        apy_key = os.getenv("API_TOKEN")
        res = []
        for i in stoks_lst:
            params_ = {"tickers": i, "token": apy_key, "format": "json"}
            url = f"https://api.tiingo.com/tiingo/daily/prices"
            response = requests.get(url, params=params_)
            response_data = json.loads(response.text)  ##

            res.append({"stock": i, "price": response_data[0]["close"]})

        return res  # [{'stock': 'AAPL', 'price': 208.62}, {'stock': 'AMZN', 'price': 225.69}, {'stock': 'GOOGL', 'price': 181.56}, {'stock': 'MSFT', 'price': 503.02}, {'stock': 'TSLA', 'price': 316.9}]
    except Exception:
        return ["нет данных"]
