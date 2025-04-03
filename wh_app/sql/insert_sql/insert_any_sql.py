from wh_app.sql.sql_constant import sql_consts_dict
from wh_app.sql.select_sql.select_sql import log_decorator


@log_decorator
def sql_add_new_bug(problem: str) -> str:
    """Return SQL-string contain query to insert new record in bugzilla"""
    query = ("""INSERT INTO %(bugzilla)s (%(problem)s,""" +\
            """ %(status)s) VALUES ('{0}', true)""") % sql_consts_dict
    return query.format(problem)


@log_decorator
def sql_insert_new_session_in_sessions(hash: str) -> str:
    """Return INSERT string to add new session in sessions"""

    query = """INSERT INTO %(sessions_hashs)s (%(hash)s) VALUES ('{0}')""" % sql_consts_dict
    return query.format(hash)