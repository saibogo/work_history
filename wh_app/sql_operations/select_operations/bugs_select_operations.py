from wh_app.sql_operations.select_operations.decorators import *
from wh_app.sql.select_sql import select_sql


@get_selected_decorator
def get_all_bugz_in_bugzilla(cursor) -> list:
    """Function return all records in bugzilla"""
    return select_sql.sql_select_all_bugs_in_bugzilla()


@get_selected_decorator
def get_all_bugz_in_bugzilla_limit(cursor, page_num: int) -> list:
    """Function return all records in bugzilla use limit records on page"""
    return select_sql.sql_select_all_bugs_in_bugzilla_limit(str(page_num))


@get_selected_decorator
def get_all_bugz_in_work_in_bugzilla(cursor) -> list:
    """Function return all records in bugzilla if bug's status = in work"""
    return select_sql.sql_select_all_bugs_in_work_in_bugzilla()


@get_selected_decorator
def get_all_bugz_in_work_in_bugzilla_limit(cursor, page_num: int) -> list:
    """Function return all records in bugzilla if bug's status = in work"""
    return select_sql.sql_select_all_bugs_in_work_in_bugzilla_limit(str(page_num))


@list_to_first_tuple_decorator
@get_selected_decorator
def get_bug_by_id(cursor, bug_id: str) -> list:
    """Return bug information with ID = bug_id"""
    return select_sql.sql_select_get_bug_by_id(bug_id)
