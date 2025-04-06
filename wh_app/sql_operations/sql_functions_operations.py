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


def create_or_replase_total_last_month(cursor) -> None:
    """Add or replace SQL function to calculate consumption to last month from meter device"""
    create_function(cursor, functions_sql.total_last_month())


def create_or_replace_average_from_last_readings(cursor) -> None:
    """Add or replace SQL function to calculate average in day from two last reading"""
    create_function(cursor, functions_sql.average_from_last_readings())


def create_or_replace_analytics_in_scheme(cursor) -> None:
    """Add or replace function return (average, average for month future, average sum between two last reading)"""
    create_function(cursor, functions_sql.sum_pu_in_scheme())


def create_or_replace_full_calculation_scheme(cursor) -> None:
    """Create or replace function return dta from scheme liked [type, positive devices, negative_devices, comment,
     type units, avr, avr in month, total last month]. All elements are TEXT"""
    create_function(cursor, functions_sql.full_calculation_in_scheme())


def create_or_replace_full_calc_all_schemes_in_point(cursor) -> None:
    """Create or replace SQL function return ARRAY liked [str1, str2, ...., strN]"""
    create_function(cursor, functions_sql.full_calc_all_schemes_in_point())


def create_or_replace_first_day_of_month(cursor) -> None:
    """Create or replace SQL function return first months day of ANY date"""
    create_function(cursor, functions_sql.first_day_of_month())


def create_or_replace_readings_with_the_nearest_date(cursor) -> None:
    """Create or replace SQL function to find records ID with date and device_id nearst readings date"""
    create_function(cursor, functions_sql.readings_with_the_nearest_date())


def create_or_replace_last_N_first_dates(cursor) -> None:
    """Create or replace SQL function to get ARRAY with last N months"""
    create_function(cursor, functions_sql.last_N_first_dates())


def create_or_replace_last_N_nearest_readings(cursor) -> None:
    """Create or replace function to get last N reading to device_id = dev_id on 01 day of all monts"""
    create_function(cursor, functions_sql.last_N_nearest_readings())


def create_or_replace_complexes_and_points_not_closed(cursor) -> None:
    """Create or replace function to SELECT points not closed ORDER complex and sub_points"""
    create_function(cursor, functions_sql.complexes_and_points_not_closed())


def create_or_replace_complexes_and_points_all(cursor) -> None:
    """Create or replace function to SELECT points not closed ORDER complex and sub_points"""
    create_function(cursor, functions_sql.complexes_and_points_all())


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
            create_or_replace_units_of_measure_string,
            create_or_replase_total_last_month,
            create_or_replace_average_from_last_readings,
            create_or_replace_analytics_in_scheme,
            create_or_replace_full_calculation_scheme,
            create_or_replace_full_calc_all_schemes_in_point,
            create_or_replace_first_day_of_month,
            create_or_replace_readings_with_the_nearest_date,
            create_or_replace_last_N_first_dates,
            create_or_replace_last_N_nearest_readings,
            create_or_replace_complexes_and_points_not_closed,
            create_or_replace_complexes_and_points_all]
