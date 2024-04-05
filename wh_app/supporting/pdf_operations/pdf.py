"""This module create and save pdf-documents"""

from fpdf import FPDF, HTMLMixin
from typing import List, Any, Tuple
from flask import render_template

from wh_app.postgresql.database import Database
from wh_app.supporting import functions
from wh_app.sql_operations import select_operations
from wh_app.config_and_backup import table_headers
from wh_app.config_and_backup.config import path_to_fonts
from wh_app.web.orders_section import _correct_orders_table

functions.info_string(__name__)


class HTML2PDF(FPDF, HTMLMixin):
    pass


normal_font_path = "{}{}".format(path_to_fonts() ,'DejaVuSansCondensed.ttf')
bold_font_path = "{}{}".format(path_to_fonts(), 'DejaVuSansCondensed-Bold.ttf')
font_size = 10
font_alias = 'DejaVu'


def equips_in_point(point_id: int) -> FPDF:
    """Create pdf contain all equips in current_point"""

    with Database() as base:
        _, cursor = base
        all_equips = select_operations.get_equip_in_point(cursor, str(point_id))
        pdf = create_document('Landscape')
        table = make_html_table(all_equips, table_headers.equips_table_to_pdf)
        pdf.write_html(table ,table_line_separators=True)
        return pdf


def works_from_equip(equip_id: int, page_num: int) -> FPDF:
    """Create pdf contain all works from current equip"""

    with Database() as base:
        _, cursor = base
        all_works = select_operations.get_works_from_equip_id_limit(cursor, str(equip_id), page_num)
        pdf = create_document('Landscape')
        pdf.write_html(make_html_table(all_works, table_headers.works_table[:len(table_headers.works_table) - 1]),
                       table_line_separators=True)
        return pdf


def find_work_without_date(find_string: str, page_num: int) -> FPDF:
    """Create PDf contain all works likes string without date"""

    with Database() as base:
        _, cursor = base
        all_works = select_operations.get_all_works_like_word_limit(cursor, find_string, int(page_num))
        pdf = create_document('Landscape')
        pdf.write_html(make_html_table(all_works, table_headers.works_table[:len(table_headers.works_table) - 1]),
                       table_line_separators=True)
        return pdf


def find_work_with_date(find_string: str, date_start: str, date_stop: str, page_num: int) -> FPDF:
    """Create PDf contain all works likes string without date"""

    with Database() as base:
        _, cursor = base
        all_works = select_operations.get_all_works_like_word_and_date_limit(cursor, find_string, date_start,
                                                                             date_stop, int(page_num))
        pdf = create_document('Landscape')
        pdf.write_html(make_html_table(all_works, table_headers.works_table[:len(table_headers.works_table) - 1]),
                       table_line_separators=True)
        return pdf


def find_equip(find_string: str, page_num: int) -> FPDF:
    """Create PDF contain all equips likes find-string"""
    with Database() as base:
        _, cursor = base
        all_equips = select_operations.get_all_equips_list_from_like_str_limit(cursor, find_string, int(page_num))
        pdf = create_document('Landscape')
        pdf.write_html(make_html_table(all_equips, table_headers.equips_table_to_pdf), table_line_separators=True)
        return pdf


def find_point(find_string: str, page_num: int) -> FPDF:
    """Create PDF contain all equips likes find-string"""
    with Database() as base:
        _, cursor = base
        all_points = select_operations.get_all_points_list_from_like_str_limit(cursor, find_string, int(page_num))
        pdf = create_document('Landscape')
        local_headers = ['ID'] + table_headers.points_table[:len(table_headers.points_table) - 2]
        pdf.write_html(make_html_table(all_points, local_headers),
                       table_line_separators=True)
        return pdf


def move_equip(equip_id: int) -> FPDF:
    """Create pdf contain all records from current equip"""

    with Database() as base:
        _, cursor = base
        all_records = []
        equip_info = [str(equip_id)] + select_operations.get_full_equip_information(cursor, str(equip_id))
        all_records.insert(0, equip_info)
        while str(equip_info[0]) != str(equip_info[5]):
            old_equip_id = str(equip_info[5])
            equip_info = [old_equip_id] + \
                         select_operations.get_full_equip_information(cursor, old_equip_id)
            all_records.insert(0, equip_info)
        pdf = create_document('Portrait')
        pdf.write_html(make_html_table(all_records, table_headers.remove_table),
                       table_line_separators=True)
        return pdf


def works_from_performer(performer_id: int, page_num: int) -> FPDF:
    """Create PDF contain all works from current performer"""

    with Database() as base:
        _, cursor = base
        all_works = select_operations.get_all_works_from_worker_id_limit(cursor, str(performer_id), page_num)
        pdf = create_document('Landscape')
        pdf.write_html(make_html_table(all_works,
                                       table_headers.works_table[: len(table_headers.works_table) - 1]),
                       table_line_separators=True)
        return pdf


def works_from_performer_with_date(performer_id: int, date_start: str, date_stop: str, page_num: int) -> FPDF:
    """Create PDF contain all works from current performer"""

    with Database() as base:
        _, cursor = base
        all_works = select_operations.get_works_from_performer_and_date(cursor, performer_id,
                                                                        date_start, date_stop, int(page_num))
        pdf = create_document('Landscape')
        pdf.write_html(make_html_table(all_works,
                                       table_headers.works_table[: len(table_headers.works_table) - 1]),
                       table_line_separators=True)
        return pdf


def point_tech_information(point_num: int) -> FPDF:
    """Create PDF contain all technical information from current point"""

    def if_tech_list_empthy(lst: list) -> list:
        """Replace data if data not found"""

        if not lst:
            return ["Нет данных"] * 4
        else:
            return lst[0]

    pdf = create_document('Landscape')

    with Database() as base:
        _, cursor = base
        info_list = [select_operations.get_electric_point_info(cursor, str(point_num)),
                     select_operations.get_cold_water_point_info(cursor, str(point_num)),
                     select_operations.get_hot_water_point_info(cursor, str(point_num)),
                     select_operations.get_heating_point_info(cursor, str(point_num)),
                     select_operations.get_sewerage_point_info(cursor, str(point_num))]
        table = table_headers.point_tech_table[1: ]
        for i in range(len(info_list)):
            tmp_table = make_html_table([if_tech_list_empthy(info_list[i])[ 2 : ]],
                                        ['{0} Договор'.format(table[i]), '{0} Описание'.format(table[i])])
            pdf.write_html(tmp_table)

    return pdf


def work_from_id(work_id: int) -> FPDF:
    """Create PDF contain all technical information from current point"""
    pdf = create_document('Landscape')
    with Database() as base:
        _, cursor = base
        html = make_html_table([select_operations.get_full_information_to_work(cursor, work_id)],
                               table_headers.works_table[:len(table_headers.works_table) - 1])
        pdf.write_html(html)
    return pdf


def weekly_charts_pdf(values: Any) -> FPDF:
    """Create PDF contain all works days to all workers"""

    with Database() as base:
        _, cursor = base
        days = select_operations.get_weekly_chart(cursor)
        days_human_view = list()
        for human in days:
            days_human_view.append(list())
            days_human_view[-1].append(human[0])
            for i in range(1, len(human)):
                days_human_view[-1].append("Работает" if human[i] else "Выходной")
        pdf = create_document('Landscape')
        html = render_template('pdf/workers.html', days_names=table_headers.workers_days_table,
                               humans_days=days_human_view, humans=select_operations.get_all_workers_real(cursor))
        pdf.write_html("".join(html), table_line_separators=True)
        return pdf


def top10workers() -> FPDF:
    """Create PDF contain top 10 workers table"""
    with Database() as base:
        _, cursor = base
        pdf = create_document('Landscape')
        html = make_html_table(select_operations.get_top_10_workers(cursor), table_headers.top_10_workers_table)
        pdf.write_html(html, table_line_separators=True)
        return pdf


def top10points() -> FPDF:
    """Create PDF contain top 10 workers table"""
    with Database() as base:
        _, cursor = base
        pdf = create_document('Landscape')
        html = make_html_table(select_operations.get_top_10_points(cursor), table_headers.top_10_points)
        pdf.write_html(html, table_line_separators=True)
        return pdf


def top10equips() -> FPDF:
    """Create PDF contain top 10 workers table"""
    with Database() as base:
        _, cursor = base
        pdf = create_document('Landscape')
        html = make_html_table(select_operations.get_top_10_works(cursor), table_headers.top_10_equips)
        pdf.write_html(html, table_line_separators=True)
        return pdf


def order_to_pdf(order_id: int) -> FPDF:
    """Create PDF table contain full info from order = order_id"""
    with Database() as base:
        _, cursor = base
        pdf = create_document('Landscape')
        order_info = select_operations.get_order_from_id(cursor, order_id)
        correct_order = _correct_orders_table([order_info])
        order = [correct_order[0][: len(correct_order[0]) - 1]]
        html = make_html_table(order, table_headers.orders_table[ :len(table_headers.orders_table) - 1])
        pdf.write_html(html, table_line_separators=True)
        return pdf


def no_closed_orders(page_num: int) -> FPDF:
    """Create PDF table contain all noclosed orders table with paging. Page = 0 -> all noclosed orders"""
    with Database() as base:
        _, cursor = base
        pdf = create_document('Landscape')
        if int(page_num) != 0:
            orders = select_operations.get_all_no_closed_orders_limit(cursor, page_num)
        else:
            orders = select_operations.get_all_no_closed_orders(cursor)
        correct_orders = _correct_orders_table(orders)
        for i in range(len(orders)):
            correct_orders[i] = correct_orders[i][ : len(correct_orders[i]) - 1]
        html = make_html_table(correct_orders, table_headers.orders_table_no_closed[:len(table_headers.orders_table)])
        pdf.write_html(html, table_line_separators=True)
        return pdf


def all_orders(page_num: int) -> FPDF:
    """Create PDF table contain all noclosed orders table with paging. Page = 0 -> all noclosed orders"""
    with Database() as base:
        _, cursor = base
        pdf = create_document('Landscape')
        if int(page_num) != 0:
            orders = select_operations.get_all_orders_limit(cursor, page_num)
        else:
            orders = select_operations.get_all_orders(cursor)
        correct_orders = _correct_orders_table(orders)
        for i in range(len(orders)):
            correct_orders[i] = correct_orders[i][ : len(correct_orders[i]) - 1]
        html = make_html_table(correct_orders, table_headers.orders_table[:len(table_headers.orders_table) - 1])
        pdf.write_html(html, table_line_separators=True)
        return pdf


def create_document(orientation: str) -> HTML2PDF:
    """Create main document/ Orientation may be Landscape or Portrait"""

    pdf = HTML2PDF(font_cache_dir=None)
    try:
        pdf.add_font('DejaVu', style='', fname=normal_font_path, uni=True)
        pdf.add_font('DejaVu', style='B', fname=bold_font_path, uni=True)
    except:
        print("Невозможно добавить шрифт")
    try:
        pdf.set_font(font_alias, '', font_size)
    except:
        print("Невозможно зарегистрировать шрифт")
    pdf.add_page(orientation)
    return pdf


def make_html_table(data: List[Tuple[Any]], header: List[str]) -> str:
    """Create <table>...</table><table1>...</table1> from data-list"""

    if len(header) != len(data[0]):
        result = render_template("pdf_template.html", not_corrected=True)
    else:
        result = render_template("pdf/pdf_template.html", not_corrected=False, header=header, data=data)

    return result

