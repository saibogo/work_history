import psycopg2

import config
import select_sql
import functions

functions.info_string(__name__)


def open_database() -> psycopg2.connect:
    """Creates a new connection to the database specified in the config file"""

    return psycopg2.connect(database=config.database_name,
                            user=config.user_name,
                            password=config.user_password,
                            host=config.database_host,
                            port=config.database_port)


def commit(connection: psycopg2.connect) -> None:
    """Applies changes to the database"""

    connection.commit()


def close_database(connection: psycopg2.connect, save: bool = True) -> None:
    """Disconnects to database. The save option determines if changes should be applied."""

    if save:
        commit(connection)
    connection.close()


def create_cursor(connection: psycopg2.connect):
    """Creates a new cursor to an open connection"""

    return connection.cursor()


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


def get_equip_in_point(cursor, point_id: str) -> list:
    """Returns all equipment for this point"""

    sql = select_sql.sql_select_all_equipment \
        if point_id == '' or point_id == '0' \
        else select_sql.sql_select_equipment_in_point(point_id)
    return get_selected(cursor, sql)


def get_works_from_equip_id(cursor, id: str) -> list:
    """Returns a list object containing all jobs for a given piece of equipment"""

    sql = select_sql.sql_select_all_works \
        if id == '' or id == '0' \
        else select_sql.sql_select_work_to_equipment_id(id)
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


def get_full_equips_list_info(cursor, ls: list) -> list:
    """Returns a list object containing the complete information of the equipment specified in the list"""

    return [get_full_equip_information(cursor, elem[0]) for elem in ls]


def get_full_information_to_work(cursor, work_id: str) -> list:
    """Returns a list object containing complete information about the work done with the specified number"""

    return list(get_selected(cursor, select_sql.sql_select_work_from_id(work_id))[0])


def get_full_info_from_works_list(cursor, ls: list) -> list:
    """Returns a list object containing complete information about the work performed as specified by the list"""

    return [get_full_information_to_work(cursor, elem[0]) for elem in ls]


def get_all_equips_list_from_like_str(cursor, s: str) -> list:
    """Return all equips names contain s-string"""

    return get_selected(cursor, select_sql.sql_select_equip_from_like_str(s))


def get_all_points_list_from_like_str(cursor, s:str) -> list:
    """Return all points names contain s-string"""

    return get_selected(cursor, select_sql.sql_select_point_from_like_str(s))


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

