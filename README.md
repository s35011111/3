 # Проект для анализа банковских транзакций
 
 ## Описание
Проект считывает информацию из XLSX c файла банковскими транзакциями. Предусмотрена возможность выбора отрезка времени на котором производить анализ. У проекта есть консольное приложение через которое можно задать параметры. Результат работы проекта - JSON файл с запрошеной информациейю

## Тестирование 
Проект прошел тестирование детальную  информацию можно найти в HTML.

## Функции и файлы содержащиеся в проекте
src\main.py	main
	
src\reports.py	report_noparam
src\reports.py	report_noparam.inner
src\reports.py	report_param
src\reports.py	report_param.decorator_function
src\reports.py	report_param.decorator_function.inner
src\reports.py	expenses_dotw
src\reports.py	spending_by_workday
	
src\services.py	top_cashback
src\services.py	investment_bank
src\services.py	simple_search
src\services.py	phone_search
src\services.py	names_search
	
src\utils.py	reading_excel
src\utils.py	reading_json
src\utils.py	output
src\utils.py	time_period
src\utils.py	beginin_period
src\utils.py	greeting
src\utils.py	main_page
src\utils.py	events
	
src\views1.py	card_expenses
src\views1.py	top_transactions
src\views1.py	expenses_total
src\views1.py	income_main
src\views1.py	transfers_and_cash
src\views1.py	expenses_main
src\views1.py	income_total
src\views1.py	get_currency_rate
src\views1.py	get_stoks_rate