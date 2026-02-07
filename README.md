Приветствую.

Надеюсь я справился.

Понимаю что прошу возможно лишнего, но если я допустил где-то ошибку или есть замечания критические прошу сообщить.


Установка зависимостей:

pip install -r requirements.txt ----> для запуска

pip install -r requirements_test.txt ----> для тестирования

Запуск:

python src/main.py --files economic1.csv economic2.csv --report average-gdp
python src/main.py --files economic1.xls economic2.csv economic3.xlsx  economic4.py --report average-gdp
python src/main.py --files economic2.txt --report average-inflation
python src/main.py --files economic1.csv economic2.py --report average-population

python src/main.py --files ВАШИ ФАИЛЫ --report average-gdp

Тестирование:

pytest
pytest tests/test_main_integration.py
pytest tests/test_economic_analysis.py
pytest tests/test_economic_analysis.py::test_merging_scan_reads_file -v
pytest tests/test_economic_analysis.py::test_search_col_finds_column -v
pytest tests/test_economic_analysis.py::test_sort_info_country_groups_data -v
pytest tests/test_economic_analysis.py::test_sort_value_calculates_averages -v
pytest tests/test_economic_analysis.py::test_full_process_simple -v
pytest tests/test_economic_analysis.py::test_empty_file -v
pytest tests/test_economic_analysis.py::test_duplicate_rows -v
pytest tests/test_economic_analysis.py::test_column_not_found -v
pytest tests/test_economic_analysis.py::test_single_file_processing -v
pytest tests/test_economic_analysis.py::test_invalid_number_handling -v
