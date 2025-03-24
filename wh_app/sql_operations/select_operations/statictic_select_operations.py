import datetime

from wh_app.sql_operations.select_operations.decorators import *
from wh_app.sql.select_sql import select_sql


@get_selected_decorator
def get_statistic(cursor) -> List[Tuple[int, str, int, int, datetime.datetime]]:
    """Function return list contain stat info from all points
    Return value [elem1, elem2, ..., elem_n] while elem = (point_id, point_name, equips_num,
     works_num, last_works_date)"""
    return select_sql.sql_select_statistic()


@list_to_first_str_decorator
@get_selected_decorator
def get_size_database(cursor) -> str:
    """Function return size workhistory database in humans view"""
    return select_sql.sql_select_size_database()


@get_selected_decorator
def get_top_10_works(cursor) -> List[Tuple]:
    """Return top 10 equip with maximal works"""

    return select_sql.sql_select_top_works()


@get_selected_decorator
def get_top_10_points(cursor) -> List[Tuple]:
    """Return top 10 equip with maximal works"""

    return select_sql.sql_select_top_points()


@get_selected_decorator
def get_top_10_workers(cursor) -> List[Tuple]:
    """Return top 10 workers with maximal works"""

    return select_sql.sql_select_top_workers()


@get_selected_decorator
def get_database_version(cursor) -> list:
    """Return info from current database"""
    return select_sql.sql_select_database_version()


