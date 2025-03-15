"""This module contain all SELECT to USER"""

from wh_app.sql.sql_constant import sql_consts_dict

from wh_app.sql.select_sql.points_select import log_decorator


@log_decorator
def sql_select_all_bindings_to_point(point_id: str):
    """Return SQL to all workers bindings in current point"""
    query = """SELECT %(bindings)s.%(id)s, %(sub_name)s, %(is_main)s FROM %(bindings)s 
    JOIN %(workers)s ON %(bindings)s.%(worker_id)s = %(workers)s.%(id)s WHERE %(point_id)s = {0}""" % sql_consts_dict
    return query.format(point_id)


@log_decorator
def sql_select_all_customers() -> str:
    """Return all records in table customer"""

    return """SELECT %(id)s, %(full_name)s, %(description)s FROM %(customer_table)s ORDER BY %(id)s""" % sql_consts_dict


@log_decorator
def sql_select_customer_info(customer_id: str) -> str:
    """Return full information from customer_id"""

    return ("""SELECT * FROM %(customer_table)s WHERE %(id)s = {0}""" % sql_consts_dict).format(customer_id)


@log_decorator
def sql_select_all_posts() -> str:
    """Return SELECT-query to ALL POST in database"""

    query = ("""SELECT * FROM %(posts)s""") % sql_consts_dict
    return query


@log_decorator
def sql_select_user_in_customers(user_name: str) -> str:
    """Return SQL-string to find user in customer table"""

    query = """SELECT '{0}' IN (SELECT %(full_name)s FROM %(customer)s) as all_users""" % sql_consts_dict
    return query.format(user_name)


@log_decorator
def sql_select_hash_from_user(user_name: str) -> str:
    """Return SQL-string to find hash from user = full_name"""

    query = """SELECT %(hash_pass)s FROM %(customer)s WHERE %(full_name)s = '{0}'""" % sql_consts_dict
    return query.format(user_name)


@log_decorator
def sql_select_all_telegram_chats() -> str:
    """Return SQL-string to select all telegramm chats"""

    query = """SELECT ARRAY(SELECT %(chat_id)s FROM %(chats)s WHERE %(is_blocked)s = False)""" % sql_consts_dict
    return query


@log_decorator
def sql_select_telegram_user_is_reader(user_id: int) -> str:
    """Return SQL-string to true/false from current user read access"""

    query = """SELECT {0} IN (SELECT %(chat_id)s FROM %(chats)s WHERE %(acs_read)s = True 
    AND %(is_blocked)s = False)""" % sql_consts_dict
    return query.format(user_id)


@log_decorator
def sql_select_telegram_user_is_writer(user_id: int) -> str:
    """Return SQL-string to true/false from current user write access"""

    query = """SELECT {0} IN (SELECT %(chat_id)s FROM %(chats)s WHERE %(acs_write)s = True 
    AND %(is_blocked)s = False)""" % sql_consts_dict
    return query.format(user_id)