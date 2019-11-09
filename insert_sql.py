from metadata import *


def sql_insert_new_point(point_id: str, name: str, addres: str) -> str:
    """Returns the query string to add a new point"""

    return 'INSERT INTO workspoints (point_id, point_name, point_address) ' \
           'VALUES (' + point_id + ', \'' + str(name) + '\', \'' + str(addres) + '\')'


def sql_insert_new_equip(id: str, point: str, name: str, model: str, serial: str, pre_id: str) -> str:
    """Returns the query string to add a new piece of equipment"""

    if pre_id == "NULL":
        return 'INSERT INTO oborudovanie (id, point_id, name, model, serial_num) VALUES' \
               + '(' + str(id) + ', ' + str(point) + ', \'' + str(name) + '\', \'' +\
               str(model) + '\', \'' + str(serial) + '\', ' + str(id) + ')'
    else:
        return 'INSERT INTO oborudovanie (id, point_id, name, model, serial_num, pre_id) VALUES' \
               + '(' + str(id) + ', ' + str(point) + ', \'' + str(name) + '\', \'' + str(model) + '\', \'' +\
               str(serial) + '\', ' + str(pre_id) + ')'


def sql_insert_new_work(id:str, id_obor: str, date: str, problem: str, result:str) -> str:
    """Function return query string to add new work"""

    return 'INSERT INTO works (id, id_obor, date, problem, result) VALUES (' + str(id) + ', ' + str(id_obor) +\
           ', \'' + str(date) + '\', \'' + str(problem) + '\', \'' + str(result) + '\')'