"""This module contain all SELECT to ORDER and BUG"""

from wh_app.sql.sql_constant import sql_consts_dict

from wh_app.sql.select_sql.points_select import log_decorator, limit_and_offset


__orders_columns = {1: 'orders.id', 2: 'point_name', 3: 'customer.description', 4: 'orders.date',
                        5: 'orders.closed_date', 6: 'problem', 7: 'ord_stat', 8: 'orders.comment', 9: 'workers.sub_name'}


@log_decorator
def sql_select_all_orders_type() -> str:
    """Return all orders type and descriptions"""

    query = """SELECT status, CASE WHEN status = 'in_work' THEN 'В работе' WHEN status = 'closed' THEN 'Закрыта' 
    ELSE 'Отменена' END AS description FROM unnest(enum_range(null::%(order_status)s)) AS status""" % sql_consts_dict

    return query


@log_decorator
def sql_select_all_orders_limit_ord(page_num: int, ord=False, ord_column=1) -> str:
    """Returns the query string to select all repairs corresponding to the orders use LIMIT"""
    if ord:
        try:
            formatter = __orders_columns[int(ord_column)]
        except:
            formatter = __orders_columns[1]
    else:
        formatter = __orders_columns[1]
    query = """SELECT orders.%(id)s, %(point_name)s, %(customer)s.%(description)s, %(orders)s.%(date)s, %(orders)s.%(closed_date)s,
     %(problem)s, (%(order_in_work)s) AS ord_stat, %(orders)s.comment, %(workers)s.%(sub_name)s FROM %(orders)s JOIN %(customer)s ON
      %(customer_id)s = %(customer)s.%(id)s JOIN %(workspoints)s ON %(workspoints)s.%(point_id)s = %(orders)s.%(point_id)s
       LEFT JOIN %(workers)s ON %(workers)s.%(id)s = %(orders)s.%(performer_id)s
       ORDER BY {0} """ % sql_consts_dict + limit_and_offset(page_num)

    return query.format(formatter)


@log_decorator
def sql_select_all_orders_from_customer_limit(customer_id: int, page_num: int) -> str:
    """Returns the query string to select all repairs corresponding to the orders use LIMIT"""

    query = """SELECT orders.%(id)s, %(point_name)s, %(customer)s.%(description)s, %(orders)s.%(date)s, %(orders)s.%(closed_date)s,
     %(problem)s, (%(order_in_work)s) AS ord_stat, %(orders)s.comment, %(workers)s.%(sub_name)s FROM %(orders)s JOIN %(customer)s ON
      (%(customer_id)s = {0} AND %(customer)s.%(id)s = %(customer_id)s) JOIN %(workspoints)s ON %(workspoints)s.%(point_id)s = %(orders)s.%(point_id)s
       LEFT JOIN %(workers)s ON %(workers)s.%(id)s = %(orders)s.%(performer_id)s
       ORDER BY %(id)s """ % sql_consts_dict + limit_and_offset(page_num)

    return query.format(customer_id)


@log_decorator
def sql_select_all_orders(ord=False, ord_column=1) -> str:
    """Return all records in table orders"""

    if ord:
        try:
            formatter = __orders_columns[int(ord_column)]
        except:
            formatter = __orders_columns[1]
    else:
        formatter = __orders_columns[1]

    query = ("""SELECT orders.%(id)s, %(point_name)s, %(customer)s.%(description)s, %(orders)s.%(date)s, %(orders)s.%(closed_date)s, %(problem)s, """ +
             """(%(order_in_work)s), %(orders)s.comment, %(workers)s.%(sub_name)s FROM %(orders)s JOIN %(customer)s 
             ON %(customer_id)s = %(customer)s.%(id)s
              JOIN %(workspoints)s ON %(workspoints)s.%(point_id)s = %(orders)s.%(point_id)s 
              LEFT JOIN %(workers)s ON %(workers)s.%(id)s = %(orders)s.%(performer_id)s ORDER BY {0}""") % sql_consts_dict

    return query.format(formatter)


@log_decorator
def sql_select_all_orders_from_customer_id(customer_id: int) -> str:
    """Return SELECT string to get all orders from customer with id = customer_id"""

    query = ("""SELECT orders.%(id)s, %(point_name)s, %(customer)s.%(description)s, %(orders)s.%(date)s,
     %(orders)s.%(closed_date)s, %(problem)s, (%(order_in_work)s), %(orders)s.comment, %(workers)s.%(sub_name)s FROM %(orders)s JOIN %(customer)s 
     ON (%(customer_id)s = {0} AND %(customer)s.%(id)s = %(customer_id)s) 
     JOIN %(workspoints)s ON %(workspoints)s.%(point_id)s = %(orders)s.%(point_id)s 
     LEFT JOIN %(workers)s ON %(workers)s.%(id)s = %(orders)s.%(performer_id)s ORDER BY %(id)s""") % sql_consts_dict

    return query.format(customer_id)


@log_decorator
def sql_select_no_closed_orders(ord=False, ord_column=1) -> str:
    """Return all records in table orders"""

    if ord:
        try:
            formatter = __orders_columns[int(ord_column)]
        except:
            formatter = __orders_columns[1]
    else:
        formatter = __orders_columns[1]

    query = ("""SELECT orders.%(id)s, %(point_name)s, %(customer)s.%(description)s, %(orders)s.%(date)s,
     %(orders)s.%(closed_date)s, %(problem)s, (%(order_in_work)s) AS ord_stat, %(orders)s.comment,
      %(workers)s.%(sub_name)s, row_number() OVER (ORDER BY orders.id) FROM %(orders)s
       JOIN %(customer)s ON %(customer_id)s = %(customer)s.%(id)s 
       JOIN %(workspoints)s ON %(workspoints)s.%(point_id)s = %(orders)s.%(point_id)s 
       LEFT JOIN %(workers)s ON %(workers)s.%(id)s = %(orders)s.%(performer_id)s 
       WHERE %(orders)s.%(status)s = 'in_work' ORDER BY {0}""") % sql_consts_dict

    return query.format(formatter)


@log_decorator
def sql_select_no_closed_orders_limit(page_num: int, ord=False, ord_column=1) -> str:
    """Return all records in table orders with LIMIT"""

    if ord:
        try:
            formatter = __orders_columns[int(ord_column)]
        except:
            formatter = __orders_columns[1]
    else:
        formatter = __orders_columns[1]

    query = ("""SELECT orders.%(id)s, %(point_name)s, %(customer)s.%(description)s, %(orders)s.%(date)s,
          %(orders)s.%(closed_date)s, %(problem)s, (%(order_in_work)s) AS ord_stat, %(orders)s.comment,
           %(workers)s.%(sub_name)s, row_number() OVER (ORDER BY orders.id) FROM %(orders)s
            JOIN %(customer)s ON %(customer_id)s = %(customer)s.%(id)s 
            JOIN %(workspoints)s ON %(workspoints)s.%(point_id)s = %(orders)s.%(point_id)s 
            LEFT JOIN %(workers)s ON %(workers)s.%(id)s = %(orders)s.%(performer_id)s 
            WHERE %(orders)s.%(status)s = 'in_work' ORDER BY {0}""") % sql_consts_dict + limit_and_offset(page_num)

    return query.format(formatter)


@log_decorator
def sql_select_max_order_id() -> str:
    """Return SELECT string with find maximal ID in orders table"""

    query = """SELECT MAX(%(id)s) FROM %(orders)s""" % sql_consts_dict
    return query


@log_decorator
def sql_select_order_from_id(order_id: str) -> str:
    """Return SQL query from select full information from ID = order_id"""

    query = """SELECT %(orders)s.%(id)s, %(point_name)s, %(customer)s.%(description)s, %(orders)s.%(date)s, %(orders)s.%(closed_date)s, %(problem)s,
     (%(order_in_work)s), %(orders)s.comment, %(workers)s.%(sub_name)s FROM %(orders)s JOIN %(customer)s ON %(customer_id)s = %(customer)s.%(id)s 
      JOIN %(workspoints)s ON %(workspoints)s.%(point_id)s = %(orders)s.%(point_id)s
       LEFT JOIN %(workers)s ON %(workers)s.%(id)s = %(orders)s.%(performer_id)s
       WHERE %(orders)s.%(id)s = {} """ % sql_consts_dict
    return query.format(order_id)


@log_decorator
def sql_select_all_bugs_in_bugzilla() -> str:
    """Return all records in bugzilla table"""

    query = ("""SELECT %(id)s, %(problem)s, %(bug_in_work)s,""" +
             """ TO_CHAR( %(date_start)s, 'yyyy-mm-dd HH:MI:SS'), TO_CHAR( %(date_close)s, 'yyyy-mm-dd HH:MI:SS')""" +
             """ FROM %(bugzilla)s ORDER BY %(id)s""") % sql_consts_dict
    return query


@log_decorator
def sql_select_all_bugs_in_bugzilla_limit(page_num: str) -> str:
    """Return all records in bugzilla table use paging"""

    query = ("""SELECT %(id)s, %(problem)s, %(bug_in_work)s,""" +
             """ TO_CHAR( %(date_start)s, 'yyyy-mm-dd HH:MI:SS'),""" +
             """ TO_CHAR( %(date_close)s, 'yyyy-mm-dd HH:MI:SS') FROM %(bugzilla)s """ +
             """ ORDER BY %(id)s """) % sql_consts_dict + limit_and_offset(page_num)
    return query


@log_decorator
def sql_select_all_bugs_in_work_in_bugzilla() -> str:
    """Return all records in bugzilla table if status = in work"""

    query = ("""SELECT %(id)s, %(problem)s, %(bug_in_work)s,""" +
             """ TO_CHAR( %(date_start)s, 'yyyy-mm-dd HH:MI:SS') FROM %(bugzilla)s""" +
             """ WHERE %(status)s = true ORDER BY %(id)s""") % sql_consts_dict
    return query


@log_decorator
def sql_select_all_bugs_in_work_in_bugzilla_limit(page_num: str) -> str:
    """Return all records in bugzilla table if status = in work"""

    query = ("""SELECT %(id)s, %(problem)s, %(bug_in_work)s,""" +
             """ TO_CHAR( %(date_start)s, 'yyyy-mm-dd HH:MI:SS') FROM %(bugzilla)s""" +
             """ WHERE %(status)s = true ORDER BY %(id)s """) % sql_consts_dict + limit_and_offset(page_num)
    return query


@log_decorator
def sql_select_get_bug_by_id(bug_id: str) -> str:
    """Return query string likes SELECT * FROM bugzilla WHERE id = 123"""

    query = ("""SELECT %(id)s, %(problem)s, %(bug_in_work)s, %(date_start)s, %(date_close)s
     FROM %(bugzilla)s WHERE %(id)s = {0}""") % sql_consts_dict
    return query.format(bug_id)


@log_decorator
def sql_select_last_orders_id_in_work() -> str:
    """Return query string to get last order id in work"""

    query = """SELECT %(id)s FROM %(orders)s WHERE %(status)s = 'in_work' ORDER BY %(id)s DESC LIMIT 1""" % sql_consts_dict
    return query


@log_decorator
def sql_select_orders_from_user_limit(user_name: str, page_num: int) -> str:
    """Return all records in table orders with LIMIT"""

    query = ("""SELECT orders.%(id)s, %(point_name)s, %(customer)s.%(description)s, %(orders)s.%(date)s, %(orders)s.%(closed_date)s, %(problem)s, """ +
             """(%(order_in_work)s), %(orders)s.comment, %(workers)s.%(sub_name)s, row_number()
              OVER (ORDER BY orders.id) FROM %(orders)s JOIN %(customer)s ON %(customer_id)s = %(customer)s.%(id)s""" +
             """ JOIN %(workspoints)s ON %(workspoints)s.%(point_id)s = %(orders)s.%(point_id)s
              LEFT JOIN %(workers)s ON %(workers)s.%(id)s = %(orders)s.%(performer_id)s
             WHERE full_name = '{}'
              ORDER BY %(id)s """) % sql_consts_dict + limit_and_offset(page_num)

    return query.format(user_name)


@log_decorator
def sql_select_orders_from_user(user_name: str) -> str:
    """Return ALL customers orders"""

    query = ("""SELECT orders.%(id)s, %(point_name)s, %(customer)s.%(description)s, %(orders)s.%(date)s, %(orders)s.%(closed_date)s, %(problem)s, """ +
             """(%(order_in_work)s), %(orders)s.comment, %(workers)s.%(sub_name)s, row_number()
              OVER (ORDER BY orders.id) FROM %(orders)s JOIN %(customer)s ON %(customer_id)s = %(customer)s.%(id)s""" +
             """ JOIN %(workspoints)s ON %(workspoints)s.%(point_id)s = %(orders)s.%(point_id)s
              LEFT JOIN %(workers)s ON %(workers)s.%(id)s = %(orders)s.%(performer_id)s
             WHERE full_name = '{}'
              ORDER BY %(id)s """) % sql_consts_dict

    return query.format(user_name)


@log_decorator
def sql_select_order_status(order_id: str) -> str:
    """Return status to order with id = order_id"""

    query = """SELECT %(status)s FROM %(orders)s WHERE %(id)s = {}""" % sql_consts_dict
    return query.format(order_id)