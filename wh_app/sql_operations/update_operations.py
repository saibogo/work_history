from wh_app.sql.update_sql import *

functions.info_string(__name__)


def update_point_information(cursor, point_id: str, point_name:str, point_address: str) -> None:
    """Update point info in database"""

    cursor.execute(sql_update_point(point_id, point_name, point_address))


def invert_point_is_work(cursor, point_id:str) -> None:
    """Invert is_work status"""

    cursor.execute(sql_inverse_points_status(point_id))


def update_equip_information(cursor, equip_id: str, equip_name: str, equip_model: str,
                             equip_serial: str, equip_pre_id: str) -> None:
    """Update equip info in database"""

    cursor.execute(sql_update_equip(equip_id, equip_name, equip_model, equip_serial, equip_pre_id))
