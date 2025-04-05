from wh_app.sql.select_sql.select_sql import log_decorator
from wh_app.sql.sql_constant import sql_consts_dict


@log_decorator
def sql_invert_bug_status(bug_id: str) -> str:
    """Create query to inverted bug-status in database"""

    query = ("""UPDATE %(bugzilla)s SET %(status)s = NOT %(status)s,""" + \
             """ %(date_close)s = CASE %(status)s WHEN true THEN NOW() ELSE NULL END """ + \
             """  WHERE %(id)s = {}""") % sql_consts_dict
    return query.format(bug_id)


@log_decorator
def sql_update_order_info_in_work(order_id: str, comment: str) -> str:
    """Create query to set order status in in_work and update comment"""

    query = """UPDATE %(orders)s SET %(status)s = 'in_work', %(closed_date)s = NULL, %(comment)s = '{1}'
     WHERE %(id)s = {0}""" % sql_consts_dict
    return query.format(order_id, comment)


@log_decorator
def sql_update_order_info_not_work(order_id: str, status: str, comment: str) -> str:
    """Create query to set order status in in_work and update comment"""

    query = """UPDATE %(orders)s SET %(status)s = '{1}', %(closed_date)s = NOW(), %(comment)s = '{2}' WHERE %(id)s = {0}
     """ % sql_consts_dict
    return query.format(order_id, status, comment)


@log_decorator
def sql_update_invert_customer_status(customer_id: int) -> str:
    """Update is_active customer's status in database"""

    query = """UPDATE %(customer)s SET %(is_active)s = NOT %(is_active)s WHERE %(id)s = {}""" % sql_consts_dict
    return query.format(customer_id)


@log_decorator
def sql_update_customer_password(customer_id: int, new_password_hash: str) -> str:
    """Update password to customer with id = customer_id"""

    query = """UPDATE %(customer)s SET %(hash_pass)s = '{1}' WHERE %(id)s = {0}""" % sql_consts_dict
    return query.format(customer_id, new_password_hash)


@log_decorator
def sql_update_performer_in_order(order_id: int, performer_id: int) -> str:
    """Update performer in order with id = order_id"""

    query = """UPDATE %(orders)s SET %(performer_id)s = {0} WHERE %(id)s = {1}""" % sql_consts_dict
    return query.format(performer_id, order_id)