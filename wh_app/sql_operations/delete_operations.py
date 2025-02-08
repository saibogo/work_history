from wh_app.sql.delete_sql import *

functions.info_string(__name__)


def delete_binding(cursor, binding_id: str) -> None:
    """Delete binding with selected id in database"""
    cursor.execute(sql_delete_binding(binding_id))


def delete_performer_from_work(cursor, work_id: str, performer_id: str) -> None:
    """Delete record with performer = performer_id in work = work_id"""
    cursor.execute(sql_delete_performer(work_id, performer_id))


def delete_work_day_from_schedule(cursor, worker_id: int, work_date: str) -> None:
    """Delete record from schedule with work_day and worker_id"""
    cursor.execute(sql_delete_day_from_schedule(worker_id, work_date))