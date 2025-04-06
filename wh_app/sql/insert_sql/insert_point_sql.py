from wh_app.sql.sql_constant import sql_consts_dict, tech_tables
from wh_app.sql.select_sql.select_sql import log_decorator


@log_decorator
def sql_insert_new_point(point_id: str, name: str, address: str, main_point_id: int) -> str:
    """Returns the query string to add a new point"""
    if main_point_id == 0 or main_point_id == '0':
        query = ("""INSERT INTO %(workspoints)s (%(point_id)s, %(point_name)s, %(point_address)s) """ +
                 """VALUES ('{0}', '{1}', '{2}')""") % sql_consts_dict

        return query.format(point_id,
                            name,
                            address)
    else:
        query = ("""INSERT INTO %(workspoints)s (%(point_id)s, %(point_name)s, %(point_address)s, %(main_point_id)s) """ +
                 """VALUES ('{0}', '{1}', '{2}', {3})""") % sql_consts_dict

        return query.format(point_id, name, address, main_point_id)


@log_decorator
def sql_insert_tech_section(point_id: str, section: str, dogovor: str, resume: str) -> str:
    """Return SQL-string contain query to insert new record in technical database"""

    query = """INSERT INTO {0} (%(point_id)s, %(treaty)s, %(resume)s) VALUES ({1}, '{2}', '{3}')""" % sql_consts_dict
    return query.format(tech_tables[section], point_id, dogovor, resume)


@log_decorator
def sql_add_new_reading_to_meter_device(device_id: int, reading_date: str, value: int) -> str:
    """Return INSERT-string to Add new record in devices history"""

    query = """INSERT INTO %(meter_readings)s (%(devices_id)s, %(read_date)s, %(reading)s) 
    VALUES ({0}, '{1}'::DATE, {2})""" % sql_consts_dict
    return query.format(device_id, reading_date, value)