import json
import logging
import pathlib
from typing import Any, Callable, Dict, Union

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


def report_noparam(function: Callable) -> Callable:
    """Выкладывает результат в файл JSON"""
    logger.debug("")

    def inner(*args: Any, **kwargs: Any) -> Any:
        result = function(*args, **kwargs)
        if isinstance(result, pd.DataFrame):
            df = result.replace({np.nan: None}).astype(object)
            result_ = df.to_dict()
            with open("report.json", "w") as f:
                json.dump(result_, f, ensure_ascii=False, indent=True)
        else:
            with open("report.json", "w") as f:
                json.dump(result, f, ensure_ascii=False, indent=True)

        return result

    return inner


def report_param(filename: Any = None) -> Callable:
    """Выкладывает результат в файл JSON, параметр - имя файла"""
    logger.debug("")

    def decorator_function(function: Callable) -> Callable:
        def inner(*args: Any, **kwargs: Any) -> Any:
            result = function(*args, **kwargs)
            if isinstance(result, pd.DataFrame):
                df = result.replace({np.nan: None}).astype(object)
                result_ = df.to_dict()
                with open(filename, "w") as f:
                    json.dump(result_, f, ensure_ascii=False, indent=True)
            else:
                with open(filename, "w") as f:
                    json.dump(result, f, ensure_ascii=False, indent=True)

            return result

        return inner

    return decorator_function


def expenses_dotw(df: pd.DataFrame) -> Union[dict, Any]:  #
    """Средние расходы по дням недели"""
    logger.debug("")
    if df.empty:
        return {}
    df = df[(df["sum"] < 0)]
    df.loc[:, ["day"]] = df["date"].dt.day_name()

    day_sum = df.groupby("day")["sum"].mean().round(2)
    res_dict = day_sum.to_dict()
    return res_dict


def spending_by_workday(df: pd.DataFrame) -> Dict:  #
    """Средние расходы в выходные и будние"""
    logger.debug("")
    if df.empty:
        return {}

    df = df[(df["sum"] < 0)]
    df.loc[:, ["day"]] = df["date"].dt.day_name()

    workday_df = df[
        (df["day"] == "Monday")
        | (df["day"] == "Tuesday")
        | (df["day"] == "Wednesday")
        | (df["day"] == "Thursday")
        | (df["day"] == "Friday")
    ]
    weekend_df = df[(df["day"] == "Saturday") | (df["day"] == "Sunday")]

    workday_sum = workday_df["sum"].mean()  # .round(2)
    weekend_sum = weekend_df["sum"].mean()  # .round(2)
    res_dict = {"Workday": round(workday_sum), "Weekend": round(weekend_sum)}
    return res_dict
