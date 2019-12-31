from flask import redirect

import wh_app.web.template as web_template
import wh_app.web.universal_html as uhtml
from wh_app.config_and_backup import config
from wh_app.postgresql.database import Database
from wh_app.sql_operations import insert_operations
from wh_app.sql_operations import select_operations
from wh_app.supporting import functions

functions.info_string(__name__)


def works_menu():
    name = 'Действия с ремонтами и диагностиками'
    menu = [(1, 'Все зарегистрированные работы'), (2, 'Поиск работы по ID')]
    links_list = ['/all-works', '/find-work-to-id']
    table = uhtml.universal_table(name, ['№', 'Доступное действие'], menu, True, links_list)
    return web_template.result_page(table, '/')


def find_work_to_id_page():
    with Database() as base:
        connection, cursor = base
        max_work_id = select_operations.get_maximal_work_id(cursor)
        find_table = list()
        find_table.append('<table><caption>Поиск выполненной работы по уникальному ID</caption>')
        find_table.append('<form action="/select-work-to-id" method="post">')
        find_table.append('<tr><td><input type="number" name="id" min="0" max="' + max_work_id + '"></td></tr>')
        find_table.append('<tr><td><input type="submit" value="Найти"></td></tr>')
        return web_template.result_page("\n".join(find_table), '/works')


def select_work_to_id_method(data, method):
    pre_adr = '/works'
    if method == "POST":
        work_id = data['id']
        if work_id == '0':
            return redirect('/all-works')
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


def work_to_equip_paging(equip_id, page_id):

    with Database() as base:
        connection, cursor = base
        pre_adr = ('/equip/' + str(select_operations.get_point_id_from_equip_id(cursor, equip_id))) if \
            str(equip_id) != '0' else '/works'
        full_works = select_operations.get_works_from_equip_id_limit(cursor, equip_id, page_id)
        full_works = functions.works_table_add_new_performer(full_works)
        table1 = uhtml.universal_table(config.works_table_name,
                                       config.works_table,
                                       full_works)
        table2 = uhtml.add_new_work(equip_id) if str(equip_id) != 0 else ""
        table_paging = uhtml.paging_table("/work/{0}/page".format(equip_id),
                                          functions.list_of_pages(select_operations.get_works_from_equip_id(cursor,
                                                                                                            equip_id)),
                                          int(page_id))
        return web_template.result_page(table1 + table_paging + table2, pre_adr)


def add_work_method(data, method):
    if method == "POST":
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