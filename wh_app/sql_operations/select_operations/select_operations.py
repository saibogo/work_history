import datetime

import psycopg2

from wh_app.supporting import functions
from wh_app.sql.select_sql import select_sql
from wh_app.sql_operations.select_operations.decorators import *
from wh_app.sql_operations.select_operations.point_select_operation import *
from wh_app.sql_operations.select_operations.equip_select_operations import *
from wh_app.sql_operations.select_operations.works_select_operations import *
from wh_app.sql_operations.select_operations.workers_select_operations import *
from wh_app.sql_operations.select_operations.tech_select_operation import *
from wh_app.sql_operations.select_operations.statictic_select_operations import *
from wh_app.sql_operations.select_operations.orders_and_customers_select_operations import *
from wh_app.sql_operations.select_operations.bugs_select_operations import *
from wh_app.sql_operations.select_operations.telegram_select_operations import *
from wh_app.sql_operations.select_operations.find_select_operations import *


def commit(connection: psycopg2.connect) -> None:
    """Applies changes to the database"""

    connection.commit()


@list_to_first_int_decorator
@get_selected_decorator
def get_last_id_in_sessions(cursor) -> int:
    """Return last id from sessions in database"""

    return select_sql.sql_select_last_session_id()


@list_to_first_str_decorator
@get_selected_decorator
def get_session_hash_from_id(cursor, session_id: int) -> str:
    """Return session hash if session active. Else exception"""

    return select_sql.sql_select_session_hash_from_id(session_id)