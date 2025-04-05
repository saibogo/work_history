from wh_app.sql.update_sql.update_sql import *


def invert_bug_status_in_bugzilla(cursor, bug_id: str) -> None:
    """On-OFF bug-status in database"""

    cursor.execute(sql_invert_bug_status(bug_id))


def update_order_info_in_work(cursor, order_id: str, comment: str) -> None:
    """set order status 'in_work' and update information"""

    cursor.execute(sql_update_order_info_in_work(order_id, comment))


def update_order_info_not_work(cursor, order_id: str, status: str,comment: str) -> None:
    """set order status 'in_work' and update information"""

    cursor.execute(sql_update_order_info_not_work(order_id, status,comment))


def update_invert_customer_status(cursor, customer_id: int) -> None:
    """Invert is_active customer's status in database"""

    cursor.execute(sql_update_invert_customer_status(customer_id))


def update_customer_hash_pass(cursor, customer_id: int, new_hash: str) -> None:
    """Update hash_pass to customer with id = customer_id"""

    cursor.execute(sql_update_customer_password(customer_id, new_hash))