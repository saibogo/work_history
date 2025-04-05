from wh_app.sql_operations.select_operations import select_operations
from wh_app.sql.insert_sql.insert_sql import *


def insert_new_order(cursor, customer_id: str, point_id: str, order_info: str) -> None:
    """add new order in database"""

    cursor.execute(sql_add_new_order(customer_id, point_id, order_info))


def insert_new_customer_in_database(cursor, nickname: str, description: str, hash_pass: str) -> None:
    """Add new customer in database"""

    cursor.execute(sql_add_new_customer(nickname, description, hash_pass))