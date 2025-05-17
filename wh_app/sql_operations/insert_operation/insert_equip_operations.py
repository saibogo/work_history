from wh_app.sql_operations.select_operations import select_operations
from wh_app.sql.insert_sql.insert_sql import *


def create_new_equip(cursor, point_id: str, name: str,
                     model: str = "not model", serial_num: str = "not number", pre_id: str = "") -> None:
    """Creates a new piece of equipment in the database"""

    new_id = int(select_operations.get_next_equip_id(cursor))
    cursor.execute(sql_insert_new_equip(new_id ,point_id, name, model, serial_num,
                                        pre_id if pre_id != "" else str(new_id)))


def insert_new_equip_subclass(cursor, meta_class: str, new_class: str, new_dir: str, description: str) -> None:
    """Add new equip`s class in database"""

    cursor.execute(sql_insert_new_equips_class(meta_class, new_class, new_dir, description))


def insert_new_equips_detail(cursor, equip_type: int, filename: str, description: str) -> None:
    """Add new equips detail in database"""

    cursor.execute(sql_insert_new_equip_detail(equip_type, filename, description))


def insert_new_equips_manual(cursor, equip_type: int, filename: str, description: str) -> None:
    """Add new equips detail in database"""

    cursor.execute(sql_insert_new_equip_manual(equip_type, filename, description))

