from wh_app.config_and_backup import config
from wh_app.sql.sql_constant import *

functions.info_string(__name__)


def sql_select_point(id_point: str) -> str:
    """Returns the string of the query for selecting a point by a unique number"""

    query = """SELECT {1}, {3}, point_address, 
    CASE WHEN is_work = true THEN 'Работает' ELSE 'Закрыто' END 
    FROM {0} {2} ORDER BY {3}"""

    formatter = ("WHERE point_id = " + str(id_point)) if (str(id_point) != '' and str(id_point) != '0') else ""
    return query.format(workspoints_const, point_id_const, formatter, point_name_const)


def sql_select_all_works_points() -> str:
    """Return the string of the query for selected a point where status is 'work'"""
    return """SELECT {1}, {2}, point_address, 
    CASE WHEN is_work = true THEN 'Работает' ELSE 'Закрыто' END 
    FROM {0} WHERE is_work = true ORDER BY {2}""".format(workspoints_const, point_id_const, point_name_const)


def sql_select_equipment_in_point(point: str) -> str:
    """Returns the query string for selecting all equipment items at a given point"""

    query = """SELECT oborudovanie.id, {0}.{3}, oborudovanie.name, oborudovanie.model,
    oborudovanie.serial_num, oborudovanie.pre_id FROM oborudovanie JOIN {0} ON {0}.{1} = 
    oborudovanie.{1} {2} ORDER BY oborudovanie.name"""

    formatter = ("WHERE oborudovanie.point_id = " + str(point)) if (str(point) != '' and str(point) != '0') else ''
    return query.format(workspoints_const, point_id_const, formatter, point_name_const)


sql_select_all_equipment = sql_select_equipment_in_point('')


def sql_select_equipment_in_point_limit(point: str, page_num: int) -> str:
    """Returns the query string for selecting all equipment items at a given point use LIMIT"""

    query = """SELECT oborudovanie.id, {0}.{1}, oborudovanie.name, oborudovanie.model,
        oborudovanie.serial_num, oborudovanie.pre_id FROM oborudovanie JOIN {0} ON {0}.{3} = 
        oborudovanie.{3} {2} ORDER BY oborudovanie.name"""
    formatter = ("WHERE oborudovanie.point_id = " + str(point)) if (str(point) != '' and str(point) != '0') else ''
    query = query.format(workspoints_const,
                         point_name_const,
                         formatter, point_id_const) + """ LIMIT {0} OFFSET {1}"""
    return query.format(config.max_records_in_page, (int(page_num) - 1) * config.max_records_in_page)


def sql_select_all_equipment_limit(page_num: int) -> str:
    return sql_select_equipment_in_point_limit('', page_num)


def sql_select_work_to_equipment_id(id_equip: str) -> str:
    """Returns the query string to select all repairs corresponding to the equipment with the given number"""

    query = """SELECT * FROM works_likes WHERE id IN (SELECT id FROM works WHERE id_obor = {0}) ORDER BY date"""

    return query.format(id_equip)


def sql_select_work_from_equip_id_limit(id_equip: str, page_num: int) -> str:
    """Return the query string to select limited all repairs corresponding to the equips with the given number"""

    query = """SELECT * FROM works_likes WHERE id IN (SELECT id FROM works WHERE id_obor = {0}) ORDER BY date 
    LIMIT {1} OFFSET {2}"""

    return query.format(id_equip, config.max_records_in_page, (int(page_num) - 1) * config.max_records_in_page)


def sql_select_all_works() -> str:
    """Returns the query string to select all repairs corresponding to the equipments"""
    return """SELECT * FROM works_likes ORDER BY date"""


def sql_select_all_works_limit(page_num: int) -> str:
    """Returns the query string to select all repairs corresponding to the equipments use LIMIT"""

    query = """SELECT * FROM works_likes ORDER BY date LIMIT {0} OFFSET {1}"""
    return query.format(config.max_records_in_page, (int(page_num) - 1) * config.max_records_in_page)


def sql_select_information_to_point(id_point: str) -> str:
    """Returns the string of the request for complete information about the point with the given number"""

    query = """SELECT {3}, point_address FROM {0} WHERE {1}={2}"""
    return query.format(workspoints_const, point_id_const, id_point, point_name_const)


def sql_select_work_from_id(id_work: str) -> str:
    """Returns the query string corresponding to the work performed with the specified number"""

    query = """SELECT * FROM works_likes WHERE id = {0}"""

    return query.format(id_work)


def sql_select_equip_from_like_str(s: str) -> str:
    """Return the query string select equips from like-string"""

    words = '%' + s.replace(' ', '%') + '%'
    query = """SELECT id, {0}.{3}, name, model, serial_num, pre_id FROM oborudovanie 
    JOIN {0} ON oborudovanie.{1} = {0}.{1} WHERE LOWER(name)
     LIKE LOWER('{2}') ORDER BY name"""
    return query.format(workspoints_const, point_id_const, words, point_name_const)


def sql_select_equip_from_like_str_limit(s: str, page_num: str) -> str:
    """Return the query string select equips from like-string use LIMIT and OFFSET"""

    words = '%' + s.replace(' ', '%') + '%'
    query = """SELECT id, {0}.{5}, name, model, serial_num, pre_id FROM oborudovanie 
    JOIN {0} ON oborudovanie.{1} = {0}.{1} WHERE LOWER(name)
     LIKE LOWER('{2}') ORDER BY name LIMIT {3} OFFSET {4}"""
    return query.format(workspoints_const, point_id_const,
                        words, config.max_records_in_page, (int(page_num) - 1) * config.max_records_in_page,
                        point_name_const)


def sql_select_point_from_like_str(s: str) -> str:
    """Return the query string select points from like-string"""

    like_string = '%' + s.replace(' ', '%') + '%'
    query = """SELECT * FROM {0} WHERE (LOWER({2}) LIKE LOWER('{1}')) OR (LOWER(point_address) LIKE
    LOWER('{1}')) ORDER BY {2}"""

    return query.format(workspoints_const, like_string, point_name_const)


def sql_select_point_from_like_str_limit(s: str, page_num: str) -> str:
    """Return the query string select points from like-string"""

    like_string = '%' + s.replace(' ', '%') + '%'
    query = """SELECT {5}, {4}, point_address, 
    CASE WHEN is_work = true THEN 'Работает' ELSE 'Закрыто' END 
    FROM {0} WHERE (LOWER({4}) LIKE LOWER('{1}')) OR (LOWER(point_address) LIKE
    LOWER('{1}')) ORDER BY {4} LIMIT {2} OFFSET {3}"""

    return query.format(workspoints_const,
                        like_string,
                        config.max_records_in_page,
                        (int(page_num) - 1) * config.max_records_in_page,
                        point_name_const,
                        point_id_const)


def sql_select_all_works_from_like_str(s: str) -> str:
    """Function return string contain sql-query from table works like all records to s-string"""

    like_string = '%' + s.replace(' ', '%') + '%'
    query = """SELECT * FROM works_likes WHERE (LOWER (problem) LIKE LOWER('{0}')) OR 
    (LOWER(result) LIKE LOWER('{0}')) ORDER BY date, name"""

    return query.format(like_string)


def sql_select_all_works_from_like_str_limit(s: str, page_num: str) -> str:
    """Function return string contain sql-query from table works like all records to s-string"""

    like_string = '%' + s.replace(' ', '%') + '%'
    query = """SELECT * FROM works_likes WHERE (LOWER (problem) LIKE LOWER('{0}')) OR 
    (LOWER(result) LIKE LOWER('{0}')) ORDER BY date, name LIMIT {1} OFFSET {2}"""

    return query.format(like_string, config.max_records_in_page, (int(page_num) - 1) * config.max_records_in_page)


def sql_select_all_works_from_like_str_and_date(s: str, date_start: str, date_stop: str) -> str:
    """Function return SQL-string contain query from table works like all records to s-string and in dates range"""

    like_string = '%' + s.replace(' ', '%') + '%'
    query = """SELECT * FROM works_likes WHERE ((LOWER (problem) LIKE LOWER('{0}')) OR (LOWER(result) 
    LIKE LOWER('{0}'))) AND (date BETWEEN '{1}' AND '{2}') ORDER BY  date, name"""

    return query.format(like_string, date_start, date_stop)


def sql_select_all_works_from_like_str_and_date_limit(s: str, date_start: str, date_stop: str, page_num: str) -> str:
    """Function return SQL-string contain query from table works like all records to s-string and in dates range"""

    like_string = '%' + s.replace(' ', '%') + '%'
    query = """SELECT * FROM works_likes WHERE ((LOWER (problem) LIKE LOWER('{0}')) OR (LOWER(result) 
    LIKE LOWER('{0}'))) AND (date BETWEEN '{1}' AND '{2}') ORDER BY  date, name LIMIT {3} OFFSET {4}"""

    return query.format(like_string, date_start,
                        date_stop,
                        config.max_records_in_page,
                        (int(page_num) - 1) * config.max_records_in_page)


def sql_select_max_id_equip() -> str:
    """Return the query string select maximal number in col ID in table oborudovanie"""

    return """SELECT MAX(id) FROM oborudovanie"""


def sql_select_max_id_point() -> str:
    """Return the query string select maximal number in column point_id in table workspoints"""

    return """SELECT MAX({1}) FROM {0}""".format(workspoints_const, point_id_const)


def sql_select_max_work_id() -> str:
    """Return the query string select maximal number in column id in table works"""

    return """SELECT MAX(id) FROM works"""


def sql_select_point_id_from_equip_id(equip_id: str) -> str:
    """Return the query string select a point contain this equip"""

    return """SELECT {0} FROM oborudovanie WHERE id = {1}""".format(point_id_const, equip_id)


def sql_select_full_equips_info(equip_id: str) -> str:
    """Return SQL-query contain query to complete information from equip"""

    query = """SELECT {0}.{3} AS {3}, oborudovanie.name AS name, oborudovanie.model AS model,
     oborudovanie.serial_num AS serial_num, oborudovanie.pre_id AS pre_id FROM oborudovanie 
     JOIN {0} ON {0}.{1} = oborudovanie.{1} WHERE oborudovanie.id = {2}"""

    return query.format(workspoints_const, point_id_const, equip_id, point_name_const)


def sql_select_statistic() -> str:
    """Return SQL-string contain query to statistic from database records"""

    return """SELECT * FROM statistic"""


def sql_select_size_database() -> str:
    """Return SQL-string contain query to size database workhistory"""

    return """SELECT pg_size_pretty(pg_database_size(current_database()))"""


def sql_select_count_uniques_dates() -> str:
    """Return SQL-string contain query to count unique dates in works table"""

    return """SELECT  COUNT(DISTINCT DATE(date)) FROM works"""


def sql_select_count_uniques_works() -> str:
    """Return SQL-string contain query to count unique id in works table"""

    return """SELECT  COUNT(id) FROM works"""


def sql_select_all_workers() -> str:
    """Return SQL-query return table with all workers"""

    return """SELECT * FROM all_workers"""


def sql_select_table_current_workers() -> str:
    """Return SQL-query contain table workers"""

    return """SELECT * FROM workers WHERE is_work = true"""


def sql_select_works_from_worker(id_worker: str) -> str:
    """Return SQL-query contain all works from current performer"""

    query = """SELECT works_from_worker.id, {1}, name, model, serial_num, date, problem,
     result, all_workers FROM works_from_worker JOIN performers ON performers.worker_id = {0} 
     AND works_from_worker.id = performers.work_id ORDER BY date"""

    return query.format(id_worker, point_name_const)


def sql_select_works_days() -> str:
    """Return SQL-query contain points, workers and days of week"""

    return """SELECT * FROM firsts_bindings"""


def sql_select_alter_works_days() -> str:
    """Return SQL-query contain alternative bindings point <--> workers"""

    return """SELECT * FROM seconds_bindings ORDER BY point"""
