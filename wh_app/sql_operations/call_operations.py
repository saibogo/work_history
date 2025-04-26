from wh_app.sql.call_sql import *

functions.info_string(__name__)


def delete_all_closed_session_records(cursor) -> None:
    """Delete all sessions records with status != active"""

    cursor.execute(call_delete_all_closed_sessions())


def set_all_old_session_that_closed(cursor) -> None:
    """Update is_active = False in all sessions records with start_date > 48 hours"""

    cursor.execute(call_update_all_old_sessions())


def find_all_table_to_vacuum(cursor) -> None:
    """CALL vacuum_tables PROCEDURE to find all tables with dead strings"""

    cursor.execute(call_vacuum_tables())