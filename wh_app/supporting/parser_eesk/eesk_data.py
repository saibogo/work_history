import pandas as pd
import requests
from datetime import date, datetime

from wh_app.supporting.parser_eesk.parser_config import url_eesk
from wh_app.supporting.parser_eesk.eesk_exception import EeskException
from wh_app.supporting import functions
from wh_app.postgresql.database import Database
from wh_app.sql_operations.select_operations.select_operations import get_all_find_patterns

functions.info_string(__name__)


def is_cell_correct(cell) -> bool:
    """True if cell not empty"""
    return not pd.isnull(cell)


def is_row_correct(row) -> bool:
    """True if all cell in row correct"""
    result = True
    for cell in row:
        result = result and is_cell_correct(cell)
    return result


def is_date_correct(cell) -> bool:
    """date >= date_now"""
    try:
        return date.today() <= datetime.strptime(str(cell), "%Y-%m-%d %H:%M:%S").date()
    except:
        return False


def is_row_with_correct_date(row) -> bool:
    """True if one or more cells with correct_date"""
    result = False
    for cell in row:
        result = result or is_date_correct(cell)
    return result


def is_cell_equal_pattern(cell) -> bool:
    """True if one or more string from patterns found in cell"""
    pattern_list = []
    with Database() as base:
        _, cursor = base
        pattern_list = get_all_find_patterns(cursor)
    for pattern in pattern_list:
        if pattern.lower() in str(cell).lower():
            return True
    return False


def is_row_equal_pattern(row) -> bool:
    """True if one or more string from patterns found in row"""
    for cell in row:
        if is_cell_equal_pattern(cell):
            return True
    return False


def get_eesk_data() -> list:
    """Return all correct data from eesk"""
    try:
        print("Попытка получения данных с {}".format(url_eesk))
        response = requests.get(url_eesk)
        result_data = []

        with open("result.xls", "wb") as file:
            file.write(response.content)

        df = pd.read_excel('result.xls', sheet_name='Плановые отключения')
        rows_count = len(df)
        print("Всего строк получено {}".format(rows_count))

        for index, row in df.iterrows():
            if is_row_correct(row):  # строки не содержат пустых ячеек
                if is_row_with_correct_date(row):  # хотя бы одна из ячеек дата и дата больше текущей
                    if is_row_equal_pattern(row):  # Хотя бы одна ячейка соответствует хотя бы одному паттерну из списка
                        result_data.append([str(elem) for elem in row])
        return result_data
    except:
        raise EeskException




