from wh_app.sql.sql_constant import sql_consts_dict
from wh_app.sql.select_sql.select_sql import log_decorator


@log_decorator
def sql_insert_new_work(work_id: str, id_obor: str, date: str,
                        problem: str, result: str, worker_id: str) -> str:
    """Function return query string to add new work"""
    query = ("""BEGIN; INSERT INTO %(works)s (%(id)s,""" +\
            """ %(id_obor)s, %(date)s, %(problem)s, %(result)s) """ +\
            """VALUES ('{0}', '{1}', '{2}', '{3}', '{4}'); """ +\
            """INSERT INTO %(performers)s (%(work_id)s, %(worker_id)s)""" +\
            """ VALUES ('{5}', '{6}'); COMMIT;""") % sql_consts_dict
    return query.format(work_id,
                        id_obor,
                        date,
                        problem,
                        result,
                        work_id,
                        worker_id)