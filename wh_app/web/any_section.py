"""This module contain any web-pages"""

import wh_app.web.template as web_template
import wh_app.web.universal_html as uhtml
from wh_app.config_and_backup import config
from wh_app.postgresql.database import Database
from wh_app.sql_operations import select_operations
from wh_app.supporting import functions
from wh_app.supporting import system_status
from wh_app.config_and_backup import table_headers
from wh_app.web.universal_html import selected_new_theme, logpass_table
from wh_app.supporting.metadata import CHANGELOG

functions.info_string(__name__)


def main_web_menu(stylesheet_number: str) -> str:
    """Function create main web-page"""
    name = "Доступные действия в базе ремонтов Малахит-Екатеринбург"
    menu_items = ['Операции с предприятиями', 'Операции с оборудованием', 'Операции с ремонтами',
                  'Операции с сотрудниками', 'Баг-трекер системы', 'Работа с заявками',
                  'Изменить тему оформления', 'Изменения в системе', 'Выйти из системы']
    links_list = ['/points', '/equips', '/works', '/workers', '/bugs', '/orders-and-customers', '/next-themes',
                  '/changelog-page', '/logout']
    table = uhtml.universal_table(name, ['№', 'Перейти к'], [(i + 1, menu_items[i]) for i in range(len(menu_items))],
                                  True, links_list)
    return web_template.result_page(table, "", stylesheet_number)


def faq_page(pre_adr: str, stylesheet_number: str) -> str:
    """Function create FAQ web-page"""
    with Database() as base:
        _, cursor = base
        page = list()
        page.append('<table><caption>Наиболее частые вопросы по системе:</caption><tr><td>')
        page.append('<ul>')
        page.append('<li class="faq_question">Что нужно для использования системы?'+\
                    web_template.faq_state_machine('hardware') + '</li>')
        page.append('<li class="faq_question">С использованием каких технологий ' +
                    'написана система?' + web_template.faq_state_machine('tecnology') + '</li>')
        page.append('<li class="faq_question">Сколько пользователей поддерживает система?' +\
                    web_template.faq_state_machine('multiuser') + '</li>')
        page.append('<li class="faq_question">Планируется ли развитие системы?' +\
                    web_template.faq_state_machine('update') + '</li>')
        max_equip_id = select_operations.get_maximal_equip_id(cursor)
        max_point_id = select_operations.get_maximal_points_id(cursor)
        max_work_id = select_operations.get_maximal_work_id(cursor)
        page.append('<li class="faq_question">Сколько записей зарегистрированно на ' +
                    ' данный момент?' +\
                    uhtml.list_to_ul(['Единиц или групп оборудования: <a href="' +
                                      config.full_address + '/all-equips">' +
                                      str(max_equip_id) + '</a>',
                                      'Предприятий: <a href="' + config.full_address +
                                      '/all-points">' +
                                      str(max_point_id) + '</a>',
                                      'Произведенных работ: <a href="' +
                                      config.full_address + '/all-works">' +
                                      str(max_work_id) + '</a>']) + '</li>')
        page.append('<li class="faq_question">Текущий размер базы данных : ' +
                    str(select_operations.get_size_database(cursor)) + '</li>')
        page.append('<li class="faq_question">Среднее количество работ на смену : ' +
                    str(select_operations.get_count_unique_works(cursor) /
                        select_operations.get_count_unique_dates_in_works(cursor)) + '</li>')
        page.append('</ul></td></tr></table>')
        return web_template.result_page('\n'.join(page),
                                        pre_adr,
                                        str(stylesheet_number))


def statistics_page(preview_page, stylesheet_number: str) -> str:
    """Function create STATISTIC web-page"""
    with Database() as base:
        _, cursor = base
        statistics = select_operations.get_statistic(cursor)
        links_list = ['/equip/' + str(elem[0]) for elem in statistics]
        result = uhtml.universal_table(table_headers.statistics_table_name,
                                       table_headers.statistics_table,
                                       [[elem[i] for i in range(1, len(elem))]
                                        for elem in statistics],
                                       True,
                                       links_list)
        return web_template.result_page(result, preview_page, str(stylesheet_number))


def system_status_page(preview_page, stylesheet_number: str) -> str:
    """Function create System-Status Web-page"""
    current_status = system_status.SystemStatus.get_status()
    status_to_list = [[key, current_status[key]] for key in current_status]
    result = uhtml.universal_table(table_headers.all_workers_table_name,
                                   table_headers.system_status_table,
                                   status_to_list)
    return web_template.result_page(result, preview_page, str(stylesheet_number))


def new_theme_page(stylesheet_number: str) -> str:
    """Function create information web-page from New CSS theme"""
    return web_template.result_page(selected_new_theme(), "/", str(stylesheet_number))


def viev_changelog(stylesheet_number: str) -> str:
    """Function create Changelog web-page"""
    table = uhtml.universal_table(table_headers.changelog_table_name,
                                  table_headers.changelog_table,
                                  CHANGELOG)
    return web_template.result_page(table, '/', str(stylesheet_number))


def login_input_page() -> str:
    """Function create new form to input login and page"""
    return web_template.result_page(logpass_table(), '/')
