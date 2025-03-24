import datetime

from wh_app.sql_operations.select_operations.decorators import *
from wh_app.sql.select_sql import select_sql


@get_selected_decorator
def get_all_equips_list_from_like_str(cursor, s: str) -> List[Tuple]:
    """Return all equips names contain s-string
    [elem1, elem2, ..., elem_n] while elem = (equip_ID, point_name, model, serial, pre_ID)"""

    return select_sql.sql_select_equip_from_like_str(s)


@get_selected_decorator
def get_all_equips_list_from_like_str_limit(cursor, s: str, page_num: int) -> List[Tuple]:
    """Return all equips names contain s-string use LIMIT and OFFSET
    See also get_all_equips_list_from_like_str"""

    return select_sql.sql_select_equip_from_like_str_limit(s, str(page_num))


@get_selected_decorator
def get_all_points_list_from_like_str(cursor, s:str) -> List[Tuple[int, str, str, bool]]:
    """Return all points names contain s-string
    Return value [elem1, elem2, ..., elem_n] while elem = (point_ID, point_name, point_address, point_status)"""

    return select_sql.sql_select_point_from_like_str(s)


@get_selected_decorator
def get_all_points_list_from_like_str_limit(cursor, s:str, page_num: int) -> List[Tuple[int, str, str, bool]]:
    """Return all points names contain s-string use LIMIT and OFFSET
    see also get_all_points_list_from_like_str"""

    return select_sql.sql_select_point_from_like_str_limit(s, str(page_num))


@get_selected_decorator
def get_all_works_like_word(cursor, word: str) -> List[Tuple[int, str, str, str, str,
                                                             datetime.datetime, str, str, str]]:
    """Function return list contain ID work likes word
    Return value [elem1, elem2, ..., elem_n] while elem = (work_ID, point_name, equip_name, model, serial,
    datetime, problem, result, performers_names)"""

    return select_sql.sql_select_all_works_from_like_str(word)


@list_tuples_to_list_decorator
@get_selected_decorator
def get_all_find_patterns(cursor) -> List[str]:
    """Function return list of all unique find patterns"""

    return select_sql.sql_select_all_find_patterns()


@get_selected_decorator
def get_all_works_like_word_limit(cursor, word: str, page_num: int) -> List[Tuple[int, str, str, str, str,
                                                             datetime.datetime, str, str, str]]:
    """Function return list contain ID work likes word
    See also get_all_works_like_word"""

    return select_sql.sql_select_all_works_from_like_str_limit(word, str(page_num))


@get_selected_decorator
def get_all_works_like_word_and_date(cursor, word: str, date_start: str, date_stop: str) -> \
        List[Tuple[int, str, str, str, str, datetime.datetime, str, str, str]]:
    """Function return list contain all works in date-date interval and like word
    See also get_all_works_like_word"""

    return select_sql.sql_select_all_works_from_like_str_and_date(word, date_start, date_stop)


@get_selected_decorator
def get_all_works_like_word_and_date_limit(cursor, word: str, date_start: str, date_stop: str, page_num: int) \
        -> List[Tuple[int, str, str, str, str, datetime.datetime, str, str, str]]:
    """Function return list contain all works in date-date interval and like word use LIMIT and OFFSET
    See also get_all_works_like_word"""

    return select_sql.sql_select_all_works_from_like_str_and_date_limit(word, date_start, date_stop, str(page_num))