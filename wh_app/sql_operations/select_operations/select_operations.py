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

