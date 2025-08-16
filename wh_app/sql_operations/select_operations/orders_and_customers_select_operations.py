from wh_app.sql_operations.select_operations.decorators import *
from wh_app.sql.select_sql import select_sql


@get_selected_decorator
def get_all_customers(cursor) -> list:
    """Function return list contains all record in customer table"""
    return select_sql.sql_select_all_customers()


@list_to_first_tuple_decorator
@get_selected_decorator
def get_full_customer_info(cursor, customer_id: str) -> list:
    """Function return list contains all record in customer table"""
    return select_sql.sql_select_customer_info(customer_id)


@list_to_first_str_decorator
@get_selected_decorator
def get_hash_to_customer(cursor, user_name: str) -> str:
    """Function return hash with user = full_name"""
    return select_sql.sql_select_hash_from_user(user_name)


@get_selected_decorator
def get_all_orders(cursor, ord=False, ord_column=1) -> list:
    """Function return list contains all records in table orders"""
    return select_sql.sql_select_all_orders()


@get_selected_decorator
def get_all_orders_from_customer_id(cursor, customer_id: int) -> List[Tuple]:
    """Function return list contain all orders from customer"""

    return select_sql.sql_select_all_orders_from_customer_id(customer_id)


@get_selected_decorator
def get_all_orders_limit_ord(cursor, page_num: int, ord=False, ord_column=1) -> List[Tuple]:
    """Returns a list object containing all jobs for a given piece of equipment use LIMIT and OFFSET
    See also get_works_from_equip_id"""

    return select_sql.sql_select_all_orders_limit_ord(page_num, ord, ord_column)


@get_selected_decorator
def get_all_orders_from_customer_limit(cursor, customer_id:int, page_num: int) -> List[Tuple]:
    """Returns a list object containing all jobs for a given piece of equipment use LIMIT and OFFSET
    See also get_works_from_equip_id"""

    return select_sql.sql_select_all_orders_from_customer_limit(customer_id, page_num)


@get_selected_decorator
def get_all_no_closed_orders(cursor, ord=False, ord_column=1) -> list:
    """Function return list contains all records in table orders"""
    return select_sql.sql_select_no_closed_orders(ord, ord_column)


@get_selected_decorator
def get_all_no_closed_orders_limit(cursor, page_num: int, ord=False, ord_column=1) -> list:
    """Function return list contains all records in table orders"""
    return select_sql.sql_select_no_closed_orders_limit(page_num, ord, ord_column)


@list_to_first_int_decorator
@get_selected_decorator
def get_maximal_orders_id(cursor) -> int:
    """Function return maximal id from orders table"""
    return select_sql.sql_select_max_order_id()


@get_selected_decorator
def get_all_order_status(cursor) -> List[Tuple]:
    """return all status and description from orders_types"""
    return select_sql.sql_select_all_orders_type()


@list_to_first_tuple_decorator
@get_selected_decorator
def get_order_from_id(cursor, order_id: str) -> Tuple:
    """Function return tuple contain full information from order with ID = order_id"""
    return select_sql.sql_select_order_from_id(order_id)


@list_to_first_int_decorator
@get_selected_decorator
def get_last_order_id_in_work(cursor) -> int:
    """Function return id to last order with status in_work"""
    return select_sql.sql_select_last_orders_id_in_work()


@list_to_first_bool_decorator
@get_selected_decorator
def user_in_customers(cursor, user_name: str) -> bool:
    """Function find user in customer table"""
    return select_sql.sql_select_user_in_customers(user_name)


@get_selected_decorator
def get_all_customers_orders_limit(cursor, user_name: str, page_num: int) -> List[Tuple]:
    """Function return all customers order using LIMIT"""
    return select_sql.sql_select_orders_from_user_limit(user_name, page_num)


@get_selected_decorator
def get_all_customers_orders(cursor, user_name: str) -> List[Tuple]:
    """Function return all customers order using LIMIT"""
    return select_sql.sql_select_orders_from_user(user_name)


@list_to_first_str_decorator
@get_selected_decorator
def get_order_status(cursor, order_id: int) -> str:
    """Function return current status to order with id = order_id"""
    return select_sql.sql_select_order_status(order_id)


@get_selected_decorator
def get_worked_orders_from_point(cursor, point_id: int) -> List:
    """Function return all oders with status = in_work from current point"""

    return select_sql.sql_select_orders_in_work_from_point_id(point_id)


@get_selected_decorator
def get_all_worked_orders_with_equal_problem(cursor, problem: str, point_id: int) -> List:
    """Function return all orders with equal problem and status in_work"""

    return select_sql.sql_select_all_equal_worked_problem(problem, point_id)
