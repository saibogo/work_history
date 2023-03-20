"""This module implement any web-pages from work to workpoints"""
from flask import render_template

import wh_app.config_and_backup.table_headers
import wh_app.web.template as web_template
import wh_app.web.universal_html as uhtml
from wh_app.postgresql.database import Database
from wh_app.sql_operations import insert_operations
from wh_app.sql_operations import select_operations
from wh_app.sql_operations import update_operations
from wh_app.supporting import functions
from wh_app.config_and_backup import table_headers

functions.info_string(__name__)




def create_edit_links(point_id: str) -> str:
    """Create EDIT and ON-OFF links"""
    return '<a href="/edit-point/{0}">{1}</a> <a href="/on-off-point/{0}">{2}</a>'. \
        format(point_id, uhtml.EDIT_CHAR, uhtml.ON_OFF_CHAR)


def create_tech_links(point_id: str) -> str:
    """Create technical info links"""
    return '<a href="/tech-info/{0}">{1}</a> <a href="/svu/{0}">{2}</a>'. \
        format(point_id, uhtml.PAPERS_CHAR, uhtml.SVU_CHAR)


def points_operations(stylesheet_number: str) -> str:
    """Create main page in points-section"""
    name = 'Действия с предприятиями:'
    menu = [(1, 'Все предприятия'),
            (2, 'Только действующие'),
            (3, 'Добавить предприятие')]
    links_list = ['/all-points', '/works-points', '/create-new-point']
    table = uhtml.universal_table(name, ['№', 'Доступное действие'], menu, True, links_list)
    return web_template.result_page(table, '/', str(stylesheet_number))


def all_points_table(stylesheet_number: str) -> str:
    """Create page, contain all works points"""
    with Database() as base:
        _, cursor = base
        all_points = select_operations.get_all_points(cursor)
        links_list = ['/equip/' + str(elem[0]) for elem in all_points]
        rows = [[point[i] for i in range(1, len(point))] for point in all_points]
        for row_num, row in enumerate(rows):
            rows[row_num].append(create_edit_links(all_points[row_num][0]))
            rows[row_num].append(create_tech_links(all_points[row_num][0]))

        table1 =  uhtml.universal_table(table_headers.points_table_name,
                                        table_headers.points_table,
                                        rows,
                                        True, links_list)
        table2 = uhtml.add_new_point()
        return web_template.result_page(table1 + table2, '/points', str(stylesheet_number))


def create_new_point_page(stylesheet_number: str) -> str:
    """Create page to append new works point in database"""
    html = uhtml.style_custom(str(stylesheet_number)) + '\n' + uhtml.add_new_point()
    return web_template.result_page(html, '/points', str(stylesheet_number))


def add_point_method(data, method, stylesheet_number: str) -> str:
    """Method append new works point in database"""
    pre_adr = '/all-points'
    if method == "POST":
        point_name = data[uhtml.POINT_NAME]
        point_adr = data[uhtml.POINT_ADDRESS]
        password = data[uhtml.PASSWORD]
        if functions.is_valid_password(password):
            if point_name.replace(" ", '') == '' or point_adr.replace(" ", '') == '':
                page = uhtml.data_is_not_valid()
            else:
                with Database() as base:
                    connection, cursor = base
                    insert_operations.create_new_point(cursor, point_name, point_adr)
                    connection.commit()
                    page = uhtml.operation_completed()
        else:
            page = uhtml.pass_is_not_valid()

    else:
        page = "Method in add Point not corrected!"

    return web_template.result_page(page, pre_adr, str(stylesheet_number))


def all_works_points_table(stylesheet_number: str) -> str:
    """Return only points have status WORK"""

    with Database() as base:
        _, cursor = base
        all_points = select_operations.get_all_works_points(cursor)
        links_list = ['/equip/' + str(elem[0]) for elem in all_points]
        rows = [[point[i] for i in range(1, len(point))] for point in all_points]
        for row_num, row in enumerate(rows):
            rows[row_num].append(create_edit_links(all_points[row_num][0]))
            rows[row_num].append(create_tech_links(all_points[row_num][0]))
        table1 =  uhtml.universal_table(table_headers.points_table_name,
                                        table_headers.points_table,
                                        rows,
                                        True, links_list)
        table2 = uhtml.add_new_point()
        return web_template.result_page(table1 + table2, '/points', str(stylesheet_number))


def edit_point_method(point_id: str, stylesheet_number: str):
    """Return page editable selected point"""

    with Database() as base:
        _, cursor = base
        point = select_operations.get_full_point_information(cursor, point_id)
        point.insert(0, point_id)
        return web_template.result_page(uhtml.edit_point_information(point),
                                        '/points',
                                        str(stylesheet_number))


def on_off_point_method(point_id: str, stylesheet_number: str) -> str:
    """Return page for on-off select"""

    with Database() as base:
        _, cursor = base
        point = select_operations.get_full_point_information(cursor, point_id)
        point.insert(0, point_id)
        return web_template.result_page(uhtml.on_off_point_table(point),
                                        '/points',
                                        str(stylesheet_number))


def invert_point_status_method(data, method, stylesheet_number: str) -> str:
    """ON/OFF works point in database"""
    pre_adr = '/all-points'
    if method == 'POST':
        point_id = data[uhtml.POINT_ID]
        password = data[uhtml.PASSWORD]
        if functions.is_superuser_password(password):
            with Database() as base:
                connection, cursor = base
                update_operations.invert_point_is_work(cursor, point_id)
                connection.commit()
                page = uhtml.operation_completed()
        else:
            page = uhtml.pass_is_not_valid()
    else:
        page = "Method in Invert Points Status not corrected!"
    return web_template.result_page(page, pre_adr, str(stylesheet_number))


def upgrade_point_method(data, method, stylesheet_number: str) -> str:
    """Upgrade data from works point in database"""
    pre_adr = '/all-points'
    if method == "POST":
        point_name = data[uhtml.POINT_NAME]
        point_adr = data[uhtml.POINT_ADDRESS]
        point_id = data[uhtml.POINT_ID]
        password = data[uhtml.PASSWORD]
        if functions.is_superuser_password(password):
            if point_name.replace(" ", '') == '' or point_adr.replace(" ", '') == '':
                page = uhtml.data_is_not_valid()
            else:
                with Database() as base:
                    connection, cursor = base
                    update_operations.update_point_information(cursor,
                                                               point_id,
                                                               point_name,
                                                               point_adr)
                    connection.commit()
                    page = uhtml.operation_completed()
        else:
            page = uhtml.pass_is_not_valid()
    else:
        page = "Method in Edit Point not corrected!"
    return web_template.result_page(page, pre_adr, str(stylesheet_number))


def point_tech_info(point_num: int, stylesheet_number: str) -> str:
    """Create page contain all technical information from current point"""

    def if_tech_list_empthy(lst: list) -> list:
        """Replace data if data not found"""

        if not lst:
            return ["Нет данных"] * 4
        else:
            return lst[0]

    with Database() as base:
        _, cursor = base
        dogovors = list()
        table_header = wh_app.config_and_backup.table_headers.point_tech_table
        point_name = select_operations.get_full_point_information(cursor, str(point_num))[0]

        list_info = [select_operations.get_electric_point_info(cursor, str(point_num)),
                     select_operations.get_cold_water_point_info(cursor, str(point_num)),
                     select_operations.get_hot_water_point_info(cursor, str(point_num)),
                     select_operations.get_heating_point_info(cursor, str(point_num)),
                     select_operations.get_sewerage_point_info(cursor, str(point_num))]

        for i in range(1, len(table_header)):
            info = if_tech_list_empthy(list_info[i - 1])
            dogovors.append([table_header[i], info[2], info[3]])

        tmp = render_template('point_tech_info.html', point_name=point_name, parameters=dogovors)
        result = web_template.result_page(tmp,
                                          '/points',
                                          str(stylesheet_number),
                                          True,
                                          'point-tech={0}'.format(point_num))

    return result
