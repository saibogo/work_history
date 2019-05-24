__author__ = "Andrey Gleykh"
__license__ = "GPL"
__email__ = "gleykh@gmail.com"
__status__ = "Prototype"


def link_or_str(elem: str, link_type: bool = False, link: str = '') -> str:
    """Function return simple string or link-string"""
    return '<a href="' + str(link) + '">' + str(elem) + '</a>' if link_type else str(elem)


def style_custom():
    """Function return string contain sections <style>"""
    result = list()
    result.append('<style>')
    result.append('body {background: Khaki; color: MidnightBlue}')
    result.append('table {background: Khaki}')
    result.append('caption {color: Navy; font-size: large; font-style: italic}')
    result.append('th {font-style: italic}')
    result.append('a:link {color: DarkSlateGrey; text-decoration: none}')
    result.append('a:visited {color: DarkSlateGrey; text-decoration: none}')
    result.append('a:hover {color: Purple; text-decoration: none; background: DarkKhaki}')
    result.append('a:active {color: DarkSlateGrey; text-decoration: none; font-size: large}')
    result.append('</style>')
    return '\n'.join(result)


def universal_table(name: str, headers: list, data: list, links: bool = False, links_list: list = []) -> str:
    """Function return string contain html-table"""
    result = [style_custom()]
    result.append('<table align="center" border=2><caption>' + str(name) + '</caption>')
    result.append('<tr>' + "".join(['<th>' + str(elem) + '</th>' for elem in headers]) + '</tr>')
    for i in range(len(data)):
        result.append('<tr>' + "".join(['<td>' + link_or_str(elem, links, links_list[i] if links else '') +
                                        '</td>' for elem in data[i]]) + '</tr>')

    return "\n".join(result)
