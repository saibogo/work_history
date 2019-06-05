import sqlite3

import config
import select_sql

__author__ = "Andrey Gleykh"
__license__ = "GPL"
__email__ = "gleykh@gmail.com"
__status__ = "Prototype"


def open_database() -> sqlite3.Connection:
    """Creates a new connection to the database specified in the config file"""

    return sqlite3.connect(config.database_name)


def commit(conn: sqlite3.Connection) -> None:
    """Applies changes to the database"""

    conn.commit()


def close_database(conn: sqlite3.Connection, save: bool = True) -> None:
    """Disconnects to database. The save option determines if changes should be applied."""

    if save:
        commit(conn)
    conn.close()


def create_cursor(conn: sqlite3.Connection) -> sqlite3.Cursor:
    """Creates a new cursor to an open connection"""

    return conn.cursor()


def get_selected(curr: sqlite3.Cursor, sql: str) -> list:
    """Returns a list of database objects that match the query."""

    curr.execute(sql)
    return curr.fetchall()


def get_point(curr: sqlite3.Cursor, point_id: str) -> list:
    """Returns a list object containing the selected point"""

    return get_selected(curr, select_sql.sql_select_point(point_id))


def get_all_points(curr: sqlite3.Cursor) -> list:
    """Return a list object containing all points"""

    return get_point(curr, '0')


def get_equip_in_point(curr: sqlite3.Cursor, point_id: str) -> list:
    """Returns all equipment for this point"""

    sql = select_sql.sql_select_all_equipment \
        if point_id == '' or point_id == '0' \
        else select_sql.sql_select_equipment_in_point(point_id)
    return get_selected(curr, sql)


def get_works_from_equip_id(curr: sqlite3.Cursor, id: str) -> list:
    """Returns a list object containing all jobs for a given piece of equipment"""

    sql = select_sql.sql_select_all_works \
        if id == '' or id == '0' \
        else select_sql.sql_select_work_to_equipment_id(id)
    return get_selected(curr, sql)


def get_works_from_point_and_equip(curr: sqlite3.Cursor, point_id: str , equip_id: str) -> list:
    """Returns a list object containing all jobs at a given point and a given equipment number"""

    equips = get_equip_in_point(curr, point_id)
    equips_id = [elem[0] for elem in equips] if equip_id == '' or equip_id == '0' else [equip_id]
    works = []
    for id in equips_id:
        works = works + get_works_from_equip_id(curr, id)
    return works


def get_full_point_information(curr: sqlite3.Cursor, point_id: str) -> list:
    """Returns the object list containing complete information about the given point"""

    return list(get_selected(curr, select_sql.sql_select_information_to_point(point_id))[0])


def get_full_information_list_points(curr: sqlite3.Cursor, ls: list) -> list:
    """Returns a list object containing complete information about points in the list ls"""

    return [get_full_point_information(curr, elem[0]) for elem in ls]


def get_full_equip_information(curr: sqlite3.Cursor, equip_id: str) -> list:
    """Returns a list object containing complete information about a given piece of equipment"""

    tmp = list(get_selected(curr, select_sql.sql_select_equip_information(equip_id))[0])
    return get_full_point_information(curr, tmp[0]) + tmp[1:]


def get_full_equips_list_info(curr: sqlite3.Cursor, ls: list) -> list:
    """Returns a list object containing the complete information of the equipment specified in the list"""

    return [get_full_equip_information(curr, elem[0]) for elem in ls]


def get_full_information_to_work(curr: sqlite3.Cursor, work_id: str) -> list:
    """Returns a list object containing complete information about the work done with the specified number"""

    tmp = list(get_selected(curr, select_sql.sql_select_work_from_id(work_id))[0])
    equip_id = tmp[1]
    return get_full_equip_information(curr, equip_id) + tmp[2:]


def get_full_info_from_works_list(curr: sqlite3.Cursor, ls: list) -> list:
    """Returns a list object containing complete information about the work performed as specified by the list"""

    return [get_full_information_to_work(curr, elem[0]) for elem in ls]


def get_all_equips_list_from_like_str(curr: sqlite3.Cursor, s: str) -> list:
    """Return all equips names contain s-string"""

    return get_selected(curr, select_sql.sql_select_equip_from_like_str(s))


def get_all_points_list_from_like_str(curr: sqlite3.Cursor, s:str) -> str:
    """Return all points names contain s-string"""

    return get_selected(curr, select_sql.sql_select_point_from_like_str(s))


def get_works_list_from_equips_list(curr: sqlite3.Cursor, list_equips: list) -> list:
    """Return works list create from equips list"""

    works = []
    for equip in list_equips:
        works = works + get_works_from_equip_id(curr, equip[0])
    return works


def get_maximal_equip_id(curr: sqlite3.Cursor) -> str:
    """Return string number of maximal id in table oborudovanie"""

    return str(get_selected(curr, select_sql.sql_select_max_id_equip())[0][0])


def get_point_id_from_equip_id(curr: sqlite3.Cursor, equip_id: str) -> str:
    """Return point_id, where point contain equip"""

    return str(get_selected(curr, select_sql.sql_select_point_id_from_equip_id(equip_id))[0][0])
