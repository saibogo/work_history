"""This module contain any actions for Flask server.py"""

from fpdf import FPDF
from wh_app.web.servers_parts.support_part import *
from wh_app.web.any_section import main_web_menu, faq_page, statistics_page,\
    system_status_page, view_changelog, view_changelog_page, external_services_page, power_outages_page
from wh_app.supporting.pdf_operations.pdf import equips_in_point, works_from_equip,\
    works_from_performer, weekly_charts_pdf, move_equip, point_tech_information, find_work_without_date, find_equip,\
    find_point, find_work_with_date, works_from_performer_with_date, top10workers, top10points, top10equips,\
    work_from_id, order_to_pdf, no_closed_orders, all_orders, schedule_td, schedule_wk


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


@app.route('/statistics', methods=['GET'])
def statistics() -> Response:
    """Return STATISTIC-page"""
    return goto_or_redirect(lambda: statistics_page(request.args.get('page',
                                                                     default=config.full_address(),
                                                                     type=str),
                                                    stylesheet_number()), functions.NO_ROLE)


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


