"""This module contain any actions for Flask server.py"""

from fpdf import FPDF
from wh_app.web.servers_parts.support_part import *
from wh_app.web.any_section import (main_web_menu, faq_page, statistics_page,\
    system_status_page, view_changelog, view_changelog_page, external_services_page, power_outages_page,\
    meter_devices_menu_page, all_meter_devices_page, all_reading_to_device_page, add_reading_method,\
    all_meter_devices_in_point_page, meter_readings_bar_page, meter_readings_bar_page_avr, all_worked_meter_devices,\
    only_reading_to_device_page, last_24_monthly_expense_page, all_meter_devices_with_paging,\
    all_worked_meter_devices_with_paging, power_profile_common, add_meter_device_form, add_meter_device_method,
                                    user_manual_page, trivial_manual_page)
from wh_app.supporting.pdf_operations.pdf import equips_in_point, works_from_equip,\
    works_from_performer, weekly_charts_pdf, move_equip, point_tech_information, find_work_without_date, find_equip,\
    find_point, find_work_with_date, works_from_performer_with_date, top10workers, top10points, top10equips,\
    work_from_id, order_to_pdf, no_closed_orders, all_orders, schedule_td, schedule_wk, order_to_pdf_in_point


@app.route("/")
def main_page() -> Response:
    """Return main web-page"""
    return goto_or_redirect(lambda:  main_web_menu(stylesheet_number()), functions.NO_ROLE)


@app.route("/access-denied")
def access_denied() -> str:
    """Return Access Is Denied"""
    return result_page("<h2>Доступ к данному разделу для данного пользователя запрещен!</h2>", '/login', stylesheet_number())


@app.route("/FAQ", methods=['GET'])
def faq() -> Response:
    """Return FAQ-page"""
    return goto_or_redirect(lambda: faq_page(request.args.get('page',
                                                              default=config.full_address(),
                                                              type=str),
                                             stylesheet_number()), functions.NO_ROLE)


@app.route("/external-services")
def external_services() -> Response:
    """Return page with list of external services"""
    return goto_or_redirect(lambda: external_services_page(stylesheet_number()), functions.NO_ROLE)


@app.route("/power-outages")
def power_outages() -> Response:
    """Return page with list of external services"""
    return goto_or_redirect(lambda: power_outages_page(stylesheet_number()), functions.NO_ROLE)


@app.route("/meter-devices")
def meter_devices() -> Response:
    """Goto to page with menu included all action with meter devices"""

    return goto_or_redirect(lambda: meter_devices_menu_page(stylesheet_number()), functions.ROLE_WORKER)


@app.route("/all-meter-devices")
def all_meter_devices() -> Response:
    """Goto to page with all meter devices in database"""

    return goto_or_redirect(lambda: all_meter_devices_page(stylesheet_number()), functions.ROLE_WORKER)


@app.route("/all-meter-devices/page/<page_num>")
def all_meter_devices_paging(page_num: int) -> Response:
    """Goto to page with all meter devices in database"""

    return goto_or_redirect(lambda: all_meter_devices_with_paging(page_num, stylesheet_number()), functions.ROLE_WORKER)


@app.route("/all-meter-devices/page/<page_num>/<ord_column>")
def all_meter_devices_paging_ord(page_num: int, ord_column: int) -> Response:
    """Goto to page with all meter devices in database"""

    return goto_or_redirect(lambda: all_meter_devices_with_paging(page_num, stylesheet_number(), ord_column),
                            functions.ROLE_WORKER)


@app.route("/worked-meter-devices")
def all_worked_devices() -> Response:
    """Goto to page with all meter devices in database"""

    return goto_or_redirect(lambda: all_worked_meter_devices(stylesheet_number()), functions.ROLE_WORKER)


@app.route("/worked-meter-devices/page/<page_num>/<ord_column>")
def all_worked_devices_paging(page_num: int, ord_column: int) -> Response:
    """Goto to page with all meter devices in database"""

    return goto_or_redirect(lambda: all_worked_meter_devices_with_paging(page_num, stylesheet_number(), ord_column),
                            functions.ROLE_WORKER)


@app.route('/get-devices-reading/<device_id>')
def get_devices_reading(device_id: int) -> Response:
    """Goto to page with all records from current meter device"""

    return goto_or_redirect(lambda: all_reading_to_device_page(int(device_id), stylesheet_number()), functions.ROLE_WORKER)


@app.route('/add-meter-device-in-point/<point_num>')
def add_meter_device_in_form(point_num: int) -> Response:
    """Goto to form addiction new meter device"""

    return goto_or_redirect(lambda: add_meter_device_form(int(point_num), stylesheet_number()), functions.ROLE_SUPERUSER)


@app.route('/add-new-meter-device', methods=['POST'])
def add_new_meter_device_common() -> Response:
    """Go to analyze and create new meter device"""
    return goto_or_redirect(lambda: add_meter_device_method(functions.form_to_data(request.form), request.method,
                                                       stylesheet_number()), functions.ROLE_SUPERUSER)


@app.route('/meters-in-point/<point_id>')
def meters_in_point(point_id: int) -> Response:
    """Go to page with meter devices table"""
    return goto_or_redirect(lambda: all_meter_devices_in_point_page(int(point_id), stylesheet_number()), functions.ROLE_WORKER)


@app.route('/to-only-reading/<device_id>')
def to_only_reading(device_id: int) -> Response:
    """Goto to create simple table with all records for this meter device"""
    return goto_or_redirect(lambda: only_reading_to_device_page(device_id, stylesheet_number()), functions.ROLE_WORKER)


@app.route('/to-bar-meter/<device_id>')
def to_bar_meter(device_id: int) -> Response:
    """Goto to simple bar with data from device meter with id = device_id"""
    return goto_or_redirect(lambda: meter_readings_bar_page(device_id, stylesheet_number()), functions.ROLE_WORKER)


@app.route('/to-bar-meter-avr/<device_id>')
def to_bar_meter_avr(device_id: int) -> Response:
    """Goto to simple bar with data from device meter with id = device_id"""
    return goto_or_redirect(lambda: meter_readings_bar_page_avr(device_id, stylesheet_number()), functions.ROLE_WORKER)


@app.route('/to-bar-meter-mnth/<device_id>')
def to_bar_meter_mounths(device_id: int) -> Response:
    """Goto to simple bar with last_24_monthly_expense from device meter with id = device_id"""
    return goto_or_redirect(lambda: last_24_monthly_expense_page(device_id, stylesheet_number()), functions.ROLE_SUPERUSER)


@app.route('/get-power-profile/<device_id>')
def get_power_profile(device_id: int) -> Response:
    """Goto to get pdf with current power profile if exist"""

    return goto_or_redirect(lambda: power_profile_common(device_id, stylesheet_number()), functions.ROLE_SUPERUSER)


@app.route('/add-reading', methods=['POST'])
def add_reading() -> Response:
    """Goto to method add new record in history devices_readings"""
    return goto_or_redirect(lambda: add_reading_method(functions.form_to_data(request.form), request.method,
                                                       stylesheet_number()), functions.ROLE_WORKER)


@app.route('/statistics/<ord_column>', methods=['GET'])
def statistics(ord_column: int) -> Response:
    """Return STATISTIC-page"""
    return goto_or_redirect(lambda: statistics_page(request.args.get('page',
                                                                     default=config.full_address(),
                                                                     type=str),
                                                    stylesheet_number(), ord_column), functions.NO_ROLE)


@app.route('/system-status', methods=['GET'])
def system_status() -> Response:
    """Return page, contain status all system components"""
    return goto_or_redirect(lambda: system_status_page(request.args.get('page',
                                                                        default=config.full_address(),
                                                                        type=str),
                                                       stylesheet_number()), functions.NO_ROLE)


@app.route('/changelog-page')
def changelog_page() -> Response:
    """Return ALL CHANGELOG page"""
    return goto_or_redirect(lambda: view_changelog(stylesheet_number()), functions.NO_ROLE)


@app.route('/changelog-page/page/<page_num>')
def changelog_page_paging(page_num: int) -> Response:
    """Return ALL CHANGELOG page"""
    return goto_or_redirect(lambda: view_changelog_page(int(page_num), stylesheet_number()), functions.NO_ROLE)


@app.route("/table-to-pdf/<data>")
def html_table_to_pdf(data:str) -> Response:
    """Redirect to method generate pdf-version current main-table
    correct adr /table-to-pdf/<section>=<value> or /table-to-pdf/<section>=<value>=<page_num>"""

    command_table = {"point": equips_in_point,
                     "equip": works_from_equip,
                     "performer": works_from_performer,
                     "performer-with-date": works_from_performer_with_date,
                     "weekly": weekly_charts_pdf,
                     "move-equip-pdf": move_equip,
                     "point-tech": point_tech_information,
                     "find-work-not-date": find_work_without_date,
                     "find-equip": find_equip,
                     "point": find_point,
                     "find-work-with-date": find_work_with_date,
                     "top10workers": top10workers,
                     "top10points": top10points,
                     "top10equips": top10equips,
                     "work": work_from_id,
                     "order-to-pdf": order_to_pdf,
                     "order-to-pdf-in-point": order_to_pdf_in_point,
                     "no-closed-orders": no_closed_orders,
                     "all-orders": all_orders,
                     "schedule-td": schedule_td,
                     "schedule-wk": schedule_wk}

    lst_data = data.split('=')
    if len(lst_data) == 1:
        section = lst_data[0]
    elif len(lst_data) == 2:
        section, value = lst_data
    elif len(lst_data) == 3:
        section, value, page_num = lst_data
    elif len(lst_data) == 5:
        section, value, date1, date2, page_num = lst_data
    else:
        print("Команда {} для формирования PDF не опознана".format(data))
    try:
        if len(lst_data) == 1:
            pdf = command_table[section]()
        elif len(lst_data) == 2:
            pdf = command_table[section](value)
        elif len(lst_data) == 5:
            pdf = command_table[section](value, date1, date2, page_num)
        else:
            pdf = command_table[section](value, page_num)
    except Exception as err:
        print(err)
        pdf: FPDF = FPDF()

    pdf.output(config.path_to_pdf())
    return send_file(config.path_to_pdf()) \
        if section == "weekly" \
        else goto_or_redirect(lambda : send_file(config.path_to_pdf()))


@app.route('/user-manual')
def user_manual() -> Response:
    """Redirect to page with all information to use system"""

    return goto_or_redirect(lambda: user_manual_page(stylesheet_number()), functions.NO_ROLE)

@app.route('/trivial_manual.html')
def trivial_manual() -> Response:
    """Redirect to mage with manual to trivial user"""

    return goto_or_redirect(lambda: trivial_manual_page(stylesheet_number()), functions.NO_ROLE)


