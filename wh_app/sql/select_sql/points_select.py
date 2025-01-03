"""This module contain all SELECT to POINT"""

from typing import *
from datetime import datetime

from wh_app.sql.sql_constant import sql_consts_dict
from wh_app.config_and_backup import config


def limit_and_offset(page_num: int) -> str:
    """Return substring like LIMIT 5 OFFSET 7"""

    return " LIMIT {0} OFFSET {1}".format(config.max_records_in_page(),
                        (int(page_num) - 1) * config.max_records_in_page())


def log_decorator(func: Callable) -> Callable:
    """This decorator insert new record in log-file for function"""
    def wrap(*args) -> str:
        tmp = func(*args)
        try:
            with open(config.path_to_sql_log(), 'a') as log_file:
                log_file.write("====\n")
                log_file.write(str(datetime.now()) + '\n')
                log_file.write(tmp + '\n')
        except OSError:
            print("Невозможно записать данные в лог-файл!")
        return tmp
    return wrap


@log_decorator
def sql_select_point(id_point: str) -> str:
    """Returns the string of the query for selecting a point by a unique number
    Example:
     SELECT point_id, point_name, point_address, CASE WHEN is_work = true
     THEN 'Open' ELSE 'Closed' END
     FROM workspoints WHERE point_id = 13 ORDER BY point_name"""

    formatter = ("WHERE %(point_id)s = " % sql_consts_dict + str(id_point))\
        if (str(id_point) != '' and str(id_point) != '0') else ""

    query = """SELECT %(point_id)s, %(point_name)s, %(point_address)s,
     %(cast_open_close)s 
     FROM %(workspoints)s {0} ORDER BY %(point_name)s""" % sql_consts_dict
    return query.format(formatter)


@log_decorator
def sql_select_all_works_points() -> str:
    """Return the string of the query for selected a point where status is 'work'
    Example:
    SELECT point_id, point_name, point_address,
    CASE WHEN is_work = true THEN 'Работает' ELSE 'Закрыто' END
    FROM workspoints WHERE is_work = true ORDER BY point_name"""

    return ("""SELECT %(point_id)s, %(point_name)s, %(point_address)s, """ +
            """%(cast_open_close)s FROM %(workspoints)s""" +
            """ WHERE %(point_working)s ORDER BY %(point_name)s""") % sql_consts_dict


@log_decorator
def sql_select_information_to_point(id_point: str) -> str:
    """Returns the string of the request for complete information
    about the point with the given number
    Example:
        SELECT point_name, point_address FROM workspoints WHERE point_id = id_point
        """

    query = ("""SELECT %(point_name)s, %(point_address)s, %(cast_open_close)s  """ +
             """FROM %(workspoints)s WHERE %(point_id)s = {0}""") % sql_consts_dict
    return query.format(id_point)


@log_decorator
def sql_select_point_from_like_str(pattern: str) -> str:
    """Return the query string select points from like-string
    Example:
        SELECT * FROM workspoints
        WHERE (LOWER(point_name) LIKE LOWER('PoINT'))
        OR
        (LOWER(point_address) LIKE LOWER('PoINT'))
        ORDER BY point_name
        """

    if pattern != '*':
        like_string = '%' + pattern.replace(' ', '%') + '%'
        query = ("""SELECT * FROM %(workspoints)s WHERE (LOWER(%(point_name)s)""" +
                 """ LIKE LOWER('{0}')) OR (LOWER(%(point_address)s) LIKE""" +
                 """ LOWER('{0}')) ORDER BY %(point_name)s""") % sql_consts_dict

        result = query.format(like_string)
    else:
        query = ("""SELECT * FROM %(workspoints)s  ORDER BY %(point_name)s""") %\
                sql_consts_dict
        result = query
    return result


@log_decorator
def sql_select_point_from_like_str_limit(pattern: str, page_num: str) -> str:
    """Return the query string select points from like-string
    Example:
        SELECT point_id, point_name, point_address,
        CASE WHEN is_work = true THEN 'Работает' ELSE 'Закрыто' END
        FROM workspoints WHERE (LOWER({point_name})
        LIKE LOWER('Пб')) OR (LOWER(point_address) LIKE LOWER('Пб'))
        ORDER BY point_name LIMIT 15 OFFSET 45
        """

    if pattern != '*':
        like_string = '%' + pattern.replace(' ', '%') + '%'
        query = ("""SELECT %(point_id)s, %(point_name)s, %(point_address)s,""" +
                 """ %(cast_open_close)s FROM %(workspoints)s WHERE""" +
                 """ (LOWER(%(point_name)s) LIKE LOWER('{0}')) OR """ +
                 """ (LOWER(%(point_address)s) LIKE LOWER('{0}')) ORDER BY """ +
                 """ %(point_name)s """) % sql_consts_dict + limit_and_offset(page_num)

        result = query.format(like_string)
    else:
        query = ("""SELECT %(point_id)s, %(point_name)s, %(point_address)s,""" +
                 """ %(cast_open_close)s FROM %(workspoints)s ORDER BY""" +
                 """ %(point_name)s """) % sql_consts_dict + limit_and_offset(page_num)
        result = query
    return result


@log_decorator
def sql_select_max_id_point() -> str:
    """Return the query string select maximal number in column point_id in table workspoints"""

    return """SELECT MAX(%(point_id)s) FROM %(workspoints)s""" % sql_consts_dict


@log_decorator
def sql_select_top_points() -> str:
    """Return query contain SELECT-strintg to 10 first string in point -> sum works"""

    query = ("""SELECT %(workspoints)s.%(point_id)s, %(point_name)s, COUNT(%(works)s.%(id)s) AS all_works,
     MIN(works.date), MAX(works.date), (SELECT COUNT(%(works)s.%(id)s) FROM %(works)s JOIN %(oborudovanie)s 
     ON %(oborudovanie)s.%(point_id)s = %(workspoints)s.%(point_id)s WHERE %(works)s.%(date)s >= last_year_date() 
     AND %(works)s.%(id_obor)s = %(oborudovanie)s.%(id)s) AS lastyear, (SELECT COUNT(%(works)s.%(id)s) FROM %(works)s 
     JOIN %(oborudovanie)s ON %(oborudovanie)s.%(point_id)s = %(workspoints)s.%(point_id)s WHERE %(works)s.%(date)s >= 
     last_month_date() AND %(works)s.%(id_obor)s = %(oborudovanie)s.%(id)s) AS lastmonth, (SELECT COUNT(%(works)s.%(id)s) 
     FROM %(works)s JOIN %(oborudovanie)s ON %(oborudovanie)s.%(point_id)s = %(workspoints)s.%(point_id)s WHERE 
     %(works)s.%(date)s >= last_day_date() AND %(works)s.%(id_obor)s = %(oborudovanie)s.%(id)s) AS lastday
    FROM %(workspoints)s JOIN %(oborudovanie)s ON %(oborudovanie)s.%(point_id)s = %(workspoints)s.%(point_id)s 
    JOIN %(works)s ON %(works)s.%(id_obor)s = %(oborudovanie)s.%(id)s 
    WHERE %(workspoints)s.%(point_working)s GROUP BY %(workspoints)s.%(point_id)s ORDER BY
     all_works DESC LIMIT 10""") % sql_consts_dict
    return query


@log_decorator
def sql_select_count_works_point() -> str:
    """Return the query string select maximal number in column point_id in table workspoints"""

    return """SELECT COUNT(*) FROM %(workspoints)s WHERE (%(point_working)s) AND
     %(point_id)s != %(not_find_in_point)s""" % sql_consts_dict


@log_decorator
def sql_select_point_id_from_equip_id(equip_id: str) -> str:
    """Return the query string select a point contain this equip"""

    return (("""SELECT %(point_id)s FROM %(oborudovanie)s""" +
             """ WHERE %(id)s = {0}""") % sql_consts_dict).format(equip_id)


@log_decorator
def sql_select_name_from_point_id(point_id: str) -> str:
    """Return point_name from point_id == id"""

    query = ("""SELECT %(point_name)s FROM %(workspoints)s""" +
             """ WHERE %(point_id)s = {0};""") % sql_consts_dict

    return query.format(str(point_id))


@log_decorator
def sql_select_all_point_except_id(point_id: str) -> str:
    """Return all point except point_id == id"""

    query = ("""SELECT %(point_id)s, %(point_name)s FROM %(workspoints)s""" +
             """ WHERE %(point_id)s != {0} and %(point_working)s ORDER BY %(point_name)s""") % sql_consts_dict

    return query.format(point_id)

