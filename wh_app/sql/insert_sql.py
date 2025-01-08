"""This module create RAW query to insert in database operations"""

from wh_app.supporting import functions
from wh_app.sql.sql_constant import sql_consts_dict, tech_tables
from wh_app.sql.select_sql.select_sql import log_decorator

functions.info_string(__name__)


@log_decorator
def sql_insert_new_point(point_id: str, name: str, address: str) -> str:
    """Returns the query string to add a new point"""
    query = ("""INSERT INTO %(workspoints)s (%(point_id)s, %(point_name)s, %(point_address)s) """ +
             """VALUES ('{0}', '{1}', '{2}')""") % sql_consts_dict

    return query.format(point_id,
                        name,
                        address)


@log_decorator
def sql_insert_new_equip(equip_id: str, point: str, name: str,
                         model: str, serial: str, pre_id: str) -> str:
    """Returns the query string to add a new piece of equipment"""
    if pre_id == "NULL":
        query = ("""INSERT INTO %(oborudovanie)s (%(id)s, %(point_id)s, %(name)s, """ +\
                """ %(model)s, %(serial_num)s) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}')""") %\
                sql_consts_dict
        result = query.format(equip_id, point, name, model, serial)
    else:
        query = ("""INSERT INTO %(oborudovanie)s (%(id)s, %(point_id)s,""" +\
                """ %(name)s, %(model)s, %(serial_num)s, %(pre_id)s)""" +\
                """ VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')""") % sql_consts_dict
        result = query.format(equip_id, point, name, model, serial, pre_id)
    return result


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


@log_decorator
def sql_add_new_performers(work_id: str, worker_id: str) -> str:
    """Return SQL-string contain query to insert new performer in performers table"""
    query = ("""INSERT INTO %(performers)s (%(work_id)s,""" +\
            """ %(worker_id)s) VALUES ('{0}', '{1}')""") % sql_consts_dict
    return query.format(work_id,
                        worker_id)


@log_decorator
def sql_add_new_bug(problem: str) -> str:
    """Return SQL-string contain query to insert new record in bugzilla"""
    query = ("""INSERT INTO %(bugzilla)s (%(problem)s,""" +\
            """ %(status)s) VALUES ('{0}', true)""") % sql_consts_dict
    return query.format(problem)


@log_decorator
def sql_insert_tech_section(point_id: str, section: str, dogovor: str, resume: str) -> str:
    """Return SQL-string contain query to insert new record in technical database"""

    query = """INSERT INTO {0} (%(point_id)s, %(treaty)s, %(resume)s) VALUES ({1}, '{2}', '{3}')""" % sql_consts_dict
    return query.format(tech_tables[section], point_id, dogovor, resume)


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
def sql_add_new_order(customer_id: str, point_id: str, order_info: str) -> str:
    """Return SQL-string contain query to insert new order in orders table"""
    query = """INSERT INTO %(orders)s (%(customer_id)s, %(date)s, %(status)s, %(problem)s, %(point_id)s) 
    VALUES ({0}, NOW(), 'in_work', '{1}', {2})""" % sql_consts_dict
    return query.format(customer_id, order_info, point_id)


@log_decorator
def sql_add_new_day_in_schedule(work_day: str, worker_id: int, day_type: str) -> str:
    """Return SQL-string to insert new schedule-day in schedule database"""
    query = """INSERT INTO %(workers_schedule)s VALUES('{0}', {1}, '{2}')""" % sql_consts_dict
    return query.format(work_day, worker_id, day_type)