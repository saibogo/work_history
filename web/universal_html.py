__author__ = "Andrey Gleykh"
__license__ = "GPL"
__email__ = "gleykh@gmail.com"
__status__ = "Prototype"


def link_or_str(elem: str, link_type: bool = False, link: str = '') -> str:
    """Function return simple string or link-string"""
    return '<a href="' + str(link) + '">' + str(elem) + '</a>' if link_type else str(elem)


def style_custom() -> str:
    """Function return string contain sections <style>"""
    result = list()
    result.append('<style>')
    result.append('body {background: Khaki; color: MidnightBlue}')
    result.append('h1 {text-align: center}')
    result.append('table {background: Khaki; border: 3px solid; margin: auto}')
    result.append('caption {color: Navy; font-size: large; font-style: italic}')
    result.append('th {font-style: italic; border: 1px solid}')
    result.append('td {font-style: italic; border: 1px solid}')
    result.append('a:link {color: DarkSlateGrey; text-decoration: none}')
    result.append('a:visited {color: DarkSlateGrey; text-decoration: none}')
    result.append('a:hover {color: Purple; text-decoration: none; background: DarkKhaki}')
    result.append('a:active {color: DarkSlateGrey; text-decoration: none; font-size: large}')
    result.append('</style>')
    return '\n'.join(result)


def universal_table(name: str, headers: list, data: list, links: bool = False, links_list: list = []) -> str:
    """Function return string contain html-table"""
    result = list()
    result.append(style_custom())
    result.append('<table><caption>' + str(name) + '</caption>')
    result.append('<tr>' + "".join(['<th>' + str(elem) + '</th>' for elem in headers]) + '</tr>')
    for i in range(len(data)):
        result.append('<tr>' + "".join(['<td>' + link_or_str(elem, links, links_list[i] if links else '') +
                                        '</td>' for elem in data[i]]) + '</tr>')

    return "\n".join(result)


def add_new_point() -> str:
    """Function return string contain form to add new point"""
    result = list()
    result.append('<table><caption> Добавить новое предприятие</caption>')
    result.append('<tr><th>Название</th><th>Адрес</th><th>Пароль доступа</th><th></th></tr>')
    result.append('<form action="/add-point" method="post"><tr>')
    result.append('<td><input name="point_name"></td>')
    result.append('<td><input name="point_addres"></td>')
    result.append('<td><input type="password" name="password"></td>')
    result.append('<td><input type="submit" value="Отправить"></td>')
    result.append('</tr></form></table>')
    return "\n".join(result)


def add_new_equip(point_id: str) -> str:
    """Function return string contain form to add new equipment"""
    result = list()
    result.append('<table><caption>Добавить новое оборудование</caption>')
    result.append('<tr><th>ID предприятия.</th><th>Наименование</th><th>Модель</th>'
                  '<th>Серийник</th><th>Предыдущий ID</th><th>Пароль доступа</th><th>Отправить</th></tr>')
    result.append('<form action="/add-equip" method="post"><tr>')
    result.append('<td><input name="point_id" value="' + str(point_id) + '" readonly></td>')
    result.append('<td><input name="equip_name"></td>')
    result.append('<td><input name="model"></td>')
    result.append('<td><input name="serial_num"></td>')
    result.append('<td><input name="pre_id"></td>')
    result.append('<td><input type="password" name="password"></td>')
    result.append('<td><input type="submit" value="Отправить"></td>')
    result.append('</tr></form></table>')
    return "\n".join(result)


def pass_is_not_valid() -> str:
    """Function return string contain message NOT VALID"""
    return style_custom() + '\n' + '<h1>Неверный пароль!</h1>'


def operation_completed() -> str:
    """Function return string contain message to insert in DB"""
    return style_custom() + '\n' + '<h1>Добавлена запись в базу данных</h1>'
