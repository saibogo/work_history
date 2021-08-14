from flask import redirect

import wh_app.web.template as web_template
import wh_app.web.universal_html as uhtml
from wh_app.postgresql.database import Database
from wh_app.sql_operations import insert_operations
from wh_app.sql_operations import select_operations
from wh_app.sql_operations import update_operations
from wh_app.supporting import functions
from wh_app.config_and_backup import table_headers

functions.info_string(__name__)

EDIT_CHAR = '&#9998'
REMOVE_CHAR = 'A&#8646;B'
TABLE_REMOVE_CHAR = '&#8694'


def equips_menu(stylesheet_number) -> str:
    name = 'Действия с оборудованием'
    menu = [(1, 'Все зарегестрированное оборудование'), (2, 'Поиск по ID')]
    links_list = ['/all-equips', '/find-equip-to-id']
    table = uhtml.universal_table(name, ['№', 'Доступное действие'], menu, True, links_list)
    return web_template.result_page(table, '/', str(stylesheet_number))


def equip_to_point_limit(point_id, page_num, stylesheet_number: str) -> str:
    with Database() as base:
        connection, cursor = base
        all_equips = select_operations.get_equip_in_point_limit(cursor, point_id, page_num)
        links_list = ['/work/{}'.format(equip[0]) for equip in all_equips]
        data = [[equip[i] for i in range(0, len(equip))]  for equip in all_equips]
        for row_num in range(len(data)):
            extended_links = ['<a href="/edit-equip/{0}" title="Редактировать">{1}</a>'.
                                  format(data[row_num][0], EDIT_CHAR) +
                              '&nbsp;' +
                              '<a href="/change-point/{0}" title="Переместить на другой обьект">{1}</a>'.
                                  format(data[row_num][0], REMOVE_CHAR)]
            if data[row_num][0] != data[row_num][5]:
                extended_links[0] += '&nbsp;' + \
                                     '<a href="/remove-table/{0}" title="Таблица перемещений">{1}</a>'.\
                                         format(data[row_num][0], TABLE_REMOVE_CHAR)
            data[row_num] = data[row_num][1:] + extended_links
        table1 = uhtml.universal_table(table_headers.equips_table_name,
                                       table_headers.equips_table,
                                       data,
                                       True, links_list)
        pages = uhtml.paging_table("/equip/{0}/page".format(point_id),
                                   functions.list_of_pages(select_operations.get_equip_in_point(cursor,
                                                                                                str(point_id))),
                                   int(page_num))
        table2 = uhtml.add_new_equip(point_id) if point_id != '0' else ""
        return web_template.result_page(table1 + pages + table2, '/all-points', str(stylesheet_number))


def remove_table_page(equip_id: str, stylesheet_number: str) -> str:
    result = []
    with Database() as base:
        connection, cursor = base
        equip_info = [str(equip_id)]  + select_operations.get_full_equip_information(cursor, str(equip_id))
        result.insert(0,equip_info)
        while str(equip_info[0]) != str(equip_info[5]):
            old_equip_id = str(equip_info[5])
            equip_info = [old_equip_id] + select_operations.get_full_equip_information(cursor, old_equip_id)
            result.insert(0, equip_info)
    links = ['/work/{0}'.format(elem[0]) for elem in result]
    page = uhtml.universal_table(table_headers.remove_table_name, table_headers.remove_table, result, True, links)
    return web_template.result_page(page, "/", str(stylesheet_number))


def edit_equip_method(equip_id: str, stylesheet_number: str) -> str:
    """Return page for edit equips information"""

    with Database() as base:
        connection, cursor = base
        equip = select_operations.get_full_equip_information(cursor, str(equip_id))
        page = uhtml.edit_equip_information([equip_id] + equip)
        return web_template.result_page(page, '/all-equips', str(stylesheet_number))


def select_point_to_equip_method(equip_id: str, stylesheet_number: str) -> str:
    """Create form to select new point to current equip"""

    with Database() as base:
        connection, cursor = base
        equip = select_operations.get_full_equip_information(cursor, str(equip_id))
        point_id = select_operations.get_point_id_from_equip_id(cursor, equip_id)
        equip = [equip_id] + equip
        page = uhtml.select_point_form(equip, point_id)
        return web_template.result_page(page, '/', str(stylesheet_number))


def upgrade_equip_method(data, method, stylesheet_number: str) -> str:
    """Upgrade database if all values is correct and return html-page"""

    pre_adr = '/all-equips'
    if method == "POST":
        equip_name = data[uhtml.EQUIP_NAME]
        equip_id = data[uhtml.EQUIP_ID]
        equip_model = data[uhtml.MODEL]
        equip_number = data[uhtml.SERIAL_NUM]
        equip_pre_id = data[uhtml.PRE_ID]
        password = data[uhtml.PASSWORD]
        if functions.is_superuser_password(password):
            if equip_name.replace(" ", '') == '' :
                return web_template.result_page(uhtml.data_is_not_valid(), pre_adr, str(stylesheet_number))
            else:
                with Database() as base:
                    connection, cursor = base
                    update_operations.update_equip_information(cursor, equip_id, equip_name, equip_model,
                                                               equip_number, equip_pre_id)
                    connection.commit()
                    return web_template.result_page(uhtml.operation_completed(), pre_adr, str(stylesheet_number))
        else:
            return web_template.result_page(uhtml.pass_is_not_valid(), pre_adr, str(stylesheet_number))
    else:
        return web_template.result_page("Method in Edit Point not corrected!", pre_adr, str(stylesheet_number))


def move_equip_method(data, method, stylesheet_number: str) -> str:
    """Move equip to new point"""

    pre_adr = '/'
    if method == 'POST':
        equip_id = data[uhtml.EQUIP_ID]
        point_id = data[uhtml.POINT_ID]
        equip_name = data[uhtml.EQUIP_NAME]
        model = data[uhtml.MODEL]
        serial_num = data[uhtml.SERIAL_NUM]
        pre_id = data[uhtml.PRE_ID]
        new_point_id = data[uhtml.NEW_POINT_ID]
        password = data[uhtml.PASSWORD]
        if functions.is_superuser_password(password):
            if point_id == new_point_id:
                return web_template.result_page(uhtml.data_is_not_valid(), pre_adr, str(stylesheet_number))
            else:
                with Database() as base:
                    connection, cursor = base
                    name_old = select_operations.get_point_name_from_id(cursor, str(point_id))
                    name_new = select_operations.get_point_name_from_id(cursor, str(new_point_id))
                    date_remove = functions.date_to_browser().replace("T", ' ') + ':00'
                    insert_operations.create_new_work(cursor, str(equip_id), date_remove, "Перемещение оборудования",
                                                      "Перемещено из {0} в {1}.".format(name_old, name_new), '1')
                    insert_operations.create_new_equip(cursor, new_point_id, equip_name, model, str(serial_num),
                                                       str(equip_id))
                    connection.commit()
                    return web_template.result_page(uhtml.operation_completed(), pre_adr, str(stylesheet_number))
        else:
            return web_template.result_page(uhtml.pass_is_not_valid(), pre_adr, str(stylesheet_number))
    else:
        return web_template.result_page("Method in Edit Point not corrected!", pre_adr, str(stylesheet_number))


def find_equip_to_id_page(stylesheet_number: str) -> str:
    with Database() as base:
        connection, cursor = base
        max_equip_id = select_operations.get_maximal_equip_id(cursor)
        find_table = list()
        find_table.append('<table><caption>Поиск оборудования по уникальному ID</caption>')
        find_table.append('<form action="/select-equip-to-id" method="post">')
        find_table.append('<tr><td><input type="number" name="id" min="0" max="' + max_equip_id + '"></td></tr>')
        find_table.append('<tr><td><input type="submit" value="Найти"></td></tr>')
        return web_template.result_page("\n".join(find_table), '/equips', str(stylesheet_number))


def select_equip_to_id_page(data, method, stylesheet_number: str) -> str:
    pre_adr = '/equips'
    if method == "POST":
        equip_id = data['id']
        if equip_id == '0':
            return redirect('/all-equips')
        with Database() as base:
            connection, cursor = base
            equip = select_operations.get_full_equip_information(cursor, str(equip_id))
            links_list = ['/work/' + str(equip_id)]
            table1 = uhtml.universal_table(table_headers.equips_table_name,
                                           table_headers.equips_table, [equip], True,
                                           links_list)
            return web_template.result_page(table1, pre_adr, str(stylesheet_number))
    else:
        return web_template.result_page("Method in Select Equip not corrected!", pre_adr, str(stylesheet_number))


def add_equip_method(data, method, stylesheet_number: str) -> str:
    if method == "POST":
        point_id = data[uhtml.POINT_ID]
        equip_name = data[uhtml.EQUIP_NAME]
        model = data[uhtml.MODEL]
        serial_num = data[uhtml.SERIAL_NUM]
        pre_id = data[uhtml.PRE_ID]
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
                return web_template.result_page(uhtml.operation_completed(),
                                                '/equip/' + str(point_id),
                                                str(stylesheet_number))
        else:
            return web_template.result_page(uhtml.pass_is_not_valid(),
                                            '/equip/' + str(point_id),
                                            str(stylesheet_number))

    else:
        return web_template.result_page('Method in Add Equip not corrected!', '/all-points', str(stylesheet_number))
