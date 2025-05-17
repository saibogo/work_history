from wh_app.sql.sql_constant import sql_consts_dict
from wh_app.sql.select_sql.select_sql import log_decorator


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
def sql_insert_new_equips_class(meta_class: str, new_class: str, new_dir: str, description: str) -> str:
    """Return INSERT string to add new equips subclass"""

    query = """INSERT INTO %(equip_sub_types)s (%(super_type)s, %(equip_type)s, %(type_folder)s, %(comment)s) 
    VALUES ('{}', '{}', '{}', '{}')""" % sql_consts_dict
    return query.format(meta_class, new_class, new_dir, description)


@log_decorator
def sql_insert_new_equip_detail(equip_type: int, filename: str, description: str) -> str:
    """Return INSERT string to add new equip`s detail in database"""

    query = """INSERT INTO %(equip_details)s (%(full_type)s, %(equip_name_detail)s, %(description)s) 
    VALUES ({0}, '{1}', '{2}')""" % sql_consts_dict
    return query.format(equip_type, filename, description)


@log_decorator
def sql_insert_new_equip_manual(equip_type: int, filename: str, description: str) -> str:
    """Return INSERT string to add new equip`s detail in database"""

    query = """INSERT INTO %(equip_manuals)s (%(full_type)s, %(equip_name_detail)s, %(description)s) 
    VALUES ({0}, '{1}', '{2}')""" % sql_consts_dict
    return query.format(equip_type, filename, description)