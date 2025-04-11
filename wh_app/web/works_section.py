"""This module contain all pages implements to WORKS section database"""

from flask import redirect, render_template

import wh_app.web.template as web_template
import wh_app.web.universal_html as uhtml
from wh_app.postgresql.database import Database
from wh_app.sql_operations.insert_operation import insert_operations
from wh_app.sql_operations.select_operations import select_operations
from wh_app.sql_operations.update_operations import update_operations
from wh_app.supporting import functions
from wh_app.config_and_backup import table_headers

functions.info_string(__name__)


def create_work_edit_link(work_id: str) -> str:
    """Create EDIT link to current work"""
    edit_link = '<a href="/work-edit/{0}" title="Редактировать">{1}</a>'.format(work_id, uhtml.EDIT_CHAR)
    move_link = '<a href="/replace-work-to-point/{0}" title="Перенести на другое оборудование">{1}</a>'.\
        format(work_id, uhtml.REMOVE_CHAR)
    return '{0} {1}'.format(edit_link, move_link)


def works_menu(stylesheet_number: str) -> str:
    """Return main menu in WORKS section"""
    name = 'Действия с ремонтами и диагностиками'
    menu = ['Все зарегистрированные работы', 'Поиск работы по ID']
    links_list = ['/all-works', '/find-work-to-id']
    table = uhtml.universal_table(name, ['№', 'Доступное действие'], functions.list_to_numer_list(menu), True, links_list)
    return web_template.result_page(table, '/', str(stylesheet_number))


def find_work_to_id_page(stylesheet_number: str) -> str:
    """Return page, contain form to find work like WORK_ID"""
    with Database() as base:
        _, cursor = base
        max_work_id = select_operations.get_maximal_work_id(cursor)
        return web_template.result_page(render_template('works/find_work_to_id.html', max_work_id=max_work_id),
                                        '/works',
                                        str(stylesheet_number))


def select_new_point_for_work_form(work_id: int, stylesheet_number: str) -> str:
    """Create form to select new point to move work"""
    with Database() as base:
        _, cursor = base
        work = select_operations.get_full_information_to_work(cursor, work_id)
        all_points = select_operations.get_all_points(cursor)
        return web_template.result_page(render_template("points/select_point_to_replace.html", work_id_name=uhtml.WORK_ID,
                                                    work_id=work_id,
                                                        work_description="{0} --> {1}".format(work[6], work[7]),
                                                        point_id_name=uhtml.POINT_ID, all_points=all_points),
                                                    '/works', str(stylesheet_number))


def select_new_equip_for_work_form(data, method, stylesheet_number: str) -> str:
    """Create form to select equip to move work"""
    pre_adr = '/works'
    if method == 'POST':
        point_id = data[uhtml.POINT_ID]
        work_id = data[uhtml.WORK_ID]
        with Database() as base:
            _, cursor = base
            work = select_operations.get_full_information_to_work(cursor, work_id)
            equip_in_point = select_operations.get_equip_in_point(cursor, point_id)
            return web_template.result_page(render_template("equip/select_equip_to_replace.html", work_id_name=uhtml.WORK_ID,
                                                            work_id=work_id,
                                                            work_description="{0} --> {1}".format(work[6], work[7]),
                                                            point_id_name=uhtml.POINT_ID,
                                                            point_id=point_id, equip_id_name=uhtml.EQUIP_ID,
                                                            all_equips=equip_in_point, password=uhtml.PASSWORD),
                                            '/works', str(stylesheet_number))
    else:
        return web_template.result_page("Method in Move Work not corrected!",
                                        pre_adr,
                                        str(stylesheet_number))


def move_work_to_new_equip(data, method, stylesheet_number: str) -> str:
    """analyze and move work to correct equip if data is correct"""
    pre_adr = '/works'
    if method == 'POST':
        work_id = data[uhtml.WORK_ID]
        equip_id = data[uhtml.EQUIP_ID]
        password = data[uhtml.PASSWORD]
        if functions.is_superuser_password(password):
            with Database() as base:
                connection, cursor = base
                update_operations.update_equip_in_work_record(cursor, work_id, equip_id)
                connection.commit()
                page = uhtml.operation_completed()
        else:
            page = uhtml.pass_is_not_valid()
    else:
        page = web_template.result_page("Method in Move Work not corrected!",
                                        pre_adr,
                                        str(stylesheet_number))
    return web_template.result_page(page, pre_adr, stylesheet_number)


def select_work_to_id_method(data, method, stylesheet_number: str) -> str:
    """Method return page, contain work likes WORK_ID"""
    pre_adr = '/works'
    if method == "POST":
        work_id = data['id']
        if work_id == '0':
            return redirect('/all-works')
        with Database() as base:
            _, cursor = base
            work = select_operations.get_full_information_to_work(cursor, str(work_id))
            work = functions.works_table_add_new_performer([work])
            work[0].append(create_work_edit_link(work_id))
            table1 = uhtml.universal_table(table_headers.works_table_name,
                                           table_headers.works_table,
                                           work)
            return web_template.result_page(table1, pre_adr, str(stylesheet_number), True, 'work={}'.format(work_id))
    else:
        return web_template.result_page("Method in Select Work not corrected!",
                                        pre_adr,
                                        str(stylesheet_number))


def work_to_equip_paging(equip_id, page_id, stylesheet_number: str, ord_column=1) -> str:
    """Return page, contain works from current equip"""
    with Database() as base:
        _, cursor = base
        pre_adr = ('/equip/' +
                   str(select_operations.
                       get_point_id_from_equip_id(cursor, equip_id))) \
            if str(equip_id) != '0' \
            else '/works'
        full_works = select_operations.get_works_from_equip_id_limit(cursor, equip_id, page_id, ord_column)
        full_works = functions.works_table_add_new_performer(full_works)
        for work in full_works:
            work.append(create_work_edit_link(work[0]))
        headers = []
        for elem in table_headers.works_table_ext:
            headers.append(elem.format('/work/{0}/page/{1}'.format(equip_id, page_id)))
        table1 = uhtml.universal_table(table_headers.works_table_name,
                                       headers,
                                       full_works)
        if str(equip_id) != '0' and not select_operations.get_equip_deleted_status(cursor, equip_id):
                table2 = uhtml.add_new_work(equip_id)
        else:
            table2 = ""

        table_paging = uhtml.paging_table("/work/{0}/page".format(equip_id),
                                          functions.
                                          list_of_pages(select_operations.
                                                        get_works_from_equip_id(cursor,
                                                                                equip_id)),
                                          int(page_id), True, ord_column)
        return web_template.result_page(table1 + table_paging + table2,
                                        pre_adr,
                                        str(stylesheet_number),
                                        True,
                                        "equip={0}={1}".format(equip_id, page_id))


def create_edit_work_form(work_id: int, stylesheet_number: str) -> str:
    """Create new web-form to EDIT current work"""
    with Database() as base:
        _, cursor = base
        pre_adr = '/works'
        works_info = select_operations.get_full_information_to_work(cursor, str(work_id))
        print(works_info)
        main_table = render_template('works/edit_work.html', work_id=work_id, works_info=works_info,
                                     order_info=uhtml.ORDER_INFO, description=uhtml.DESCRIPTION,
                                     password=uhtml.PASSWORD)
    return web_template.result_page(main_table, pre_adr, stylesheet_number)


def update_work_method(work_id: int, data, method, stylesheet_number: str) -> str:
    """UPDATE selected work-string in work-table in DATABASE"""

    pre_adr = '/works'
    if method == "POST":
        password = data[uhtml.PASSWORD]
        order_info = data[uhtml.ORDER_INFO]
        description = data[uhtml.DESCRIPTION]
        work_datetime = data[uhtml.WORK_DATETIME].replace("T", ' ')
        if work_datetime.count(':') < 2: #YYYY-MM-DD HH:MM:SS
            work_datetime += ':00'
        if functions.is_superuser_password(password):
            if order_info.replace(" ", "") == '' or description.replace(" ", "") == '':
                page = uhtml.data_is_not_valid()
            else:
                with Database() as base:
                    connection, cursor = base
                    update_operations.update_work_info(cursor, str(work_id), order_info, description, work_datetime)
                    connection.commit()
                    page = uhtml.operation_completed()
        else:
            page = uhtml.pass_is_not_valid()
    else:
        page = "Method in Edit Work not corrected!"

    return web_template.result_page(page, pre_adr, str(stylesheet_number))


def add_work_method(data, method, stylesheet_number: str) -> str:
    """Method add new work in database"""
    if method == "POST":
        password = data[uhtml.PASSWORD]
        equip_id = data[uhtml.EQUIP_ID]
        query = data[uhtml.QUERY]
        work = data[uhtml.WORK]
        work_datetime = data[uhtml.WORK_DATETIME].replace("T", ' ') + ':00'
        pre_adr = '/work/' + str(equip_id)
        perfomer = data[uhtml.PERFORMER]
        if functions.is_valid_password(password):
            if work.replace(" ", "") == '':
                page = uhtml.data_is_not_valid()
            else:
                with Database() as base:
                    connection, cursor = base
                    insert_operations.create_new_work(cursor,
                                                      equip_id,
                                                      work_datetime,
                                                      query,
                                                      work,
                                                      perfomer)
                    connection.commit()
                    page = uhtml.operation_completed()
        else:
            page = uhtml.pass_is_not_valid()
    else:
        page = "Method in Add Work not corrected!"
        pre_adr = '/'

    return web_template.result_page(page, pre_adr, str(stylesheet_number))
