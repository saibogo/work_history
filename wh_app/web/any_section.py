"""This module contain any web-pages"""
import flask
import os.path
from flask import render_template, Response, abort
from typing import List

import wh_app.web.template as web_template
import wh_app.web.universal_html as uhtml
from wh_app.config_and_backup import config
from wh_app.postgresql.database import Database
from wh_app.sql_operations.select_operations import select_operations
from wh_app.sql_operations.insert_operation.insert_operations import insert_new_reading_to_meter_device
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
                  'Операции с сотрудниками', 'Баг-трекер системы', 'Заявки и Заказчики',
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
    menu_items = ['Планируемые отключения электроэнергии', 'Приборы учета']
    links_list = ['/power-outages', '/meter-devices']
    table = uhtml.universal_table(name, ['№', 'Перейти к'], [(i + 1, menu_items[i]) for i in range(len(menu_items))],
                                  True, links_list)
    return web_template.result_page(table, "", str(stylesheet_number))


@replace_decor
def meter_devices_menu_page(stylesheet_number: str) -> str:
    """Function create main menu for work with all meter devices"""
    name = "Работа с приборами учета энергоресурсов"
    menu_items = ['Все зарегистрированные приборы учета', 'Только действующие']
    links_list = ['/all-meter-devices', '/worked-meter-devices']
    table = uhtml.universal_table(name, ['№', 'Перейти к'], [(i + 1, menu_items[i]) for i in range(len(menu_items))],
                                  True, links_list)
    return web_template.result_page(table, "/external-services", str(stylesheet_number))


def all_meter_devices_page(stylesheet_number: str) -> str:
    """Function create page with all meter devices in database"""

    with Database() as base:
        _, cursor = base
        devices = select_operations.get_all_meter_devices(cursor)
        if len(devices) > config.max_records_in_page():
            return flask.redirect('/all-meter-devices/page/1')
        links = ['/get-devices-reading/{}'.format(elem[0]) for elem in devices]
        table = uhtml.universal_table(table_headers.meter_devices_table_name, table_headers.meter_devices_table,
                                      devices, True, links)

        return web_template.result_page(table, "/meter-devices", str(stylesheet_number))


def all_meter_devices_with_paging(page_num: int, stylesheet_number: str, ord_column=1) -> str:
    """Function create page with all meter devices in database"""

    with Database() as base:
        _, cursor = base
        devices = select_operations.get_all_meter_devices_limit(cursor, page_num, True, ord_column)
        links = ['/get-devices-reading/{}'.format(elem[0]) for elem in devices]
        headers = []
        for elem in table_headers.meter_devices_table_ext:
            headers.append(elem.format('/all-meter-devices/page/{0}'.format(page_num)))
        table = uhtml.universal_table(table_headers.meter_devices_table_name, headers, devices, True, links)
        link = '/all-meter-devices/page'
        all_elems = functions.list_of_pages(select_operations.get_all_meter_devices(cursor))
        pages = uhtml.paging_table(link, all_elems, page_num, True, ord_column)
        return web_template.result_page(table + pages, "/meter-devices", str(stylesheet_number))


def all_worked_meter_devices(stylesheet_number: str) -> str:
    """Function create page with all meter devices in database"""

    with Database() as base:
        _, cursor = base
        devices = select_operations.get_all_worked_meter_devices(cursor)
        if len(devices) > config.max_records_in_page():
            return flask.redirect("/worked-meter-devices/page/1/1")
        links = ['/get-devices-reading/{}'.format(elem[0]) for elem in devices]
        table = uhtml.universal_table(table_headers.meter_devices_table_name, table_headers.meter_devices_table,
                                      devices, True, links)

        return web_template.result_page(table, "/meter-devices", str(stylesheet_number))


def all_worked_meter_devices_with_paging(page_num: int, stylesheet_number: str, ord_column=1) -> str:
    """Function create page with all meter devices in database"""

    with Database() as base:
        _, cursor = base
        devices = select_operations.get_all_worked_meter_devices_limit(cursor, page_num, True, ord_column)
        links = ['/get-devices-reading/{}'.format(elem[0]) for elem in devices]
        link = '/worked-meter-devices/page'
        all_elems = functions.list_of_pages(select_operations.get_all_worked_meter_devices(cursor))
        pages = uhtml.paging_table(link, all_elems, page_num, True, ord_column)
        headers = []
        for elem in table_headers.meter_devices_table_ext:
            headers.append(elem.format('/worked-meter-devices/page/{0}'.format(page_num)))
        table = uhtml.universal_table(table_headers.meter_devices_table_name, headers, devices, True, links)

        return web_template.result_page(table + pages, "/meter-devices", str(stylesheet_number))


def all_meter_devices_in_point_page(point_id: int, stylesheet_number: str) -> str:
    """Function create page with all meter devices in current point"""
    with Database() as base:
        _, cursor = base
        devices = select_operations.get_all_worked_meter_in_point(cursor, point_id)
        links = ['/get-devices-reading/{}'.format(elem[0]) for elem in devices]
        table = uhtml.universal_table(table_headers.meter_devices_table_name, table_headers.meter_devices_table,
                                      devices, True, links)
        devices_button = '<div id="navigation_div"><div class="navigation_elem">' \
                        '<a href="/add-meter-device-in-point/{0}">Добавить прибор учета</a></div>' \
                        '<div class="navigation_elem"><a href="/delete-meter-device-from-point/{0}">Удалить прибор учета</a></div>'  \
                        '</div>'.format(point_id)
        if functions.session['role'] == functions.ROLE_SUPERUSER:
            table1 = _table_with_schemes(point_id) + devices_button
        else:
            table1 = ''
        return web_template.result_page(table + table1, "/meter-devices", str(stylesheet_number))


def __all_calk_data_to_list(point_id: int) -> List[List]:
    """List[str] -> List[List[str]]"""
    with Database() as base:
        _, cursor = base
        raw_data = select_operations.get_all_full_calc_schemes_in_point(cursor, point_id)
        result = []
        len_small = len(table_headers.calc_schemes_table)
        try:
            for i in range(len(raw_data) // len_small):
                result.append(raw_data[i * len_small: (i + 1) * len_small])
        except TypeError:
            pass
        return result


def _table_with_schemes(point_id) -> str:
    """Function return table with all calculating schemes if they exist"""
    schemes = __all_calk_data_to_list(point_id)
    if len(schemes) == 0:
        result = ""
    else:
        result = uhtml.universal_table(table_headers.calc_schemes_table_name,
                                       table_headers.calc_schemes_table,
                                       schemes)
    return result


def all_reading_to_device_page(device_id: int, stylesheet_number: str) -> str:
    """Function create table with all reading to meter device with device_id"""

    with Database() as base:
        _, cursor = base
        readings = select_operations.get_all_reading_from_device(cursor, device_id)
        table = uhtml.universal_table(table_headers.readings_device_table_name, table_headers.readings_device_table,
                                      readings, False)

        pp_filename = '{}power_profiles/{}_pp.pdf'.format(config.static_dir() ,device_id)
        pp_exist = os.path.exists(pp_filename) and os.path.isfile(pp_filename)

        bar_part_1 = '<div id="navigation_div">' \
                        '<div class="navigation_elem">' \
                        '<a href="/to-only-reading/{0}">Только показания</a>' \
                        '</div>' \
                        '<div class="navigation_elem">' \
                        '<a href="/to-bar-meter/{0}">График расходов за периоды</a>' \
                        '</div>' \
                        '<div class="navigation_elem">' \
                        '<a href="/to-bar-meter-avr/{0}">График средних расходов</a>' \
                        '</div>' \
                        '<div class="navigation_elem">' \
                        '<a href="/to-bar-meter-mnth/{0}">График месячных расходов</a>' \
                        '</div>'.format(device_id)
        if pp_exist:
            bar_part_2 = '<div class="navigation_elem">'\
                            '<a href="/get-power-profile/{0}">Профиль мощности</a>'\
                            '</div>'\
                            '</div>'.format(device_id)
        else:
            bar_part_2 = '</div>'
        to_bar_button = '{}{}'.format(bar_part_1, bar_part_2)

        table_new = uhtml.add_new_reading(device_id)
        return web_template.result_page(table + to_bar_button + table_new, "/all-meter-devices", str(stylesheet_number))


def only_reading_to_device_page(device_id: int, stylesheet_number: str) -> str:
    """Function create page with simple table including all readings for this device meter"""
    with Database() as base:
        _, cursor = base
        device_info = select_operations.get_full_info_from_meter_device(cursor, device_id)
        if len(device_info) == 0:
            table = uhtml.data_is_not_valid()
        else:
            readings = select_operations.get_all_date_and_readings_from_device(cursor, device_id)
            table_name = table_headers.small_readings_table_name.format(device_info[0][3] + ' ' + device_info[0][2],
                                                                        device_info[0][9], device_info[0][1])
            table = uhtml.universal_table(table_name, table_headers.small_readings_table, readings)
    return web_template.result_page(table, '/get-devices-reading/{}'.format(device_id), stylesheet_number)


def power_profile_common(device_id: int,  stylesheet_number: str) -> Response:
    """If pdf exist then return current power profile"""
    try:
        return flask.send_from_directory(config.static_dir(), 'power_profiles/{0}_pp.pdf'.format(device_id))
    except:
        return abort(404)


def meter_readings_bar_page(device_id: int,  stylesheet_number: str) -> str:
    """Create simple bar with data from device meter"""
    with Database() as base:
        _, cursor = base
        try:
            readings = select_operations.get_all_reading_from_device(cursor, device_id)
            data = [(reading[6], reading[2]) for reading in readings]
            max_elem = max([reading[6] for reading in readings])
            data_new = list(map(lambda elem: (elem[0] * 400 / max_elem, '{0}\n{1}'.format(elem[0], elem[1])), data))
            table = render_template('techs/meter_bar.html', data=data_new)
        except:
            table = render_template('techs/error_meter_bar.html')
        return web_template.result_page(table, '/get-devices-reading/{}'.format(device_id), str(stylesheet_number))


def meter_readings_bar_page_avr(device_id: int,  stylesheet_number: str) -> str:
    """Create simple bar with data from device meter"""
    with Database() as base:
        _, cursor = base
        try:
            readings = select_operations.get_all_reading_from_device(cursor, device_id)
            data = [(reading[7], reading[2]) for reading in readings]
            max_elem = max([reading[7] for reading in readings])
            data_new = list(map(lambda elem: (elem[0] * 400 / max_elem, '{0}\n{1}'.format(elem[0], elem[1])), data))
            table = render_template('techs/meter_bar.html', data=data_new)
        except ValueError:
            table = render_template('techs/error_meter_bar.html')
        return web_template.result_page(table, '/get-devices-reading/{}'.format(device_id), str(stylesheet_number))


def last_24_monthly_expense_page(device_id: int, stylesheet_number: str) -> str:
    """Create simple bar with last_24_monthly_expense from device meter"""
    with Database() as base:
        _, cursor = base
        try:
            data = select_operations.get_last_24_monthly_expense(cursor, device_id)
            max_elem = max([reading[3] for reading in data])
            data_new = []
            # data_new liked [[id, date_begin, date_end, total, to_bar_total]]
            for row in data:
                data_new.append([])
                for elem in row:
                    data_new[-1].append(elem)
                data_new[-1].append(row[3] * 400 / max_elem)
            page = render_template('techs/meter_bar_extended.html', data=data_new)
        except ValueError:
            page = render_template('techs/error_meter_bar.html')
        return web_template.result_page(page, '/get-devices-reading/{}'.format(device_id), str(stylesheet_number))


def add_reading_method(data, method, stylesheet_number: str) -> str:
    """Function validate all data and if correct add record in devices rading history"""
    if method == 'POST':
        reading = data[uhtml.READING_NAME]
        device_id = data[uhtml.DEVICE_ID]
        pre_adr = '/get-devices-reading/{}'.format(device_id)
        reading_datetime = data[uhtml.WORK_DATETIME].replace("T", ' ')
        if reading_datetime.count(':') < 2: #YYYY-MM-DD HH:MM:SS
            reading_datetime += ':00'
        password = data[uhtml.PASSWORD]
        if functions.is_superuser_password(password):
            try:
                correct_reading = float(reading)
                if correct_reading >= 0:
                    with Database() as base:
                        connection, cursor = base
                        insert_new_reading_to_meter_device(cursor, device_id, reading_datetime, reading)
                        connection.commit()
                        page = uhtml.operation_completed()
                else:
                    page = uhtml.data_is_not_valid()
            except:
                page = uhtml.data_is_not_valid()
        else:
            page = uhtml.pass_is_not_valid()
        return web_template.result_page(page, pre_adr, str(stylesheet_number))
    else:
        return web_template.result_page("Method in Move Work not corrected!",
                                        "/all-meter-devices",
                                        str(stylesheet_number))


@replace_decor
def power_outages_page(stylesheet_number: str) -> str:
    """Function create page with all correct outages"""

    try:
        eens_list = [[elem['num'], elem['startDate'], elem['endDate'],
                      elem['objects'], elem['street'], elem['link']] for elem in get_eens_data()]
        for phone in eens_list:
            phone[-1] = '<a href="{}">Телефонограмма</a>'.format(phone[-1])

        table1 = render_template('any/universal_table.html', table_name=table_headers.eens_table_name,
                                 headers=table_headers.eens_table, data=eens_list,
                                 num_columns=len(table_headers.eens_table))
    except EeensException as e:
        table1 = render_template('any/universal_table.html', table_name='Данные Екатеринбургэнергосбыт недоступны',
                                 table_headers=[], date=[])

    try:
        eesk_list = [[elem[2], elem[3], elem[4], elem[6]] for elem in get_eesk_data()]
        table2 = render_template('any/universal_table.html', table_name=table_headers.eesk_table_name,
                                 headers=table_headers.eesk_table, data=eesk_list,
                                 num_columns=len(table_headers.eesk_table))
    except EeskException as e:
        table2 = render_template('any/universal_table.html', table_name='Данные Екатеринбургской Электросетевой Компании недоступны',
                                 table_headers=[], date=[])

    with Database() as base:
        _, cursor = base
        find_list = select_operations.get_all_find_patterns(cursor)
        table3 = render_template('any/universal_table.html', table_name='Список слов для поиска',
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
        all_meter_devices = select_operations.get_count_all_meter_devices(cursor)
        worked_meter_devices = select_operations.get_count_worked_meter_devices(cursor)
        hardware = web_template.faq_state_machine('hardware')
        tecnology = web_template.faq_state_machine('tecnology')
        multiuser = web_template.faq_state_machine('multiuser')
        update = web_template.faq_state_machine('update')
        all_counts = select_operations.get_all_counts_from_device_type(cursor)
        records = ['Единиц или групп оборудования на предприятиях: <a href="{0}/all-equips">{1}</a>'.
                   format(config.full_address(), count_equip),
                   'Предприятий всего: <a href="{0}/all-points">{1}</a>'.format(config.full_address(), max_point_id),
                   'Предприятий действующих: <a href="{0}/works-points">{1}</a>'.format(config.full_address(),
                                                                                        count_works_points),
                   'Произведенных работ: <a href="{0}/all-works">{1}</a>'.format(config.full_address(), count_works),
                   'Приборов учета зарегистрировано: <a href="/all-meter-devices">{0}</a>'.format(all_meter_devices),
                   'Из них работающих на данный момент:<a href="/worked-meter-devices">{0}</a>'.format(worked_meter_devices),
                   ]
        for elem in all_counts:
            records.append('Тип учета {}: {} шт.'.format(elem[0], elem[1]))
        database_size = select_operations.get_size_database(cursor)
        average_works_in_date = "{:.2f}".format(select_operations.get_count_unique_works(cursor) /
                                               select_operations.get_count_unique_dates_in_works(cursor))
        main_table = render_template('any/faq.html', hardware=hardware, tecnology=tecnology, multiuser=multiuser,
                                     update=update, records=records, database_size=database_size,
                                     average_works_in_date=average_works_in_date)
        return web_template.result_page(main_table,
                                        pre_adr,
                                        str(stylesheet_number))


def statistics_page(preview_page, stylesheet_number: str, ord_column=1) -> str:
    """Function create STATISTIC web-page"""
    with Database() as base:
        _, cursor = base
        statistics = select_operations.get_statistic(cursor, True, ord_column)
        links_list = ['/equip/' + str(elem[0]) for elem in statistics]
        headers = []
        for elem in table_headers.statistics_table_ext:
            headers.append(elem.format('/statistics'))

        result = uhtml.universal_table(table_headers.statistics_table_name,
                                       headers,
                                       [[elem[i] for i in range(1, len(elem))]
                                        for elem in statistics],
                                       True,
                                       links_list)
        return web_template.result_page(result, preview_page, str(stylesheet_number))


def system_status_page(preview_page, stylesheet_number: str) -> str:
    """Function create System-Status Web-page"""
    current_status = system_status.SystemStatus.get_status()
    status_to_list = [[key, current_status[key]] for key in current_status]
    result = render_template('any/system_status.html', parameters=status_to_list)
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
