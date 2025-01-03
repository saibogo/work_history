"""This module contain all SELECT to NON-INCLUDE in OTHER parts SELECT INFORMATION"""

from wh_app.sql.sql_constant import sql_consts_dict

from wh_app.sql.select_sql.points_select import log_decorator


@log_decorator
def sql_select_works_days() -> str:
    """Return SQL-query contain points, workers and days of week"""

    return """SELECT * FROM %(firsts_bindings)s""" % sql_consts_dict


@log_decorator
def sql_select_alter_works_days() -> str:
    """Return SQL-query contain alternative bindings point <--> workers"""

    return """SELECT * FROM %(seconds_bindings)s ORDER BY %(point)s""" % sql_consts_dict


@log_decorator
def sql_select_all_weekly_chart() -> str:
    """Return SELECT-query to ALL WORKS DAYS From ALL Workers"""

    query = ("""SELECT %(workers)s.%(sub_name)s, day1, day2, day3, day4, day5, day6, day7 """ +
             """FROM %(works_days)s JOIN %(workers)s """ +
             """ON %(works_days)s.%(worker_id)s = %(workers)s.%(id)s AND %(workers)s.%(status)s != 'fired' """ +
             """ORDER BY %(workers)s.%(sub_name)s;""") % sql_consts_dict

    return query


@log_decorator
def sql_select_database_version() -> str:
    """Return select-string for get current version database"""

    return """SELECT VERSION()"""


@log_decorator
def sql_select_all_find_patterns() -> str:
    return """SELECT * FROM %(find_patterns)s""" % sql_consts_dict