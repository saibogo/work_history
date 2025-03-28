from wh_app.sql_operations.select_operations import select_operations
from wh_app.sql.insert_sql import *


def create_new_point(cursor, point_name: str, point_address: str) -> None:
    """Creates a new point in the database"""

    new_point_id = str(int(select_operations.get_maximal_points_id(cursor)) + 1)
    cursor.execute(sql_insert_new_point(new_point_id, point_name, point_address))


def create_new_equip(cursor, point_id: str, name: str,
                     model: str = "not model", serial_num: str = "not number", pre_id: str = "") -> None:
    """Creates a new piece of equipment in the database"""

    new_id = int(select_operations.get_next_equip_id(cursor))
    cursor.execute(sql_insert_new_equip(new_id ,point_id, name, model, serial_num,
                                        pre_id if pre_id != "" else str(new_id)))


def create_new_work(cursor, id_obor: str, date: str, problem: str, result: str, worker_id: str) -> None:
    """Create a new work record in database"""

    new_id = str(select_operations.get_next_work_id(cursor))
    cursor.execute(sql_insert_new_work(new_id, id_obor, date, problem, result, worker_id))


def add_new_performer_in_performers_table(cursor, work_id: str, worker_id: str) -> None:
    """Add new performer in performers table"""

    cursor.execute(sql_add_new_performers(work_id, worker_id))


def add_new_bug_in_bugzilla(cursor, problem: str) -> None:
    """Add new record in bugzilla"""

    cursor.execute(sql_add_new_bug(problem))


def insert_tech_section(cursor, section: str, point_id: str, dogovor: str, resume: str) -> None:
    """Update section in technical information for workpoint"""

    cursor.execute(sql_insert_tech_section(point_id, section, dogovor, resume))


def insert_new_binding(cursor, point_id: str, worker_id: str, is_main: str) -> None:
    """Update information from bindings section"""

    cursor.execute(sql_insert_new_binding(point_id, worker_id, is_main))


def insert_new_worker(cursor, name: str, sub_name: str, phone_number: str, post: int) -> None:
    """Add new worker in database"""

    cursor.execute(sql_add_new_worker(name, sub_name, phone_number, post))


def insert_new_order(cursor, customer_id: str, point_id: str, order_info: str) -> None:
    """add new order in database"""

    cursor.execute(sql_add_new_order(customer_id, point_id, order_info))


def insert_new_day_in_schedule(cursor, work_day: str, worker_id: int, day_type: str) -> None:
    """add new record in work schedule"""

    cursor.execute(sql_add_new_day_in_schedule(str(work_day), int(worker_id), str(day_type)))


def insert_new_reading_to_meter_device(cursor, device_id: int, reading_date: str, value: int) -> None:
    """Add new record in history current device meter"""

    cursor.execute(sql_add_new_reading_to_meter_device(device_id, reading_date, value))


def insert_new_customer_in_database(cursor, nickname: str, description: str, hash_pass: str) -> None:
    """Add new customer in database"""

    cursor.execute(sql_add_new_customer(nickname, description, hash_pass))


def insert_new_session_in_sessions(cursor, hash: str) -> None:
    """Add new session in database"""

    cursor.execute(sql_insert_new_session_in_sessions(hash))


