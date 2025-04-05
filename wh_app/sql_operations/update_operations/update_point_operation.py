from wh_app.sql.update_sql.update_sql import *


def update_point_information(cursor, point_id: str, point_name:str, point_address: str) -> None:
    """Update point info in database"""

    cursor.execute(sql_update_point(point_id, point_name, point_address))


def invert_point_is_work(cursor, point_id:str) -> None:
    """Invert is_work status"""

    cursor.execute(sql_inverse_points_status(point_id))


def update_meter_reading(cursor, device_id: int, current_date: str, new_reading: float) -> None:
    """Update reading in database where device_id and current_date"""

    cursor.execute(sql_update_meter_reading(device_id, current_date, new_reading))


def update_tech_section(cursor, section: str, point_id: str, dogovor: str, resume: str) -> None:
    """Update section in technical information for workpoint"""

    cursor.execute(sql_update_tech_section(point_id, section, dogovor, resume))