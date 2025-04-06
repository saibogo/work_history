from wh_app.sql_operations.select_operations import select_operations
from wh_app.sql.insert_sql.insert_sql import *


def create_new_point(cursor, point_name: str, point_address: str, main_point_id: int) -> None:
    """Creates a new point in the database"""

    new_point_id = str(int(select_operations.get_maximal_points_id(cursor)) + 1)
    cursor.execute(sql_insert_new_point(new_point_id, point_name, point_address, main_point_id))


def insert_tech_section(cursor, section: str, point_id: str, dogovor: str, resume: str) -> None:
    """Update section in technical information for workpoint"""

    cursor.execute(sql_insert_tech_section(point_id, section, dogovor, resume))


def insert_new_reading_to_meter_device(cursor, device_id: int, reading_date: str, value: int) -> None:
    """Add new record in history current device meter"""

    cursor.execute(sql_add_new_reading_to_meter_device(device_id, reading_date, value))