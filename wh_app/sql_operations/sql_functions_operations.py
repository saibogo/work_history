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


def create_or_replace_work_day_type_to_string(cursor) -> None:
    """Add or replace in database function work day type to string"""
    create_function(cursor, functions_sql.work_day_type_to_string())


def create_or_replace_date_to_date_and_day(cursor) -> None:
    """Add or replace in database function date -> date and day"""
    create_function(cursor, functions_sql.date_to_date_and_day_of_week())


def create_or_replace_meter_type_to_string(cursor) -> None:
    """Add or replace in database function meter_type -> string(meter_type)"""
    create_function(cursor, functions_sql.meter_type_to_string())


def create_or_replace_units_of_measure_string(cursor) -> None:
    """Add or replace SQL function to mapping meter_type to units of measure"""
    create_function(cursor, functions_sql.units_of_measure())


def all_sql_functions_list() -> list:
    """Return list contain all function to create virtual tables"""

    return [create_or_replace_status_to_text,
            create_or_replace_bug_status_to_text,
            create_or_replace_point_status_to_text,
            create_or_replace_all_works_from_equip,
            create_or_replace_last_day_funct,
            create_or_replace_last_week_funct,
            create_or_replace_last_month_funct,
            create_or_replace_last_year_funct,
            create_or_replace_work_day_type_to_string,
            create_or_replace_date_to_date_and_day,
            create_or_replace_meter_type_to_string,
            create_or_replace_units_of_measure_string]
