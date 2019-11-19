from flask import Flask, request
from flask import send_from_directory

import select_operations
import insert_operations
import web.universal_html as uhtml
import config
import functions
from database import Database


app = Flask(__name__, static_folder=config.static_dir)
functions.info_string(__name__)


@app.route("/")
def hello():
    name = "Доступные действия в базе ремонтов Малахит-Екатеринбург"
    menu = [(1, 'Операции с предприятиями'), (2, 'Операции с оборудованием'), (3, 'Операции с ремонтами')]
    links_list = ['/points', '/equips', '/works']
    return uhtml.universal_table(name, ['№', 'выполнить:'], menu, True, links_list)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(config.static_dir, 'favicon.ico')


@app.route("/equips")
def equips_operations():
    name = 'Действия с оборудованием'
    menu = [(1, 'Все зарегестрированное оборудование'), (2, 'Поиск по ID')]
    links_list = ['/all-equips', '/find-equip-to-id']
    table = uhtml.universal_table(name, ['№', 'Доступное действие'], menu, True, links_list)
    return table + '\n' + uhtml.navigations_menu(config.full_address + '/')


@app.route("/points")
def points_operations():
    name = 'Действия с предприятиями'
    menu = [(1, 'Все зарегестрированные предприятия'), (2, 'Добавить предприятие')]
    links_list = ['/all-points', '/create_new_point']
    table = uhtml.universal_table(name, ['№', 'Доступное действие'], menu, True, links_list)
    return table + '\n' + uhtml.navigations_menu(config.full_address + '/')


@app.route("/all-points")
def all_points_table():
    with Database() as base:
        connection, cursor = base
        all_points = select_operations.get_all_points(cursor)
        links_list = ['/equip/' + str(elem[0]) for elem in all_points]
        table1 =  uhtml.universal_table(config.points_table_name,
                                        config.points_table,
                                        [[point[i] for i in range(1, len(point))] for point in all_points],
                                        True, links_list)
        table2 = uhtml.add_new_point()
        return table1 + '\n' + table2 + '\n' + uhtml.navigations_menu(config.full_address + '/points')


@app.route("/create_new_point")
def create_new_point():
    html = uhtml.style_custom() + '\n' + uhtml.add_new_point()
    return html + '\n' + uhtml.navigations_menu(config.full_address + '/points')


@app.route('/add-point', methods=['POST'])
def add_point():
    navigation = uhtml.navigations_menu(config.full_address + "/all-points")
    if request.method == "POST":
        data = functions.form_to_data(request.form)
        point_name = data['point_name'].replace('"', '\'')
        point_adr = data['point_addres'].replace('"', '\'')
        password = data["password"]
        if functions.is_valid_password(password):
            if point_name.replace(" ", '') == '' or point_adr.replace(" ", '') == '':
                return uhtml.data_is_not_valid() + '\n' + navigation
            else:
                with Database() as base:
                    connection, cursor = base
                    insert_operations.create_new_point(cursor, point_name, point_adr)
                    select_operations.commit(connection)
                    return uhtml.operation_completed() + '\n' + navigation
        else:
            return uhtml.pass_is_not_valid() + '\n' + navigation

    else:
        return "Method not correct!" + uhtml.navigations_menu(config.full_address + '/all-points')


@app.route("/equip/<point_id>")
def equip_to_point(point_id):
    with Database() as base:
        connection, cursor = base
        all_equips = select_operations.get_equip_in_point(cursor, str(point_id))
        links_list = ['/work/' + str(equip[0]) for equip in all_equips]
        table1 = uhtml.universal_table(config.equips_table_name,
                                       config.equips_table,
                                       [[equip[i] for i in range(1, len(equip))] for equip in all_equips],
                                       True, links_list)
        table2 = uhtml.add_new_equip(point_id)
        return (table1 + '\n' + table2 if point_id != '0' else table1) + '\n' +\
               uhtml.navigations_menu(config.full_address + '/all-points')


@app.route('/find-equip-to-id')
def find_equip_to_id():
    with Database() as base:
        connection, cursor = base
        max_equip_id = select_operations.get_maximal_equip_id(cursor)
        find_table = list()
        find_table.append(uhtml.style_custom())
        find_table.append('<table><caption>Поиск оборудования по уникальному ID</caption>')
        find_table.append('<form action="/select-equip-to-id" method="post">')
        find_table.append('<tr><td><input type="number" name="id" min="0" max="' + max_equip_id + '"></td></tr>')
        find_table.append('<tr><td><input type="submit" value="Найти"></td></tr>')
        return "\n".join(find_table) + '\n' + uhtml.navigations_menu(config.full_address + '/equips')


@app.route("/all-equips")
def all_equips_table():
    return equip_to_point('0')


@app.route("/select-equip-to-id", methods=['POST'])
def select_equip_to_id():
    if request.method == "POST":
        data = functions.form_to_data(request.form)
        equip_id = data['id']
        if equip_id == '0':
            return all_equips_table()
        with Database() as base:
            connection, cursor = base
            equip = select_operations.get_full_equip_information(cursor, str(equip_id))
            links_list = ['/work/' + str(equip_id)]
            correct_full_equip = [[equip[i] for i in [0, 2, 3, 4, 5]]]
            table1 = uhtml.universal_table(config.equips_table_name, config.equips_table, correct_full_equip, True,
                                           links_list)
            return table1 + '\n' + uhtml.navigations_menu(config.full_address + '/equips')
    else:
        return "Method not correct!" + '\n' + uhtml.navigations_menu(config.full_address + '/equips')


@app.route("/add-equip", methods=['POST'])
def add_equip():
    if request.method == "POST":
        data = functions.form_to_data(request.form)
        point_id = data['point_id']
        equip_name = data['equip_name'].replace('"', '\'')
        model = data['model'].replace('"', '\'')
        serial_num = data['serial_num'].replace('"', '\'')
        pre_id = data['pre_id'].replace('"', '\'')
        password = data["password"]
        navigation = uhtml.navigations_menu(config.full_address + '/equip/' + str(point_id))
        if functions.is_valid_password(password):
            with Database() as base:
                connection, cursor = base
                if equip_name.replace(" ", '') == '':
                    return uhtml.data_is_not_valid()
                elif model == '':
                    insert_operations.create_new_equip(cursor, point_id, equip_name)
                elif serial_num == '':
                    insert_operations.create_new_equip(cursor, point_id, equip_name, model)
                elif pre_id == '':
                    insert_operations.create_new_equip(cursor, point_id, equip_name, model, serial_num)
                else:
                    insert_operations.create_new_equip(cursor, point_id, equip_name, model, serial_num, pre_id)
                connection.commit()
                return uhtml.operation_completed() + '\n' + navigation
        else:
            return uhtml.pass_is_not_valid() + '\n' + navigation

    else:
        return "Method not correct!" + '\n' + uhtml.navigations_menu(config.full_address + '/all-points')


@app.route("/works")
def works_operations():
    name = 'Действия с ремонтами и диагностиками'
    menu = [(1, 'Все зарегистрированные работы')]
    links_list = ['/all-works']
    table = uhtml.universal_table(name, ['№', 'Доступное действие'], menu, True, links_list)
    return table + '\n' + uhtml.navigations_menu(config.full_address + '/')


@app.route("/work/<equip_id>")
def work_to_equip(equip_id):
    with Database() as base:
        connection, cursor = base
        navigation = uhtml.navigations_menu(config.full_address + '/equip/' +
                                            str(select_operations.get_point_id_from_equip_id(cursor, equip_id))) if \
            str(equip_id) != '0' else uhtml.navigations_menu(config.full_address + '/works')
        full_works = select_operations.get_works_from_equip_id(cursor, equip_id)
        table1 = uhtml.universal_table(config.works_table_name,
                                       config.works_table,
                                       full_works)
        table2 = uhtml.add_new_work(equip_id)
        return ((table1 + '\n' + table2) if str(equip_id) != '0' else table1) + '\n' + navigation


@app.route("/all-works")
def all_works():
    return work_to_equip('0')


@app.route("/add-work", methods=['POST'])
def add_work():
    if request.method == "POST":
        data = functions.form_to_data(request.form)
        password = data['password']
        equip_id = data['equip_id']
        query = data['query'].replace('"', '\'')
        work = data['work'].replace('"', '\'')
        work_datetime = data['work_datetime'].replace("T", ' ') + ':00'
        navigation = uhtml.navigations_menu(config.full_address + '/work/' + str(equip_id))
        if functions.is_valid_password(password):
            if work.replace(" ", "") == '':
                return uhtml.data_is_not_valid() + '\n' + navigation
            else:
                with Database() as base:
                    connection, cursor = base
                    insert_operations.create_new_work(cursor, equip_id, work_datetime, query, work)
                    connection.commit()
                    return uhtml.operation_completed() + '\n' + navigation
        else:
            return uhtml.pass_is_not_valid() + '\n' + navigation

    else:
        return "Method not correct!" + uhtml.navigations_menu(config.full_address + '/')


@app.route("/FAQ", methods=['GET'])
def faq():
    with Database() as base:
        connection, cursor = base
        page = list()
        page.append(uhtml.style_custom())
        page.append('<table><caption>Наиболее частые вопросы по системе:</caption><tr><td>')
        page.append('<ul>')
        page.append('<li>Что нужно для использования системы?'+\
                    uhtml.list_to_ul(['Компьютер во внутренней сети компании Малахит',
                                      'Браузер с поддержкой технологии ' +
                                      '<a href="https://www.w3.org/Style/CSS/Overview.en.html">CSS</a>']) + '</li>')
        page.append('<li>С использованием каких технологий написана система?' +\
                    uhtml.list_to_ul(['Используется база данных <a href="https://www.postgresql.org/"> PostgreSQL</a>',
                                      'Используется веб-сервер ' +
                                      '<a href="https://flask.palletsprojects.com/en/1.0.x/changelog/">Flask</a>',
                                      'Используется язык программирования ' +
                                      '<a href="https://www.python.org/">Python3</a>',
                                      'Для клиентского приложения использована связка ' +
                                      '<a href="https://www.python.org/">Python3</a> + ' +
                                      '<a href="https://docs.python.org/3/library/tk.html">tkinter</a>']) + '</li>')
        page.append('<li>Сколько пользователей поддерживает система?' +\
                    uhtml.list_to_ul(['Структура базы данных поддерживает только одного исполнителя',
                                      'Одновременно над добавлением записей может работать неограниченное количество' +\
                                      ' пользователей, но все они будут использовать одну учетную запись']) + '</li>')
        page.append('<li>Планируется ли развитие системы?' +\
                    uhtml.list_to_ul(['Планируется процедура автоматического бэкапа PostgreSQL-базы',
                                      'Планируется изменение структуры базы данных и внедрение многопользовательского' +\
                                      ' режима', 'Планируется внедрение системы поиска по записям',
                                      'В планах внедрение возможности редактирования записей']) + '</li>')
        max_equip_id = select_operations.get_maximal_equip_id(cursor)
        max_point_id = select_operations.get_maximal_points_id(cursor)
        max_work_id = select_operations.get_maximal_work_id(cursor)
        page.append('<li>Сколько записей зарегистрированно на данный момент?' +\
                    uhtml.list_to_ul(['Единиц или групп оборудования: <a href="' + config.full_address + '/all-equips">' +
                                      str(max_equip_id) + '</a>',
                                      'Предприятий: <a href="' + config.full_address + '/all-points">' +
                                      str(max_point_id) + '</a>',
                                      'Произведенных работ: <a href="' + config.full_address + '/all-works">' +
                                      str(max_work_id) + '</a>']) + '</li>')
        page.append('<li>Текущий размер базы данных?: ' + str(select_operations.get_size_database(cursor)) + '</li>')
        page.append('</ul></td></tr></table>')
        preview_page = request.args.get('page', default=config.full_address, type=str)
        page.append(uhtml.navigations_menu(preview_page))
        result = ''.join(page)
        return result


@app.route('/find')
def find_page():
    return uhtml.find_table()


@app.route('/findresult', methods=['POST'])
def find_from_works():
    if request.method == "POST":
        data = functions.form_to_data(request.form)
        find_request = data['find_request']
        with Database() as base:
            connection, cursor = base
            find_from_table = data['find_in_table']
            if find_from_table == 'works_ignored_date':
                works = select_operations.get_all_works_like_word(cursor, find_request)
                result = uhtml.universal_table(config.works_table_name,
                                               config.works_table,
                                               [list(work) for work in works])
                return result + uhtml.navigations_menu('/works')
            elif find_from_table == 'works':
                date_start = data['work_datetime_start']
                date_stop = data['work_datetime_stop']
                works = select_operations.get_all_works_like_word_and_date(cursor, find_request, date_start, date_stop)
                result = uhtml.universal_table(config.works_table_name,
                                               config.works_table,
                                               [list(work) for work in works])
                return result + uhtml.navigations_menu('/works')
            elif find_from_table == 'workspoints':
                points = select_operations.get_all_points_list_from_like_str(cursor, find_request)
                links_list = ['/equip/' + str(elem[0]) for elem in points]
                result = uhtml.universal_table(config.points_table_name,
                                               config.points_table,
                                               [[point[1], point[2]] for point in points],
                                               True,
                                               links_list)
                return result + uhtml.navigations_menu('/points')
            elif find_from_table == 'oborudovanie':
                equips = select_operations.get_all_equips_list_from_like_str(cursor, find_request)
                links_list = ['/work/' + str(equip[0]) for equip in equips]
                result = uhtml.universal_table(config.equips_table_name,
                                               config.equips_table,
                                               [[equip[i] for i in range(1, len(equip))] for equip in equips],
                                               True,
                                               links_list)
                return result + uhtml.navigations_menu('/equips')
            else:
                return 'Not corrected selected!'
    else:
        return "Method not correct!" + uhtml.navigations_menu(config.full_address + '/')


@app.route('/statistics')
def statistics_page():
    with Database() as base:
        connection, cursor = base
        statistics = select_operations.get_statistic(cursor)
        links_list = ['/equip/' + str(elem[0]) for elem in statistics]
        result = uhtml.universal_table(config.statistics_table_name,
                                       config.statistics_table,
                                       [[elem[i] for i in range(1, len(elem))] for elem in statistics],
                                       True,
                                       links_list)
        return result + uhtml.navigations_menu('/points')


def start_server():
    app.run(host='0.0.0.0')


if __name__ == "__main__":
    start_server()