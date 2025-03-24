from wh_app.sql_operations.select_operations.decorators import *
from wh_app.sql.select_sql import select_sql


@get_selected_decorator
def get_point(cursor, point_id: str) -> List[Tuple]:
    """Returns a list object containing the selected point
    [elem] while elem = (point_id, point_name, point_address, point_status)"""

    return select_sql.sql_select_point(point_id)


def get_all_points(cursor) -> List[Tuple]:
    """Return a list object containing all points
    See get_point: return value [elem, elem1, ..., elem_n]"""

    return get_point(cursor, '0')


@get_selected_decorator
def get_all_works_points(cursor) -> List[Tuple]:
    """Return a list object containing all points haves status 'in work'
    See also get_point: return value [elem, elem1, .... elem_n]"""

    return select_sql.sql_select_all_works_points()


@list_to_list_decorator
@get_selected_decorator
def get_full_point_information(cursor, point_id: str) -> List[str]:
    """Returns the object list containing complete information about the given point
    return value = [point_name, point_address, point_status]"""

    return select_sql.sql_select_information_to_point(point_id)


def get_full_information_list_points(cursor, ls: list) -> list:
    """Returns a list object containing complete information about points in the list ls"""

    return [get_full_point_information(cursor, elem[0]) for elem in ls]


@list_to_first_str_decorator
@get_selected_decorator
def get_maximal_points_id(cursor) -> str:
    """Return string number of maximal id in table workspoints"""

    return select_sql.sql_select_max_id_point()


@list_to_first_str_decorator
@get_selected_decorator
def get_point_id_from_equip_id(cursor, equip_id: str) -> str:
    """Return point_id, where point contain equip"""

    return select_sql.sql_select_point_id_from_equip_id(equip_id)


@list_to_first_str_decorator
@get_selected_decorator
def get_point_name_from_id(cursor, id: str) -> str:
    """Function return string-name of point"""
    return select_sql.sql_select_name_from_point_id(str(id))


@get_selected_decorator
def get_all_point_except_id(cursor, id: str) -> list:
    """Function return all points except point_id == id"""
    return select_sql.sql_select_all_point_except_id(str(id))


@list_to_first_str_decorator
@get_selected_decorator
def get_count_works_points(cursor) -> str:
    """Return string number of maximal id in table workspoints"""

    return select_sql.sql_select_count_works_point()