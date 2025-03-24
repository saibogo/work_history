from wh_app.sql_operations.select_operations.decorators import *
from wh_app.sql.select_sql import select_sql


@get_selected_decorator
def get_list_performers_in_work(cursor, work_id: str) -> List[str]:
    """Return list contain all performers in current work"""

    return select_sql.sql_select_all_current_performers_in_work(work_id)


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
def get_all_posts(cursor) -> list:
    """Function return all post in POSTS-table"""
    return select_sql.sql_select_all_posts()


@get_selected_decorator
def get_weekly_chart(cursor) -> list:
    """Function return all works days from all workers in weekly"""
    return select_sql.sql_select_all_weekly_chart()


@list_to_first_str_decorator
@get_selected_decorator
def get_worker_id_from_name(cursor, name: str) -> str:
    """Return worker_id from name or sub_name pattern"""
    return select_sql.sql_select_worker_id_like_str(name)


@get_selected_decorator
def get_all_desriptions_workers_status(cursor) -> List[Tuple]:
    """Return list of pairs (worker_status. description)"""

    return select_sql.sql_select_all_description_worker_status()


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
def get_table_current_workers(cursor) -> List[Tuple[int, str, str, bool, str, int]]:
    """Function return list contain current workers
    Return value [elem1, elem2, ..., elem_n] while elem = (worker_id, first_name,
    second_name, status, phone, post_id)"""
    return select_sql.sql_select_table_current_workers()


@get_selected_decorator
def get_workers_in_work(cursor, work_id: str) -> list:
    """Return info from current database"""
    return select_sql.sql_select_all_workers_in_work(work_id)