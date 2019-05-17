from sqlite3 import Cursor

from insert_sql import *

__author__ = "Andrey Gleykh"
__license__ = "GPL"
__email__ = "gleykh@gmail.com"
__status__ = "Prototype"


def create_new_point(curr: Cursor, point_name: str, point_address: str) -> None:
    """Creates a new point in the database"""

    curr.execute(sql_insert_new_point(point_name, point_address))


def create_new_equip(curr: Cursor, point_id: str, name: str,
                     model: str = "not model", serial_num: str = "not number", pre_id: str = "NULL") -> None:
    """Creates a new piece of equipment in the database"""

    curr.execute(sql_insert_new_equip(point_id, name, model, serial_num, pre_id))


def create_new_work(curr: Cursor, id_obor: str, date: str, problem: str, result: str) -> None:
    """Create a new work record in database"""

    curr.execute(sql_insert_new_work(id_obor, date, problem, result))

