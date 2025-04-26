"""This module contain functions to CALL procedures in database"""

from wh_app.supporting import functions
from wh_app.sql.select_sql.select_sql import log_decorator

functions.info_string(__name__)


@log_decorator
def call_delete_all_closed_sessions() -> str:
    """Return string to CALL delete all closed session procedure"""

    return """CALL delete_not_active_sessions();"""


@log_decorator
def call_update_all_old_sessions() -> str:
    """Return string to CALL find and update all session record with start_date older 48 hours"""

    return """CALL update_old_sessions();"""


@log_decorator
def call_vacuum_tables() -> str:
    """Return string to CALL vacuum_tables PROCEDURE"""

    return """CALL vacuum_tables()"""