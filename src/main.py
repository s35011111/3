import datetime
import pathlib

from src.reports import expenses_dotw, spending_by_workday
from src.services import investment_bank, names_search, phone_search, simple_search, top_cashback
from src.utils import beginin_period, events, main_page, output, reading_excel, time_period

projectdir = pathlib.Path(__file__).parent.parent
filename_ = projectdir / "data/operations.xlsx"


def main() -> None:
    n = 0
    df = reading_excel(filename_)
    input_1 = input("дата?")
    if input_1 == "":
        input_1 = "2020-06-26 14:23:40"
    time_t = datetime.datetime.strptime(input_1, "%Y-%m-%d %H:%M:%S")

    input_2 = input("тип отчета?")
    if input_2 == "1":
        df = time_period(beginin_period(time_t, 2), time_t, df)
        dict_ = main_page(df, time_t)
        output(dict_)

    elif input_2 == "2":
        input_3 = input("начальная точка во времени? неделя (1),месяц(2), год(3)")
        if input_3 == "1":
            n = 1
        elif input_3 == "2":
            n = 2
        elif input_3 == "3":
            n = 3
        else:
            n = 10
        df = time_period(beginin_period(time_t, n), time_t, df)
        dict_ = events(df)
        output(dict_)

    else:
        input_3 = input(
            "1.top_cashback\n2.investment_bank\n3.simple_search\n4.phone_search\n5.names_search\n6.expenses_dotw\n7.spending_by_workday"
        )
        if input_3 == "1":
            df = time_period(beginin_period(time_t, 4), time_t, df)
            dict_ = top_cashback(df)
            output(dict_)
        if input_3 == "2":
            df = time_period(beginin_period(time_t, 2), time_t, df)
            input_4 = int(input("передел?"))
            print(investment_bank(df, input_4))

        if input_3 == "3":
            df = time_period(beginin_period(time_t, 10), time_t, df)
            input_4 = str(input("строка поиска?"))
            print(simple_search(df, str(input_4)))

        if input_3 == "4":
            df = time_period(beginin_period(time_t, 10), time_t, df)
            print(phone_search(df).loc[:,["category","descript"]])

        if input_3 == "5":
            df = time_period(beginin_period(time_t, 10), time_t, df)
            print(names_search(df).loc[:,["date","sum","descript"]])

        if input_3 == "6":
            df = time_period(beginin_period(time_t, 5), time_t, df)
            dict_ = expenses_dotw(df)
            output(dict_)
        if input_3 == "7":
            df = time_period(beginin_period(time_t, 5), time_t, df)
            dict_ = spending_by_workday(df)
            output(dict_)


main()
