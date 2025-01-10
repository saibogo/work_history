"""This module contain all SELECT to WORKERS"""

from wh_app.sql.sql_constant import sql_consts_dict
from wh_app.sql.select_sql.points_select import log_decorator


@log_decorator
def sql_select_all_workers() -> str:
    """Return SQL-query return table with all workers"""

    return """SELECT * FROM %(all_workers)s""" % sql_consts_dict


@log_decorator
def sql_select_all_workers_in_work(work_id: str) -> str:
    """Return SQL-query return table with all workers"""
    query = """SELECT %(worker_id)s, %(sub_name)s FROM %(performers)s 
    JOIN %(workers)s ON %(worker_id)s = %(workers)s.%(id)s WHERE %(work_id)s = {0}""" % sql_consts_dict
    return query.format(work_id)


@log_decorator
def sql_select_all_current_performers_in_work(work_id: str) -> str:
    """Return SQL-query will return table with all workers in current work"""
    query = """SELECT %(worker_id)s, %(sub_name)s, %(name)s, %(phone_number)s, worker_status_to_string(%(status)s),
     %(post_name)s, %(emloyee_date)s FROM %(performers)s 
     JOIN %(workers)s ON %(workers)s.%(id)s = %(performers)s.%(worker_id)s 
     JOIN %(posts)s ON %(posts)s.%(id)s = %(workers)s.%(post_id)s
     WHERE %(work_id)s = {0} AND %(worker_is_work)s""" % sql_consts_dict

    return query.format(work_id)


@log_decorator
def sql_select_all_workers_real() -> str:
    """Also sql_select_all_workers() where is_work == TRUE"""

    return """SELECT * FROM %(all_workers)s WHERE %(all_workers)s.%(case)s != 'Уволен'""" % sql_consts_dict


@log_decorator
def sql_select_worker_info(worker_id: str) -> str:
    """Return full info from worker where ID = worker_id"""

    query = """SELECT * FROM %(all_workers)s WHERE ID = {0}""" % sql_consts_dict
    return query.format(worker_id)


@log_decorator
def sql_select_table_current_workers() -> str:
    """Return SQL-query contain table workers"""

    return ("""SELECT %(id)s, %(sub_name)s, %(name)s, %(phone_number)s, "%(case)s", %(post_name)s, %(emloyee_date)s """ +\
            """FROM %(all_workers)s WHERE %(id)s NOT IN """ +\
            """(SELECT %(id)s FROM %(workers)s WHERE %(status)s = 'fired')""") % sql_consts_dict


@log_decorator
def sql_select_worker_id_like_str(pattern: str) -> str:
    """Return query like worker name or sub_name liked pattern"""

    query = """SELECT %(id)s FROM %(workers)s WHERE LOWER(%(name)s) = LOWER('{0}') 
    OR LOWER(%(sub_name)s) = LOWER('{0}')""" % sql_consts_dict
    return query.format(pattern)


@log_decorator
def sql_select_all_description_worker_status() -> str:
    """Return query contain select to all pairs [status - description]"""

    query = """SELECT name_status, worker_status_to_string(name_status) AS descript
    FROM (SELECT unnest(enum_range(NULL::worker_status)) AS name_status) AS t;"""
    return query


@log_decorator
def sql_select_worker_id_from_chats(user_id: int) -> str:
    """Return SQL-string to find worker_id with current chat_id"""

    query = """SELECT %(worker_id)s FROM %(chats)s WHERE %(chat_id)s = {0}""" % sql_consts_dict
    return query.format(user_id)


@log_decorator
def sql_select_schedule_from_date(date: str) -> str:
    """Return SQL-string fo select all worker and schedule for selected date
    Date is format: YYYY-MM-DD"""

    query = """SELECT DISTINCT date_to_date_and_day_string(%(work_date)s), %(name)s, %(sub_name)s, %(post_name)s,
     %(phone_number)s, work_day_type_to_string(%(day_type)s)
        FROM %(workers_schedule)s
        JOIN %(workers)s ON %(workers)s.%(id)s = %(worker_id)s
        JOIN %(posts)s ON %(posts)s.%(id)s = %(workers)s.%(post_id)s 
      WHERE %(worker_is_work)s AND %(work_date)s = '{}'::date
       ORDER BY %(sub_name)s, %(name)s""" % sql_consts_dict

    return query.format(date)


@log_decorator
def sql_select_all_work_days_type() -> str:
    """Return all pairs (work day type, str(work day type))"""

    query = """SELECT tmp1, work_day_type_to_string(tmp1) FROM (SELECT unnest(enum_range(NULL::work_day_type)) AS tmp1)
     AS tmp""" % sql_consts_dict

    return query