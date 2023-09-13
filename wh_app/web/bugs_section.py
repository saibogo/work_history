"""This module implements methods for bugs-section web-pages"""

from typing import List, Any, Tuple
from flask import render_template

import wh_app.web.template as web_template
import wh_app.web.universal_html as uhtml
from wh_app.postgresql.database import Database
from wh_app.sql_operations import select_operations, insert_operations, update_operations
from wh_app.supporting import functions
from wh_app.config_and_backup import table_headers, config

functions.info_string(__name__)


def add_on_off_links_to_bug_table(bugs_list: List[Tuple[Any]]) -> List[List[Any]]:
    """Add Button ON-OFF in any bugs-table"""
    pattern = '<a href="/invert-bug-status/{0}">{1}</a>'
    result = list(map(lambda elem: list(elem) + [pattern.format(elem[0], uhtml.ON_OFF_CHAR)], bugs_list))
    return result


def replace_none_in_list(ls: list) -> list:
    """Replace all None in bugs-list"""
    return [[elem if elem else "" for elem in row] for row in ls]


def bugs_menu(stylesheet_number: str) -> str:
    """Method create main bugs-page"""
    menu = [(1, 'Отобразить все'),
            (2, 'Отобразить незакрытые'),
            (3, 'Зарегистрировать проблему')]
    headers = ['№', 'Выполнить']
    links_list = ['/all-bugs', '/all-bugs-in-work', '/add-bug']
    table = uhtml.universal_table('Возможные действия', headers, menu, True, links_list)
    return web_template.result_page(table, '/bugs', str(stylesheet_number))


def all_bugs_table(stylesheet_number: str) -> str:
    """Method create page, contain all registred bugs"""
    with Database() as base:
        _, cursor = base
        bugs_list = select_operations.get_all_bugz_in_bugzilla(cursor)
        if len(bugs_list) > config.max_records_in_page():
            result = all_bugs_table_limit(1, stylesheet_number)
        else:
            bugs_list = replace_none_in_list(bugs_list)
            bugs_list = add_on_off_links_to_bug_table(bugs_list)
            table = uhtml.universal_table(table_headers.bugs_table_name,
                                          table_headers.bugs_table,
                                          bugs_list)
            result = web_template.result_page(table, '/bugs', str(stylesheet_number))
        return result


def all_bugs_table_limit(page_num: int, stylesheet_number: str) -> str:
    """Method create page, contain all registred bugs use limit records in page"""
    with Database() as base:
        _, cursor = base
        bugs_list = select_operations.get_all_bugz_in_bugzilla_limit(cursor, page_num)
        bugs_list = replace_none_in_list(bugs_list)
        bugs_list = add_on_off_links_to_bug_table(bugs_list)
        table = uhtml.universal_table(table_headers.bugs_table_name,
                                      table_headers.bugs_table,
                                      bugs_list)
        pages = uhtml.paging_table("/all-bugs/",
                                   functions.list_of_pages(select_operations.get_all_bugz_in_bugzilla(cursor)),
                                   int(page_num))

        return web_template.result_page(table + pages, '/bugs', str(stylesheet_number))


def all_bugs_in_work_table(stylesheet_number: str) -> str:
    """Method create page. contain all unclosed bugs"""
    with Database() as base:
        _, cursor = base
        bugs_list = select_operations.get_all_bugz_in_work_in_bugzilla(cursor)
        if len(bugs_list) > config.max_records_in_page():
            result = all_bugs_in_work_limit(1, stylesheet_number)
        else:
            bugs_list = add_on_off_links_to_bug_table(bugs_list)
            table = uhtml.universal_table(table_headers.bugs_table_name,
                                          table_headers.bugs_in_work_table,
                                          bugs_list)
            result = web_template.result_page(table, '/bugs', str(stylesheet_number))
        return result


def all_bugs_in_work_limit(page_num: int, stylesheet_number: str) -> str:
    """Method create page. contain all unclosed bugs use limit records on page"""
    with Database() as base:
        _, cursor = base
        bugs_list = select_operations.get_all_bugz_in_work_in_bugzilla_limit(cursor, page_num)
        bugs_list = add_on_off_links_to_bug_table(bugs_list)
        table = uhtml.universal_table(table_headers.bugs_table_name,
                                      table_headers.bugs_in_work_table,
                                      bugs_list)
        pages = uhtml.paging_table("/all-bugs-in-work/",
                                   functions.list_of_pages(select_operations.get_all_bugz_in_work_in_bugzilla(cursor)),
                                   int(page_num))
        return web_template.result_page(table + pages, '/bugs', str(stylesheet_number))


def add_bugs_result_table(data, method, stylesheet_number: str) -> str:
    """Add new bug in bug tracker after use input form to add bug"""

    if method == 'POST':
        bug_description = data[uhtml.DESCRIPTION]
        password = data[uhtml.PASSWORD]
        pre_adr = '/bugs'
        if functions.is_valid_password(password):
            with Database() as base:
                connection, cursor = base
                insert_operations.add_new_bug_in_bugzilla(cursor, bug_description)
                connection.commit()
                return web_template.result_page(uhtml.operation_completed(),
                                                pre_adr,
                                                str(stylesheet_number))
        else:
            return web_template.result_page(uhtml.pass_is_not_valid(),
                                            pre_adr,
                                            str(stylesheet_number))
    else:
        return web_template.result_page('Method in Add New Bug not corrected!',
                                        '/bugs',
                                        str(stylesheet_number))


def create_invert_bug_status_form(bug_num: str, stylesheet_number: str) -> str:
    """Create form to invert bug-status"""

    with Database() as base:
        _, cursor = base
        bug = select_operations.get_bug_by_id(cursor, bug_num)
        header = table_headers.bugs_table
        description = [(header[i], bug[i]) for i in range(len(bug))]
        main_table = render_template('invert_bug_status_form.html', description=description,
                                     bug_id_name= uhtml.BUG_ID, bug_id=bug_num, password=uhtml.PASSWORD)
        return web_template.result_page(main_table, '/bugs', str(stylesheet_number))


def invert_bug_status_method(data, method, stylesheet_number: str) -> str:
    """Invert bug status if all data is valid"""

    if method == 'POST':
        bug_id = data[uhtml.BUG_ID]
        password = data[uhtml.PASSWORD]
        pre_adr = '/bugs'
        if functions.is_valid_password(password):
            print('BUG_ID = {}'.format(bug_id))
            with Database() as base:
                connection, cursor = base
                update_operations.invert_bug_status_in_bugzilla(cursor, bug_id)
                connection.commit()
                return web_template.result_page(uhtml.operation_completed(),
                                                pre_adr,
                                                str(stylesheet_number))
        else:
            return web_template.result_page(uhtml.pass_is_not_valid(),
                                            pre_adr,
                                            str(stylesheet_number))
    else:
        return web_template.result_page('Method in Invert Bug Status not corrected!',
                                        '/bugs',
                                        str(stylesheet_number))