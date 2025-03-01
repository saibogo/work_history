"""This module implement any web-pages from work to workpoints"""
from flask import render_template

import wh_app.config_and_backup.table_headers
import wh_app.web.template as web_template
import wh_app.web.universal_html as uhtml
from wh_app.postgresql.database import Database
from wh_app.sql_operations import insert_operations
from wh_app.sql_operations.select_operations import select_operations
from wh_app.sql_operations import update_operations
from wh_app.supporting import functions
from wh_app.config_and_backup import table_headers, config

functions.info_string(__name__)


def create_edit_links(point_id: str) -> str:
    """Create EDIT and ON-OFF links"""
    return '<a href="/edit-point/{0}" title="Редактировать сведения">{1}</a>' \
           ' <a href="/on-off-point/{0}" title="Изменить статус">{2}</a>' \
           ' <a href="/edit-bindings/{0}" title="Редактировать привязки сотрудников">{3}</a>'. \
        format(point_id, uhtml.EDIT_CHAR, uhtml.ON_OFF_CHAR, uhtml.BINDING_CHAR)


def create_tech_links(point_id: str) -> str:
    """Create technical info links"""
    return '<a href="/tech-info/{0}">{1}</a> <a href="/svu/{0}">{2}</a>'. \
        format(point_id, uhtml.PAPERS_CHAR, uhtml.SVU_CHAR) + create_meter_links(point_id)


def create_meter_links(point_id: str) -> str:
    """Create link to meter devices"""
    return '<a href="/meters-in-point/{0}" title = "Перечень приборов учета">{1}</a>'.format(point_id, uhtml.METER_CHAR)


def points_operations(stylesheet_number: str) -> str:
    """Create main page in points-section"""
    name = 'Действия с предприятиями:'
    menu = ['Все предприятия', 'Только действующие', 'Добавить предприятие', 'TOP-10 по количеству ремонтов']
    links_list = ['/all-points', '/works-points', '/create-new-point', '/top-10-points']
    table = uhtml.universal_table(name, ['№', 'Доступное действие'], functions.list_to_numer_list(menu), True, links_list)
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


def create_bindings_form(point_num: str, stylesheet_number: str) -> str:
    """Create form to add or delete bindings in point"""
    with Database() as base:
        _, cursor = base
        point_info = select_operations.get_full_point_information(cursor, point_num)
        workers = select_operations.get_table_current_workers(cursor)
        current_bindings = select_operations.get_all_bindings_to_point(cursor, point_num)
        bindings_to_html = [[elem[0], elem[1] +" - " + ("основная" if elem[2] else "вторичная")] for elem in current_bindings]
        tmp = render_template('add_or_delete_binding.html', point_id=uhtml.POINT_ID, point_num=point_num,
                              point=point_info, point_name=uhtml.POINT_NAME, worker_id=uhtml.WORKER_ID, workers=workers,
                              type_binding=uhtml.TYPE_BINDINGS, password=uhtml.PASSWORD, binding_id=uhtml.BINDING_ID,
                              current_bindings=bindings_to_html)
    return web_template.result_page(tmp, "/points", stylesheet_number)


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
    links = ['edit-electric', 'edit-cold-water', 'edit-hot-water', 'edit-heating', 'edit-sewerage']
    for i in range(len(links)):
        links[i] = '{}/{}/{}'.format(config.full_address(), links[i], point_num)
    with Database() as base:
        _, cursor = base
        dogovors = list()
        table_header = wh_app.config_and_backup.table_headers.point_tech_table
        point_name = select_operations.get_full_point_information(cursor, str(point_num))[0]
        list_info = functions.get_technical_info(point_num)

        for i in range(1, len(table_header)):
            dogovors.append([table_header[i],
                             list_info[i - 1][2],
                             list_info[i - 1][3],
                             links[i - 1]])

        tmp = render_template('point_tech_info.html', point_name=point_name, parameters=dogovors,
                              edit_char=uhtml.EDIT_CHAR)
        result = web_template.result_page(tmp,
                                          '/points',
                                          str(stylesheet_number),
                                          True,
                                          'point-tech={0}'.format(point_num))

    return result


def edit_tech_section(point_num: int, section: str, stylesheet_number: str) -> str:
    """Create form to edit any section: electric, cold-water, hot-water, heating, sewerage"""

    sections = {"electric": "Электроснабжение", 'cold-water': "Холодное водовснабжение",
                'hot-water': "Горячее водоснабжение", 'heating': "Отопление", 'sewerage': 'Канализация'}
    with Database() as base:
        _, cursor = base
        point_name = select_operations.get_point_name_from_id(cursor, str(point_num))
        list_info = functions.get_technical_info(point_num)
        parameters = list()
        if section == 'electric':
            parameters = list_info[0][2:]
        elif section == 'cold-water':
            parameters = list_info[1][2:]
        elif section == 'hot-water':
            parameters = list_info[2][2:]
        elif section == 'heating':
            parameters = list_info[3][2:]
        else:
            parameters = list_info[4][2:]
        tmp = render_template('edit_tech_section.html', point_name=point_name, section_name=sections[section],
                              parameter=parameters, point_num=point_num, section=section, password=uhtml.PASSWORD)
        return web_template.result_page(tmp, '/tech-info/{}'.format(point_num), str(stylesheet_number))


def edit_point_tech_method(section:str, data, method, stylesheet_number: str) -> str:
    """Edit points tech section in database"""
    pre_adr = '/all-points'
    sections = ["electric", 'cold-water', 'hot-water', 'heating', 'sewerage']
    if method == "POST":
        point_id = data[uhtml.POINT_ID]
        resume = data[uhtml.RESUME]
        dogovor = data[uhtml.DOGOVOR]
        password = data[uhtml.PASSWORD]
        if functions.is_superuser_password(password):
            if resume.replace(" ", '') == '' or dogovor.replace(" ", '') == '':
                page = uhtml.data_is_not_valid()
            else:
                with Database() as base:
                    connection, cursor = base
                    tech_list = functions.get_technical_info(point_id)
                    index = sections.index(section)
                    section_list = tech_list[index]
                    if section_list[0] != functions.NOT_VALUES and section_list[1] != functions.NOT_VALUES:
                        update_operations.update_tech_section(cursor, section, str(point_id), dogovor, resume)
                        connection.commit()
                    else:
                        insert_operations.insert_tech_section(cursor, section, str(point_id), dogovor, resume)
                        connection.commit()
                    page = uhtml.operation_completed()

        else:
            page = uhtml.pass_is_not_valid()

    else:
        page = "Method in add Point not corrected!"

    return web_template.result_page(page, pre_adr, str(stylesheet_number))


def top_10_points_page(stylesheet_number: str) -> str:
    """Create table TOP-10 points with maximal works"""

    with Database() as base:
        _, cursor = base
        points = select_operations.get_top_10_points(cursor)
        lst = [['<a href="/equip/{0}">{1}</a>'.format(row[0], elem)  for elem in row] for row in points]
        page = render_template('universal_table.html', table_name=table_headers.top_10_points_name,
                               num_columns=len(table_headers.top_10_points), headers=table_headers.top_10_points,
                               data=lst)
        return web_template.result_page(page, '/points', stylesheet_number, True, 'top10points')