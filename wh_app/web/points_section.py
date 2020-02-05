import wh_app.web.template as web_template
import wh_app.web.universal_html as uhtml
from wh_app.postgresql.database import Database
from wh_app.sql_operations import insert_operations
from wh_app.sql_operations import select_operations
from wh_app.supporting import functions
from wh_app.config_and_backup import table_headers

functions.info_string(__name__)


def points_operations():
    name = 'Действия с предприятиями'
    menu = [(1, 'Все зарегестрированные предприятия'),
            (2, 'Только действующие'),
            (3, 'Добавить предприятие')]
    links_list = ['/all-points', '/works-points', '/create-new-point']
    table = uhtml.universal_table(name, ['№', 'Доступное действие'], menu, True, links_list)
    return web_template.result_page(table, '/')


def all_points_table():
    with Database() as base:
        connection, cursor = base
        all_points = select_operations.get_all_points(cursor)
        links_list = ['/equip/' + str(elem[0]) for elem in all_points]
        table1 =  uhtml.universal_table(table_headers.points_table_name,
                                        table_headers.points_table,
                                        [[point[i] for i in range(1, len(point))] for point in all_points],
                                        True, links_list)
        table2 = uhtml.add_new_point()
        return web_template.result_page(table1 + table2, '/points')


def create_new_point_page():
    html = uhtml.style_custom() + '\n' + uhtml.add_new_point()
    return web_template.result_page(html, '/points')


def add_point_method(data, method):
    pre_adr = '/all-points'
    if method == "POST":
        point_name = data[uhtml.POINT_NAME]
        point_adr = data[uhtml.POINT_ADDRESS]
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


def all_works_points_table():
    """Return only points have status WORK"""

    with Database() as base:
        connection, cursor = base
        all_points = select_operations.get_all_works_points(cursor)
        links_list = ['/equip/' + str(elem[0]) for elem in all_points]
        table1 =  uhtml.universal_table(table_headers.points_table_name,
                                        table_headers.points_table,
                                        [[point[i] for i in range(1, len(point))] for point in all_points],
                                        True, links_list)
        table2 = uhtml.add_new_point()
        return web_template.result_page(table1 + table2, '/points')