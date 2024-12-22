"""This module create RAW-query to SELECT in database"""

from wh_app.sql.select_sql.points_select import *
from wh_app.sql.select_sql.equipments_select import *
from wh_app.sql.select_sql.work_select import *
from wh_app.sql.select_sql.workers_select import *
from wh_app.sql.select_sql.orders_and_bugs_select import *
from wh_app.sql.select_sql.statistic_select import *
from wh_app.sql.select_sql.user_select import *


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
def sql_select_electric_info(point_id: str) -> str:
    """Return SELECT-string for get electric information to point"""

    query = ("""SELECT * FROM %(electric)s WHERE point_id={0}""") % sql_consts_dict
    return query.format(point_id)


@log_decorator
def sql_select_cold_water_info(point_id: str) -> str:
    """Return SELECT-string for get cold_water information to point"""

    query = ("""SELECT * FROM %(cold_water)s WHERE point_id={0}""") % sql_consts_dict
    return query.format(point_id)


@log_decorator
def sql_select_hot_water_info(point_id: str) -> str:
    """Return SELECT-string for get hot_water information to point"""

    query = ("""SELECT * FROM %(hot_water)s WHERE point_id={0}""") % sql_consts_dict
    return query.format(point_id)


@log_decorator
def sql_select_heating_info(point_id: str) -> str:
    """Return SELECT-string for get heating information to point"""

    query = ("""SELECT * FROM %(heating)s WHERE point_id={0}""") % sql_consts_dict
    return query.format(point_id)


@log_decorator
def sql_select_sewerage_info(point_id: str) -> str:
    """Return SELECT-string for get sewerage information to point"""

    query = ("""SELECT * FROM %(sewerage)s WHERE point_id={0}""") % sql_consts_dict
    return query.format(point_id)


@log_decorator
def sql_select_database_version() -> str:
    """Return select-string for get current version database"""

    return """SELECT VERSION()"""


@log_decorator
def sql_select_all_find_patterns() -> str:
    return """SELECT * FROM %(find_patterns)s""" % sql_consts_dict

