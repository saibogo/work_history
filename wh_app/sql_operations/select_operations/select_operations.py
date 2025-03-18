import datetime

import psycopg2
from typing import *

from wh_app.supporting import functions
from wh_app.sql.select_sql import select_sql


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


def list_tuples_to_list_decorator(func: Callable) -> Callable:
    """[(elem,), (elem1,), ...] -> [elem, elem1, ...]"""
    def wrap(*args) -> List[Any]:
        return [elem[0] for elem in func(*args)]
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
def get_list_performers_in_work(cursor, work_id: str) -> List[str]:
    """Return list contain all performers in current work"""

    return select_sql.sql_select_all_current_performers_in_work(work_id)


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
def get_count_equips(cursor) -> str:
    """Return count not-deleted string in oborudovanie"""
    return select_sql.sql_select_count_equip()


@list_to_first_str_decorator
@get_selected_decorator
def get_last_equip_id(cursor) -> str:
    """Return string number of maximal id in table oborudovanie"""
    return select_sql.sql_select_last_equip_id()


@list_to_first_str_decorator
@get_selected_decorator
def get_next_equip_id(cursor) -> str:
    """Return string number of maximal id in table oborudovanie"""
    return select_sql.sql_select_next_id_equip()


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
def get_count_works_points(cursor) -> str:
    """Return string number of maximal id in table workspoints"""

    return select_sql.sql_select_count_works_point()


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


@list_tuples_to_list_decorator
@get_selected_decorator
def get_all_find_patterns(cursor) -> List[str]:
    """Function return list of all unique find patterns"""

    return select_sql.sql_select_all_find_patterns()


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
    """Return all workers where worker.status  != fired"""
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
def get_all_bindings_to_point(cursor, point_id: str) -> List[Tuple[int, str, bool]]:
    """Return list, contain all bindings in current point"""
    return select_sql.sql_select_all_bindings_to_point(point_id)


@get_selected_decorator
def get_all_bugz_in_bugzilla(cursor) -> list:
    """Function return all records in bugzilla"""
    return select_sql.sql_select_all_bugs_in_bugzilla()


@get_selected_decorator
def get_all_bugz_in_bugzilla_limit(cursor, page_num: int) -> list:
    """Function return all records in bugzilla use limit records on page"""
    return select_sql.sql_select_all_bugs_in_bugzilla_limit(str(page_num))


@get_selected_decorator
def get_all_bugz_in_work_in_bugzilla(cursor) -> list:
    """Function return all records in bugzilla if bug's status = in work"""
    return select_sql.sql_select_all_bugs_in_work_in_bugzilla()


@get_selected_decorator
def get_all_bugz_in_work_in_bugzilla_limit(cursor, page_num: int) -> list:
    """Function return all records in bugzilla if bug's status = in work"""
    return select_sql.sql_select_all_bugs_in_work_in_bugzilla_limit(str(page_num))


@list_to_first_tuple_decorator
@get_selected_decorator
def get_bug_by_id(cursor, bug_id: str) -> list:
    """Return bug information with ID = bug_id"""
    return select_sql.sql_select_get_bug_by_id(bug_id)


@get_selected_decorator
def get_all_customers(cursor) -> list:
    """Function return list contains all record in customer table"""
    return select_sql.sql_select_all_customers()


@list_to_first_tuple_decorator
@get_selected_decorator
def get_full_customer_info(cursor, customer_id: str) -> list:
    """Function return list contains all record in customer table"""
    return select_sql.sql_select_customer_info(customer_id)


@list_to_first_str_decorator
@get_selected_decorator
def get_hash_to_customer(cursor, user_name: str) -> str:
    """Function return hash with user = full_name"""
    return select_sql.sql_select_hash_from_user(user_name)


@get_selected_decorator
def get_all_orders(cursor) -> list:
    """Function return list contains all records in table orders"""
    return select_sql.sql_select_all_orders()


@get_selected_decorator
def get_all_orders_limit(cursor, page_num: int) -> List[Tuple]:
    """Returns a list object containing all jobs for a given piece of equipment use LIMIT and OFFSET
    See also get_works_from_equip_id"""

    return select_sql.sql_select_all_orders_limit(page_num)


@get_selected_decorator
def get_all_no_closed_orders(cursor) -> list:
    """Function return list contains all records in table orders"""
    return select_sql.sql_select_no_closed_orders()


@get_selected_decorator
def get_all_no_closed_orders_limit(cursor, page_num: int) -> list:
    """Function return list contains all records in table orders"""
    return select_sql.sql_select_no_closed_orders_limit(page_num)


@list_to_first_int_decorator
@get_selected_decorator
def get_maximal_orders_id(cursor) -> int:
    """Function return maximal id from orders table"""
    return select_sql.sql_select_max_order_id()


@get_selected_decorator
def get_all_order_status(cursor) -> List[Tuple]:
    """return all status and description from orders_types"""
    return select_sql.sql_select_all_orders_type()


@list_to_first_tuple_decorator
@get_selected_decorator
def get_order_from_id(cursor, order_id: str) -> Tuple:
    """Function return tuple contain full information from order with ID = order_id"""
    return select_sql.sql_select_order_from_id(order_id)


@list_to_first_int_decorator
@get_selected_decorator
def get_last_order_id_in_work(cursor) -> int:
    """Function return id to last order with status in_work"""
    return select_sql.sql_select_last_orders_id_in_work()


@list_to_first_bool_decorator
@get_selected_decorator
def user_in_customers(cursor, user_name: str) -> bool:
    """Function find user in customer table"""
    return select_sql.sql_select_user_in_customers(user_name)


@get_selected_decorator
def get_all_customers_orders_limit(cursor, user_name: str, page_num: int) -> List[Tuple]:
    """Function return all customers order using LIMIT"""
    return select_sql.sql_select_orders_from_user_limit(user_name, page_num)


@get_selected_decorator
def get_all_customers_orders(cursor, user_name: str) -> List[Tuple]:
    """Function return all customers order using LIMIT"""
    return select_sql.sql_select_orders_from_user(user_name)


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
def get_workers_in_work(cursor, work_id: str) -> list:
    """Return info from current database"""
    return select_sql.sql_select_all_workers_in_work(work_id)


@get_selected_decorator
def get_works_from_performer_and_date(cursor, worker_id: str, date_start: str, date_stop: str, page_num: str = 0) -> List[Tuple]:
    """Return list with all works where worker = worker_id in dateinterval [date_satrt, date_stop]
    if page_num == 0 then ot use limit for record in page"""

    return select_sql.sql_select_works_from_performer_and_date(worker_id, date_start, date_stop, page_num)


@get_selected_decorator
def get_all_desriptions_workers_status(cursor) -> List[Tuple]:
    """Return list of pairs (worker_status. description)"""

    return select_sql.sql_select_all_description_worker_status()


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


@list_to_list_decorator
@list_to_first_tuple_decorator
@get_selected_decorator
def get_all_telegram_chats(cursor) -> List:
    """Return all telegramm id from bot"""

    return select_sql.sql_select_all_telegram_chats()


@list_to_first_bool_decorator
@get_selected_decorator
def is_telegram_user_reader(cursor, user_id: int) -> bool:
    """Return awaliable read to current user"""

    return select_sql.sql_select_telegram_user_is_reader(user_id)


@list_to_first_bool_decorator
@get_selected_decorator
def is_telegram_user_writer(cursor, user_id: int) -> bool:
    """Return awaliable write to current user"""

    return select_sql.sql_select_telegram_user_is_writer(user_id)


@list_to_first_int_decorator
@get_selected_decorator
def get_worker_id_from_chats(cursor, user_id: int) -> int:
    """Return worker_id from chats-table"""

    return select_sql.sql_select_worker_id_from_chats(user_id)


@get_selected_decorator
def get_schedule_to_date(cursor, select_date: str) -> List[List]:
    """Return list with all workers work in selected date"""

    return select_sql.sql_select_schedule_from_date(select_date)


@get_selected_decorator
def get_all_work_days_types(cursor) -> List:
    """Return list with all pairs (day type, string with day_type)"""

    return select_sql.sql_select_all_work_days_type()


@list_to_first_int_decorator
@get_selected_decorator
def get_worker_id_from_schedule(cursor, date: str, worker_name: str, worker_subname: str) -> int:
    """Return worker_id from schedule-table where date, worker_name, subname in schedule"""

    return select_sql.sql_select_worker_id_from_schedule(date, worker_name, worker_subname)


@get_selected_decorator
def get_all_meter_devices(cursor) -> List[Tuple]:
    """Return all meter devices in database"""

    return select_sql.sql_select_all_meter_devices()


@get_selected_decorator
def get_all_worked_meter_devices(cursor) -> List[Tuple]:
    """Return all meter devices in database"""

    return select_sql.sql_select_all_meter_devices("WORKED")


@get_selected_decorator
def get_all_reading_from_device(cursor, id: int) -> List[Tuple]:
    """Return all reading from device with device_id = id"""

    return select_sql.sql_select_reading_meter_from_id(id)


@get_selected_decorator
def get_all_date_and_readings_from_device(cursor, device_id: int) -> List[Tuple]:
    """Return all records like (id, read_date, reading) from current meter device"""

    return select_sql.sql_select_readings_and_dates_from_device(device_id)


@get_selected_decorator
def get_last24_date_and_readings_from_device(cursor, device_id: int) -> List[Tuple]:
    """Return all records like (id, read_date, reading) from current meter device"""

    return select_sql.sql_select_readings_and_dates_from_device(device_id, True)


@get_selected_decorator
def get_all_worked_meter_in_point(cursor, point_id: int) -> List[Tuple]:
    """Return all worked meter devices in point"""

    return select_sql.sql_select_all_works_meter_in_point(point_id)


@get_selected_decorator
def get_full_info_from_meter_device(cursor, device_id: int) -> List[Tuple]:
    """Return all information from current device"""
    return select_sql.sql_select_full_information_from_meter_device(device_id)


@get_selected_decorator
def get_all_meter_types(cursor) -> List[Tuple]:
    """Return all meter types in database"""
    return select_sql.sql_select_all_meter_types()


@list_tuples_to_list_decorator
@get_selected_decorator
def get_all_calc_schemes_for_point_and_type(cursor, point_id: int, devices_type: str) -> List[Tuple]:
    """Return all awaliable calculation schemes"""
    return select_sql.sql_select_all_awaliable_schemes_for_type_and_point(point_id, devices_type)


@get_selected_decorator
def get_all_positive_device_in_scheme(cursor, schemes_id: int) -> List[Tuple]:
    """Return all positive elements in scheme with shemes_id"""
    return select_sql.sql_select_all_positive_schemes_from_schemes_id(schemes_id)


@get_selected_decorator
def get_all_negative_device_in_scheme(cursor, schemes_id: int) -> List[Tuple]:
    """Return all positive elements in scheme with shemes_id"""
    return select_sql.sql_select_all_negative_schemes_from_schemes_id(schemes_id)


@list_to_first_str_decorator
@get_selected_decorator
def get_comment_in_calc_scheme(cursor, schemes_id: int) -> str:
    return select_sql.sql_select_schemes_comment_from_schemes_id(schemes_id)


@list_to_first_str_decorator
@get_selected_decorator
def get_russian_units_of_measure(cursor, devices_type: str) -> str:
    return select_sql.sql_select_unit_meter_from_type(devices_type)


@list_to_first_str_decorator
@get_selected_decorator
def get_russian_devices_type(cursor, devices_type: str) -> str:
    """Return russian name to meter type"""
    return select_sql.sql_select_russian_string_from_meter_type(devices_type)


@list_to_first_str_decorator
@get_selected_decorator
def get_count_all_meter_devices(cursor) -> str:
    """Return COUNT(all meter devices)"""

    return select_sql.sql_select_count_all_meter_devices()


@list_to_first_str_decorator
@get_selected_decorator
def get_count_worked_meter_devices(cursor) -> str:
    """Return COUNT(all meter devices)"""

    return select_sql.sql_select_count_worked_meter_devices()