from wh_app.sql.sql_constant import sql_consts_dict, tech_tables
from wh_app.sql.select_sql.select_sql import log_decorator


@log_decorator
def sql_update_work_info(work_id: str, order_info: str, description: str, work_datetime: str) -> str:
    """return the query string to update work information"""

    query = ("""UPDATE %(works)s SET %(problem)s = '{1}', %(result)s = '{2}', %(date)s = '{3}'
     WHERE id = {0}""") % sql_consts_dict
    return query.format(work_id, order_info, description, work_datetime)


@log_decorator
def sql_update_set_session_inactive(session_id: int) -> str:
    """Update sessions_hash -> is_active = False"""

    query = """UPDATE %(sessions_hashs)s SET %(is_active)s = False WHERE %(id)s = {0}""" % sql_consts_dict
    return query.format(session_id)
