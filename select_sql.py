import functions

functions.info_string(__name__)


def sql_select_point(point_id: str) -> str:
    """Returns the string of the query for selecting a point by a unique number"""

    return "SELECT * FROM workspoints " + ("WHERE point_id=" + str(point_id)
                                                         if point_id != '' and point_id != '0'
                                                         else "") + ' ORDER BY point_name'


def sql_select_equipment_in_point(point: str) -> str:
    """Returns the query string for selecting all equipment items at a given point"""

    return 'SELECT oborudovanie.id, workspoints.point_name, ' + \
           'oborudovanie.name, oborudovanie.model, oborudovanie.serial_num, ' + \
           'oborudovanie.pre_id ' + \
           'FROM oborudovanie JOIN workspoints ' + \
           'ON workspoints.point_id = oborudovanie.point_id ' + \
           ('WHERE oborudovanie.point_id = ' + str(point) + ' ' if str(point) != "" else '') + \
           'ORDER BY oborudovanie.name'


sql_select_all_equipment = sql_select_equipment_in_point('')


def sql_select_work_to_equipment_id(id: str) -> str:
    """Returns the query string to select all repairs corresponding to the equipment with the given number"""

    return 'SELECT works.id, workspoints.point_name, oborudovanie.name, ' + \
           'oborudovanie.model, oborudovanie.serial_num, ' + \
           'works.date, works.problem, works.result, ' + \
           'tmp.all_workers ' + \
           'FROM works ' + \
           'JOIN oborudovanie ON oborudovanie.id = works.id_obor ' + \
           'JOIN workspoints ON oborudovanie.point_id = workspoints.point_id AND oborudovanie.id = ' + str(id) + ' ' + \
           'JOIN (SELECT works.id AS work_id, ' + \
           'string_agg(workers.sub_name, \' \') AS all_workers ' + \
           'FROM works ' + \
           'JOIN oborudovanie ' + \
           'ON works.id_obor = oborudovanie.id AND oborudovanie.id = ' + str(id) + ' ' + \
           'JOIN performers ' + \
           'ON works.id = performers.work_id ' + \
           'JOIN workers ' + \
           'ON workers.id = performers.worker_id ' + \
           'GROUP BY works.id) AS tmp ' + \
           'ON tmp.work_id = works.id ' + \
           'ORDER BY works.date'


def sql_select_all_works() -> str:
    """Returns the query string to select all repairs corresponding to the equipments"""
    return "SELECT works.id, workspoints.point_name, oborudovanie.name, " + \
           "oborudovanie.model, oborudovanie.serial_num, " + \
           "works.date, works.problem, works.result, " + \
           "tmp.all_workers " +\
           "FROM works " + \
           "JOIN oborudovanie ON oborudovanie.id = works.id_obor " + \
           "JOIN workspoints ON oborudovanie.point_id = workspoints.point_id " + \
           "JOIN (SELECT works.id AS work_id, " + \
           "string_agg(workers.sub_name, ' ') AS all_workers " + \
           "FROM works " + \
           "JOIN oborudovanie " + \
           "ON works.id_obor = oborudovanie.id " + \
           "JOIN performers " + \
           "ON works.id = performers.work_id " + \
           "JOIN workers " + \
           "ON workers.id = performers.worker_id " + \
           "GROUP BY works.id) AS tmp " + \
           "ON tmp.work_id = works.id " +\
           "ORDER BY works.date"


def sql_select_information_to_point(id: str) -> str:
    """Returns the string of the request for complete information about the point with the given number"""

    return "SELECT point_name, point_address FROM workspoints WHERE point_id=" + str(id)


def sql_select_work_from_id(id: str) -> str:
    """Returns the query string corresponding to the work performed with the specified number"""

    return "SELECT works.id, workspoints.point_name AS point_name, " + \
           "oborudovanie.name AS name, " + \
           "oborudovanie.model AS model, " + \
           "oborudovanie.serial_num AS serial_num, " + \
           "works.date AS date, " + \
           "works.problem AS problem, " + \
           "works.result AS result, " + \
           "perfs.all_workers " + \
           "FROM works " + \
           "JOIN oborudovanie " + \
           "ON oborudovanie.id = works.id_obor " + \
           "JOIN workspoints " + \
           "ON workspoints.point_id = oborudovanie.point_id " + \
           "JOIN (SELECT string_agg(tmp.sub_name, ' ') AS all_workers " + \
           "FROM " + \
           "(SELECT workers.sub_name " + \
           "FROM workers " + \
           "JOIN performers " + \
           "ON workers.id = performers.worker_id " + \
           "WHERE performers.work_id = " + str(id) + ") AS tmp) AS perfs " + \
           "ON works.id = " + str(id);


def sql_select_equip_from_like_str(s: str) -> str:
    """Return the query string select equips from like-string"""

    words = '%' + s.replace(' ', '%') + '%'
    return 'SELECT id, workspoints.point_name, name, model, serial_num, pre_id ' + \
           'FROM oborudovanie ' +\
           'JOIN workspoints ' + \
           'ON oborudovanie.point_id = workspoints.point_id ' + \
           'WHERE LOWER(name) LIKE LOWER(\'' + words + '\') ORDER BY name'


def sql_select_point_from_like_str(s: str) -> str:
    """Return the query string select points from like-string"""

    like_string = '%' + s.replace(' ', '%') + '%'
    sql_string = 'SELECT * FROM workspoints WHERE (LOWER(point_name) LIKE LOWER(\'' + like_string +\
                 '\')) OR (LOWER(point_address) LIKE LOWER(\'' + like_string + '\')) ' + 'ORDER BY point_name'
    return sql_string


def sql_select_all_works_from_like_str(s: str) -> str:
    """Function return string contain sql-query from table works like all records to s-string"""

    like_string = '%' + s.replace(' ', '%') + '%'
    return 'SELECT works.id, workspoints.point_name, oborudovanie.name, oborudovanie.model, ' + \
           'oborudovanie.serial_num, works.date, works.problem, works.result, tmp.all_workers ' + \
           'FROM works ' + \
           'JOIN oborudovanie ' + \
           'ON oborudovanie.id = works.id_obor ' + \
           'JOIN workspoints ' + \
           'ON workspoints.point_id = oborudovanie.point_id ' + \
           'JOIN (SELECT works.id AS work_id, ' + \
           'string_agg(workers.sub_name, \' \') AS all_workers ' + \
           'FROM works ' + \
           'JOIN oborudovanie ' + \
           'ON works.id_obor = oborudovanie.id ' + \
           'JOIN performers ' + \
           'ON works.id = performers.work_id ' + \
           'JOIN workers ' + \
           'ON workers.id = performers.worker_id ' + \
           'GROUP BY works.id) AS tmp ' + \
           'ON tmp.work_id = works.id ' + \
           'WHERE (LOWER (works.problem) LIKE LOWER(\'' + like_string + '\')) OR ' + \
           '(LOWER(works.result) LIKE LoWER(\'' + like_string + '\')) ' + \
           'ORDER BY oborudovanie.name, works.date '


def sql_select_all_works_from_like_str_and_date(s: str, date_start: str, date_stop: str) -> str:
    """Function return SQL-strin contain query from table works like all records to s-string and in dates range"""

    like_string = '%' + s.replace(' ', '%') + '%'
    return 'SELECT works.id, workspoints.point_name, oborudovanie.name, oborudovanie.model, ' + \
           'oborudovanie.serial_num, works.date, works.problem, works.result, tmp.all_workers ' + \
           'FROM works ' + \
           'JOIN oborudovanie ' + \
           'ON oborudovanie.id = works.id_obor ' + \
           'JOIN workspoints ' + \
           'ON workspoints.point_id = oborudovanie.point_id ' + \
           'JOIN (SELECT works.id AS work_id, ' + \
           'string_agg(workers.sub_name, \' \') AS all_workers ' + \
           'FROM works ' + \
           'JOIN oborudovanie ' + \
           'ON works.id_obor = oborudovanie.id ' + \
           'JOIN performers ' + \
           'ON works.id = performers.work_id ' + \
           'JOIN workers ' + \
           'ON workers.id = performers.worker_id ' + \
           'GROUP BY works.id) AS tmp ' + \
           'ON tmp.work_id = works.id ' + \
           'WHERE ((LOWER (works.problem) LIKE LOWER(\'' + like_string + '\')) OR ' + \
           '(LOWER(works.result) LIKE LoWER(\'' + like_string + '\'))) ' + \
           'AND (works.date ' + \
           'BETWEEN \'' + date_start + '\' AND \'' + date_stop + '\') ' + \
           'ORDER BY  works.date,oborudovanie.name '



def sql_select_max_id_equip() -> str:
    """Return the query string select maximal number in col ID in table oborudovanie"""

    return "SELECT MAX(id) FROM oborudovanie"


def sql_select_max_id_point() -> str:
    """Return the query string select maximal number in column point_id in table workspoints"""

    return "SELECT MAX(point_id) FROM workspoints"


def sql_select_max_work_id() -> str:
    """Return the query string select maximal number in column id in table works"""

    return "SELECT MAX(id) FROM works"


def sql_select_point_id_from_equip_id(equip_id: str) -> str:
    """Return the query string select a point contain this equip"""

    return 'select point_id from oborudovanie where id = ' + str(equip_id)


def sql_select_full_equips_info(equip_id: str) -> str:
    """Return SQL-query contayn query to complete information from equip"""

    return 'SELECT workspoints.point_name AS point_name,' + \
           'oborudovanie.name AS name,' + \
           'oborudovanie.model AS model,' + \
           'oborudovanie.serial_num AS serial_num,' + \
           'oborudovanie.pre_id AS pre_id ' +\
           'FROM oborudovanie ' +\
           'JOIN workspoints ON workspoints.point_id = oborudovanie.point_id ' + \
           'WHERE oborudovanie.id = ' + str(equip_id)


def sql_select_statistic() -> str:
    """Return SQL-string contain querry to statistic from database records"""

    return 'SELECT MAX(workspoints.point_id) AS point_id, workspoints.point_name AS name_point,' +\
           ' COUNT(DISTINCT oborudovanie.id) AS equips_count, ' + \
           'COUNT(works.id) AS works_count, MAX(works.date) AS last_date ' + \
           'FROM workspoints ' + \
           'JOIN oborudovanie ' + \
           'ON oborudovanie.point_id = workspoints.point_id ' + \
           'JOIN works ' + \
           'ON works.id_obor = oborudovanie.id ' + \
           'GROUP BY name_point ' + \
           'ORDER BY name_point'


def sql_select_size_database() -> str:
    """Return SQL-string contain query to size database workhistory"""

    return 'SELECT pg_size_pretty(pg_database_size(current_database()))'


def sql_select_count_uniques_dates() -> str:
    """Return SQL-string contain query to count unique dates in works table"""

    return 'SELECT  COUNT(DISTINCT DATE(date)) FROM works'


def sql_select_count_uniques_works() -> str:
    """Return SQL-string contain query to count unique id in works table"""

    return 'SELECT  COUNT(id) FROM works'


def sql_select_all_workers() -> str:
    """Return SQL-query return table with all workers"""

    return 'SELECT sub_name, name, ' + \
           'CASE ' + \
           'WHEN is_work=true THEN \'Работает\' ' + \
           'ELSE \'Уволен\' ' + \
           'END FROM workers';

def sql_select_table_current_workers() ->str:
    """Return SQL-query contain table workers"""

    return 'SELECT * FROM workers WHERE is_work = true'