"""This module contain all SELECT to WORK"""

from wh_app.sql.sql_constant import sql_consts_dict
from wh_app.config_and_backup import config

from wh_app.sql.select_sql.points_select import log_decorator, limit_and_offset


@log_decorator
def sql_select_work_to_equipment_id(id_equip: str) -> str:
    """Returns the query string to select all repairs corresponding
    to the equipment with the given number
    Example:
        SELECT * FROM works_likes
        WHERE id IN (SELECT id FROM works WHERE id_obor = 157)
        ORDER BY date
        """
    query = ("""SELECT * FROM %(works_likes)s WHERE %(id)s IN """ +
             """(SELECT * FROM all_works_from_equip({0}))""" +
             """ ORDER BY %(date)s""") % sql_consts_dict

    return query.format(id_equip)


@log_decorator
def sql_select_last_work_to_equipment_id(id_equip: str) -> str:
    """Returns the query string to select max_records_in_page * 2 last repairs corresponding
    to the equipment with the given number
    Example:
        SELECT * FROM(SELECT * FROM works_likes
        WHERE id IN (SELECT id FROM works WHERE id_obor = 30)
        ORDER BY date DESC LIMIT 20) tmp ORDER BY date;
        """

    query = ("""SELECT * FROM(SELECT * FROM %(works_likes)s WHERE %(id)s IN """ +
             """(SELECT * FROM all_works_from_equip({0}))""" +
             """ ORDER BY %(date)s DESC LIMIT {1}) tmp ORDER BY %(date)s""") % sql_consts_dict

    return query.format(id_equip, config.max_records_in_page() * 2)


@log_decorator
def sql_select_work_from_equip_id_limit(id_equip: str, page_num: int) -> str:
    """Return the query string to select limited all repairs corresponding
     to the equips with the given number
    Example:
        SELECT * FROM works_likes WHERE id IN
        (SELECT id FROM works WHERE id_obor = 37)
        ORDER BY date
        LIMIT 5 OFFSET 25
        """
    query = ("""SELECT * FROM %(works_likes)s WHERE %(id)s IN """ +
             """(SELECT * FROM all_works_from_equip({0}))""" +
             """ ORDER BY %(date)s """) % sql_consts_dict + limit_and_offset(page_num)

    return query.format(id_equip)


@log_decorator
def sql_select_all_works() -> str:
    """Returns the query string to select all repairs corresponding to the equipments"""

    return """SELECT * FROM %(works_likes)s ORDER BY %(date)s""" % sql_consts_dict


@log_decorator
def sql_select_all_works_limit(page_num: int) -> str:
    """Returns the query string to select all repairs corresponding to the equipments use LIMIT"""

    query = """SELECT * FROM %(works_likes)s ORDER BY %(date)s""" % sql_consts_dict + limit_and_offset(page_num)
    return query


@log_decorator
def sql_select_work_from_id(id_work: str) -> str:
    """Returns the query string corresponding to the work performed with the specified number
    Example:
        SELECT * FROM works_likes WHERE id = 136
        """

    query = """SELECT * FROM %(works_likes)s WHERE %(id)s = {0}""" % sql_consts_dict

    return query.format(id_work)


@log_decorator
def sql_select_all_works_from_like_str(pattern: str) -> str:
    """Function return string contain sql-query from table works like all records to s-string
    Example:
        SELECT * FROM works_likes
        WHERE (LOWER (problem)
        LIKE LOWER('nOt Working')) OR (LOWER(result) LIKE LOWER('nOt Working'))
        ORDER BY date, name
        """
    if pattern != '*':
        like_string = '%' + pattern.replace(' ', '%') + '%'
        query = ("""SELECT * FROM %(works_likes)s WHERE (LOWER (%(problem)s)""" +
                 """ LIKE LOWER('{0}')) OR (LOWER(%(result)s) LIKE LOWER('{0}'))""" +
                 """ ORDER BY %(date)s, %(name)s""") % sql_consts_dict

        result = query.format(like_string)
    else:
        query = ("""SELECT * FROM %(works_likes)s ORDER BY %(date)s, %(name)s""") \
                % sql_consts_dict
        result = query
    return result


@log_decorator
def sql_select_all_works_from_like_str_limit(pattern: str, page_num: str) -> str:
    """Function return string contain sql-query from table works like all records
     to pattern-string
    Example:
        SELECT * FROM works_likes
        WHERE (LOWER (problem)
        LIKE LOWER('не Гор')) OR (LOWER(result) LIKE LOWER('не Гор'))
        ORDER BY date, name LIMIT 13 OFFSET 39
        """

    if pattern != '*':
        like_string = '%' + pattern.replace(' ', '%') + '%'
        query = ("""SELECT * FROM %(works_likes)s WHERE (LOWER (%(problem)s)""" +
                 """ LIKE LOWER('{0}')) OR (LOWER(%(result)s) LIKE LOWER('{0}'))""" +
                 """ ORDER BY %(date)s, %(name)s """) % sql_consts_dict + limit_and_offset(page_num)

        result = query.format(like_string)
    else:
        query = ("""SELECT * FROM %(works_likes)s ORDER BY""" +
                 """ %(date)s, %(name)s """) % sql_consts_dict + limit_and_offset(page_num)
        result = query
    return result


@log_decorator
def sql_select_all_works_from_like_str_and_date(pattern: str, date_start: str,
                                                date_stop: str) -> str:
    """Function return SQL-string contain query from table works
    like all records to pattern-string and in dates range
    Example:
        SELECT * FROM works_likes
        WHERE ((LOWER (problem) LIKE LOWER('not WORking')) OR (LOWER(result)
        LIKE LOWER('not Working'))) AND (date BETWEEN '21-12-2020' AND '31-12-2020')
        ORDER BY  date, name
        """

    if pattern != '*':
        like_string = '%' + pattern.replace(' ', '%') + '%'
        query = ("""SELECT * FROM %(works_likes)s WHERE ((LOWER (%(problem)s)""" +
                 """ LIKE LOWER('{0}')) OR (LOWER(%(result)s) LIKE LOWER('{0}')))""" +
                 """ AND (date BETWEEN '{1}' AND '{2}') ORDER BY  %(date)s, %(name)s""") %\
                sql_consts_dict

        result = query.format(like_string, date_start, date_stop)
    else:
        query = ("""SELECT * FROM %(works_likes)s WHERE (date BETWEEN '{0}' AND '{1}')""" +
                 """ ORDER BY  %(date)s, %(name)s""") % sql_consts_dict
        result = query.format(date_start, date_stop)
    return result


@log_decorator
def sql_select_all_works_from_like_str_and_date_limit(pattern: str, date_start: str,
                                                      date_stop: str, page_num: str) -> str:
    """Function return SQL-string contain query from table works
     like all records to s-string and in dates range
    Example:
        SELECT * FROM works_likes
        WHERE ((LOWER (problem)
        LIKE LOWER('not WorK')) OR (LOWER(result) LIKE LOWER('not WorK')))
        AND (date BETWEEN '21-12-2020' AND '21-12-2019')
        ORDER BY  date, name LIMIT 15 OFFSET 45
        """

    if pattern != '*':
        like_string = '%' + pattern.replace(' ', '%') + '%'
        query = ("""SELECT * FROM works_likes WHERE ((LOWER (problem)""" +
                 """ LIKE LOWER('{0}')) OR (LOWER(result) LIKE LOWER('{0}')))""" +
                 """ AND (date BETWEEN '{1}' AND '{2}') ORDER BY """ +
                 """ date, name """) % sql_consts_dict + limit_and_offset(page_num)

        result = query.format(like_string, date_start, date_stop)

    else:
        query = ("""SELECT * FROM works_likes WHERE date BETWEEN '{0}' AND '{1}' """ +
                 """ORDER BY  date, name """) % sql_consts_dict + limit_and_offset(page_num)
        result = query.format(date_start, date_stop)
    return result


@log_decorator
def sql_select_max_work_id() -> str:
    """Return the query string select maximal number in column id in table works"""

    return """SELECT COUNT(*) FROM %(works)s""" % sql_consts_dict


@log_decorator
def sql_select_next_work_id() -> str:
    """Return the query string select maximal number in column id in table works"""

    return """SELECT MAX(%(id)s) + 1 FROM %(works)s;""" % sql_consts_dict


@log_decorator
def sql_select_count_uniques_works() -> str:
    """Return SQL-string contain query to count unique id in works table"""

    return """SELECT  COUNT(%(id)s) FROM %(works)s""" % sql_consts_dict


@log_decorator
def sql_select_works_from_worker(id_worker: str) -> str:
    """Return SQL-query contain all works from current performer
    Example:
        SELECT works_from_worker.id, point_name, name, model, serial_num, date, problem,
        result, all_workers
        FROM works_from_worker
        JOIN performers
        ON performers.worker_id = {0} AND works_from_worker.id = performers.work_id
        ORDER BY date
        """

    query = ("""SELECT DISTINCT %(works_from_worker)s.%(id)s, %(point_name)s, %(name)s,""" +
             """ %(model)s, %(serial_num)s, %(date)s, %(problem)s, %(result)s,""" +
             """ %(all_workers)s FROM %(works_from_worker)s JOIN %(performers)s """ +
             """ON %(performers)s.%(worker_id)s = {0} AND %(works_from_worker)s.%(id)s""" +
             """ = %(performers)s.%(work_id)s ORDER BY %(date)s""") % sql_consts_dict

    return query.format(id_worker)


@log_decorator
def sql_select_works_from_worker_limit(id_worker: str, page_num: int) -> str:
    """See also sql_select_works_from_worker. Only use limit records in page"""

    query = ("""SELECT DISTINCT %(works_from_worker)s.%(id)s, %(point_name)s, %(name)s,""" +
             """ %(model)s, %(serial_num)s, %(date)s, %(problem)s, %(result)s,""" +
             """ %(all_workers)s FROM %(works_from_worker)s JOIN %(performers)s """ +
             """ON %(performers)s.%(worker_id)s = {0} AND %(works_from_worker)s.%(id)s""" +
             """ = %(performers)s.%(work_id)s ORDER BY %(date)s """) % sql_consts_dict + limit_and_offset(page_num)

    return query.format(id_worker)


@log_decorator
def sql_select_works_from_performer_and_date(id_worker: str, date_start: str, date_stop: str, page_num: int) -> str:
    """See also sql_select_works_from_worker_limit. Only use date interval. If page_num == 0 then not use limits"""
    query = ("""SELECT DISTINCT %(works_from_worker)s.%(id)s, %(point_name)s, %(name)s, """ +
             """%(model)s, %(serial_num)s, %(date)s, %(problem)s, %(result)s, %(all_workers)s """ +
             """FROM %(works_from_worker)s JOIN %(performers)s """ +
             """ON %(performers)s.%(worker_id)s = {0} AND %(works_from_worker)s.%(id)s = %(performers)s.%(work_id)s """ +
             """WHERE %(date)s >= '{1}' and %(date)s <= '{2}' """ +
             """ORDER BY %(date)s """) % sql_consts_dict
    query = query + limit_and_offset(page_num) if page_num != 0 else query
    return query.format(id_worker, date_start, date_stop)