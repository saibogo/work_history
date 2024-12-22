"""This module contain all SELECT to ORDER and BUG"""

from wh_app.sql.sql_constant import sql_consts_dict

from wh_app.sql.select_sql.points_select import log_decorator, limit_and_offset


@log_decorator
def sql_select_all_orders_type() -> str:
    """Return all orders type and descriptions"""

    query = """SELECT status, CASE WHEN status = 'in_work' THEN 'В работе' WHEN status = 'closed' THEN 'Закрыта' 
    ELSE 'Отменена' END AS description FROM unnest(enum_range(null::%(order_status)s)) AS status""" % sql_consts_dict

    return query


@log_decorator
def sql_select_all_orders_limit(page_num: int) -> str:
    """Returns the query string to select all repairs corresponding to the orders use LIMIT"""

    query = """SELECT orders.%(id)s, %(point_name)s, %(customer)s.%(full_name)s, %(orders)s.%(date)s, %(orders)s.%(closed_date)s,
     %(problem)s, (%(bug_in_work)s), %(orders)s.comment FROM %(orders)s JOIN %(customer)s ON
      %(customer_id)s = %(customer)s.%(id)s JOIN %(workspoints)s ON %(workspoints)s.%(point_id)s = %(orders)s.%(point_id)s
       ORDER BY %(id)s """ % sql_consts_dict + limit_and_offset(page_num)

    return query


@log_decorator
def sql_select_all_orders() -> str:
    """Return all records in table orders"""

    query = ("""SELECT orders.%(id)s, %(point_name)s, %(customer)s.%(full_name)s, %(orders)s.%(date)s, %(orders)s.%(closed_date)s, %(problem)s, """ +
             """(%(bug_in_work)s), %(orders)s.comment FROM %(orders)s JOIN %(customer)s ON %(customer_id)s = %(customer)s.%(id)s""" +
             """ JOIN %(workspoints)s ON %(workspoints)s.%(point_id)s = %(orders)s.%(point_id)s ORDER BY %(id)s""") % sql_consts_dict

    return query


@log_decorator
def sql_select_no_closed_orders() -> str:
    """Return all records in table orders"""

    query = ("""SELECT orders.%(id)s, %(point_name)s, %(customer)s.%(full_name)s, %(orders)s.%(date)s, %(orders)s.%(closed_date)s, %(problem)s, """ +
             """(%(bug_in_work)s), %(orders)s.comment, row_number() OVER (ORDER BY orders.id) FROM %(orders)s JOIN %(customer)s ON %(customer_id)s = %(customer)s.%(id)s""" +
             """ JOIN %(workspoints)s ON %(workspoints)s.%(point_id)s = %(orders)s.%(point_id)s WHERE %(status)s =
              'in_work' ORDER BY %(id)s""") % sql_consts_dict

    return query


@log_decorator
def sql_select_no_closed_orders_limit(page_num: int) -> str:
    """Return all records in table orders with LIMIT"""

    query = ("""SELECT orders.%(id)s, %(point_name)s, %(customer)s.%(full_name)s, %(orders)s.%(date)s, %(orders)s.%(closed_date)s, %(problem)s, """ +
             """(%(bug_in_work)s), %(orders)s.comment, row_number() OVER (ORDER BY orders.id) FROM %(orders)s JOIN %(customer)s ON %(customer_id)s = %(customer)s.%(id)s""" +
             """ JOIN %(workspoints)s ON %(workspoints)s.%(point_id)s = %(orders)s.%(point_id)s WHERE %(status)s =
              'in_work' ORDER BY %(id)s """) % sql_consts_dict + limit_and_offset(page_num)

    return query


@log_decorator
def sql_select_max_order_id() -> str:
    """Return SELECT string with find maximal ID in orders table"""

    query = """SELECT MAX(%(id)s) FROM %(orders)s""" % sql_consts_dict
    return query


@log_decorator
def sql_select_order_from_id(order_id: str) -> str:
    """Return SQL query from select full information from ID = order_id"""

    query = """SELECT %(orders)s.%(id)s, %(point_name)s, %(customer)s.%(full_name)s, %(orders)s.%(date)s, %(orders)s.%(closed_date)s, %(problem)s,
     (%(bug_in_work)s), %(orders)s.comment FROM %(orders)s JOIN %(customer)s ON %(customer_id)s = %(customer)s.%(id)s 
      JOIN %(workspoints)s ON %(workspoints)s.%(point_id)s = %(orders)s.%(point_id)s WHERE %(orders)s.%(id)s = {} """ % sql_consts_dict
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