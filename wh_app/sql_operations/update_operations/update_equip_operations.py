from wh_app.sql.update_sql.update_sql import *


def update_equip_information(cursor, equip_id: str, equip_name: str, equip_model: str,
                             equip_serial: str, equip_pre_id: str) -> None:
    """Update equip info in database"""

    cursor.execute(sql_update_equip(equip_id, equip_name, equip_model, equip_serial, equip_pre_id))


def set_deleted_status(cursor, equip_id: str) -> None:
    """Create label DELETED to equip"""

    cursor.execute(sql_set_deleted_status(equip_id))


def update_equip_in_work_record(cursor, work_id: str, equip_id: str) -> None:
    """Update equip_id in work-record with id == work_id"""

    cursor.execute(sql_update_equip_in_works(work_id, equip_id))


def update_set_detail_id_to_equip(cursor, equip_id: int, detail_id: int) -> None:
    """Attach detail_id to equip with equip_id"""

    cursor.execute(sql_update_attach_detail_to_equip(equip_id, detail_id))


def update_set_manual_id_to_equip(cursor, equip_id: int, manual_id: int) -> None:
    """Attach manual_id to equip with equip_id"""

    cursor.execute(sql_update_attach_manual_to_equip(equip_id, manual_id))