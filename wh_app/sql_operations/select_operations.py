import psycopg2

from wh_app.supporting import functions
from wh_app.sql import select_sql

functions.info_string(__name__)


def commit(connection: psycopg2.connect) -> None:
    """Applies changes to the database"""

    connection.commit()


def get_selected(cursor, sql: str) -> list:
    """Returns a list of database objects that match the query."""

    cursor.execute(sql)
    return cursor.fetchall()


def get_point(cursor, point_id: str) -> list:
    """Returns a list object containing the selected point"""

    return get_selected(cursor, select_sql.sql_select_point(point_id))


def get_all_points(cursor) -> list:
    """Return a list object containing all points"""

    return get_point(cursor, '0')


def get_all_works_points(cursor) -> list:
    """Return a list object containing all points haves status 'in work' """
    return get_selected(cursor, select_sql.sql_select_all_works_points())


def get_equip_in_point(cursor, point_id: str) -> list:
    """Returns all equipment for this point"""

    sql = select_sql.sql_select_all_equipment \
        if point_id == '' or point_id == '0' \
        else select_sql.sql_select_equipment_in_point(point_id)
    return get_selected(cursor, sql)


def get_equip_in_point_limit(cursor, point_id: str, page_num: int) -> list:
    """Returns all equipment for this point use LIMIT and OFFSET"""

    sql = select_sql.sql_select_all_equipment_limit(page_num) \
        if point_id == '' or point_id == '0' \
        else select_sql.sql_select_equipment_in_point_limit(point_id, page_num)
    return get_selected(cursor, sql)


def get_works_from_equip_id(cursor, id: str) -> list:
    """Returns a list object containing all jobs for a given piece of equipment"""

    sql = select_sql.sql_select_all_works() \
        if id == '' or id == '0' \
        else select_sql.sql_select_work_to_equipment_id(id)
    return get_selected(cursor, sql)


def get_works_from_equip_id_limit(cursor, id: str, page_num: int) -> list:
    """Returns a list object containing all jobs for a given piece of equipment use LIMIT and OFFSET"""

    sql = select_sql.sql_select_all_works_limit(page_num) \
        if id == '' or id == '0' \
        else select_sql.sql_select_work_from_equip_id_limit(id, page_num)
    return get_selected(cursor, sql)


def get_works_from_point_and_equip(cursor, point_id: str, equip_id: str) -> list:
    """Returns a list object containing all jobs at a given point and a given equipment number"""

    equips = get_equip_in_point(cursor, point_id)
    equips_id = [elem[0] for elem in equips] if equip_id == '' or equip_id == '0' else [equip_id]
    works = []
    for id in equips_id:
        works = works + get_works_from_equip_id(cursor, id)
    return works


def get_full_point_information(cursor, point_id: str) -> list:
    """Returns the object list containing complete information about the given point"""

    return list(get_selected(cursor, select_sql.sql_select_information_to_point(point_id))[0])


def get_full_information_list_points(cursor, ls: list) -> list:
    """Returns a list object containing complete information about points in the list ls"""

    return [get_full_point_information(cursor, elem[0]) for elem in ls]


def get_full_equip_information(cursor, equip_id: str) -> list:
    """Returns a list object containing complete information about a given piece of equipment"""

    return list(get_selected(cursor, select_sql.sql_select_full_equips_info(equip_id))[0])


def get_full_information_to_work(cursor, work_id: str) -> list:
    """Returns a list object containing complete information about the work done with the specified number"""

    return list(get_selected(cursor, select_sql.sql_select_work_from_id(work_id))[0])


def get_full_info_from_works_list(cursor, ls: list) -> list:
    """Returns a list object containing complete information about the work performed as specified by the list"""

    return [get_full_information_to_work(cursor, elem[0]) for elem in ls]


def get_all_equips_list_from_like_str(cursor, s: str) -> list:
    """Return all equips names contain s-string"""

    return get_selected(cursor, select_sql.sql_select_equip_from_like_str(s))


def get_all_equips_list_from_like_str_limit(cursor, s: str, page_num: int) -> list:
    """Return all equips names contain s-string use LIMIT and OFFSET"""

    return get_selected(cursor, select_sql.sql_select_equip_from_like_str_limit(s, str(page_num)))



def get_all_points_list_from_like_str(cursor, s:str) -> list:
    """Return all points names contain s-string"""

    return get_selected(cursor, select_sql.sql_select_point_from_like_str(s))


def get_all_points_list_from_like_str_limit(cursor, s:str, page_num: int) -> list:
    """Return all points names contain s-string use LIMIT and OFFSET"""

    return get_selected(cursor, select_sql.sql_select_point_from_like_str_limit(s, str(page_num)))


def get_works_list_from_equips_list(cursor, list_equips: list) -> list:
    """Return works list create from equips list"""

    works = []
    for equip in list_equips:
        works = works + get_works_from_equip_id(cursor, equip[0])
    return works


def get_maximal_equip_id(cursor) -> str:
    """Return string number of maximal id in table oborudovanie"""

    return str(get_selected(cursor, select_sql.sql_select_max_id_equip())[0][0])


def get_maximal_points_id(cursor) -> str:
    """Return string number of maximal id in table workspoints"""

    return str(get_selected(cursor, select_sql.sql_select_max_id_point())[0][0])


def get_maximal_work_id(cursor) -> str:
    """Return string number of maximal id in table works"""

    return str(get_selected(cursor, select_sql.sql_select_max_work_id())[0][0])


def get_point_id_from_equip_id(cursor, equip_id: str) -> str:
    """Return point_id, where point contain equip"""

    return str(get_selected(cursor, select_sql.sql_select_point_id_from_equip_id(equip_id))[0][0])


def get_all_works_like_word(cursor, word: str) -> list:
    """Function return list contain ID work likes word"""

    return get_selected(cursor, select_sql.sql_select_all_works_from_like_str(word))


def get_all_works_like_word_limit(cursor, word: str, page_num: int) -> list:
    """Function return list contain ID work likes word"""

    return get_selected(cursor, select_sql.sql_select_all_works_from_like_str_limit(word, str(page_num)))


def get_all_works_like_word_and_date(cursor, word: str, date_start: str, date_stop: str) -> list:
    """Function return list contain all works in date-date interval and like word"""

    return get_selected(cursor, select_sql.sql_select_all_works_from_like_str_and_date(word, date_start, date_stop))


def get_all_works_like_word_and_date_limit(cursor, word: str, date_start: str, date_stop: str, page_num: int) -> list:
    """Function return list contain all works in date-date interval and like word use LIMIT and OFFSET"""

    return get_selected(cursor, select_sql.sql_select_all_works_from_like_str_and_date_limit(word,
                                                                                             date_start,
                                                                                             date_stop,
                                                                                             str(page_num)))


def get_statistic(cursor) -> list:
    """Function return list contain stat info from all points"""

    return get_selected(cursor, select_sql.sql_select_statistic())


def get_size_database(cursor) -> str:
    """Function return size workhistory database"""

    return get_selected(cursor, select_sql.sql_select_size_database())[0][0]


def get_count_unique_dates_in_works(cursor) -> int:
    """Function return count(unique date) in works table"""

    return get_selected(cursor, select_sql.sql_select_count_uniques_dates())[0][0]


def get_count_unique_works(cursor) -> int:
    """Function return count(id) in work table"""

    return get_selected(cursor, select_sql.sql_select_count_uniques_works())[0][0]


def get_all_workers(cursor) -> list:
    """Function return list contain all workers"""

    return get_selected(cursor, select_sql.sql_select_all_workers())


def get_table_current_workers(cursor) -> list:
    """Function return list contain current workers"""

    return get_selected(cursor, select_sql.sql_select_table_current_workers())


def get_all_works_from_worker_id(cursor, worker_id: str) -> list:
    """Function return list contain all formatting works from current performers"""

    return get_selected(cursor, select_sql.sql_select_works_from_worker(worker_id))


def get_works_days_table(cursor) -> list:
    """Function return table contain points, workers and days of week"""

    return get_selected(cursor, select_sql.sql_select_works_days())


def get_alter_works_days_table(cursor) -> list:
    """Function return all alternatives bindings worers <--> points"""

    return get_selected(cursor, select_sql.sql_select_alter_works_days())


def get_all_bugz_in_bugzilla(cursor) -> list:
    """Function return all records in bugzilla"""

    return get_selected(cursor, select_sql.sql_select_all_bugs_in_bugzilla())


def get_all_bugz_in_work_in_bugzilla(cursor) -> list:
    """Function return all records in bugzilla if bug's status = in work"""

    return get_selected(cursor, select_sql.sql_select_all_bugs_in_work_in_bugzilla())


def get_all_customers(cursor) -> list:
    """Function return list contains all record in customer table"""

    return get_selected(cursor, select_sql.sql_select_all_customers())


def get_all_orders(cursor) -> list:
    """Function return list contains all records in table orders"""

    return get_selected(cursor, select_sql.sql_select_all_orders())

