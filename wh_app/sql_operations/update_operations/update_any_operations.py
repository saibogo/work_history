from wh_app.sql.update_sql.update_sql import *


def update_work_info(cursor, work_id: str, order_info: str, description: str, work_datetime: str) -> None:
    """Update information for selected work"""

    cursor.execute(sql_update_work_info(work_id, order_info, description, work_datetime))


def update_set_session_inactive(cursor, session_id: int) -> None:
    """Set is_active = False to session with session_id"""

    cursor.execute(sql_update_set_session_inactive(session_id))