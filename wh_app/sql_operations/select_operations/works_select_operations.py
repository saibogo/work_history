import datetime

from wh_app.supporting import functions
from wh_app.sql_operations.select_operations.decorators import *
from wh_app.sql.select_sql import select_sql
from wh_app.sql_operations.select_operations.equip_select_operations import get_equip_in_point


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
def get_works_from_equip_id_limit(cursor, id: str, page_num: int, ord_column=1) -> List[Tuple]:
    """Returns a list object containing all jobs for a given piece of equipment use LIMIT and OFFSET
    See also get_works_from_equip_id"""

    return select_sql.sql_select_all_works_limit(page_num, ord_column) \
        if id == '' or id == '0' \
        else select_sql.sql_select_work_from_equip_id_limit(id, page_num, ord_column)


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
def get_full_information_to_work(cursor, work_id: str) -> List[str]:
    """Returns a list object containing complete information about the work done with the specified number
    Result value [work_ID, point_name, equip_name, model, number, datetime, problem, result, names_of_performers]"""

    return select_sql.sql_select_work_from_id(work_id)


def get_full_info_from_works_list(cursor, ls: list) -> list:
    """Returns a list object containing complete information about the work performed as specified by the list"""

    return [get_full_information_to_work(cursor, elem[0]) for elem in ls]


def get_works_list_from_equips_list(cursor, list_equips: list) -> list:
    """Return works list create from equips list"""
    works = []
    for equip in list_equips:
        works = works + get_works_from_equip_id(cursor, equip[0])
    return works


@list_to_first_str_decorator
@get_selected_decorator
def get_maximal_work_id(cursor) -> str:
    """Return string number of maximal id in table works"""

    return select_sql.sql_select_max_work_id()


@list_to_first_str_decorator
@get_selected_decorator
def get_next_work_id(cursor) -> str:
    """Return string number of maximal id in table works"""

    return select_sql.sql_select_next_work_id()


@get_selected_decorator
def get_all_works_from_worker_id(cursor, worker_id: str) -> List[Tuple[int, str, str, str, str,
                                                                       datetime.datetime, str, str, str]]:
    """Function return list contain all formatting works from current performers
    Return value [elem1, elem2, ..., elem_n] while elem = (work_id, point_name, equip_name, model, serial,
    datetime, problem, work resume, performers names)"""
    return select_sql.sql_select_works_from_worker(worker_id)


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
def get_works_from_performer_and_date(cursor, worker_id: str, date_start: str, date_stop: str, page_num: str = 0,
                                      ord=False, ord_column=1) -> List[Tuple]:
    """Return list with all works where worker = worker_id in dateinterval [date_satrt, date_stop]
    if page_num == 0 then ot use limit for record in page"""

    return select_sql.sql_select_works_from_performer_and_date(worker_id, date_start, date_stop, page_num, ord, ord_column)

