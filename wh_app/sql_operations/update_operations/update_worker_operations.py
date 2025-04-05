from wh_app.sql.update_sql.update_sql import *


def invert_worker_status(cursor, worker_id: str) -> None:
    """Invert current worker-status"""

    cursor.execute(sql_inverse_worker_status(worker_id))


def update_worker_info(cursor, worker_id: str, name: str, sub_name: str, phone_number: str,
                       post_id: str, status: str, employee_date: datetime.date) -> None:
    """Update information for selected worker in workers-table"""

    cursor.execute(sql_update_worker_info(worker_id, name, sub_name, phone_number, post_id, status, employee_date))


def set_worker_dismissal_date(cursor, worker_id: id) -> None:
    """Set dismissal_date"""

    cursor.execute(sql_update_dismissla_date(worker_id))


def set_worker_dismissal_date_in_null(cursor, worker_id: id) -> None:
    """Set dismissal_date in Null"""

    cursor.execute(sql_remove_dismissal_date(worker_id))


def update_schedule_day(cursor, worker_id: int, work_date: str, day_type: str) -> None:
    """Update information from day type in schedule table"""

    cursor.execute(sql_update_schedule(worker_id, work_date, day_type))


def update_performer_in_order(cursor, order_id: int, performer_id: int) -> None:
    """Set worker with id = performer_in in order with id = order_id"""

    cursor.execute(sql_update_performer_in_order(order_id, performer_id))