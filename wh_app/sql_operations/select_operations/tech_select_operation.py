from wh_app.sql_operations.select_operations.decorators import *
from wh_app.sql.select_sql import select_sql


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


@list_to_first_decimal_decorator
@get_selected_decorator
def get_last_month_consumption_from_device(cursor, device_id: int) -> float:
    """Return calculation consumption in last 28, 29, 30 or 31 days"""

    return select_sql.sql_select_last_month_from_device_id(device_id)


@list_to_first_decimal_decorator
@get_selected_decorator
def get_average_from_device_id(cursor, device_id: int) -> float:
    """Return average from two last reading. If error function -> 0"""

    return select_sql.sql_select_average_from_device_id(device_id)


@list_to_list_decorator
@list_to_list_decorator
@get_selected_decorator
def get_calculation_in_scheme(cursor, scheme_id: int) -> Tuple:
    """Return tuple contain (average, average for month future, average sum between two last reading)"""

    return select_sql.sql_select_calculate_in_scheme(scheme_id)


@list_to_first_tuple_decorator
@list_to_first_tuple_decorator
@get_selected_decorator
def get_all_full_calc_schemes_in_point(cursor, point_id: int):
    """Return all calculated data for all schemes in point"""

    return select_sql.sql_select_full_calc_all_schemes_in_point(point_id)