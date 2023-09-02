import psycopg2

from wh_app.supporting import functions
from wh_app.sql import functions_sql

functions.info_string(__name__)


def commit(connection: psycopg2.connect) -> None:
    """Applies changes to the database"""

    connection.commit()


def create_function(cursor, sql: str) -> None:
    """Create virtual table"""

    cursor.execute(sql)


def create_or_replace_status_to_text(cursor) -> None:
    """Add or replace in database function worker_status to text"""
    create_function(cursor, functions_sql.worker_status_to_text())


def create_or_replace_bug_status_to_text(cursor) -> None:
    """Add or replace in database function bug_status to text"""
    create_function(cursor, functions_sql.bug_status_to_text())


def create_or_replace_point_status_to_text(cursor) -> None:
    """Add or replace in database function bug_status to text"""
    create_function(cursor, functions_sql.point_status_to_text())


def create_or_replace_all_works_from_equip(cursor) -> None:
    """Add or replace in database function works from equip_id to text"""
    create_function(cursor, functions_sql.all_works_from_equip_id_funct())


def create_or_replace_last_day_funct(cursor) -> None:
    """Add or replace in database function lastday"""
    create_function(cursor, functions_sql.last_day_funct())


def create_or_replace_last_week_funct(cursor) -> None:
    """Add or replace in database function lastday"""
    create_function(cursor, functions_sql.last_week_funct())


def create_or_replace_last_month_funct(cursor) -> None:
    """Add or replace in database function lastday"""
    create_function(cursor, functions_sql.last_month_funct())


def create_or_replace_last_year_funct(cursor) -> None:
    """Add or replace in database function lastday"""
    create_function(cursor, functions_sql.last_year_funct())


def all_sql_functions_list() -> list:
    """Return list contain all function to create virtual tables"""

    return [create_or_replace_status_to_text,
            create_or_replace_bug_status_to_text,
            create_or_replace_point_status_to_text,
            create_or_replace_all_works_from_equip,
            create_or_replace_last_day_funct,
            create_or_replace_last_week_funct,
            create_or_replace_last_month_funct,
            create_or_replace_last_year_funct]
