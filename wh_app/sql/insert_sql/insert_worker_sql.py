from wh_app.sql.sql_constant import sql_consts_dict
from wh_app.sql.select_sql.select_sql import log_decorator


@log_decorator
def sql_add_new_performers(work_id: str, worker_id: str) -> str:
    """Return SQL-string contain query to insert new performer in performers table"""
    query = ("""INSERT INTO %(performers)s (%(work_id)s,""" +\
            """ %(worker_id)s) VALUES ('{0}', '{1}')""") % sql_consts_dict
    return query.format(work_id,
                        worker_id)


@log_decorator
def sql_insert_new_binding(point_id: str, worker_id: str, is_main: str) -> str:
    """Return SQL-string to insert new bindings in database"""
    query = """INSERT INTO %(bindings)s (%(worker_id)s, %(point_id)s, %(is_main)s)
     VALUES ({0}, {1}, {2})""" % sql_consts_dict
    return query.format(worker_id, point_id, is_main)


@log_decorator
def sql_add_new_worker(name: str, sub_name: str, phone_number: str, post_id: int) -> str:
    """Return SQL-string contain query to insert new worker in workers table"""
    query = """INSERT INTO %(workers)s (%(name)s, %(sub_name)s, %(phone_number)s, %(post_id)s) VALUES
     ('{0}', '{1}', '{2}', {3})""" % sql_consts_dict
    return query.format(name, sub_name, phone_number, post_id)


@log_decorator
def sql_add_new_day_in_schedule(work_day: str, worker_id: int, day_type: str) -> str:
    """Return SQL-string to insert new schedule-day in schedule database"""
    query = """INSERT INTO %(workers_schedule)s VALUES('{0}', {1}, '{2}')""" % sql_consts_dict
    return query.format(work_day, worker_id, day_type)