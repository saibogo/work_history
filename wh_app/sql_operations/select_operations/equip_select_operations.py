from wh_app.sql_operations.select_operations.decorators import *
from wh_app.sql.select_sql import select_sql


@get_selected_decorator
def get_equip_in_point(cursor, point_id: str) -> List[Tuple]:
    """Returns all equipment for this point
    Return value [elem, elem1, ..., elem_n] while elem = (equip_id, point_name, equip_name, model, serial, pre_id)"""

    return select_sql.sql_select_all_equipment \
        if point_id == '' or point_id == '0' \
        else select_sql.sql_select_equipment_in_point(point_id)


@get_selected_decorator
def get_equip_in_point_limit(cursor, point_id: str, page_num: int) -> List[Tuple]:
    """Returns all equipment for this point use LIMIT and OFFSET
    Return value see get_equip_in_point"""

    return select_sql.sql_select_all_equipment_limit(page_num) \
        if point_id == '' or point_id == '0' \
        else select_sql.sql_select_equipment_in_point_limit(point_id, page_num)


@list_to_list_decorator
@get_selected_decorator
def get_full_equip_information(cursor, equip_id: str) -> List[str]:
    """Returns a list object containing complete information about a given piece of equipment
    Return value [point_name, equip_name, model, serial, pre_ID]"""

    return select_sql.sql_select_full_equips_info(equip_id)


@list_to_first_str_decorator
@get_selected_decorator
def get_count_equips(cursor) -> str:
    """Return count not-deleted string in oborudovanie"""
    return select_sql.sql_select_count_equip()


@list_to_first_str_decorator
@get_selected_decorator
def get_last_equip_id(cursor) -> str:
    """Return string number of maximal id in table oborudovanie"""
    return select_sql.sql_select_last_equip_id()


@list_to_first_str_decorator
@get_selected_decorator
def get_next_equip_id(cursor) -> str:
    """Return string number of maximal id in table oborudovanie"""
    return select_sql.sql_select_next_id_equip()


@list_to_first_bool_decorator
@get_selected_decorator
def get_equip_deleted_status(cursor, equip_id: str) -> bool:
    """Return current deleted-status from equip with id = equip_id"""

    return select_sql.sql_select_equip_deleted_status(equip_id)

