from wh_app.sql.sql_constant import sql_consts_dict
from wh_app.sql.select_sql.select_sql import log_decorator


@log_decorator
def sql_add_new_order(customer_id: str, point_id: str, order_info: str) -> str:
    """Return SQL-string contain query to insert new order in orders table"""
    query = """INSERT INTO %(orders)s (%(customer_id)s, %(date)s, %(status)s, %(problem)s, %(point_id)s) 
    VALUES ({0}, NOW(), 'in_work', '{1}', {2})""" % sql_consts_dict
    return query.format(customer_id, order_info, point_id)


@log_decorator
def sql_add_new_customer(nickname: str, description: str, hash_pass: str) -> str:
    """Return INSERT string to add new customer"""

    query = """INSERT INTO %(customer)s (%(hash_pass)s, %(full_name)s, %(description)s) VALUES ('{}', '{}', '{}')""" % sql_consts_dict
    return query.format(hash_pass, nickname, description)