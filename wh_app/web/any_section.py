"""This module contain any web-pages"""

from flask import render_template

import wh_app.web.template as web_template
import wh_app.web.universal_html as uhtml
from wh_app.config_and_backup import config
from wh_app.postgresql.database import Database
from wh_app.sql_operations.select_operations import select_operations
from wh_app.supporting import functions
from wh_app.supporting import system_status
from wh_app.config_and_backup import table_headers
from wh_app.web.universal_html import selected_new_theme, logpass_table, replace_decor
from wh_app.supporting.metadata import CHANGELOG
from wh_app.supporting.parser_eesk.eens_data import get_eens_data, EeensException
from wh_app.supporting.parser_eesk.eesk_data import get_eesk_data, EeskException

functions.info_string(__name__)


def main_web_menu(stylesheet_number: str) -> str:
    """Function create main web-page"""
    name = "Доступные действия"
    menu_items = ['Операции с предприятиями', 'Операции с оборудованием', 'Операции с ремонтами',
                  'Операции с сотрудниками', 'Баг-трекер системы', 'Работа с заявками',
                  'Изменить тему оформления', 'Изменения в системе', 'Вспомогательные сервисы', 'Выйти из системы']
    links_list = ['/points', '/equips', '/works', '/workers', '/bugs', '/orders-and-customers', '/next-themes',
                  '/changelog-page', '/external-services', '/logout']
    table = uhtml.universal_table(name, ['№', 'Перейти к'], [(i + 1, menu_items[i]) for i in range(len(menu_items))],
                                  True, links_list)
    return web_template.result_page(table, "", stylesheet_number)


@replace_decor
def external_services_page(stylesheet_number: str) -> str:
    """Function create page with all services in services-list"""
    name = "Доступные сервисы"
    menu_items = ['Планируемые отключения электроэнергии']
    links_list = ['/power-outages']
    table = uhtml.universal_table(name, ['№', 'Перейти к'], [(i + 1, menu_items[i]) for i in range(len(menu_items))],
                                  True, links_list)
    return web_template.result_page(table, "", str(stylesheet_number))


@replace_decor
def power_outages_page(stylesheet_number: str) -> str:
    """Function create page with all correct outages"""

    try:
        eens_list = [[elem['num'], elem['startDate'], elem['endDate'],
                      elem['objects'], elem['street'], elem['link']] for elem in get_eens_data()]
        for phone in eens_list:
            phone[-1] = '<a href="{}">Телефонограмма</a>'.format(phone[-1])

        table1 = render_template('universal_table.html', table_name=table_headers.eens_table_name,
                                 headers=table_headers.eens_table, data=eens_list,
                                 num_columns=len(table_headers.eens_table))
    except EeensException as e:
        table1 = render_template('universal_table.html', table_name='Данные Екатеринбургэнергосбыт недоступны',
                                 table_headers=[], date=[])

    try:
        eesk_list = [[elem[2], elem[3], elem[4], elem[6]] for elem in get_eesk_data()]
        table2 = render_template('universal_table.html', table_name=table_headers.eesk_table_name,
                                 headers=table_headers.eesk_table, data=eesk_list,
                                 num_columns=len(table_headers.eesk_table))
    except EeskException as e:
        table2 = render_template('universal_table.html', table_name='Данные Екатеринбургской Электросетевой Компании недоступны',
                                 table_headers=[], date=[])

    with Database() as base:
        _, cursor = base
        find_list = select_operations.get_all_find_patterns(cursor)
        table3 = render_template('universal_table.html', table_name='Список слов для поиска',
                                 headers=['Ищется', " ".join(find_list)], data=[], num_columns=2)

    return web_template.result_page(table1 + table2 + table3, "/external-services", str(stylesheet_number), False)


@replace_decor
def faq_page(pre_adr: str, stylesheet_number: str) -> str:
    """Function create FAQ web-page"""
    with Database() as base:
        _, cursor = base
        count_equip = select_operations.get_count_equips(cursor)
        max_point_id = select_operations.get_maximal_points_id(cursor)
        count_works_points = select_operations.get_count_works_points(cursor)
        count_works = select_operations.get_maximal_work_id(cursor)
        hardware = web_template.faq_state_machine('hardware')
        tecnology = web_template.faq_state_machine('tecnology')
        multiuser = web_template.faq_state_machine('multiuser')
        update = web_template.faq_state_machine('update')
        records = ['Единиц или групп оборудования на предприятиях: <a href="{0}/all-equips">{1}</a>'.
                   format(config.full_address(), count_equip),
                   'Предприятий всего: <a href="{0}/all-points">{1}</a>'.format(config.full_address(), max_point_id),
                   'Предприятий действующих: <a href="{0}/works-points">{1}</a>'.format(config.full_address(),
                                                                                        count_works_points),
                   'Произведенных работ: <a href="{0}/all-works">{1}</a>'.format(config.full_address(), count_works)]
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
    result = render_template('system_status.html', parameters=status_to_list)
    return web_template.result_page(result, preview_page, str(stylesheet_number))


def new_theme_page(stylesheet_number: str) -> str:
    """Function create information web-page from New CSS theme"""
    return web_template.result_page(selected_new_theme(), "/", str(stylesheet_number))


def view_changelog(stylesheet_number: str) -> str:
    """Function create Changelog web-page"""
    if len(CHANGELOG) > config.max_records_in_page():
        return view_changelog_page(1, stylesheet_number)
    table = uhtml.universal_table(table_headers.changelog_table_name,
                                  table_headers.changelog_table,
                                  CHANGELOG)
    return web_template.result_page(table, '/', str(stylesheet_number))


def view_changelog_page(page_num: int, stylesheet_number: str) -> str:
    """Function create changelog web-page with paging"""
    start = config.max_records_in_page() * (page_num - 1)
    stop = start + config.max_records_in_page()
    changelog_slice = CHANGELOG[start : stop]
    table = uhtml.universal_table(table_headers.changelog_table_name,
                                  table_headers.changelog_table,
                                  changelog_slice)
    table_paging = uhtml.paging_table('/changelog-page/page', functions.list_of_pages(CHANGELOG), int(page_num))
    return web_template.result_page(table + table_paging, '/', stylesheet_number, False)


def login_input_page() -> str:
    """Function create new form to input login and page"""
    return web_template.result_page(logpass_table(), '/')
