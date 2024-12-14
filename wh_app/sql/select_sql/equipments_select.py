from typing import *
from datetime import datetime

from wh_app.sql.sql_constant import sql_consts_dict
from wh_app.config_and_backup import config

from wh_app.sql.select_sql.points_select import log_decorator, limit_and_offset


@log_decorator
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
             """ AND %(oborudovanie)s.%(deleted)s = false""" +
             """ ORDER BY %(oborudovanie)s.%(name)s""") % sql_consts_dict

    return query.format(formatter)


sql_select_all_equipment = sql_select_equipment_in_point('')


@log_decorator
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
             """ON %(workspoints)s.%(point_id)s = %(oborudovanie)s.%(point_id)s {0}""" +
             """ AND %(oborudovanie)s.%(deleted)s = false""" +
             """ ORDER BY %(oborudovanie)s.%(name)s""") % sql_consts_dict

    return  query.format(formatter) + limit_and_offset(page_num)


@log_decorator
def sql_select_all_equipment_limit(page_num: int) -> str:
    """Create SELECT to ALL equipment use Limit records in page"""
    return sql_select_equipment_in_point_limit('', page_num)


@log_decorator
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


@log_decorator
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
                 """OR LOWER(%(serial_num)s) LIKE LOWER('{0}')  ORDER BY %(name)s """) % sql_consts_dict + limit_and_offset(page_num)
        result = query.format(words)
    else:
        query = ("""SELECT %(id)s, %(workspoints)s.%(point_name)s, %(name)s,""" +
                 """ %(model)s, %(serial_num)s, %(pre_id)s FROM %(oborudovanie)s""" +
                 """ JOIN %(workspoints)s ON %(oborudovanie)s.%(point_id)s = """ +
                 """ %(workspoints)s.%(point_id)s ORDER BY %(name)s""") % sql_consts_dict + limit_and_offset(page_num)
        result = query
    return result


@log_decorator
def sql_select_count_equip() -> str:
    """Return the query string select maximal number in column ID in table oborudovanie"""

    return """SELECT COUNT(*) FROM %(oborudovanie)s JOIN %(workspoints)s 
    ON %(oborudovanie)s.%(point_id)s = %(workspoints)s.%(point_id)s AND %(workspoints)s.%(point_id)s != %(not_find_in_point)s
    WHERE %(deleted)s = False AND (%(point_working)s)""" % sql_consts_dict


@log_decorator
def sql_select_last_equip_id() -> str:
    """return query, contain select to last equip-id"""

    return """SELECT MAX(%(id)s) from %(oborudovanie)s""" %sql_consts_dict


@log_decorator
def sql_select_next_id_equip() -> str:
    """Return the query string select maximal number in column ID in table oborudovanie"""

    return """SELECT MAX(%(id)s) + 1 FROM %(oborudovanie)s""" % sql_consts_dict


@log_decorator
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

