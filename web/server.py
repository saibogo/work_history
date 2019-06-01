from flask import Flask, request

import select_operations
import insert_operations
import web.universal_html as uhtml
import config
import functions

__author__ = "Andrey Gleykh"
__license__ = "GPL"
__email__ = "gleykh@gmail.com"
__status__ = "Prototype"

app = Flask(__name__)


def database():
    conn = select_operations.open_database()
    curr = select_operations.create_cursor(conn)

    return conn, curr


def close_database(conn):
    select_operations.close_database(conn, False)


@app.route("/")
def hello():
    name = "Доступные действия в базе ремонтов Малахит-Екатеринбург"
    menu = [(1, 'Операции с предприятиями'), (2, 'Операции с оборудованием'), (3, 'Операции с ремонтами')]
    links_list = ['/points', '/equips', '/works']
    return uhtml.universal_table(name, ['№', 'выполнить:'], menu, True, links_list)


@app.route("/equips")
def equips_operations():
    name = 'Действия с оборудованием'
    menu = [(1, 'Все зарегестрированное оборудование')]
    links_list = ['/all-equips']
    return uhtml.universal_table(name, ['№', 'Доступное действие'], menu, True, links_list)


@app.route("/points")
def points_operations():
    name = 'Действия с предприятиями'
    menu = [(1, 'Все зарегестрированные предприятия'), (2, 'Добавить предприятие')]
    links_list = ['/all-points', '/create_new_point']
    return uhtml.universal_table(name, ['№', 'Доступное действие'], menu, True, links_list)


@app.route("/all-points")
def all_points_table():
    conn, curr = database()
    all_points = select_operations.get_all_points(curr)
    full_points = select_operations.get_full_information_list_points(curr, all_points)
    links_list = ['/equip/' + str(elem) for elem in functions.get_id_list(all_points)]
    close_database(conn)
    table1 =  uhtml.universal_table(config.points_table_name, config.points_table, full_points, True, links_list)
    table2 = uhtml.add_new_point()
    return table1 + '\n' + table2


@app.route("/create_new_point")
def create_new_point():
    html = uhtml.style_custom() + '\n' + uhtml.add_new_point()
    return html


@app.route('/add-point', methods=['POST'])
def add_point():
    if request.method == "POST":
        data = functions.form_to_data(request.form)
        point_name = data['point_name']
        point_adr = data['point_addres']
        password = data["password"]
        if functions.is_valid_password(password):
            conn, curr = database()
            insert_operations.create_new_point(curr, point_name, point_adr)
            select_operations.commit(conn)
            close_database(conn)
            return uhtml.operation_completed()
        else:
            return uhtml.pass_is_not_valid()

    else:
        return "Method not correct!"


@app.route("/equip/<point_id>")
def equip_to_point(point_id):
    conn, curr = database()
    all_equips = select_operations.get_equip_in_point(curr, str(point_id))
    full_equips = select_operations.get_full_equips_list_info(
        curr, all_equips)
    links_list = ['/work/' + str(elem) for elem in functions.get_id_list(all_equips)]
    correct_full_equips = [[elem[i] for i in [0, 2, 3, 4, 5]] for elem in full_equips]
    close_database(conn)
    table1 = uhtml.universal_table(config.equips_table_name, config.equips_table, correct_full_equips, True, links_list)
    table2 = uhtml.add_new_equip(point_id)
    return table1 + '\n' + table2


@app.route("/all-equips")
def all_equips_table():
    return equip_to_point('0')


@app.route("/add-equip", methods=['POST'])
def add_equip():
    if request.method == "POST":
        data = functions.form_to_data(request.form)
        point_id = data['point_id']
        equip_name = data['equip_name']
        model = data['model']
        serial_num = data['serial_num']
        pre_id = data['pre_id']
        password = data["password"]
        if functions.is_valid_password(password):
            conn, curr = database()
            if model == '':
                insert_operations.create_new_equip(curr, point_id, equip_name)
            elif serial_num == '':
                insert_operations.create_new_equip(curr, point_id, equip_name, model)
            elif pre_id == '':
                insert_operations.create_new_equip(curr, point_id, equip_name, model, serial_num)
            else:
                insert_operations.create_new_equip(curr, point_id, equip_name, model, serial_num, pre_id)
            select_operations.commit(conn)
            close_database(conn)
            return uhtml.operation_completed()
        else:
            return uhtml.pass_is_not_valid()

    else:
        return "Method not correct!"


@app.route("/works")
def works_operations():
    name = 'Действия с ремонтами и диагностиками'
    menu = [(1, 'Все зарегестрированные работы')]
    links_list = ['/all-works']
    return uhtml.universal_table(name, ['№', 'Доступное действие'], menu, True, links_list)


@app.route("/work/<equip_id>")
def work_to_equip(equip_id):
    conn, curr = database()
    full_works = select_operations.get_full_info_from_works_list(
        curr, select_operations.get_works_from_equip_id(curr, str(equip_id)))
    correct_full_works = [[elem[i] for i in [0, 2, 3, 4, 6, 7, 8]] for elem in full_works]
    close_database(conn)
    return uhtml.universal_table(config.works_table_name, config.works_table, correct_full_works)


@app.route("/all-works")
def all_works():
    return work_to_equip('0')


if __name__ == "__main__":
    app.run(host='0.0.0.0')