from wh_app.sql_operations.select_operations import select_operations
from wh_app.sql.insert_sql.insert_sql import *


def create_new_work(cursor, id_obor: str, date: str, problem: str, result: str, worker_id: str) -> None:
    """Create a new work record in database"""

    new_id = str(select_operations.get_next_work_id(cursor))
    cursor.execute(sql_insert_new_work(new_id, id_obor, date, problem, result, worker_id))


def add_new_performer_in_performers_table(cursor, work_id: str, worker_id: str) -> None:
    """Add new performer in performers table"""

    cursor.execute(sql_add_new_performers(work_id, worker_id))


def insert_new_binding(cursor, point_id: str, worker_id: str, is_main: str) -> None:
    """Update information from bindings section"""

    cursor.execute(sql_insert_new_binding(point_id, worker_id, is_main))


def insert_new_worker(cursor, name: str, sub_name: str, phone_number: str, post: int) -> None:
    """Add new worker in database"""

    cursor.execute(sql_add_new_worker(name, sub_name, phone_number, post))


def insert_new_day_in_schedule(cursor, work_day: str, worker_id: int, day_type: str) -> None:
    """add new record in work schedule"""

    cursor.execute(sql_add_new_day_in_schedule(str(work_day), int(worker_id), str(day_type)))