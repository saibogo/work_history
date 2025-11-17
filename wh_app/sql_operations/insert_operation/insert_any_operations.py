from typing import List, Tuple

from wh_app.sql_operations.select_operations import select_operations
from wh_app.sql.insert_sql.insert_sql import *


def add_new_bug_in_bugzilla(cursor, problem: str) -> None:
    """Add new record in bugzilla"""

    cursor.execute(sql_add_new_bug(problem))


def insert_new_session_in_sessions(cursor, hash: str) -> None:
    """Add new session in database"""

    cursor.execute(sql_insert_new_session_in_sessions(hash))


def insert_new_meter_device(cursor, dev_type: str, model: str, serial: str, is_active: bool, start_date: str, verif_date: str, Kt: int, is_inner: bool, comment: str) -> List[Tuple]:
    """Add new meter device in database and return new id"""

    return cursor.execute(sql_insert_new_meter_device(dev_type, model, serial, is_active, start_date, verif_date, Kt, is_inner, comment))
