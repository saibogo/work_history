from flask import Flask, request
from flask import send_from_directory

import config
import functions
import insert_operations
import select_operations
import web.template as web_template
import web.universal_html as uhtml
from database import Database

app = Flask(__name__, static_folder=config.static_dir)
functions.info_string(__name__)


@app.route("/")
def hello():
    name = "Доступные действия в базе ремонтов Малахит-Екатеринбург"
    menu = [(1, 'Операции с предприятиями'),
            (2, 'Операции с оборудованием'),
            (3, 'Операции с ремонтами'),
            (4, 'Операции с сотрудниками')]
    links_list = ['/points', '/equips', '/works', '/workers']
    table = uhtml.universal_table(name, ['№', 'выполнить:'], menu, True, links_list)
    return web_template.result_page(table)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(config.static_dir, 'favicon.ico')


@app.route("/equips")
def equips_operations():
    name = 'Действия с оборудованием'
    menu = [(1, 'Все зарегестрированное оборудование'), (2, 'Поиск по ID')]
    links_list = ['/all-equips', '/find-equip-to-id']
    table = uhtml.universal_table(name, ['№', 'Доступное действие'], menu, True, links_list)
    return web_template.result_page(table, '/')


@app.route("/points")
def points_operations():
    name = 'Действия с предприятиями'
    menu = [(1, 'Все зарегестрированные предприятия'), (2, 'Добавить предприятие')]
    links_list = ['/all-points', '/create_new_point']
    table = uhtml.universal_table(name, ['№', 'Доступное действие'], menu, True, links_list)
    return web_template.result_page(table, '/')


@app.route("/workers")
def workers_operations():
    name = 'Действия с сотрудниками'
    menu = [(1, 'Все зарегистрированные сотрудники'), (2, 'Базовый график')]
    links_list = ['/all-workers', '/works-days']
    table = uhtml.universal_table(name, ['№', 'Доступное действие'], menu, True, links_list)
    return web_template.result_page(table, '/')


@app.route("/all-workers")
def all_workers_table():
    with Database() as base:
        connection, cursor = base
        all_workers = select_operations.get_all_workers(cursor)
        links = ['/performer/' + str(elem[0]) for elem in all_workers]
        table = uhtml.universal_table(config.all_workers_table_name,
                                      config.workers_table,
                                      all_workers, True, links)
        return web_template.result_page(table, '/workers')


@app.route("/works-days")
def works_days_page():
    with Database() as base:
        connection, cursor = base
        works_days_list = select_operations.get_works_days_table(cursor)
        alter_works_days = select_operations.get_alter_works_days_table(cursor)
        table = uhtml.universal_table(config.works_days_table_name,
                                      config.works_days_table,
                                      works_days_list)
        table2 = uhtml.universal_table(config.alter_works_days_table_name,
                                       config.alter_works_days_table,
                                       alter_works_days)
        return web_template.result_page(table + uhtml.info_from_alter_works() + table2, '/workers')


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
        return web_template.result_page(table1 + table2, '/points')


@app.route("/create_new_point")
def create_new_point():
    html = uhtml.style_custom() + '\n' + uhtml.add_new_point()
    return web_template.result_page(html, '/points')


@app.route('/add-point', methods=['POST'])
def add_point():
    pre_adr = '/all-points'
    if request.method == "POST":
        data = functions.form_to_data(request.form)
        point_name = data[uhtml.POINT_NAME].replace('"', '\'')
        point_adr = data[uhtml.POINT_ADDRESS].replace('"', '\'')
        password = data[uhtml.PASSWORD]
        if functions.is_valid_password(password):
            if point_name.replace(" ", '') == '' or point_adr.replace(" ", '') == '':
                return web_template.result_page(uhtml.data_is_not_valid(), pre_adr)
            else:
                with Database() as base:
                    connection, cursor = base
                    insert_operations.create_new_point(cursor, point_name, point_adr)
                    connection.commit()
                    return web_template.result_page(uhtml.operation_completed(), pre_adr)
        else:
            return web_template.result_page(uhtml.pass_is_not_valid(), pre_adr)

    else:
        return web_template.result_page("Method in add Point not corrected!", pre_adr)


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
        table2 = uhtml.add_new_equip(point_id) if point_id != '0' else ""
        return web_template.result_page(table1 + table2, '/all-points')


@app.route('/find-equip-to-id')
def find_equip_to_id():
    with Database() as base:
        connection, cursor = base
        max_equip_id = select_operations.get_maximal_equip_id(cursor)
        find_table = list()
        find_table.append('<table><caption>Поиск оборудования по уникальному ID</caption>')
        find_table.append('<form action="/select-equip-to-id" method="post">')
        find_table.append('<tr><td><input type="number" name="id" min="0" max="' + max_equip_id + '"></td></tr>')
        find_table.append('<tr><td><input type="submit" value="Найти"></td></tr>')
        return web_template.result_page("\n".join(find_table), '/equips')


@app.route("/all-equips")
def all_equips_table():
    return equip_to_point('0')


@app.route("/select-equip-to-id", methods=['POST'])
def select_equip_to_id():
    pre_adr = '/equips'
    if request.method == "POST":
        data = functions.form_to_data(request.form)
        equip_id = data['id']
        if equip_id == '0':
            return all_equips_table()
        with Database() as base:
            connection, cursor = base
            equip = select_operations.get_full_equip_information(cursor, str(equip_id))
            links_list = ['/work/' + str(equip_id)]
            table1 = uhtml.universal_table(config.equips_table_name, config.equips_table, [equip], True,
                                           links_list)
            return web_template.result_page(table1, pre_adr)
    else:
        return web_template.result_page("Method in Select Equip not corrected!", pre_adr)


@app.route("/add-equip", methods=['POST'])
def add_equip():
    if request.method == "POST":
        data = functions.form_to_data(request.form)
        point_id = data[uhtml.POINT_ID]
        equip_name = data[uhtml.EQUIP_NAME].replace('"', '\'')
        model = data[uhtml.MODEL].replace('"', '\'')
        serial_num = data[uhtml.SERIAL_NUM].replace('"', '\'')
        pre_id = data[uhtml.PRE_ID].replace('"', '\'')
        password = data[uhtml.PASSWORD]
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
                return web_template.result_page(uhtml.operation_completed(), '/equip/' + str(point_id))
        else:
            return web_template.result_page(uhtml.pass_is_not_valid(), '/equip/' + str(point_id))

    else:
        return web_template.result_page('Method in Add Equip not corrected!', '/all-points')


@app.route("/works")
def works_operations():
    name = 'Действия с ремонтами и диагностиками'
    menu = [(1, 'Все зарегистрированные работы'), (2, 'Поиск работы по ID')]
    links_list = ['/all-works', '/find-work-to-id']
    table = uhtml.universal_table(name, ['№', 'Доступное действие'], menu, True, links_list)
    return web_template.result_page(table, '/')


@app.route('/find-work-to-id')
def find_work_to_id():
    with Database() as base:
        connection, cursor = base
        max_work_id = select_operations.get_maximal_work_id(cursor)
        find_table = list()
        find_table.append('<table><caption>Поиск выполненной работы по уникальному ID</caption>')
        find_table.append('<form action="/select-work-to-id" method="post">')
        find_table.append('<tr><td><input type="number" name="id" min="0" max="' + max_work_id + '"></td></tr>')
        find_table.append('<tr><td><input type="submit" value="Найти"></td></tr>')
        return web_template.result_page("\n".join(find_table), '/works')


@app.route("/select-work-to-id", methods=['POST'])
def select_work_to_id():
    pre_adr = '/works'
    if request.method == "POST":
        data = functions.form_to_data(request.form)
        work_id = data['id']
        if work_id == '0':
            return all_works()
        with Database() as base:
            connection, cursor = base
            work = select_operations.get_full_information_to_work(cursor, str(work_id))
            work = functions.works_table_add_new_performer([work])
            table1 = uhtml.universal_table(config.works_table_name,
                                           config.works_table,
                                           work)
            return web_template.result_page(table1, pre_adr)
    else:
        return web_template.result_page("Method in Select Work not corrected!", pre_adr)


@app.route("/work/<equip_id>")
def work_to_equip(equip_id):
    with Database() as base:
        connection, cursor = base
        pre_adr = ('/equip/' + str(select_operations.get_point_id_from_equip_id(cursor, equip_id))) if\
            str(equip_id) != '0' else '/works'
        full_works = select_operations.get_works_from_equip_id(cursor, equip_id)
        full_works = functions.works_table_add_new_performer(full_works)
        table1 = uhtml.universal_table(config.works_table_name,
                                       config.works_table,
                                       full_works)
        table2 = uhtml.add_new_work(equip_id) if str(equip_id) != 0 else ""
        return web_template.result_page(table1 + table2, pre_adr)


@app.route("/performer/<performer_id>", methods=['GET'])
def works_from_performers(performer_id):
    with Database() as base:
        connection, cursor = base
        pre_adr = request.args.get('page', default=config.full_address, type=str)
        full_works = select_operations.get_all_works_from_worker_id(cursor, performer_id)
        full_works = functions.works_table_add_new_performer(full_works)
        table = uhtml.universal_table(config.works_table_name,
                                      config.works_table,
                                      full_works)
        return web_template.result_page(table, pre_adr)


@app.route("/all-works")
def all_works():
    return work_to_equip('0')


@app.route("/add-work", methods=['POST'])
def add_work():
    if request.method == "POST":
        data = functions.form_to_data(request.form)
        password = data[uhtml.PASSWORD]
        equip_id = data[uhtml.EQUIP_ID]
        query = data[uhtml.QUERY].replace('"', '\'')
        work = data[uhtml.WORK].replace('"', '\'')
        work_datetime = data[uhtml.WORK_DATETIME].replace("T", ' ') + ':00'
        pre_adr = '/work/' + str(equip_id)
        perfomer = data[uhtml.PERFORMER]
        if functions.is_valid_password(password):
            if work.replace(" ", "") == '':
                return web_template.result_page(uhtml.data_is_not_valid(), pre_adr)
            else:
                with Database() as base:
                    connection, cursor = base
                    insert_operations.create_new_work(cursor, equip_id, work_datetime, query, work, perfomer)
                    connection.commit()
                    return web_template.result_page(uhtml.operation_completed(), pre_adr)
        else:
            return web_template.result_page(uhtml.pass_is_not_valid(), pre_adr)
    else:
        return web_template.result_page("Method in Add Work not corrected!", '/')


@app.route("/FAQ", methods=['GET'])
def faq():
    with Database() as base:
        connection, cursor = base
        page = list()
        page.append(uhtml.style_custom())
        page.append('<table><caption>Наиболее частые вопросы по системе:</caption><tr><td>')
        page.append('<ul>')
        page.append('<li>Что нужно для использования системы?'+\
                    web_template.faq_state_machine('hardware') + '</li>')
        page.append('<li>С использованием каких технологий написана система?' +\
                    web_template.faq_state_machine('tecnology') + '</li>')
        page.append('<li>Сколько пользователей поддерживает система?' +\
                    web_template.faq_state_machine('multiuser') + '</li>')
        page.append('<li>Планируется ли развитие системы?' +\
                    web_template.faq_state_machine('update') + '</li>')
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
        page.append('<li>Текущий размер базы данных : ' + str(select_operations.get_size_database(cursor)) + '</li>')
        page.append('<li>Среднее количество работ на смену : ' +
                    str(select_operations.get_count_unique_works(cursor) /
                        select_operations.get_count_unique_dates_in_works(cursor)) + '</li>')
        page.append('</ul></td></tr></table>')
        preview_page = request.args.get('page', default=config.full_address, type=str)
        return web_template.result_page('\n'.join(page), preview_page)


@app.route('/find', methods=['GET'])
def find_page():
    preview_page = request.args.get('page', default=config.full_address, type=str)
    return web_template.result_page(uhtml.find_table(), preview_page)


@app.route('/findresult', methods=['POST'])
def find_from_works():
    if request.method == "POST":
        data = functions.form_to_data(request.form)
        find_request = data[uhtml.FIND_REQUEST]
        with Database() as base:
            connection, cursor = base
            find_from_table = data[uhtml.FIND_IN_TABLE]
            if find_from_table == uhtml.WORKS_IGNORED_DATE:
                works = select_operations.get_all_works_like_word(cursor, find_request)
                works = functions.works_table_add_new_performer(works)
                result = uhtml.universal_table(config.works_table_name,
                                               config.works_table,
                                               [list(work) for work in works])
                return web_template.result_page(result, '/works')

            elif find_from_table == uhtml.WORKS:
                date_start = data[uhtml.WORK_DATETIME_START].replace('T', ' ')
                date_stop = data[uhtml.WORK_DATETIME_STOP].replace('T', ' ')
                works = select_operations.get_all_works_like_word_and_date(cursor, find_request, date_start, date_stop)
                works = functions.works_table_add_new_performer(works)
                result = uhtml.universal_table(config.works_table_name,
                                               config.works_table,
                                               [list(work) for work in works])
                return web_template.result_page(result, '/works')

            elif find_from_table == uhtml.WORKS_POINTS:
                points = select_operations.get_all_points_list_from_like_str(cursor, find_request)
                links_list = ['/equip/' + str(elem[0]) for elem in points]
                result = uhtml.universal_table(config.points_table_name,
                                               config.points_table,
                                               [[point[1], point[2]] for point in points],
                                               True,
                                               links_list)
                return web_template.result_page(result, '/points')

            elif find_from_table == uhtml.EQUIPS:
                equips = select_operations.get_all_equips_list_from_like_str(cursor, find_request)
                links_list = ['/work/' + str(equip[0]) for equip in equips]
                result = uhtml.universal_table(config.equips_table_name,
                                               config.equips_table,
                                               [[equip[i] for i in range(1, len(equip))] for equip in equips],
                                               True,
                                               links_list)
                return web_template.result_page(result, '/equips')

            else:
                return web_template.result_page('Not corrected selected in Find!', '/')

    else:
        return web_template.result_page('Method in Find Page not corrected!', '/')


@app.route('/statistics', methods=['GET'])
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
        preview_page = request.args.get('page', default=config.full_address, type=str)
        return web_template.result_page(result, preview_page)


@app.route("/add-performer-to-work/<work_id>", methods=['GET'])
def add_performer_to_work(work_id):
    with Database() as base:
        connection, cursor = base
        pre_adr = request.args.get('page', default=config.full_address, type=str)
        full_works = [select_operations.get_full_information_to_work(cursor, work_id)]
        full_works = functions.works_table_add_new_performer(full_works)
        table1 = uhtml.add_performer_in_work(full_works)
        return web_template.result_page(table1, pre_adr)


@app.route('/add-performer-result', methods=['POST'])
def add_performer_result():
    if request.method == 'POST':
        data = functions.form_to_data(request.form)
        worker_id = data[uhtml.PERFORMER]
        work_id = data[uhtml.WORK_ID]
        password = data[uhtml.PASSWORD]
        pre_addrr = '/'
        if functions.is_valid_password(password):
            with Database() as base:
                connection, cursor = base
                insert_operations.add_new_performer_in_performers_table(cursor, work_id, worker_id)
                connection.commit()
                return web_template.result_page(uhtml.operation_completed(), pre_addrr)
        else:
            return web_template.result_page(uhtml.pass_is_not_valid(), pre_addrr)
    else:
        return web_template.result_page('Method in Add performer not corrected!', '/')


@app.errorhandler(404)
def page_not_found(error):
    return web_template.result_page(uhtml.html_page_not_found(), '/')


@app.errorhandler(500)
def page_internal_server_error(error):
    return web_template.result_page(uhtml.html_internal_server_error(), '/')


@app.route('/not_found')
def not_found():
    return 'Oops!', 404


def start_server():
    app.run(host='0.0.0.0')


if __name__ == "__main__":
    start_server()