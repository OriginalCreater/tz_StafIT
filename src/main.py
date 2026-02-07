import csv
import argparse
from tabulate import tabulate


def merging_scan(files):
    result = []
    for info in files:
        try:
            with open(info, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row not in result:
                        if row != []:
                            result.append(row)
        except UnicodeDecodeError:
            print(f"Ошибка кодировки фаила '{info}'.")
            exit()
        except FileNotFoundError:
            print(f"Ошибка: Фаил '{info}' не найден.")
            exit()
        except PermissionError:
            print(f"Ошибка: Нет доступа к фаилу '{info}'.")
            exit()
        except Exception as e:
            print(f"Ошибка при чтении фаила '{info}'- {e}")
            exit(0)
    if result == []:
        print("Ошибка: Нет данных для обработки.")
        exit()
    return result


def search_col(cols, value):
    if not cols:
        print("Ошибка: Отсутствуют заголовки колонок.")
    try:
        col_name = cols[0]
        if value in col_name:
            col = col_name.index(value)
            return col
        else:
            print(f"Ошибка: Колонка '{value}' не наидена.")
            exit()
    except IndexError:
        print(f"Ошибка: Фаил пуст.")
        exit()


def sort_info_country(info, col_country, col_average):
    country_stats = {}
    for value in info[1:]:
        try:
            country_value = value[col_country]
            average_value = float(value[col_average])
            if country_value not in country_stats:
                country_stats[country_value] = {
                    'values': [],
                    'sum': 0,
                    'count': 0
                }
            country_stats[country_value]['values'].append(average_value)
            country_stats[country_value]['sum'] += average_value
            country_stats[country_value]['count'] += 1
        except IndexError:
            print("Ошибка: Присутствуют пустые строки")

    if not country_stats:
        print("Ошибка: Нет данных для анализа.")
        exit()
    return country_stats


def sort_value(sort_info):
    economic_info = []
    for country_value, stats in sort_info.items():
        info = []
        a_mean_value = stats['sum'] / stats['count']
        info.append(country_value)
        info.append(round(a_mean_value, 2)) # Округление до сотых
        economic_info.append(info)
    if not economic_info:
        print("Ошибка: Нет данных для анализа.")
        exit()
    try:
        economic_info.sort(key=lambda x: x[1], reverse=True) # Сортировка лябдой по 1 индексу вписного списка и реверсием
        return economic_info
    except IndexError:
        print("Ошибка: Недостаточно колонок в расчитаной таблице.")
        exit()


def main():
    parser = argparse.ArgumentParser(description='Анализ фаила')
    try:
        parser.add_argument('--files', nargs='+', help='--files')
    except NameError:
        print(r"Ошибка: фаил отсутствует или вы ошиблись в имени\пути")
        exit()
    try:
        parser.add_argument('--report', help='--report')
    except NameError:
        print("Ошибка: отсутствует искомый параметр")
        exit()
    args = parser.parse_args()
    file_list = []
    for i in args.files:
        file = str(i).split(".")
        name = file[-1]
        if name == "csv":
            file_list.append(i)
        else:
            name = f"{file[0]}.csv"
            file_list.append(name)
    average = str(args.report).split("-")[-1]
    country = str("country")
    merged_list = merging_scan(file_list)
    col_country = search_col(merged_list, country)
    col_average = search_col(merged_list, average)
    sort_info = sort_info_country(merged_list, col_country, col_average)
    finish_list = sort_value(sort_info)
    headers = [country, average]
    # Понял
    table = [tabulate(finish_list,
             headers=headers,
             tablefmt="presto",
             floatfmt=".2f",
             numalign="right",
             stralign="left",
             showindex=range(1, len(finish_list)+1))]
    print(tabulate([], headers=table, stralign='center', numalign='center', tablefmt="rounded_grid")) # Самый вонючий костыль


if __name__ == "__main__":
    main()
