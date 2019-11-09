from metadata import *


def sql_select_point(point_id: str) -> str:
    """Returns the string of the query for selecting a point by a unique number"""

    return "SELECT * FROM workspoints " + ("WHERE point_id=" + str(point_id)
                                                         if point_id != '' and point_id != '0'
                                                         else "")


sql_select_all_points = sql_select_point('')


def sql_select_equipment_in_point(point: str) -> str:
    """Returns the query string for selecting all equipment items at a given point"""

    return "SELECT * FROM oborudovanie" + (" WHERE point_id=" + str(point) if point != "" else "")


sql_select_all_equipment = sql_select_equipment_in_point('')


def sql_select_work_to_equipment_id(id: str) -> str:
    """Returns the query string to select all repairs corresponding to the equipment with the given number"""

    return "SELECT * FROM works" + (" WHERE id_obor=" + str(id) if str(id) != '' else '')


sql_select_all_works = sql_select_work_to_equipment_id('')


def sql_select_information_to_point(id :str) -> str:
    """Returns the string of the request for complete information about the point with the given number"""

    return "SELECT point_name, point_address FROM workspoints WHERE point_id=" + str(id)


def sql_select_equip_information(id: str) -> str:
    """Returns the query string for the complete information of the equipment with the given number"""

    return "SELECT point_id, name, model, serial_num, pre_id FROM oborudovanie WHERE id=" + str(id)


def sql_select_work_from_id(id: str) -> str:
    """Returns the query string corresponding to the work performed with the specified number"""

    return "SELECT * FROM works WHERE id=" + str(id)


def sql_select_equip_from_like_str(s: str) -> str:
    """Return the query string select equips from like-string"""

    words = s.split()
    return 'SELECT * FROM oborudovanie WHERE name LIKE "%' + str('%'.join(words)) + '%"'


def sql_select_point_from_like_str(s: str) -> str:
    """Return the query string select points from like-string"""

    words = s.split()
    return 'SELECT * FROM workspoints WHERE LOWER(point_name) LiKE "%' + str('%'.join(words)) + '%"'


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

