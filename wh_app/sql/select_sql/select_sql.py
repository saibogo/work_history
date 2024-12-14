"""This module create RAW-query to SELECT in database"""

from wh_app.sql.select_sql.points_select import *
from wh_app.sql.select_sql.equipments_select import *


@log_decorator
def sql_counter(sql_query: str) -> str:
    """Return SELECT likes SELECT COUNT..."""

    return """SELECT COUNT (*) FROM ({0}) AS foo""".format(sql_query)






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
def sql_select_statistic() -> str:
    """Return SQL-string contain query to statistic from database records"""

    return """SELECT * FROM %(statistic)s""" % sql_consts_dict


@log_decorator
def sql_select_size_database() -> str:
    """Return SQL-string contain query to size database workhistory"""

    return """SELECT pg_size_pretty(pg_database_size(current_database()))"""


@log_decorator
def sql_select_count_uniques_dates() -> str:
    """Return SQL-string contain query to count unique dates in works table"""

    return """SELECT  COUNT(DISTINCT DATE(%(date)s)) FROM %(works)s""" % sql_consts_dict


@log_decorator
def sql_select_count_uniques_works() -> str:
    """Return SQL-string contain query to count unique id in works table"""

    return """SELECT  COUNT(%(id)s) FROM %(works)s""" % sql_consts_dict


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


@log_decorator
def sql_select_works_days() -> str:
    """Return SQL-query contain points, workers and days of week"""

    return """SELECT * FROM %(firsts_bindings)s""" % sql_consts_dict


@log_decorator
def sql_select_alter_works_days() -> str:
    """Return SQL-query contain alternative bindings point <--> workers"""

    return """SELECT * FROM %(seconds_bindings)s ORDER BY %(point)s""" % sql_consts_dict


@log_decorator
def sql_select_all_bindings_to_point(point_id: str):
    """Return SQL to all workers bindings in current point"""
    query = """SELECT %(bindings)s.%(id)s, %(sub_name)s, %(is_main)s FROM %(bindings)s 
    JOIN %(workers)s ON %(bindings)s.%(worker_id)s = %(workers)s.%(id)s WHERE %(point_id)s = {0}""" % sql_consts_dict
    return query.format(point_id)


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
def sql_select_all_customers() -> str:
    """Return all records in table customer"""

    return """SELECT id, full_name FROM %(customer_table)s ORDER BY %(id)s""" % sql_consts_dict


@log_decorator
def sql_select_customer_info(customer_id: str) -> str:
    """Return full information from customer_id"""

    return ("""SELECT * FROM %(customer_table)s WHERE %(id)s = {0}""" % sql_consts_dict).format(customer_id)


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
def sql_select_get_bug_by_id(bug_id: str) -> str:
    """Return query string likes SELECT * FROM bugzilla WHERE id = 123"""

    query = ("""SELECT %(id)s, %(problem)s, %(bug_in_work)s, %(date_start)s, %(date_close)s
     FROM %(bugzilla)s WHERE %(id)s = {0}""") % sql_consts_dict
    return query.format(bug_id)


@log_decorator
def sql_select_all_point_except_id(point_id: str) -> str:
    """Return all point except point_id == id"""

    query = ("""SELECT %(point_id)s, %(point_name)s FROM %(workspoints)s""" +
             """ WHERE %(point_id)s != {0} and %(point_working)s;""") % sql_consts_dict

    return query.format(point_id)


@log_decorator
def sql_select_all_posts() -> str:
    """Return SELECT-query to ALL POST in database"""

    query = ("""SELECT * FROM %(posts)s""") % sql_consts_dict
    return query


@log_decorator
def sql_select_all_weekly_chart() -> str:
    """Return SELECT-query to ALL WORKS DAYS From ALL Workers"""

    query = ("""SELECT %(workers)s.%(sub_name)s, day1, day2, day3, day4, day5, day6, day7 """ +
             """FROM %(works_days)s JOIN %(workers)s """ +
             """ON %(works_days)s.%(worker_id)s = %(workers)s.%(id)s AND %(workers)s.%(status)s != 'fired' """ +
             """ORDER BY %(workers)s.%(sub_name)s;""") % sql_consts_dict

    return query


@log_decorator
def sql_select_electric_info(point_id: str) -> str:
    """Return SELECT-string for get electric information to point"""

    query = ("""SELECT * FROM %(electric)s WHERE point_id={0}""") % sql_consts_dict
    return query.format(point_id)


@log_decorator
def sql_select_cold_water_info(point_id: str) -> str:
    """Return SELECT-string for get cold_water information to point"""

    query = ("""SELECT * FROM %(cold_water)s WHERE point_id={0}""") % sql_consts_dict
    return query.format(point_id)


@log_decorator
def sql_select_hot_water_info(point_id: str) -> str:
    """Return SELECT-string for get hot_water information to point"""

    query = ("""SELECT * FROM %(hot_water)s WHERE point_id={0}""") % sql_consts_dict
    return query.format(point_id)


@log_decorator
def sql_select_heating_info(point_id: str) -> str:
    """Return SELECT-string for get heating information to point"""

    query = ("""SELECT * FROM %(heating)s WHERE point_id={0}""") % sql_consts_dict
    return query.format(point_id)


@log_decorator
def sql_select_sewerage_info(point_id: str) -> str:
    """Return SELECT-string for get sewerage information to point"""

    query = ("""SELECT * FROM %(sewerage)s WHERE point_id={0}""") % sql_consts_dict
    return query.format(point_id)


@log_decorator
def sql_select_database_version() -> str:
    """Return select-string for get current version database"""

    return """SELECT VERSION()"""


@log_decorator
def sql_select_equip_deleted_status(equip_id: str) -> str:
    """Return query like select deleted from oborudovanie where id = 761"""

    query = """SELECT %(deleted)s FROM %(oborudovanie)s WHERE %(id)s = {}""" % sql_consts_dict
    return query.format(equip_id)


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
def sql_select_top_works() -> str:
    """Return query contain SELECT-strintg to 10 first string in equip -> sum works"""

    query = ("""SELECT %(oborudovanie)s.%(id)s, %(workspoints)s.%(point_name)s, %(name)s,  COUNT(%(works)s.%(id)s) AS
     all_works, (SELECT COUNT(%(works)s.%(id)s) FROM %(works)s WHERE %(works)s.%(date)s::DATE >= last_year_date() 
     AND %(works)s.%(id_obor)s = %(oborudovanie)s.%(id)s) AS lastyear, (SELECT COUNT(%(works)s.%(id)s) FROM %(works)s
      WHERE %(works)s.%(date)s::DATE >= last_month_date() AND %(works)s.%(id_obor)s = %(oborudovanie)s.%(id)s) 
      AS lastmonth FROM %(oborudovanie)s JOIN %(works)s ON %(works)s.%(id_obor)s = %(oborudovanie)s.%(id)s JOIN
       %(workspoints)s ON %(workspoints)s.%(point_id)s = %(oborudovanie)s.%(point_id)s GROUP BY 
       %(workspoints)s.%(point_name)s, %(oborudovanie)s.%(id)s ORDER BY all_works DESC LIMIT 10""") % sql_consts_dict

    return query


@log_decorator
def sql_select_top_workers() -> str:
    """Return SQL-string, to  select TOP-10 workers"""

    query = ("""SELECT %(workers)s.%(id)s, %(workers)s.%(name)s, %(workers)s.%(sub_name)s, COUNT(%(work_id)s) AS all_works, """ +
             """ (SELECT COUNT(%(works)s.%(id)s) FROM %(works)s JOIN %(performers)s ON %(performers)s.%(worker_id)s = %(workers)s.%(id)s""" +
             """ AND %(works)s.%(id)s = %(performers)s.%(work_id)s WHERE %(works)s.%(date)s::DATE >= last_year_date()) """ +
             """ AS last_year, (SELECT COUNT(%(works)s.%(id)s) FROM %(works)s JOIN %(performers)s ON """ +
             """ %(performers)s.%(worker_id)s = %(workers)s.%(id)s AND %(works)s.%(id)s = %(performers)s.%(work_id)s WHERE """ +
             """ %(works)s.%(date)s::DATE >= last_month_date()) AS last_month, (SELECT COUNT(%(works)s.%(id)s) """ +
             """FROM %(works)s JOIN %(performers)s ON %(performers)s.%(worker_id)s = %(workers)s.%(id)s AND %(works)s.%(id)s = """ +
             """ %(performers)s.%(work_id)s WHERE %(works)s.%(date)s::DATE >= last_week_date()) AS last_week FROM """ +
             """ %(workers)s JOIN %(performers)s ON %(workers)s.%(id)s = %(performers)s.%(worker_id)s """ +
             """GROUP BY %(workers)s.%(id)s ORDER BY all_works DESC""") %sql_consts_dict

    return query


@log_decorator
def sql_select_user_in_customers(user_name: str) -> str:
    """Return SQL-string to find user in customer table"""

    query = """SELECT '{0}' IN (SELECT %(full_name)s FROM %(customer)s) as all_users""" % sql_consts_dict
    return query.format(user_name)


@log_decorator
def sql_select_hash_from_user(user_name: str) -> str:
    """Return SQL-string to find hash from user = full_name"""

    query = """SELECT %(hash_pass)s FROM %(customer)s WHERE %(full_name)s = '{0}'""" % sql_consts_dict
    return query.format(user_name)


@log_decorator
def sql_select_all_telegram_chats() -> str:
    """Return SQL-string to select all telegramm chats"""

    query = """SELECT ARRAY(SELECT %(chat_id)s FROM %(chats)s)""" % sql_consts_dict
    return query


@log_decorator
def sql_select_telegram_user_is_reader(user_id: int) -> str:
    """Return SQL-string to true/false from current user read access"""

    query = """SELECT {0} IN (SELECT %(chat_id)s FROM %(chats)s WHERE %(acs_read)s = True)""" % sql_consts_dict
    return query.format(user_id)


@log_decorator
def sql_select_telegram_user_is_writer(user_id: int) -> str:
    """Return SQL-string to true/false from current user write access"""

    query = """SELECT {0} IN (SELECT %(chat_id)s FROM %(chats)s WHERE %(acs_write)s = True)""" % sql_consts_dict
    return query.format(user_id)


@log_decorator
def sql_select_worker_id_from_chats(user_id: int) -> str:
    """Return SQL-string to find worker_id with current chat_id"""

    query = """SELECT %(worker_id)s FROM %(chats)s WHERE %(chat_id)s = {0}""" % sql_consts_dict
    return query.format(user_id)