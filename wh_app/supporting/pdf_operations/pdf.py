"""This module create and save pdf-documents"""

from fpdf import FPDF, HTMLMixin
from typing import List, Any, Tuple

from wh_app.postgresql.database import Database
from wh_app.supporting import functions
from wh_app.sql_operations import select_operations
from wh_app.config_and_backup import table_headers

functions.info_string(__name__)


class HTML2PDF(FPDF, HTMLMixin):
    pass


def equips_in_point(point_id: int) -> FPDF:
    """Create pdf contain all equips in current_point"""

    with Database() as base:
        _, cursor = base
        all_equips = select_operations.get_equip_in_point(cursor, str(point_id))
        pdf = create_document('Portrait')
        pdf.write_html(make_html_table(all_equips, table_headers.equips_table_to_pdf, 'Portrait'),
                       table_line_separators=True)
        return pdf


def works_from_equip(equip_id: int) -> FPDF:
    """Create pdf contain all works from current equip"""

    with Database() as base:
        _, cursor = base
        all_works = select_operations.get_works_from_equip_id(cursor, str(equip_id))
        pdf = create_document('Landscape')
        pdf.write_html(make_html_table(all_works, table_headers.works_table[:len(table_headers.works_table) - 1],
                                       'Landscape'),
                       table_line_separators=True)
        return pdf


def move_equip(equip_id: int) -> FPDF:
    """Create pdf contain all records from current equip"""

    with Database() as base:
        _, cursor = base
        all_records = []
        equip_info = [str(equip_id)] + \
                     select_operations.get_full_equip_information(cursor, str(equip_id))
        all_records.insert(0, equip_info)
        while str(equip_info[0]) != str(equip_info[5]):
            old_equip_id = str(equip_info[5])
            equip_info = [old_equip_id] + \
                         select_operations.get_full_equip_information(cursor, old_equip_id)
            all_records.insert(0, equip_info)
        pdf = create_document('Portrait')
        pdf.write_html(make_html_table(all_records, table_headers.remove_table, 'Portrait'),
                       table_line_separators=True)
        return pdf


def works_from_performer(performer_id: int) -> FPDF:
    """Create PDF contain all works from current performer"""

    with Database() as base:
        _, cursor = base
        all_works = select_operations.get_all_works_from_worker_id(cursor, str(performer_id))
        pdf = create_document('Landscape')
        pdf.write_html(make_html_table(all_works,
                                       table_headers.works_table[: len(table_headers.works_table) - 1],
                                       'Landscape'),
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
                                        ['{0} Договор'.format(table[i]), '{0} Описание'.format(table[i])],
                                        'Landscape')
            pdf.write_html(tmp_table)

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
        print(pdf.font_family)
        html = list()
        html.append('<h3 align="center">По дням недели</h3>')
        html.append('<table border="1"><tbody><tr>')
        for name in table_headers.workers_days_table:
            html.append('<td width="{1}%">{0}</td>'.format(name, int(100 / len(table_headers.workers_days_table))))
        html.append('</tr>')
        for human in days_human_view:
            html.append('<tr>')
            for elem in human:
                html.append('<td>{0}</td>'.format(elem))
            html.append('</tr>')
        html.append('</tbody></table>')
        html.append('<h3 align="center">Контакты</h3>')
        html.append('<table border="1"><tbody><tr>')
        humans = select_operations.get_all_workers_real(cursor)
        workers_short_table = [('ФИО', '30%'), ('Телефон', '15%'), ('Должность', '55%')]
        for cell in workers_short_table:
            html.append('<td width="{1}">{0}</td>'.format(cell[0], cell[1]))
        html.append('</tr>')
        for human in humans:
            html.append('<tr><td>{0} {1}</td>'.format(human[1], human[2]))
            html.append('<td>{0}</td>'.format(human[3]))
            html.append('<td>{0}</td></tr>'.format(human[5]))
        html.append('</tbody></table>')
        html.append('<h3 align="center">Данный график не учитывает праздничные, больничные и отпускные</h3>')
        pdf.write_html("".join(html), table_line_separators=True)
        return pdf


def create_document(orientation: str) -> HTML2PDF:
    """Create main document/ Orientation may be Landscape or Portrait"""

    pdf = HTML2PDF()
    pdf.add_font('DejaVu',
                 '',
                 '/home/saibogo/PycharmProjects/work_history/wh_app/supporting/pdf_operations/DejaVuSansCondensed.ttf',
                 uni=True)
    pdf.set_font('DejaVu', '', 10)
    pdf.add_page(orientation)
    return pdf


def make_html_table(data: List[Tuple[Any]], header: List[str], orientation: str="Portrait") -> str:
    """Create <table>...</table><table1>...</table1> from data-list"""

    result = list()
    if len(header) != len(data[0]):
        result.append("<h1>Ошибка соответствия таблицы и заголовка!</h1>")
    else:
        for row in data:
            result.append('<table border="1"><thead><tr><th></th></tr></thead><tbody>')
            for count, elem in enumerate(row):
                result.append('<tr>')

                max_line_len = (80 if orientation == "Portrait" else 140) - len(header[count])
                lines: List[str] = list()
                for i in range(0, len(str(elem)), max_line_len):
                    lines.append(str(elem)[i : i + max_line_len])

                if len(lines) > 1:
                    result.append('<td width="100%">{0}:</td>'.format(header[count]))
                    for line in lines:
                        result.append('</tr><tr>')
                        result.append('<td width="100%">{0}</td>'.format(line))
                else:
                    result.append('<td width="100%">{1}: {0}</td>'.format(elem, header[count]))
                result.append('</tr>')
            result.append('</tbody></table>')
    return "".join(result)

