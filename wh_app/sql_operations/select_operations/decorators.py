from typing import *

def get_selected(cursor, sql: str) -> List:
    """Returns a list of database objects that match the query."""

    cursor.execute(sql)
    return cursor.fetchall()


def get_selected_decorator(func: Callable) -> Callable:
    """Returns a list of database objects that match the query."""
    def wrap(*args) -> List[Tuple]:
        cursor= args[0]
        cursor.execute(func(*args))
        return cursor.fetchall()
    return wrap


def list_to_list_decorator(func: Callable) -> Callable:
    """List[Tuple[Any]] -> List[str]"""
    def wrap(*args) -> List[str]:
        return list(func(*args)[0])
    return wrap


def list_tuples_to_list_decorator(func: Callable) -> Callable:
    """[(elem,), (elem1,), ...] -> [elem, elem1, ...]"""
    def wrap(*args) -> List[Any]:
        return [elem[0] for elem in func(*args)]
    return wrap


def list_to_first_tuple_decorator(func: Callable) -> Callable:
    """List[Tuple[Any]] -> List[str]"""
    def wrap(*args) -> List[str]:
        return func(*args)[0]
    return wrap


def list_to_first_str_decorator(func: Callable) -> Callable:
    """List[Tuple[Any]] -> String"""
    def wrap(*args) -> str:
        return str(func(*args)[0][0])
    return wrap


def list_to_first_int_decorator(func: Callable) -> Callable:
    """List[Tuple[Any]] -> String"""
    def wrap(*args) -> int:
        return int(func(*args)[0][0])
    return wrap


def list_to_first_decimal_decorator(func: Callable) -> Callable:
    """List[Tuple[Any]] -> String"""
    def wrap(*args) -> float:
        return func(*args)[0][0]
    return wrap


def list_to_first_bool_decorator(func: Callable) -> Callable:
    """List[Tuple[Any]] -> String"""
    def wrap(*args) -> bool:
        return func(*args)[0][0]
    return wrap