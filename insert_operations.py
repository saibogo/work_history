import functions
import select_operations
from insert_sql import *

functions.info_string(__name__)


def create_new_point(cursor, point_name: str, point_address: str) -> None:
    """Creates a new point in the database"""

    new_point_id = str(int(select_operations.get_maximal_points_id(cursor)) + 1)
    cursor.execute(sql_insert_new_point(new_point_id, point_name, point_address))


def create_new_equip(cursor, point_id: str, name: str,
                     model: str = "not model", serial_num: str = "not number", pre_id: str = "") -> None:
    """Creates a new piece of equipment in the database"""

    new_id = int(select_operations.get_maximal_equip_id(cursor)) + 1
    cursor.execute(sql_insert_new_equip(new_id ,point_id, name, model, serial_num,
                                        pre_id if pre_id != "" else str(new_id)))


def create_new_work(cursor, id_obor: str, date: str, problem: str, result: str, worker_id: str) -> None:
    """Create a new work record in database"""

    new_id = str(int(select_operations.get_maximal_work_id(cursor)) + 1)
    cursor.execute(sql_insert_new_work(new_id, id_obor, date, problem, result, worker_id))



