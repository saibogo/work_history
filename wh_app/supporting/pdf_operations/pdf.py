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
        pdf.write_html(make_html_table(all_works, table_headers.works_table, 'Landscape'),
                       table_line_separators=True)
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

