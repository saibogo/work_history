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


def invert_worker_status(cursor, worker_id: str) -> None:
    """Invert current worker-status"""

    cursor.execute(sql_inverse_worker_status(worker_id))


def update_worker_info(cursor, worker_id: str, name: str, sub_name: str, phone_number: str,
                       post_id: str) -> None:
    """Update information for selected worker in workers-table"""

    cursor.execute(sql_update_worker_info(worker_id, name, sub_name, phone_number, post_id))


def update_work_info(cursor, work_id: str, order_info: str, description: str, work_datetime: str) -> None:
    """Update information for selected work"""

    cursor.execute(sql_update_work_info(work_id, order_info, description, work_datetime))


def set_deleted_status(cursor, equip_id: str) -> None:
    """Create label DELETED to equip"""

    cursor.execute(sql_set_deleted_status(equip_id))


def invert_bug_status_in_bugzilla(cursor, bug_id: str) -> None:
    """On-OFF bug-status in database"""

    cursor.execute(sql_invert_bug_status(bug_id))


def update_tech_section(cursor, section: str, point_id: str, dogovor: str, resume: str) -> None:
    """Update section in technical information for workpoint"""

    cursor.execute(sql_update_tech_section(point_id, section, dogovor, resume))

