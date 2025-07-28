import logging
import pathlib
import re
from typing import Dict, Union

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)
projectdir = pathlib.Path(__file__).parent.parent
logfilename = projectdir / "log.log"

file_handler = logging.FileHandler(logfilename, "w")
logger.addHandler(file_handler)
file_formatter = logging.Formatter("%(asctime)s %(filename)s %(levelname)s %(funcName)s %(message)s")
file_handler.setFormatter(file_formatter)
logger.setLevel(logging.DEBUG)


def top_cashback(df: pd.DataFrame) -> Dict:  #
    """Наибольший кешбак по категории"""
    logger.debug("")
    if df.empty:
        return {}
    cashback_df = df.groupby("category")["cashback"].sum()
    cashback_df = cashback_df.replace({np.nan: None}).astype(object)
    cashback_dict = cashback_df.to_dict()
    res_dict = {}
    for k, v in cashback_dict.items():
        if v != 0:
            res_dict[k] = v
    return res_dict


def investment_bank(df: pd.DataFrame, n: int) -> Union[int, float]:
    """Инвесткопилка"""
    logger.debug("")
    if df.empty:
        return 0
    if n == 0:
        return 0
    expenses_df = df[(df["sum"] <= 0) & (df["sum"] % n != 0)]
    total = (n - (expenses_df["sum"].dropna() % n) * (-1)).sum()
    return round(total, 2)


def simple_search(df: pd.DataFrame, n_str: str) -> Union[pd.DataFrame, str]:
    """Поиск по слову"""
    logger.debug("")
    if df.empty:
        return ""
    res_df = df[
        (df["category"].str.contains(n_str, flags=re.IGNORECASE))
        | (df["descript"].str.contains(n_str, flags=re.IGNORECASE))
    ]
    return res_df


def phone_search(df: pd.DataFrame) -> Union[pd.DataFrame, str]:
    """Поиск телефонов"""
    logger.debug("")
    if df.empty:
        return ""
    res_df = df[(df["descript"].str.contains(r"\d{3}"))]
    return res_df


def names_search(df: pd.DataFrame) -> Union[pd.DataFrame, str]:
    """Поиск имен физ. лиц"""
    logger.debug("")
    if df.empty:
        return ""
    n_str = r"\b\s.\."
    res_df = df[
        (df["category"].str.contains("перевод", flags=re.IGNORECASE))
        | (df["descript"].str.contains("перевод", flags=re.IGNORECASE))
    ]
    res_df = res_df[(res_df["category"].str.contains(n_str)) | (res_df["descript"].str.contains(n_str))]
    return res_df
