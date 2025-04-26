import psycopg2

from wh_app.supporting import functions
from wh_app.sql import procedures_sql

functions.info_string(__name__)


def commit(connection: psycopg2.connect) -> None:
    """Applies changes to the database"""

    connection.commit()


def create_procedure(cursor, sql: str) -> None:
    """Create virtual table"""

    cursor.execute(sql)


def create_proc_delete_not_active_session(cursor) -> None:
    """Create procedure to delete all not active session in database"""
    create_procedure(cursor, procedures_sql.sql_proc_delete_not_active_sessions())


def create_proc_update_all_sessions_older_48h(cursor) -> None:
    """Create procedure to update all session with start_time older 48 hours"""
    create_procedure(cursor, procedures_sql.sql_proc_update_all_sessions_older_48h())


def create_proc_vacuum_tables(cursor) -> None:
    """Create or replace procedure to find tables with dead strings"""
    create_procedure(cursor, procedures_sql.sql_proc_vacuum_tables())


def all_sql_procedures_list() -> list:
    """Return list contain all function to create virtual tables"""

    return [create_proc_delete_not_active_session,
            create_proc_update_all_sessions_older_48h,
            create_proc_vacuum_tables]