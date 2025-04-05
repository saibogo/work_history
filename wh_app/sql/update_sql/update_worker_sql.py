import datetime

from wh_app.sql.sql_constant import sql_consts_dict, tech_tables
from wh_app.sql.select_sql.select_sql import log_decorator


@log_decorator
def sql_inverse_worker_status(worker_id: str) -> str:
    """Return the query string to invert is_work column in workers-table"""

    query = ("""UPDATE %(workers)s SET %(is_work)s = NOT %(is_work)s where ID = {0}""") % sql_consts_dict
    return query.format(worker_id)


@log_decorator
def sql_update_worker_info(worker_id: str, name: str, sub_name: str, phone_number: str, post_id: str,
                           status: str, employee_date: datetime.date) -> str:
    """Return the query string to update worker information"""

    query = ("""UPDATE %(workers)s SET %(name)s = '{0}', %(sub_name)s = '{1}', """ +
             """ %(phone_number)s = '{2}', %(post_id)s = {3}, %(status)s = '{4}', %(emloyee_date)s = '{5}'""" +
             """ WHERE %(id)s = {6}""") % sql_consts_dict
    return query.format(name, sub_name, phone_number, post_id, status, employee_date, worker_id)


@log_decorator
def sql_update_dismissla_date(worker_id: str) -> str:
    """Return the query string to set dismissal_date"""

    query = """UPDATE %(workers)s SET %(dismissal_date)s = NOW()::DATE WHERE %(id)s = {0}""" % sql_consts_dict
    return query.format(worker_id)


@log_decorator
def sql_remove_dismissal_date(worker_id: str) -> str:
    """Return the query string to set dissmissal_date in NULL"""

    query = """UPDATE %(workers)s SET %(dismissal_date)s = NULL WHERE %(id)s = {0}""" % sql_consts_dict
    return query.format(worker_id)


@log_decorator
def sql_update_schedule(worker_id: int, work_date: str, day_type: str) -> str:
    """Create query to update schedule table"""

    query = """UPDATE %(workers_schedule)s SET %(day_type)s = '{}' WHERE %(work_date)s = '{}'
     AND %(worker_id)s = {}""" % sql_consts_dict
    return query.format(day_type, work_date, worker_id)