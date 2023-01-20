"""This module contain any web-pages"""

from flask import render_template

import wh_app.web.template as web_template
import wh_app.web.universal_html as uhtml
from wh_app.config_and_backup import config
from wh_app.postgresql.database import Database
from wh_app.sql_operations import select_operations
from wh_app.supporting import functions
from wh_app.supporting import system_status
from wh_app.config_and_backup import table_headers
from wh_app.web.universal_html import selected_new_theme, logpass_table, replace_decor
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


@replace_decor
def faq_page(pre_adr: str, stylesheet_number: str) -> str:
    """Function create FAQ web-page"""
    with Database() as base:
        _, cursor = base
        max_equip_id = select_operations.get_maximal_equip_id(cursor)
        max_point_id = select_operations.get_maximal_points_id(cursor)
        max_work_id = select_operations.get_maximal_work_id(cursor)
        hardware = web_template.faq_state_machine('hardware')
        tecnology = web_template.faq_state_machine('tecnology')
        multiuser = web_template.faq_state_machine('multiuser')
        update = web_template.faq_state_machine('update')
        records = ['Единиц или групп оборудования: <a href="{0}/all-equips">{1}</a>'.format(config.full_address, max_equip_id),
                   'Предприятий: <a href="{0}/all-points">{1}</a>'.format(config.full_address, max_point_id),
                   'Произведенных работ: <a href="{0}/all-works">{1}</a>'.format(config.full_address, max_work_id)]
        database_size = select_operations.get_size_database(cursor)
        average_works_in_date = "{:.2f}".format(select_operations.get_count_unique_works(cursor) /
                                               select_operations.get_count_unique_dates_in_works(cursor))
        main_table = render_template('faq.html', hardware=hardware, tecnology=tecnology, multiuser=multiuser,
                                     update=update, records=records, database_size=database_size,
                                     average_works_in_date=average_works_in_date)
        return web_template.result_page(main_table,
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
