import pytest
import tempfile
import os
import csv
from src.main import merging_scan, search_col, sort_info_country, sort_value


def test_merging_scan_reads_file():
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
        f.write("country,inflation\nUSA,3.4\nRussia,7.4\n")
        filename = f.name
    try:
        result = merging_scan([filename])
        assert len(result) == 3
        assert result[0] == ['country', 'inflation']
        assert ['USA', '3.4'] in result
    finally:
        os.unlink(filename)


def test_search_col_finds_column():
    data = [['country', 'inflation', 'gdp']]
    result = search_col(data, 'inflation')
    assert result == 1


def test_sort_info_country_groups_data():
    data = [
        ['country', 'inflation'],
        ['USA', '3.4'],
        ['USA', '8.0'],
        ['Russia', '7.4']
    ]
    result = sort_info_country(data, 0, 1)
    assert 'USA' in result
    assert 'Russia' in result
    assert result['USA']['count'] == 2
    assert result['USA']['sum'] == 11.4


def test_sort_value_calculates_averages():
    test_data = {
        'USA': {'sum': 11.4, 'count': 2},
        'Russia': {'sum': 7.4, 'count': 1}
    }
    result = sort_value(test_data)
    assert len(result) == 2
    if result[0][0] == 'USA':
        assert result[0][1] == 5.7
        assert result[1][0] == 'Russia'
    else:
        assert result[0][0] == 'Russia'
        assert result[1][0] == 'USA'


def test_full_process_simple():
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['country', 'inflation'])
        writer.writerow(['USA', '3.4'])
        writer.writerow(['USA', '8.0'])
        writer.writerow(['Russia', '7.4'])
        filename = f.name

    try:
        data = merging_scan([filename])
        country_col = search_col(data, 'country')
        inflation_col = search_col(data, 'inflation')
        grouped = sort_info_country(data, country_col, inflation_col)
        result = sort_value(grouped)
        assert len(result) == 2
        if result[0][0] == 'USA':
            assert result[0][1] == 5.7
            assert result[1][0] == 'Russia'
        else:
            assert result[0][0] == 'Russia'
            assert result[1][0] == 'USA'

    finally:
        os.unlink(filename)


def test_empty_file():
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
        filename = f.name
    try:
        with pytest.raises(SystemExit):
            merging_scan([filename])
    finally:
        if os.path.exists(filename):
            os.unlink(filename)


def test_duplicate_rows():
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['country', 'inflation'])
        writer.writerow(['USA', '3.4'])
        writer.writerow(['USA', '3.4'])
        writer.writerow(['USA', '3.4'])
        filename = f.name
    try:
        data = merging_scan([filename])
        assert len(data) == 2
    finally:
        os.unlink(filename)


def test_column_not_found():
    data = [['country', 'inflation']]
    with pytest.raises(SystemExit):
        search_col(data, 'nonexistent')


def test_invalid_number_handling():
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['country', 'inflation'])
        writer.writerow(['USA', '3.4'])
        writer.writerow(['USA', 'not_a_number'])
        writer.writerow(['USA', '5.0'])
        filename = f.name
    try:
        data = merging_scan([filename])
        with pytest.raises(ValueError):
            sort_info_country(data, 0, 1)
    finally:
        os.unlink(filename)



def test_single_file_processing():
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['country', 'gdp', 'inflation'])
        writer.writerow(['Germany', '4086', '6.2'])
        writer.writerow(['France', '2788', '5.7'])
        filename = f.name
    try:
        data = merging_scan([filename])
        assert len(data) == 3
        country_col = search_col(data, 'country')
        inflation_col = search_col(data, 'inflation')
        assert country_col == 0
        assert inflation_col == 2
    finally:
        os.unlink(filename)