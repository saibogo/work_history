from datetime import datetime
from flask import request

import config
import functions

functions.info_string(__name__)


def link_or_str(elem: str, link_type: bool = False, link: str = '') -> str:
    """Function return simple string or link-string"""
    return '<a href="' + str(link) + '">' + str(elem) + '</a>' if link_type else str(elem)


def style_custom() -> str:
    """Function return string contain sections <style>"""
    result = list()
    result.append('<head><link rel="shortcut icon" href="' + config.full_address +
                  '/favicon.ico" sizes="32x32" type="image/x-icon" title="История произведенных работ">')
    result.append('<title>История произведенных ремонтов</title></head>')
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
    result.append('ul {font-style: italic; text-align; center}')
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
    result.append('</table>')
    return "\n".join(result)


def add_new_point() -> str:
    """Function return string contain form to add new point"""
    result = list()
    result.append('<table><caption> Добавить новое предприятие</caption>')
    result.append('<tr><th>Название</th><th>Адрес</th><th>Пароль доступа</th><th></th></tr>')
    result.append('<form action="/add-point" method="post"><tr>')
    result.append('<td><input name="point_name" placeholder="Обязательно"></td>')
    result.append('<td><input name="point_addres" placeholder="Обязательно"></td>')
    result.append('<td><input type="password" name="password" placeholder="Обязательно"></td>')
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
    result.append('<td><input name="equip_name"  placeholder="Обязательно"></td>')
    result.append('<td><input name="model" placeholder="Если есть"></td>')
    result.append('<td><input name="serial_num" placeholder="Если есть"></td>')
    result.append('<td><input name="pre_id" placeholder="Если есть"></td>')
    result.append('<td><input type="password" name="password"  placeholder="Обязательно"></td>')
    result.append('<td><input type="submit" value="Отправить"></td>')
    result.append('</tr></form></table>')
    return "\n".join(result)


def add_new_work(equip_id: str) -> str:
    """Function return string contain table to add new work"""
    curr_datetime = datetime.now()
    year = str(curr_datetime.year)
    month = str(curr_datetime.month) if curr_datetime.month > 9 else '0' + str(curr_datetime.month)
    day = str(curr_datetime.day) if curr_datetime.day > 9 else '0' + str(curr_datetime.day)
    hour = str(curr_datetime.hour) if curr_datetime.hour > 9 else '0' + str(curr_datetime.hour)
    minute = str(curr_datetime.minute) if curr_datetime.minute > 9 else '0' + str(curr_datetime.minute)
    date_to_browser = year + '-' + month + '-' + day + 'T' + hour + ':' + minute

    result = list()
    result.append('<table><caption>Зарегестрировать произведенные работы</caption>')
    result.append('<tr><th>ID оборудования</th><th>Причина ремонта</th><th>описание работ</th><th>Дата и время</th>'
                  '<th>Пароль доступа</th><th>Отправить</th></tr>')
    result.append('<form action="/add-work" method="post"><tr>')
    result.append('<td><input name="equip_id" value="' + str(equip_id) + '" readonly></td>')
    result.append('<td><input name="query" placeholder="Необязательно"></td>')
    result.append('<td><input name="work" placeholder="Обязательно"></td>')
    result.append('<td><input type="datetime-local" name="work_datetime" value="' + date_to_browser + '"></td>')
    result.append('<td><input type="password" name="password"  placeholder="Обязательно"></td>')
    result.append('<td><input type="submit" value="Отправить"></td>')
    result.append('</tr></form></table>')
    return "\n".join(result)


def pass_is_not_valid() -> str:
    """Function return string contain message NOT VALID"""
    return style_custom() + '\n' + '<h1>Неверный пароль!</h1>'


def operation_completed() -> str:
    """Function return string contain message to insert in DB"""
    return style_custom() + '\n' + '<h1>Добавлена запись в базу данных</h1>'


def data_is_not_valid() -> str:
    """Function return string contain message BAD DATA"""
    return style_custom() + '\n' + '<h1>Некорректные данные</h1>'


def navigations_menu(pre_html: str) -> str:
    """Function return string contain navigations bar"""
    result = list()
    result.append('<table><caption>Навигация</caption><tr>')
    result.append('<td><a href="' + pre_html + '">В предыдущее меню</a></td>')
    result.append('<td><a href="' + config.full_address + '">Главное меню</a></td>')
    result.append('<td><a href="mailto:gleykh@malachite.ru">Обратная связь</a></td>')
    result.append('<td><a href="' + config.full_address + '/FAQ?page=' + request.url + '">Частые вопросы</a></td>')
    result.append('<td><a href="' + config.full_address + '/find' + '">Поиск</a></td>')
    result.append('<td><a href="' + config.full_address + '/statistics' + '">Статистика</a></td>')
    result.append('</tr></table>')
    return '\n'.join(result)


def list_to_ul(ls: list) -> str:
    """Function return html-string contain notnumeric html-list"""
    result = list()
    result.append('<ul>')
    for elem in ls:
        result.append('<li>' + str(elem) + '</li>')
    result.append('</ul>')
    return '\n'.join(result)


def find_table() -> str:
    """Function return table to select find-string"""
    curr_datetime = datetime.now()
    year = str(curr_datetime.year)
    month = str(curr_datetime.month) if curr_datetime.month > 9 else '0' + str(curr_datetime.month)
    day = str(curr_datetime.day) if curr_datetime.day > 9 else '0' + str(curr_datetime.day)
    hour = str(curr_datetime.hour) if curr_datetime.hour > 9 else '0' + str(curr_datetime.hour)
    minute = str(curr_datetime.minute) if curr_datetime.minute > 9 else '0' + str(curr_datetime.minute)
    date_to_browser = year + '-' + month + '-' + day + 'T' + hour + ':' + minute

    result = list()
    result.append(style_custom())
    result.append('<table><caption>Встроенная поисковая система</caption>')
    result.append('<tr><th>Примечание к поиску</th><th>Строка поиска</th><th>Где искать</th>' +
                  '<th>Дата от(Только для работ)</th><th>Дата до(Только для работ)</th><th>Отправить</th></tr>')
    result.append('<form action="/findresult" method="post"><tr>')
    result.append('<td><input name="comment" value="Введите строку поиска.(Регистр сиволов не важен)" readonly></td>')
    result.append('<td><input name="find_request"  placeholder="Обязательно"></td>')
    result.append('<td><select name="find_in_table">')
    result.append('<option selected value="works">В работах</option>')
    result.append('<option selected value="works_ignored_date">В работах не учитывая дату</option>')
    result.append('<option value="workspoints">В предприятиях</option>')
    result.append('<option value="oborudovanie">В оборудовании</option>')
    result.append('</select></td>')
    result.append('<td><input type="datetime-local" name="work_datetime_start" value="' + date_to_browser + '"></td>')
    result.append('<td><input type="datetime-local" name="work_datetime_stop" value="' + date_to_browser + '"></td>')

    result.append('<td><input type="submit" value="Отправить"></td>')
    result.append('</tr></form></table>')
    return "\n".join(result)



