"""This module implement all pages from equip-operations"""
import flask
from flask import render_template, redirect
from os import makedirs

from wh_app.config_and_backup import config
import wh_app.web.template as web_template
import wh_app.web.universal_html as uhtml
from wh_app.postgresql.database import Database
from wh_app.sql_operations import insert_operations
from wh_app.sql_operations.select_operations import select_operations
from wh_app.sql_operations import update_operations
from wh_app.supporting import functions
from wh_app.config_and_backup import table_headers

functions.info_string(__name__)


def create_full_edit_links(equip_id: str, removed: bool=False, deleted: bool=False) -> str:
    """Create EDIT, MOVE and TABLE_REMOVE links"""
    result = list()
    result.append('<a href="/edit-equip/{0}" title="Редактировать">{1}</a>'.format(equip_id, uhtml.EDIT_CHAR))
    if not deleted:
        result.append('<a href="/change-point/{0}" title="Переместить на другой обьект">{1}</a>'.format(equip_id, uhtml.REMOVE_CHAR))
    if removed:
        result.append('<a href="/remove-table/{0}" title="Таблица перемещений">{1}</a>'.format(equip_id, uhtml.TABLE_REMOVE_CHAR))
    with Database() as base:
        _, cursor = base
        try:
            detail_id = select_operations.get_equips_detail_id(cursor, equip_id)[0]
            if detail_id:
                result.append('<a href="/get-details/{0}" title="Получить деталировку">{1}</a>'.format(detail_id, uhtml.DOWNLOAD_CHAR))
        except IndexError:
            pass
    return uhtml.SPACE_CHAR.join(result)


def equips_menu(stylesheet_number) -> str:
    """Method create main EQUIP-page"""
    name = 'Действия с оборудованием'
    menu = ['Все зарегистрированное оборудование', 'Поиск по ID', 'TOP-10 по ремонтам', 'Работа с деталировками']
    links_list = ['/all-equips', '/find-equip-to-id', '/top-10-from-works', '/details-and-subclasses']
    table = uhtml.universal_table(name, ['№', 'Доступное действие'], functions.list_to_numer_list(menu), True, links_list)
    return web_template.result_page(table, '/', str(stylesheet_number))


def details_main_menu(stylesheet_number) -> str:
    """Create equip`s detail main menu"""
    name = 'Подклассы оборудования и деталировки'
    menu = ['Существующие классы и подклассы оборудования', 'Создать подкласс', 'Загрузить деталировку']
    links_list = ['/current-subclasses', '/create-subclass', '/create-details']
    table = uhtml.universal_table(name, ['№', 'Доступное действие'], functions.list_to_numer_list(menu), True,
                                  links_list)
    return web_template.result_page(table, '/', str(stylesheet_number))


def current_subtypes_table(stylesheet_number) -> str:
    """Create table with all exists equip subtypes"""
    with Database() as base:
        _, cursor = base
        all_sub_types = select_operations.get_all_equips_subtypes(cursor)
        result_types = []
        for subtype in all_sub_types:
            result_types.append([])
            for elem in subtype:
                result_types[-1].append('<a href="/all-details-from-type/{0}">{1}</a>'.format(subtype[0], elem))
        page = render_template('any/universal_table.html', num_columns=len(table_headers.equip_types),
                               table_name=table_headers.equip_types_name, headers=table_headers.equip_types, data=result_types)
        return web_template.result_page(page, '/details-and-subclasses', stylesheet_number)


def all_exist_details_table(type_id: int, stylesheet_number: str) -> str:
    """Create table with all details from """
    with Database() as base:
        _, cursor = base
        all_details = select_operations.get_all_details_from_subtype_id(cursor, type_id)
        result = []
        for detail in all_details:
            result.append([])
            link = '<a href="/get-details/{0}" title="Получить деталировку">{1}</a>'
            for elem in detail:
                result[-1].append(link.format(detail[0], elem))
        page = uhtml.universal_table(table_headers.exist_detail_name, table_headers.exist_detail, result)
        pre_adr = '/current-subclasses'
        return web_template.result_page(page, pre_adr, stylesheet_number)


def create_equip_subclass_form(stylesheet_number: str) -> str:
    """Create form to create new equip subclass"""

    with Database() as base:
        _, cursor = base
        pre_adr = '/details-and-subclasses'
        all_meta_classes = select_operations.get_all_equips_meta_type(cursor)
        page = render_template('equip/create_subtype_form.html', meta_class_name=uhtml.EQUIP_META_CLASS,
                               meta_classes=all_meta_classes, equip_class_name=uhtml.EQUIP_CLASS,
                               equip_folder_name=uhtml.EQUIPS_TYPE_DIR, equip_description_name=uhtml.DESCRIPTION,
                               password=uhtml.PASSWORD)
        return web_template.result_page(page, pre_adr,stylesheet_number)


def create_equip_subtype_method(data, method, stylesheet_number: str) -> str:
    """Analize data and create new subtype if all correct"""
    pre_adr = '/details-and-subclasses'
    if method == 'POST':
        if functions.is_superuser_password(data[uhtml.PASSWORD]):
            with Database() as base:
                connection, cursor = base
                all_types_exist = select_operations.get_all_equips_subtypes(cursor)
                new_type = data[uhtml.EQUIP_CLASS]
                new_folder = data[uhtml.EQUIPS_TYPE_DIR]
                description = data[uhtml.DESCRIPTION]
                meta_class = data[uhtml.EQUIP_META_CLASS]
                not_exist = True
                for elem in all_types_exist:
                    not_exist = not_exist and (new_type != elem[2]) and (new_folder != elem[3]) and (description != elem[4])
                if not_exist:
                    path = '{}equips/{}/{}'.format(config.static_dir(), meta_class, new_folder)
                    print(path)
                    try:
                        makedirs(path)
                        insert_operations.insert_new_equip_subclass(cursor, meta_class, new_type, new_folder, description)
                        connection.commit()
                        page = uhtml.operation_completed()
                    except FileExistsError:
                        page = '<h2>Такая директория уже существует!</h2>'
                    except PermissionError:
                        page = '<h2>Недостаточно прав для создания директории!</h2>'
                else:
                    page = '<h2>Как минимум один из параметров нового класса уже зарегистрирован в системе! Проверьте данные!</h2>'
        else:
            page = uhtml.pass_is_not_valid()
    else:
        page = '<h2>Method in Add new equips subtype is not correct!</h2>'
    return web_template.result_page(page, pre_adr, stylesheet_number)


def equip_to_point_limit(point_id, page_num, stylesheet_number: str) -> str:
    """Method create table contain equips. Use limit view on page"""
    with Database() as base:
        _, cursor = base
        all_equips = select_operations.get_equip_in_point_limit(cursor, point_id, page_num)
        links_list = ['/work/{}'.format(equip[0]) for equip in all_equips]
        data = [[equip[i] for i in range(0, len(equip))] for equip in all_equips]
        for i, row in enumerate(data):
            extended_links = [create_full_edit_links(row[0], row[0] != row[5])]
            data[i] = row[1:] + extended_links
        table1 = uhtml.universal_table(table_headers.equips_table_name,
                                       table_headers.equips_table,
                                       data,
                                       True, links_list)
        pages = uhtml.paging_table("/equip/{0}/page".format(point_id),
                                   functions.
                                   list_of_pages(select_operations.
                                                 get_equip_in_point(cursor,
                                                                    str(point_id))),
                                   int(page_num))
        table2 = uhtml.add_new_equip(point_id) if point_id != '0' else ""
        return web_template.result_page(table1 + pages + table2,
                                        '/all-points',
                                        str(stylesheet_number),
                                        True,
                                        'point={0}'.format(point_id))


def remove_table_page(equip_id: str, stylesheet_number: str) -> str:
    """Method create table for all moving equip"""
    result = []
    with Database() as base:
        _, cursor = base
        equip_info = [str(equip_id)] +\
                     select_operations.get_full_equip_information(cursor, str(equip_id))
        result.insert(0, equip_info)
        while str(equip_info[0]) != str(equip_info[5]):
            old_equip_id = str(equip_info[5])
            equip_info = [old_equip_id] +\
                         select_operations.get_full_equip_information(cursor, old_equip_id)
            result.insert(0, equip_info + [''])
        result[-1].append(create_full_edit_links(equip_id))
    links = ['/work/{0}'.format(elem[0]) for elem in result]
    page = uhtml.universal_table(table_headers.remove_table_name,
                                 table_headers.remove_table,
                                 result,
                                 True,
                                 links)
    return web_template.result_page(page, "/", str(stylesheet_number), True, 'move-equip-pdf={0}'.format(equip_id))


def edit_equip_method(equip_id: str, stylesheet_number: str) -> str:
    """Return page for edit equips information"""

    with Database() as base:
        _, cursor = base
        equip = select_operations.get_full_equip_information(cursor, str(equip_id))
        page = uhtml.edit_equip_information([equip_id] + equip)
        return web_template.result_page(page, '/all-equips', str(stylesheet_number))


def select_point_to_equip_method(equip_id: str, stylesheet_number: str) -> str:
    """Create form to select new point to curent equip"""

    with Database() as base:
        _, cursor = base
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
            if equip_name.replace(" ", '') == '':
                page = uhtml.data_is_not_valid()
            else:
                with Database() as base:
                    connection, cursor = base
                    update_operations.update_equip_information(cursor,
                                                               equip_id,
                                                               equip_name,
                                                               equip_model,
                                                               equip_number,
                                                               equip_pre_id)
                    connection.commit()
                    page = uhtml.operation_completed()
        else:
            page = uhtml.pass_is_not_valid()
    else:
        page = "Method in Edit Point not corrected!"
    return web_template.result_page(page, pre_adr, str(stylesheet_number))


def move_equip_method(data, method, stylesheet_number: str) -> str:
    """Move equip to new point"""

    pre_adr = '/'
    if method == 'POST':
        if functions.is_superuser_password(data[uhtml.PASSWORD]):
            if data[uhtml.POINT_ID] == data[uhtml.NEW_POINT_ID]:
                page = uhtml.data_is_not_valid()
            else:
                with Database() as base:
                    connection, cursor = base
                    name_old = select_operations.get_point_name_from_id(cursor,
                                                                        str(data[uhtml.POINT_ID]))
                    name_new = select_operations.\
                        get_point_name_from_id(cursor,
                                               str(data[uhtml.NEW_POINT_ID]))
                    date_remove = functions.date_to_browser().replace("T", ' ') + ':00'
                    insert_operations.create_new_work(cursor,
                                                      str(data[uhtml.EQUIP_ID]),
                                                      date_remove,
                                                      "Перемещение оборудования",
                                                      "Перемещено из {0} в {1}.".
                                                      format(name_old, name_new),
                                                      '1')
                    insert_operations.create_new_equip(cursor,
                                                       data[uhtml.NEW_POINT_ID],
                                                       data[uhtml.EQUIP_NAME],
                                                       data[uhtml.MODEL],
                                                       str(data[uhtml.SERIAL_NUM]),
                                                       str(data[uhtml.EQUIP_ID]))
                    update_operations.set_deleted_status(cursor, str(data[uhtml.EQUIP_ID]))
                    connection.commit()
                    page = uhtml.operation_completed()
        else:
            page = uhtml.pass_is_not_valid()
    else:
        page = "Method in Move Point not corrected!"
    return web_template.result_page(page, pre_adr, str(stylesheet_number))


def find_equip_to_id_page(stylesheet_number: str) -> str:
    """Create page to FIND equip FROM EQUIP_ID"""
    with Database() as base:
        _, cursor = base
        max_equip_id = select_operations.get_count_equips(cursor)
        return web_template.result_page(render_template('equip/find_equip_to_id.html', max_equip_id=max_equip_id),
                                        '/equips',
                                        str(stylesheet_number))


def select_equip_to_id_page(data, method, stylesheet_number: str) -> str:
    """Create page to select EQUIP from EQUIP_ID"""
    pre_adr = '/equips'
    if method == "POST":
        equip_id = data['id']
        if equip_id == '0':
            return redirect('/all-equips')
        with Database() as base:
            _, cursor = base
            equip = select_operations.get_full_equip_information(cursor, str(equip_id))
            equip.append(create_full_edit_links(equip_id,
                                                equip_id != str(equip[4]),
                                                select_operations.get_equip_deleted_status(cursor, equip_id)))
            links_list = ['/work/' + str(equip_id)]
            table1 = uhtml.universal_table(table_headers.equips_table_name,
                                           table_headers.equips_table, [equip], True,
                                           links_list)
            return web_template.result_page(table1, pre_adr, str(stylesheet_number))
    else:
        return web_template.result_page("Method in Select Equip not corrected!",
                                        pre_adr,
                                        str(stylesheet_number))


def add_equip_method(data, method, stylesheet_number: str) -> str:
    """Create page from ADD NEW EQUIP"""
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
                    page = uhtml.data_is_not_valid()
                    pre_addr = '/'
                elif model == '':
                    insert_operations.create_new_equip(cursor, point_id, equip_name)
                    connection.commit()
                    page = uhtml.operation_completed()
                    pre_addr = '/equip/' + str(point_id)
                elif serial_num == '':
                    insert_operations.create_new_equip(cursor, point_id, equip_name, model)
                    connection.commit()
                    page = uhtml.operation_completed()
                    pre_addr = '/equip/' + str(point_id)
                elif pre_id == '':
                    insert_operations.create_new_equip(cursor,
                                                       point_id,
                                                       equip_name,
                                                       model,
                                                       serial_num)
                    connection.commit()
                    page = uhtml.operation_completed()
                    pre_addr = '/equip/' + str(point_id)
                else:
                    insert_operations.create_new_equip(cursor,
                                                       point_id,
                                                       equip_name,
                                                       model,
                                                       serial_num,
                                                       pre_id)
                    connection.commit()
                    page = uhtml.operation_completed()
                    pre_addr = '/equip/' + str(point_id)
        else:
            page = uhtml.pass_is_not_valid()
            pre_addr = '/equip/' + str(point_id)

    else:
        page = 'Method in Add Equip not corrected!'
        pre_addr = '/all-points'
    return web_template.result_page(page, pre_addr, str(stylesheet_number))


def top_equips_from_maximal_works(stylesheet_number: str) -> str:
    """Return page with table. contain equip and maximal works"""
    pre_adr = '/equips'
    with Database() as base:
        _, cursor = base
        top_equips = select_operations.get_top_10_works(cursor)
        lst = [['<a href="/work/{0}">{1}</a>'.format(row[0], elem) for elem in row] for row in top_equips]
        page = render_template('any/universal_table.html', table_name=table_headers.top_10_equips_name,
                               num_columns=len(table_headers.top_10_equips), headers=table_headers.top_10_equips,
                               data=lst)
        return web_template.result_page(page, pre_adr, stylesheet_number, True, 'top10equips')


def get_details_action(detail_id: int) -> str:
    """Download details if exist"""

    with Database() as base:
        _, cursor = base
        try:
            detail_info = select_operations.get_details_info(cursor, detail_id)
            detail_path = "equips{}".format(detail_info[1])
            return flask.send_from_directory(config.static_dir(), detail_path)
        except IndexError:
            return "<h2>Деталировка с ID = {} не найдена!</h2>".format(detail_id)
