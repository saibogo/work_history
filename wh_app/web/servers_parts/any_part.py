"""This module contain any actions for Flask server.py"""

from fpdf import FPDF
from wh_app.web.servers_parts.support_part import *
from wh_app.web.any_section import main_web_menu, faq_page, statistics_page,\
    system_status_page, viev_changelog
from wh_app.supporting.pdf_operations.pdf import equips_in_point, works_from_equip,\
    works_from_performer, weekly_charts_pdf, move_equip, point_tech_information, find_work_without_date, find_equip,\
    find_point, find_work_with_date, works_from_performer_with_date


@app.route("/")
def main_page() -> Response:
    """Return main web-page"""
    return goto_or_redirect(lambda:  main_web_menu(stylesheet_number()))


@app.route("/FAQ", methods=['GET'])
def faq() -> Response:
    """Return FAQ-page"""
    return goto_or_redirect(lambda: faq_page(request.args.get('page',
                                                              default=config.full_address(),
                                                              type=str),
                                             stylesheet_number()))


@app.route('/statistics', methods=['GET'])
def statistics() -> Response:
    """Return STATISTIC-page"""
    return goto_or_redirect(lambda: statistics_page(request.args.get('page',
                                                                     default=config.full_address(),
                                                                     type=str),
                                                    stylesheet_number()))


@app.route('/system-status', methods=['GET'])
def system_status() -> Response:
    """Return page, contain status all system components"""
    return goto_or_redirect(lambda: system_status_page(request.args.get('page',
                                                                        default=config.full_address(),
                                                                        type=str),
                                                       stylesheet_number()))


@app.route('/changelog-page')
def changelog_page() -> Response:
    """Return ALL CHANGELOG page"""
    return goto_or_redirect(lambda: viev_changelog(stylesheet_number()))


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
                     "find-work-with-date": find_work_with_date}
    lst_data = data.split('=')
    if len(lst_data) == 2:
        section, value = lst_data
    elif len(lst_data) == 3:
        section, value, page_num = lst_data
    elif len(lst_data) == 5:
        section, value, date1, date2, page_num = lst_data
    else:
        print("Команда {} для формирования PDF не опознана".format(data))
    try:
        if len(lst_data) == 2:
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


