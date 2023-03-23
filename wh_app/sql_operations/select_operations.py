import datetime

import psycopg2
from typing import *

from wh_app.supporting import functions
from wh_app.sql import select_sql


def commit(connection: psycopg2.connect) -> None:
    """Applies changes to the database"""

    connection.commit()


def get_selected(cursor, sql: str) -> List:
    """Returns a list of database objects that match the query."""

    cursor.execute(sql)
    return cursor.fetchall()


def get_selected_decorator(func: Callable) -> Callable:
    """Returns a list of database objects that match the query."""
    def wrap(*args) -> List[Tuple]:
        cursor= args[0]
        cursor.execute(func(*args))
        return cursor.fetchall()
    return wrap


def list_to_list_decorator(func: Callable) -> Callable:
    """List[Tuple[Any]] -> List[str]"""
    def wrap(*args) -> List[str]:
        return list(func(*args)[0])
    return wrap


def list_to_first_tuple_decorator(func: Callable) -> Callable:
    """List[Tuple[Any]] -> List[str]"""
    def wrap(*args) -> List[str]:
        return func(*args)[0]
    return wrap


def list_to_first_str_decorator(func: Callable) -> Callable:
    """List[Tuple[Any]] -> String"""
    def wrap(*args) -> str:
        return str(func(*args)[0][0])
    return wrap


def list_to_first_int_decorator(func: Callable) -> Callable:
    """List[Tuple[Any]] -> String"""
    def wrap(*args) -> int:
        return int(func(*args)[0][0])
    return wrap


def list_to_first_bool_decorator(func: Callable) -> Callable:
    """List[Tuple[Any]] -> String"""
    def wrap(*args) -> bool:
        return func(*args)[0][0]
    return wrap


@get_selected_decorator
def get_point(cursor, point_id: str) -> List[Tuple]:
    """Returns a list object containing the selected point
    [elem] while elem = (point_id, point_name, point_address, point_status)"""

    return select_sql.sql_select_point(point_id)


def get_all_points(cursor) -> List[Tuple]:
    """Return a list object containing all points
    See get_point: return value [elem, elem1, ..., elem_n]"""

    return get_point(cursor, '0')


@get_selected_decorator
def get_all_works_points(cursor) -> List[Tuple]:
    """Return a list object containing all points haves status 'in work'
    See also get_point: return value [elem, elem1, .... elem_n]"""

    return select_sql.sql_select_all_works_points()


@get_selected_decorator
def get_equip_in_point(cursor, point_id: str) -> List[Tuple]:
    """Returns all equipment for this point
    Return value [elem, elem1, ..., elem_n] while elem = (equip_id, point_name, equip_name, model, serial, pre_id)"""

    return select_sql.sql_select_all_equipment \
        if point_id == '' or point_id == '0' \
        else select_sql.sql_select_equipment_in_point(point_id)


@get_selected_decorator
def get_equip_in_point_limit(cursor, point_id: str, page_num: int) -> List[Tuple]:
    """Returns all equipment for this point use LIMIT and OFFSET
    Return value see get_equip_in_point"""

    return select_sql.sql_select_all_equipment_limit(page_num) \
        if point_id == '' or point_id == '0' \
        else select_sql.sql_select_equipment_in_point_limit(point_id, page_num)


@get_selected_decorator
def get_works_from_equip_id(cursor, id: str) -> List[Tuple]:
    """Returns a list object containing all jobs for a given piece of equipment
    [elem1, elem2, ..., elem_n] while elem = (work_ID, point_name, equip_name, model, serial, datetime,
     problem, result, performer_name)"""

    return select_sql.sql_select_all_works() \
        if id == '' or id == '0' \
        else select_sql.sql_select_work_to_equipment_id(id)


@get_selected_decorator
def get_last_works_from_equip_id(cursor, id: str) -> List[Tuple]:
    """Returns a list object containing all jobs for a given piece of equipment
    [elem1, elem2, ..., elem_n] while elem = (work_ID, point_name, equip_name, model, serial, datetime,
     problem, result, performer_name)"""

    return select_sql.sql_select_last_work_to_equipment_id(id)


@get_selected_decorator
def get_works_from_equip_id_limit(cursor, id: str, page_num: int) -> List[Tuple]:
    """Returns a list object containing all jobs for a given piece of equipment use LIMIT and OFFSET
    See also get_works_from_equip_id"""

    return select_sql.sql_select_all_works_limit(page_num) \
        if id == '' or id == '0' \
        else select_sql.sql_select_work_from_equip_id_limit(id, page_num)


def get_works_from_point_and_equip(cursor, point_id: str, equip_id: str) -> List[Tuple]:
    """Returns a list object containing all jobs at a given point and a given equipment number"""

    equips = get_equip_in_point(cursor, point_id)
    equips_id = [elem[0] for elem in equips] if equip_id == '' or equip_id == '0' else [equip_id]
    works = []
    for id in equips_id:
        works = works + get_works_from_equip_id(cursor, id)
    return works


@list_to_list_decorator
@get_selected_decorator
def get_full_point_information(cursor, point_id: str) -> List[str]:
    """Returns the object list containing complete information about the given point
    return value = [point_name, point_address, point_status]"""

    return select_sql.sql_select_information_to_point(point_id)


def get_full_information_list_points(cursor, ls: list) -> list:
    """Returns a list object containing complete information about points in the list ls"""

    return [get_full_point_information(cursor, elem[0]) for elem in ls]


@list_to_list_decorator
@get_selected_decorator
def get_full_equip_information(cursor, equip_id: str) -> List[str]:
    """Returns a list object containing complete information about a given piece of equipment
    Return value [point_name, equip_name, model, serial, pre_ID]"""

    return select_sql.sql_select_full_equips_info(equip_id)


@list_to_list_decorator
@get_selected_decorator
def get_full_information_to_work(cursor, work_id: str) -> List[str]:
    """Returns a list object containing complete information about the work done with the specified number
    Result value [work_ID, point_name, equip_name, model, number, datetime, problem, result, names_of_performers]"""

    return select_sql.sql_select_work_from_id(work_id)


def get_full_info_from_works_list(cursor, ls: list) -> list:
    """Returns a list object containing complete information about the work performed as specified by the list"""

    return [get_full_information_to_work(cursor, elem[0]) for elem in ls]


@get_selected_decorator
def get_all_equips_list_from_like_str(cursor, s: str) -> List[Tuple]:
    """Return all equips names contain s-string
    [elem1, elem2, ..., elem_n] while elem = (equip_ID, point_name, model, serial, pre_ID)"""

    return select_sql.sql_select_equip_from_like_str(s)


@get_selected_decorator
def get_all_equips_list_from_like_str_limit(cursor, s: str, page_num: int) -> List[Tuple]:
    """Return all equips names contain s-string use LIMIT and OFFSET
    See also get_all_equips_list_from_like_str"""

    return select_sql.sql_select_equip_from_like_str_limit(s, str(page_num))


@get_selected_decorator
def get_all_points_list_from_like_str(cursor, s:str) -> List[Tuple[int, str, str, bool]]:
    """Return all points names contain s-string
    Return value [elem1, elem2, ..., elem_n] while elem = (point_ID, point_name, point_address, point_status)"""

    return select_sql.sql_select_point_from_like_str(s)


@get_selected_decorator
def get_all_points_list_from_like_str_limit(cursor, s:str, page_num: int) -> List[Tuple[int, str, str, bool]]:
    """Return all points names contain s-string use LIMIT and OFFSET
    see also get_all_points_list_from_like_str"""

    return select_sql.sql_select_point_from_like_str_limit(s, str(page_num))


def get_works_list_from_equips_list(cursor, list_equips: list) -> list:
    """Return works list create from equips list"""
    works = []
    for equip in list_equips:
        works = works + get_works_from_equip_id(cursor, equip[0])
    return works


@list_to_first_str_decorator
@get_selected_decorator
def get_maximal_equip_id(cursor) -> str:
    """Return string number of maximal id in table oborudovanie"""
    return select_sql.sql_select_max_id_equip()


@list_to_first_bool_decorator
@get_selected_decorator
def get_equip_deleted_status(cursor, equip_id: str) -> bool:
    """Return current deleted-status from equip with id = equip_id"""

    return select_sql.sql_select_equip_deleted_status(equip_id)


@list_to_first_str_decorator
@get_selected_decorator
def get_maximal_points_id(cursor) -> str:
    """Return string number of maximal id in table workspoints"""

    return select_sql.sql_select_max_id_point()


@list_to_first_str_decorator
@get_selected_decorator
def get_maximal_work_id(cursor) -> str:
    """Return string number of maximal id in table works"""

    return select_sql.sql_select_max_work_id()


@list_to_first_str_decorator
@get_selected_decorator
def get_point_id_from_equip_id(cursor, equip_id: str) -> str:
    """Return point_id, where point contain equip"""

    return select_sql.sql_select_point_id_from_equip_id(equip_id)


@get_selected_decorator
def get_all_works_like_word(cursor, word: str) -> List[Tuple[int, str, str, str, str,
                                                             datetime.datetime, str, str, str]]:
    """Function return list contain ID work likes word
    Return value [elem1, elem2, ..., elem_n] while elem = (work_ID, point_name, equip_name, model, serial,
    datetime, problem, result, performers_names)"""

    return select_sql.sql_select_all_works_from_like_str(word)


@get_selected_decorator
def get_all_works_like_word_limit(cursor, word: str, page_num: int) -> List[Tuple[int, str, str, str, str,
                                                             datetime.datetime, str, str, str]]:
    """Function return list contain ID work likes word
    See also get_all_works_like_word"""

    return select_sql.sql_select_all_works_from_like_str_limit(word, str(page_num))


@get_selected_decorator
def get_all_works_like_word_and_date(cursor, word: str, date_start: str, date_stop: str) -> \
        List[Tuple[int, str, str, str, str, datetime.datetime, str, str, str]]:
    """Function return list contain all works in date-date interval and like word
    See also get_all_works_like_word"""

    return select_sql.sql_select_all_works_from_like_str_and_date(word, date_start, date_stop)


@get_selected_decorator
def get_all_works_like_word_and_date_limit(cursor, word: str, date_start: str, date_stop: str, page_num: int) \
        -> List[Tuple[int, str, str, str, str, datetime.datetime, str, str, str]]:
    """Function return list contain all works in date-date interval and like word use LIMIT and OFFSET
    See also get_all_works_like_word"""

    return select_sql.sql_select_all_works_from_like_str_and_date_limit(word, date_start, date_stop, str(page_num))


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


@list_to_first_int_decorator
@get_selected_decorator
def get_count_unique_dates_in_works(cursor) -> int:
    """Function return count(unique date) in works table"""
    return select_sql.sql_select_count_uniques_dates()


@list_to_first_int_decorator
@get_selected_decorator
def get_count_unique_works(cursor) -> int:
    """Function return count(id) in work table"""
    return select_sql.sql_select_count_uniques_works()


@get_selected_decorator
def get_all_workers(cursor) -> List[Tuple[int, str, str, str, str, str]]:
    """Function return list contain all workers
    Return value [elem1, elem2, ..., elem_n] while elem = (worker_id, second_name, first_name, phone, status, grade)"""
    return select_sql.sql_select_all_workers()


@get_selected_decorator
def get_all_workers_real(cursor) -> List[Tuple[int, str, str, str, str, str]]:
    """Return all workers where is_work == TRUE"""
    return select_sql.sql_select_all_workers_real()


@list_to_first_tuple_decorator
@get_selected_decorator
def get_info_from_worker(cursor, worker_id: str) -> Tuple[int, str, str, str, str, str]:
    """Function return full info in tuple from worker where id = worker_id"""
    return select_sql.sql_select_worker_info(worker_id)


@get_selected_decorator
def get_table_current_workers(cursor) -> List[Tuple[int, str, str, bool, str, int]]:
    """Function return list contain current workers
    Return value [elem1, elem2, ..., elem_n] while elem = (worker_id, first_name,
    second_name, status, phone, post_id)"""
    return select_sql.sql_select_table_current_workers()


@get_selected_decorator
def get_all_works_from_worker_id(cursor, worker_id: str) -> List[Tuple[int, str, str, str, str,
                                                                       datetime.datetime, str, str, str]]:
    """Function return list contain all formatting works from current performers
    Return value [elem1, elem2, ..., elem_n] while elem = (work_id, point_name, equip_name, model, serial,
    datetime, problem, work resume, performers names)"""
    return select_sql.sql_select_works_from_worker(worker_id)


@get_selected_decorator
def get_all_works_from_worker_id_limit(cursor, worker_id: str, page_num: int) -> List[Tuple[int, str, str,
                                                                                            str, str,
                                                                                            datetime.datetime,
                                                                                            str, str, str]]:
    """See also get_all_works_from_worker_id/ But records in view-page <= size in config-file"""
    return select_sql.sql_select_works_from_worker_limit(worker_id, page_num)


def get_count_all_works_from_worker_id(cursor, worker_id: str) -> int:
    """Return Len(get_all_works_from_worker_id)"""

    return functions.get_first_non_list(get_selected(
        cursor,
        select_sql.sql_counter(select_sql.sql_select_works_from_worker(worker_id))))


@get_selected_decorator
def get_works_days_table(cursor) -> list:
    """Function return table contain points, workers and days of week"""
    return select_sql.sql_select_works_days()


@get_selected_decorator
def get_alter_works_days_table(cursor) -> list:
    """Function return all alternatives bindings worers <--> points"""
    return select_sql.sql_select_alter_works_days()


@get_selected_decorator
def get_all_bugz_in_bugzilla(cursor) -> list:
    """Function return all records in bugzilla"""
    return select_sql.sql_select_all_bugs_in_bugzilla()


@get_selected_decorator
def get_all_bugz_in_work_in_bugzilla(cursor) -> list:
    """Function return all records in bugzilla if bug's status = in work"""
    return select_sql.sql_select_all_bugs_in_work_in_bugzilla()


@list_to_first_tuple_decorator
@get_selected_decorator
def get_bug_by_id(cursor, bug_id: str) -> list:
    """Return bug information with ID = bug_id"""
    return select_sql.sql_select_get_bug_by_id(bug_id)


@get_selected_decorator
def get_all_customers(cursor) -> list:
    """Function return list contains all record in customer table"""
    return select_sql.sql_select_all_customers()


@get_selected_decorator
def get_all_orders(cursor) -> list:
    """Function return list contains all records in table orders"""
    return select_sql.sql_select_all_orders()


@get_selected_decorator
def get_all_point_except_id(cursor, id: str) -> list:
    """Function return all points except point_id == id"""
    return select_sql.sql_select_all_point_except_id(str(id))


@list_to_first_str_decorator
@get_selected_decorator
def get_point_name_from_id(cursor, id: str) -> str:
    """Function return string-name of point"""
    return select_sql.sql_select_name_from_point_id(str(id))


@get_selected_decorator
def get_all_posts(cursor) -> list:
    """Function return all post in POSTS-table"""
    return select_sql.sql_select_all_posts()


@get_selected_decorator
def get_weekly_chart(cursor) -> list:
    """Function return all works days from all workers in weekly"""
    return select_sql.sql_select_all_weekly_chart()


@get_selected_decorator
def get_electric_point_info(cursor, point_id: str) -> list:
    """Return electric point information"""
    return select_sql.sql_select_electric_info(point_id)


@get_selected_decorator
def get_cold_water_point_info(cursor, point_id: str) -> list:
    """Return cold_water point information"""
    return select_sql.sql_select_cold_water_info(point_id)


@get_selected_decorator
def get_hot_water_point_info(cursor, point_id: str) -> list:
    """Return hot_water point information"""
    return select_sql.sql_select_hot_water_info(point_id)


@get_selected_decorator
def get_heating_point_info(cursor, point_id: str) -> list:
    """Return heating point information"""
    return select_sql.sql_select_heating_info(point_id)


@get_selected_decorator
def get_sewerage_point_info(cursor, point_id: str) -> list:
    """Return sewerage point information"""
    return select_sql.sql_select_sewerage_info(point_id)


@get_selected_decorator
def get_database_version(cursor) -> list:
    """Return info from current database"""
    return select_sql.sql_select_database_version()


@list_to_first_str_decorator
@get_selected_decorator
def get_worker_id_from_name(cursor, name: str) -> str:
    """Return worker_id from name or sub_name pattern"""
    return select_sql.sql_select_worker_id_like_str(name)


@get_selected_decorator
def get_works_from_performer_and_date(cursor, worker_id: str, date_start: str, date_stop: str, page_num: str = 0) -> List[Tuple]:
    """Return list with all works where worker = worker_id in dateinterval [date_satrt, date_stop]
    if page_num == 0 then ot use limit for record in page"""

    return select_sql.sql_select_works_from_performer_and_date(worker_id, date_start, date_stop, page_num)