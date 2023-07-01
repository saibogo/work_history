from wh_app.sql.delete_sql import *

functions.info_string(__name__)


def delete_binding(cursor, binding_id: str) -> None:
    """Delete binding with selected id in database"""
    cursor.execute(sql_delete_binding(binding_id))


def delete_performer_from_work(cursor, work_id: str, performer_id: str) -> None:
    """Delete record with performer = performer_id in work = work_id"""
    cursor.execute(sql_delete_performer(work_id, performer_id))