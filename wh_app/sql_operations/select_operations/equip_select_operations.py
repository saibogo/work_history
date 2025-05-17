from wh_app.sql_operations.select_operations.decorators import *
from wh_app.sql.select_sql import select_sql


@get_selected_decorator
def get_equip_in_point(cursor, point_id: str, ord=False, ord_column=1) -> List[Tuple]:
    """Returns all equipment for this point
    Return value [elem, elem1, ..., elem_n] while elem = (equip_id, point_name, equip_name, model, serial, pre_id)"""

    return select_sql.sql_select_all_equipment \
        if point_id == '' or point_id == '0' \
        else select_sql.sql_select_equipment_in_point(point_id, ord_column)


@get_selected_decorator
def get_equip_in_point_limit(cursor, point_id: str, page_num: int, ord_column=1) -> List[Tuple]:
    """Returns all equipment for this point use LIMIT and OFFSET
    Return value see get_equip_in_point"""

    return select_sql.sql_select_all_equipment_limit(page_num, ord_column) \
        if point_id == '' or point_id == '0' \
        else select_sql.sql_select_equipment_in_point_limit(point_id, page_num, ord_column)


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


@list_to_first_tuple_decorator
@get_selected_decorator
def get_equips_detail_id(cursor, equip_id: int) -> Tuple:
    """Return details_id or NULL"""

    return select_sql.sql_select_found_details(equip_id)


@list_to_first_tuple_decorator
@get_selected_decorator
def get_equips_manual_id(cursor, equip_id: int) -> Tuple:
    """Return details_id or NULL"""

    return select_sql.sql_select_found_manual(equip_id)


@list_to_first_tuple_decorator
@get_selected_decorator
def get_details_info(cursor, detail_id: int) -> Tuple:
    """Return details info"""

    return select_sql.sql_select_detail_info(detail_id)


@list_to_first_tuple_decorator
@get_selected_decorator
def get_manuals_info(cursor, manual_id: int) -> Tuple:
    """Return details info"""

    return select_sql.sql_select_manual_info(manual_id)


@get_selected_decorator
def get_all_equips_subtypes(cursor) -> List[Tuple]:
    """Return all equips subtaypes and description"""

    return select_sql.sql_select_all_equip_subtypes()


@get_selected_decorator
def get_all_details_from_subtype_id(cursor, subtype_id: int) -> List[Tuple]:
    """Return all equip`s detail from current subtype"""

    return select_sql.sql_select_all_details_from_subtype_id(subtype_id)


@get_selected_decorator
def get_all_manuals_from_subtype_id(cursor, subtype_id: int) -> List[Tuple]:
    """Return all equip`s detail from current subtype"""

    return select_sql.sql_select_all_manuals_from_subtype_id(subtype_id)


@get_selected_decorator
def get_all_equips_meta_type(cursor) -> List[Tuple]:
    """Get all values in equips_meta_type"""

    return select_sql.sql_select_all_equips_meta_type()


@list_to_first_str_decorator
@get_selected_decorator
def get_sub_dir_to_equip_class(cursor, type_id :int) -> str:
    """Return sub_dir to equip`s sub_type"""

    return select_sql.sql_select_types_sub_dir(type_id)