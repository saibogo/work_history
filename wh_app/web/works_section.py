"""This module contain all pages implements to WORKS section database"""

from flask import redirect

import wh_app.web.template as web_template
import wh_app.web.universal_html as uhtml
from wh_app.postgresql.database import Database
from wh_app.sql_operations import insert_operations
from wh_app.sql_operations import select_operations
from wh_app.sql_operations import update_operations
from wh_app.supporting import functions
from wh_app.config_and_backup import table_headers
from wh_app.web.equips_section import EDIT_CHAR

functions.info_string(__name__)


def works_menu(stylesheet_number: str) -> str:
    """Return main menu in WORKS section"""
    name = 'Действия с ремонтами и диагностиками'
    menu = [(1, 'Все зарегистрированные работы'), (2, 'Поиск работы по ID')]
    links_list = ['/all-works', '/find-work-to-id']
    table = uhtml.universal_table(name, ['№', 'Доступное действие'], menu, True, links_list)
    return web_template.result_page(table, '/', str(stylesheet_number))


def find_work_to_id_page(stylesheet_number: str) -> str:
    """Return page, contain form to find work like WORK_ID"""
    with Database() as base:
        _, cursor = base
        max_work_id = select_operations.get_maximal_work_id(cursor)
        find_table = list()
        find_table.append('<table><caption>Поиск выполненной работы по уникальному ID</caption>')
        find_table.append('<form action="/select-work-to-id" method="post">')
        find_table.append('<tr><td><input type="number" name="id" min="0" max="' +
                          max_work_id +
                          '"></td></tr>')
        find_table.append('<tr><td><input type="submit" value="Найти"></td></tr>')
        return web_template.result_page("\n".join(find_table),
                                        '/works',
                                        str(stylesheet_number))


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
            table1 = uhtml.universal_table(table_headers.works_table_name,
                                           table_headers.works_table,
                                           work)
            return web_template.result_page(table1, pre_adr, str(stylesheet_number))
    else:
        return web_template.result_page("Method in Select Work not corrected!",
                                        pre_adr,
                                        str(stylesheet_number))


def work_to_equip_paging(equip_id, page_id, stylesheet_number: str) -> str:
    """Return page, contain works from current equip"""
    with Database() as base:
        _, cursor = base
        pre_adr = ('/equip/' +
                   str(select_operations.
                       get_point_id_from_equip_id(cursor, equip_id))) \
            if str(equip_id) != '0' \
            else '/works'
        full_works = select_operations.get_works_from_equip_id_limit(cursor, equip_id, page_id)
        full_works = functions.works_table_add_new_performer(full_works)
        for work in full_works:
            work.append('<a href="/work-edit/{1}">{0}</a>'.format(EDIT_CHAR, work[0]))
        table1 = uhtml.universal_table(table_headers.works_table_name,
                                       table_headers.works_table,
                                       full_works)
        table2 = uhtml.add_new_work(equip_id) if str(equip_id) != 0 else ""
        table_paging = uhtml.paging_table("/work/{0}/page".format(equip_id),
                                          functions.
                                          list_of_pages(select_operations.
                                                        get_works_from_equip_id(cursor,
                                                                                equip_id)),
                                          int(page_id))
        return web_template.result_page(table1 + table_paging + table2,
                                        pre_adr,
                                        str(stylesheet_number),
                                        True,
                                        "equip={0}".format(equip_id))


def create_edit_work_form(work_id: int, stylesheet_number: str) -> str:
    """Create new web-form to EDIT current work"""
    with Database() as base:
        _, cursor = base
        pre_adr = '/works'
        works_info = select_operations.get_full_information_to_work(cursor, str(work_id))
        result = list()
        result.append('<table><caption>Редактирование отчета</caption><tr><th>Поле</th><th>Значение/Действие</th><tr>')
        result.append('<form action="/update-work-to-id/{0}" method="post">'.format(work_id))
        result.append('<tr><td>ID</td><td>{0}</td></tr>'.format(work_id))
        result.append('<tr><td>Обьект</td><td>{0}</td></tr>'.format(works_info[1]))
        result.append('<tr><td>Оборудование</td><td>{0}</td></tr>'.format(works_info[2]))
        result.append('<tr><td>Модель оборудования</td><td>{0}</td></tr>'.format(works_info[3]))
        result.append('<tr><td>Серийный номер</td><td>{0}</td></tr>'.format(works_info[4]))
        result.append('<tr><td>Окончание работ</td><td>{0}</td></tr>'.format(works_info[5]))
        result.append('<tr><td>Состав заявки</td><td><textarea rows=3 name="{1}">{0}</textarea></td></tr>'
                      .format(works_info[6], uhtml.ORDER_INFO))
        result.append('<tr><td>Описание произведенных работ</td><td><textarea rows=6 name="{1}">{0}'
                      '</textarea></td></tr>'.format(works_info[7], uhtml.DESCRIPTION))
        result.append('<tr><td>Перечень исполнителей</td><td>{0}</td></tr>'.format(works_info[8]))
        result.append('<tr><td>Пароль суперпользователя</td><td><input type="password" name="{0}">'
                      '</input></td></tr>'.format(uhtml.PASSWORD))
        result.append('<tr><td>Применить изменения</td><td><input type="submit" value="Отправить"></input></td></tr>')

        result.append('</form></table>')
    return web_template.result_page("".join(result), pre_adr, stylesheet_number)


def update_work_method(work_id: int, data, method, stylesheet_number: str) -> str:
    """Use UPDATE procedure to Database"""

    pre_adr = '/works'
    if method == "POST":
        password = data[uhtml.PASSWORD]
        order_info = data[uhtml.ORDER_INFO]
        description = data[uhtml.DESCRIPTION]
        if functions.is_superuser_password(password):
            if order_info.replace(" ", "") == '' or description.replace(" ", "") == '':
                page = uhtml.data_is_not_valid()
            else:
                with Database() as base:
                    connection, cursor = base
                    update_operations.update_work_info(cursor, str(work_id), order_info, description)
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
