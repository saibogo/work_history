from wh_app.sql_operations.select_operations import select_operations
from wh_app.sql.insert_sql.insert_sql import *


def add_new_bug_in_bugzilla(cursor, problem: str) -> None:
    """Add new record in bugzilla"""

    cursor.execute(sql_add_new_bug(problem))


def insert_new_session_in_sessions(cursor, hash: str) -> None:
    """Add new session in database"""

    cursor.execute(sql_insert_new_session_in_sessions(hash))