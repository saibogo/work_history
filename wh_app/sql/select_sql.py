"""This module create RAW-query to SELECT in database"""

from wh_app.config_and_backup import config
from wh_app.sql.sql_constant import sql_consts_dict
from wh_app.supporting import functions

functions.info_string(__name__)


def sql_counter(sql_query: str) -> str:
    """Return SELECT likes SELECT COUNT..."""

    return """SELECT COUNT (*) FROM ({0}) AS foo""".format(sql_query)


def sql_select_point(id_point: str) -> str:
    """Returns the string of the query for selecting a point by a unique number
    Example:
     SELECT point_id, point_name, point_address, CASE WHEN is_work = true
     THEN 'Open' ELSE 'Closed' END
     FROM workspoints WHERE point_id = 13 ORDER BY point_name"""

    formatter = ("WHERE %(point_id)s = " % sql_consts_dict + str(id_point))\
        if (str(id_point) != '' and str(id_point) != '0') else ""

    query = """SELECT %(point_id)s, %(point_name)s, %(point_address)s,
     %(cast_open_close)s 
     FROM %(workspoints)s {0} ORDER BY %(point_name)s""" % sql_consts_dict
    return query.format(formatter)


def sql_select_all_works_points() -> str:
    """Return the string of the query for selected a point where status is 'work'
    Example:
    SELECT point_id, point_name, point_address,
    CASE WHEN is_work = true THEN 'Работает' ELSE 'Закрыто' END
    FROM workspoints WHERE is_work = true ORDER BY point_name"""

    return ("""SELECT %(point_id)s, %(point_name)s, %(point_address)s, """ +
            """%(cast_open_close)s FROM %(workspoints)s""" +
            """ WHERE %(point_working)s ORDER BY %(point_name)s""") % sql_consts_dict


def sql_select_equipment_in_point(point: str) -> str:
    """Returns the query string for selecting all equipment items at a given point
    Example:
        SELECT oborudovanie.id, workspoints.point_name, oborudovanie.name,
         oborudovanie.model, oborudovanie.serial_num, oborudovanie.pre_id
         FROM oborudovanie
         JOIN workspoints ON workspoints.point_id = oborudovanie.point_id
         WHERE oborudovanie.point_id = 11 ORDER BY oborudovanie.name"""

    formatter = ("WHERE %(oborudovanie)s.%(point_id)s = " % sql_consts_dict + str(point))\
        if (str(point) != '' and str(point) != '0') else ''

    query = ("""SELECT %(oborudovanie)s.%(id)s, %(workspoints)s.%(point_name)s,""" +
             """ %(oborudovanie)s.%(name)s, %(oborudovanie)s.%(model)s,""" +
             """ %(oborudovanie)s.%(serial_num)s, %(oborudovanie)s.%(pre_id)s""" +
             """ FROM %(oborudovanie)s JOIN %(workspoints)s ON """ +
             """%(workspoints)s.%(point_id)s = %(oborudovanie)s.%(point_id)s {0}""" +
             """ ORDER BY %(oborudovanie)s.%(name)s""") % sql_consts_dict

    return query.format(formatter)


sql_select_all_equipment = sql_select_equipment_in_point('')


def sql_select_equipment_in_point_limit(point: str, page_num: int) -> str:
    """Returns the query string for selecting all equipment items at a given point use LIMIT
    Example:
        SELECT oborudovanie.id, workspoints.point_name, oborudovanie.name, oborudovanie.model,
        oborudovanie.serial_num, oborudovanie.pre_id FROM oborudovanie
        JOIN workspoints ON workspoints.point_id =oborudovanie.point_id
        WHERE oborudovanie.point_id = 7 ORDER BY oborudovanie.name LIMIT 5 OFFSET 15
        """

    formatter = ("WHERE %(oborudovanie)s.%(point_id)s = " % sql_consts_dict + str(point))\
        if (str(point) != '' and str(point) != '0') else ''
    query = ("""SELECT %(oborudovanie)s.%(id)s, %(workspoints)s.%(point_name)s,""" +
             """ %(oborudovanie)s.%(name)s, %(oborudovanie)s.%(model)s,""" +
             """ %(oborudovanie)s.%(serial_num)s, %(oborudovanie)s.%(pre_id)s """ +
             """FROM %(oborudovanie)s JOIN %(workspoints)s """ +
             """ON %(workspoints)s.%(point_id)s = %(oborudovanie)s.%(point_id)s """ +
             """{0} ORDER BY %(oborudovanie)s.%(name)s""") % sql_consts_dict

    query = query.format(formatter) + """ LIMIT {0} OFFSET {1}"""
    return query.format(config.max_records_in_page,
                        (int(page_num) - 1) * config.max_records_in_page)


def sql_select_all_equipment_limit(page_num: int) -> str:
    """Create SELECT to ALL equipment use Limit records in page"""
    return sql_select_equipment_in_point_limit('', page_num)


def sql_select_work_to_equipment_id(id_equip: str) -> str:
    """Returns the query string to select all repairs corresponding
    to the equipment with the given number
    Example:
        SELECT * FROM works_likes
        WHERE id IN (SELECT id FROM works WHERE id_obor = 157)
        ORDER BY date
        """

    query = ("""SELECT * FROM %(works_likes)s WHERE %(id)s IN """ +
             """(SELECT %(id)s FROM %(works)s WHERE %(id_obor)s = {0})""" +
             """ ORDER BY %(date)s""") % sql_consts_dict

    return query.format(id_equip)


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
             """(SELECT %(id)s FROM %(works)s WHERE %(id_obor)s = {0})""" +
             """ ORDER BY %(date)s LIMIT {1} OFFSET {2}""") % sql_consts_dict

    return query.format(id_equip,
                        config.max_records_in_page,
                        (int(page_num) - 1) * config.max_records_in_page)


def sql_select_all_works() -> str:
    """Returns the query string to select all repairs corresponding to the equipments"""

    return """SELECT * FROM %(works_likes)s ORDER BY %(date)s""" % sql_consts_dict


def sql_select_all_works_limit(page_num: int) -> str:
    """Returns the query string to select all repairs corresponding to the equipments use LIMIT"""

    query = ("""SELECT * FROM %(works_likes)s ORDER BY %(date)s""" +
             """ LIMIT {0} OFFSET {1}""") % sql_consts_dict
    return query.format(config.max_records_in_page,
                        (int(page_num) - 1) * config.max_records_in_page)


def sql_select_information_to_point(id_point: str) -> str:
    """Returns the string of the request for complete information
    about the point with the given number
    Example:
        SELECT point_name, point_address FROM workspoints WHERE point_id = id_point
        """

    query = ("""SELECT %(point_name)s, %(point_address)s, %(cast_open_close)s  """ +
             """FROM %(workspoints)s WHERE %(point_id)s = {0}""") % sql_consts_dict
    return query.format(id_point)


def sql_select_work_from_id(id_work: str) -> str:
    """Returns the query string corresponding to the work performed with the specified number
    Example:
        SELECT * FROM works_likes WHERE id = 136
        """

    query = """SELECT * FROM %(works_likes)s WHERE %(id)s = {0}""" % sql_consts_dict

    return query.format(id_work)


def sql_select_equip_from_like_str(pattern: str) -> str:
    """Return the query string select equips from like-string
    Example:
        SELECT id, workspoints.point_name, name, model, serial_num, pre_id
        FROM oborudovanie
        JOIN workspoints ON oborudovanie.point_id = workspoints.point_id
        WHERE LOWER(name) LIKE LOWER('HuraKan')
        OR LOWER(model) LIKE LOWER('HR-2000')
        ORDER BY name
        """

    if pattern != '*':
        words = '%' + pattern.replace(' ', '%') + '%'
        query = ("""SELECT %(id)s, %(workspoints)s.%(point_name)s, """ +
                 """%(name)s, %(model)s, %(serial_num)s, %(pre_id)s FROM %(oborudovanie)s""" +
                 """ JOIN %(workspoints)s ON %(oborudovanie)s.%(point_id)s = """ +
                 """ %(workspoints)s.%(point_id)s WHERE LOWER(%(name)s)""" +
                 """ LIKE LOWER('{0}') OR LOWER(%(model)s) LIKE LOWER('{0}')""" +
                 """ OR LOWER(%(serial_num)s) LIKE LOWER('{0}') ORDER BY %(name)s""") % sql_consts_dict
        result = query.format(words)
    else:
        query = ("""SELECT %(id)s, %(workspoints)s.%(point_name)s, """ +
                 """%(name)s, %(model)s, %(serial_num)s, %(pre_id)s FROM """ +
                 """ %(oborudovanie)s  JOIN %(workspoints)s ON """ +
                 """%(oborudovanie)s.%(point_id)s = %(workspoints)s.%(point_id)s """ +
                 """ORDER BY %(name)s""") % sql_consts_dict
        result = query
    return result


def sql_select_equip_from_like_str_limit(pattern: str, page_num: str) -> str:
    """Return the query string select equips from like-string use LIMIT and OFFSET
    Example:
        SELECT id, workspoints.point_name, name, model, serial_num, pre_id
        FROM oborudovanie
        JOIN workspoints
        ON oborudovanie.point_id = workspoints.point_id
        WHERE LOWER(name) LIKE LOWER('RaTiONaL')
        OR LOWER(model) LIKE LOWER('RatioNal')
        ORDER BY name LIMIT 10 OFFSET 30
        """

    if pattern != '*':
        words = '%' + pattern.replace(' ', '%') + '%'
        query = ("""SELECT %(id)s, %(workspoints)s.%(point_name)s, %(name)s,""" +
                 """ %(model)s, %(serial_num)s, %(pre_id)s FROM %(oborudovanie)s """ +
                 """JOIN %(workspoints)s ON %(oborudovanie)s.%(point_id)s =""" +
                 """ %(workspoints)s.%(point_id)s WHERE LOWER(%(name)s)""" +
                 """ LIKE LOWER('{0}') OR LOWER(%(model)s) LIKE LOWER('{0}') """ +
                 """OR LOWER(%(serial_num)s) LIKE LOWER('{0}')  ORDER BY %(name)s """ +
                 """LIMIT {1} OFFSET {2}""") % sql_consts_dict
        result = query.format(words,
                              config.max_records_in_page,
                              (int(page_num) - 1) * config.max_records_in_page)

    else:
        query = ("""SELECT %(id)s, %(workspoints)s.%(point_name)s, %(name)s,""" +
                 """ %(model)s, %(serial_num)s, %(pre_id)s FROM %(oborudovanie)s""" +
                 """ JOIN %(workspoints)s ON %(oborudovanie)s.%(point_id)s = """ +
                 """ %(workspoints)s.%(point_id)s ORDER BY %(name)s""" +
                 """ LIMIT {0} OFFSET {1}""") % sql_consts_dict
        result = query.format(config.max_records_in_page,
                              (int(page_num) - 1) * config.max_records_in_page)
    return result


def sql_select_point_from_like_str(pattern: str) -> str:
    """Return the query string select points from like-string
    Example:
        SELECT * FROM workspoints
        WHERE (LOWER(point_name) LIKE LOWER('PoINT'))
        OR
        (LOWER(point_address) LIKE LOWER('PoINT'))
        ORDER BY point_name
        """

    if pattern != '*':
        like_string = '%' + pattern.replace(' ', '%') + '%'
        query = ("""SELECT * FROM %(workspoints)s WHERE (LOWER(%(point_name)s)""" +
                 """ LIKE LOWER('{0}')) OR (LOWER(%(point_address)s) LIKE""" +
                 """ LOWER('{0}')) ORDER BY %(point_name)s""") % sql_consts_dict

        result = query.format(like_string)
    else:
        query = ("""SELECT * FROM %(workspoints)s  ORDER BY %(point_name)s""") %\
                sql_consts_dict
        result = query
    return result


def sql_select_point_from_like_str_limit(pattern: str, page_num: str) -> str:
    """Return the query string select points from like-string
    Example:
        SELECT point_id, point_name, point_address,
        CASE WHEN is_work = true THEN 'Работает' ELSE 'Закрыто' END
        FROM workspoints WHERE (LOWER({point_name})
        LIKE LOWER('Пб')) OR (LOWER(point_address) LIKE LOWER('Пб'))
        ORDER BY point_name LIMIT 15 OFFSET 45
        """

    if pattern != '*':
        like_string = '%' + pattern.replace(' ', '%') + '%'
        query = ("""SELECT %(point_id)s, %(point_name)s, %(point_address)s,""" +
                 """ %(cast_open_close)s FROM %(workspoints)s WHERE""" +
                 """ (LOWER(%(point_name)s) LIKE LOWER('{0}')) OR """ +
                 """ (LOWER(%(point_address)s) LIKE LOWER('{0}')) ORDER BY """ +
                 """ %(point_name)s LIMIT {1} OFFSET {2}""") % sql_consts_dict

        result = query.format(like_string,
                              config.max_records_in_page,
                              (int(page_num) - 1) * config.max_records_in_page)
    else:
        query = ("""SELECT %(point_id)s, %(point_name)s, %(point_address)s,""" +
                 """ %(cast_open_close)s FROM %(workspoints)s ORDER BY""" +
                 """ %(point_name)s LIMIT {0} OFFSET {1}""") % sql_consts_dict
        result = query.format(config.max_records_in_page,
                              (int(page_num) - 1) * config.max_records_in_page)
    return result


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
                 """ ORDER BY %(date)s, %(name)s LIMIT {1} OFFSET {2}""") % sql_consts_dict

        result = query.format(like_string,
                              config.max_records_in_page,
                              (int(page_num) - 1) * config.max_records_in_page)
    else:
        query = ("""SELECT * FROM %(works_likes)s ORDER BY""" +
                 """ %(date)s, %(name)s LIMIT {0} OFFSET {1}""") % sql_consts_dict
        result = query.format(config.max_records_in_page,
                              (int(page_num) - 1) * config.max_records_in_page)
    return result


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
                 """ date, name LIMIT {3} OFFSET {4}""") % sql_consts_dict

        result = query.format(like_string,
                              date_start,
                              date_stop,
                              config.max_records_in_page,
                              (int(page_num) - 1) * config.max_records_in_page)

    else:
        query = ("""SELECT * FROM works_likes WHERE date BETWEEN '{0}' AND '{1}' """ +
                 """ORDER BY  date, name LIMIT {2} OFFSET {3}""") % sql_consts_dict
        result = query.format(date_start,
                              date_stop,
                              config.max_records_in_page,
                              (int(page_num) - 1) * config.max_records_in_page)
    return result


def sql_select_max_id_equip() -> str:
    """Return the query string select maximal number in column ID in table oborudovanie"""

    return """SELECT MAX(%(id)s) FROM %(oborudovanie)s""" % sql_consts_dict


def sql_select_max_id_point() -> str:
    """Return the query string select maximal number in column point_id in table workspoints"""

    return """SELECT MAX(%(point_id)s) FROM %(workspoints)s""" % sql_consts_dict


def sql_select_max_work_id() -> str:
    """Return the query string select maximal number in column id in table works"""

    return """SELECT MAX(%(id)s) FROM %(works)s""" % sql_consts_dict


def sql_select_point_id_from_equip_id(equip_id: str) -> str:
    """Return the query string select a point contain this equip"""

    return (("""SELECT %(point_id)s FROM %(oborudovanie)s""" +
             """ WHERE %(id)s = {0}""") % sql_consts_dict).format(equip_id)


def sql_select_full_equips_info(equip_id: str) -> str:
    """Return SQL-query contain query to complete information from equip
    Example:
        SELECT workspoints.point_name
        AS point_name, oborudovanie.name AS name, oborudovanie.model AS model,
        oborudovanie.serial_num AS serial_num, oborudovanie.pre_id AS pre_id
        FROM oborudovanie
        JOIN workspoints ON workspoints.point_id = oborudovanie.point_id
        WHERE oborudovanie.id = 256
        """

    query = ("""SELECT %(workspoints)s.%(point_name)s AS %(point_name)s,""" +
             """ %(oborudovanie)s.%(name)s AS %(name)s, %(oborudovanie)s.%(model)s """ +
             """ AS %(model)s, %(oborudovanie)s.%(serial_num)s AS %(serial_num)s,""" +
             """ %(oborudovanie)s.%(pre_id)s AS %(pre_id)s FROM %(oborudovanie)s """ +
             """JOIN %(workspoints)s ON %(workspoints)s.%(point_id)s =""" +
             """ %(oborudovanie)s.%(point_id)s WHERE""" +
             """ %(oborudovanie)s.%(id)s = {0}""") % sql_consts_dict

    return query.format(equip_id)


def sql_select_statistic() -> str:
    """Return SQL-string contain query to statistic from database records"""

    return """SELECT * FROM %(statistic)s""" % sql_consts_dict


def sql_select_size_database() -> str:
    """Return SQL-string contain query to size database workhistory"""

    return """SELECT pg_size_pretty(pg_database_size(current_database()))"""


def sql_select_count_uniques_dates() -> str:
    """Return SQL-string contain query to count unique dates in works table"""

    return """SELECT  COUNT(DISTINCT DATE(%(date)s)) FROM %(works)s""" % sql_consts_dict


def sql_select_count_uniques_works() -> str:
    """Return SQL-string contain query to count unique id in works table"""

    return """SELECT  COUNT(%(id)s) FROM %(works)s""" % sql_consts_dict


def sql_select_all_workers() -> str:
    """Return SQL-query return table with all workers"""

    return """SELECT * FROM %(all_workers)s""" % sql_consts_dict


def sql_select_all_workers_real() -> str:
    """Also sql_select_all_workers() where is_work == TRUE"""

    return """SELECT * FROM %(all_workers)s WHERE %(all_workers)s.%(case)s = 'Работает'""" % sql_consts_dict


def sql_select_worker_info(worker_id: str) -> str:
    """Return full info from worker where ID = worker_id"""

    query = """SELECT * FROM %(all_workers)s WHERE ID = {0}""" % sql_consts_dict
    return query.format(worker_id)


def sql_select_table_current_workers() -> str:
    """Return SQL-query contain table workers"""

    return """SELECT * FROM %(workers)s WHERE %(point_working)s""" % sql_consts_dict


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

    query = ("""SELECT %(works_from_worker)s.%(id)s, %(point_name)s, %(name)s,""" +
             """ %(model)s, %(serial_num)s, %(date)s, %(problem)s, %(result)s,""" +
             """ %(all_workers)s FROM %(works_from_worker)s JOIN %(performers)s """ +
             """ON %(performers)s.%(worker_id)s = {0} AND %(works_from_worker)s.%(id)s""" +
             """ = %(performers)s.%(work_id)s ORDER BY %(date)s""") % sql_consts_dict

    return query.format(id_worker)


def sql_select_works_from_worker_limit(id_worker: str, page_num: int) -> str:
    """See also sql_select_works_from_worker. Only use limit records in page"""

    query = ("""SELECT %(works_from_worker)s.%(id)s, %(point_name)s, %(name)s,""" +
             """ %(model)s, %(serial_num)s, %(date)s, %(problem)s, %(result)s,""" +
             """ %(all_workers)s FROM %(works_from_worker)s JOIN %(performers)s """ +
             """ON %(performers)s.%(worker_id)s = {0} AND %(works_from_worker)s.%(id)s""" +
             """ = %(performers)s.%(work_id)s ORDER BY %(date)s LIMIT {1} OFFSET {2}""") % sql_consts_dict

    return query.format(id_worker,
                        config.max_records_in_page,
                        (int(page_num) - 1) * config.max_records_in_page)


def sql_select_works_days() -> str:
    """Return SQL-query contain points, workers and days of week"""

    return """SELECT * FROM %(firsts_bindings)s""" % sql_consts_dict


def sql_select_alter_works_days() -> str:
    """Return SQL-query contain alternative bindings point <--> workers"""

    return """SELECT * FROM %(seconds_bindings)s ORDER BY %(point)s""" % sql_consts_dict


def sql_select_all_bugs_in_bugzilla() -> str:
    """Return all records in bugzilla table"""

    query = ("""SELECT %(id)s, %(problem)s, %(bug_in_work)s""" +
             """ FROM %(bugzilla)s ORDER BY %(id)s""") % sql_consts_dict
    return query


def sql_select_all_bugs_in_bugzilla_limit(page_num: str) -> str:
    """Return all records in bugzilla table use paging"""

    query = ("""SELECT %(id)s, %(problem)s, %(bug_in_work)s FROM %(bugzilla)s """ +
             """ ORDER BY %(id)s LIMIT {0} OFFSET {1}""") % sql_consts_dict
    return query.format(config.max_records_in_page,
                        (int(page_num) - 1) * config.max_records_in_page)


def sql_select_all_bugs_in_work_in_bugzilla() -> str:
    """Return all records in bugzilla table if status = in work"""

    query = ("""SELECT %(id)s, %(problem)s, %(bug_in_work)s FROM %(bugzilla)s""" +
             """ WHERE %(status)s = true ORDER BY %(id)s""") % sql_consts_dict
    return query


def sql_select_all_customers() -> str:
    """Return all records in table customer"""

    return """SELECT id, full_name FROM %(customer_table)s ORDER BY %(id)s""" % sql_consts_dict


def sql_select_all_orders() -> str:
    """Return all records in table orders"""

    query = ("""SELECT orders.%(id)s, customer.full_name, orders.date, problem, """ +
             """(%(bug_in_work)s) FROM orders JOIN customer ON customer_id = customer.%(id)s""" +
             """ ORDER BY %(id)s""") % sql_consts_dict

    return query


def sql_select_all_point_except_id(point_id: str) -> str:
    """Return all point except point_id == id"""

    query = ("""SELECT %(point_id)s, %(point_name)s FROM %(workspoints)s""" +
             """ WHERE %(point_id)s != {0} and %(is_work)s = true;""") % sql_consts_dict

    return query.format(point_id)


def sql_select_name_from_point_id(point_id: str) -> str:
    """Return point_name from point_id == id"""

    query = ("""SELECT %(point_name)s FROM %(workspoints)s""" +
             """ WHERE %(point_id)s = {0};""") % sql_consts_dict

    return query.format(str(point_id))


def sql_select_all_posts() -> str:
    """Return SELECT-query to ALL POST in database"""

    query = ("""SELECT * FROM %(posts)s""") % sql_consts_dict
    return query


def sql_select_all_weekly_chart() -> str:
    """Return SELECT-query to ALL WORKS DAYS From ALL Workers"""

    query = ("""SELECT %(workers)s.%(sub_name)s, day1, day2, day3, day4, day5, day6, day7 """ +
             """FROM %(works_days)s JOIN %(workers)s """ +
             """ON %(works_days)s.%(worker_id)s = %(workers)s.%(id)s AND %(workers)s.%(is_work)s = True """ +
             """ORDER BY %(workers)s.%(sub_name)s;""") % sql_consts_dict

    return query


def sql_select_electric_info(point_id: str) -> str:
    """Return SELECT-string for get electric information to point"""

    query = ("""SELECT * FROM %(electric)s WHERE point_id={0}""") % sql_consts_dict
    return query.format(point_id)


def sql_select_cold_water_info(point_id: str) -> str:
    """Return SELECT-string for get cold_water information to point"""

    query = ("""SELECT * FROM %(cold_water)s WHERE point_id={0}""") % sql_consts_dict
    return query.format(point_id)


def sql_select_hot_water_info(point_id: str) -> str:
    """Return SELECT-string for get hot_water information to point"""

    query = ("""SELECT * FROM %(hot_water)s WHERE point_id={0}""") % sql_consts_dict
    return query.format(point_id)


def sql_select_heating_info(point_id: str) -> str:
    """Return SELECT-string for get heating information to point"""

    query = ("""SELECT * FROM %(heating)s WHERE point_id={0}""") % sql_consts_dict
    return query.format(point_id)


def sql_select_sewerage_info(point_id: str) -> str:
    """Return SELECT-string for get sewerage information to point"""

    query = ("""SELECT * FROM %(sewerage)s WHERE point_id={0}""") % sql_consts_dict
    return query.format(point_id)
