from wh_app.sql_operations.select_operations.decorators import *
from wh_app.sql.select_sql import select_sql


@list_to_list_decorator
@list_to_first_tuple_decorator
@get_selected_decorator
def get_all_telegram_chats(cursor) -> List:
    """Return all telegramm id from bot"""

    return select_sql.sql_select_all_telegram_chats()


@list_to_first_bool_decorator
@get_selected_decorator
def is_telegram_user_reader(cursor, user_id: int) -> bool:
    """Return awaliable read to current user"""

    return select_sql.sql_select_telegram_user_is_reader(user_id)


@list_to_first_bool_decorator
@get_selected_decorator
def is_telegram_user_writer(cursor, user_id: int) -> bool:
    """Return awaliable write to current user"""

    return select_sql.sql_select_telegram_user_is_writer(user_id)