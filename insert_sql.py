__author__ = "Andrey Gleykh"
__license__ = "GPL"
__email__ = "gleykh@gmail.com"
__status__ = "Prototype"


def sql_insert_new_point(name: str, addres: str) -> str:
    """Returns the query string to add a new point"""
    return 'INSERT INTO workspoints (point_name, point_address) VALUES ("' + str(name) + '", "' + str(addres) + '")'


def sql_insert_new_equip(point: str, name: str, model: str, serial: str, pre_id: str) -> str:
    """Returns the query string to add a new piece of equipment"""

    if pre_id == "NULL":
        return 'INSERT INTO oborudovanie (point_id, name, model, serial_num) VALUES' \
               + '("' + str(point) + '", "' + str(name) + '", "' + str(model) + '", "' + str(serial) + '")'
    else:
        return 'INSERT INTO oborudovanie (point_id, name, model, serial_num, pre_id) VALUES' \
               + '("' + str(point) + '", "' + str(name) + '", "' + str(model) + '", "' + str(serial) \
               + '", "' + str(pre_id) + '")'


def sql_insert_new_work(id_obor: str, date: str, problem: str, result:str) -> str:
    """Function return query string to add new work"""

    return 'INSERT INTO works (id_obor, date, problem, result) VALUES ("' + str(id_obor) + '", "' + str(date) + '", "' \
           + str(problem) + '", "' + str(result) + '")'