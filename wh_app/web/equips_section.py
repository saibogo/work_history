from flask import redirect

import wh_app.web.template as web_template
import wh_app.web.universal_html as uhtml
from wh_app.postgresql.database import Database
from wh_app.sql_operations import insert_operations
from wh_app.sql_operations import select_operations
from wh_app.supporting import functions
from wh_app.config_and_backup import table_headers

functions.info_string(__name__)


def equips_menu():
    name = 'Действия с оборудованием'
    menu = [(1, 'Все зарегестрированное оборудование'), (2, 'Поиск по ID')]
    links_list = ['/all-equips', '/find-equip-to-id']
    table = uhtml.universal_table(name, ['№', 'Доступное действие'], menu, True, links_list)
    return web_template.result_page(table, '/')


def equip_to_point_limit(point_id, page_num):
    with Database() as base:
        connection, cursor = base
        all_equips = select_operations.get_equip_in_point_limit(cursor, point_id, page_num)
        links_list = ['/work/{}'.format(equip[0]) for equip in all_equips]
        table1 = uhtml.universal_table(table_headers.equips_table_name,
                                       table_headers.equips_table,
                                       [[equip[i] for i in range(1, len(equip))] for equip in all_equips],
                                       True, links_list)
        pages = uhtml.paging_table("/equip/{0}/page".format(point_id),
                                   functions.list_of_pages(select_operations.get_equip_in_point(cursor,
                                                                                                str(point_id))),
                                   int(page_num))
        table2 = uhtml.add_new_equip(point_id) if point_id != '0' else ""
        return web_template.result_page(table1 + pages + table2, '/all-points')


def find_equip_to_id_page():
    with Database() as base:
        connection, cursor = base
        max_equip_id = select_operations.get_maximal_equip_id(cursor)
        find_table = list()
        find_table.append('<table><caption>Поиск оборудования по уникальному ID</caption>')
        find_table.append('<form action="/select-equip-to-id" method="post">')
        find_table.append('<tr><td><input type="number" name="id" min="0" max="' + max_equip_id + '"></td></tr>')
        find_table.append('<tr><td><input type="submit" value="Найти"></td></tr>')
        return web_template.result_page("\n".join(find_table), '/equips')


def select_equip_to_id_page(data, method):
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
            return web_template.result_page(table1, pre_adr)
    else:
        return web_template.result_page("Method in Select Equip not corrected!", pre_adr)


def add_equip_method(data, method):
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
                return web_template.result_page(uhtml.operation_completed(), '/equip/' + str(point_id))
        else:
            return web_template.result_page(uhtml.pass_is_not_valid(), '/equip/' + str(point_id))

    else:
        return web_template.result_page('Method in Add Equip not corrected!', '/all-points')
