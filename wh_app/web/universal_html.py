from flask import request

from wh_app.config_and_backup import config
from wh_app.postgresql.database import Database
from wh_app.sql_operations import select_operations
from wh_app.supporting import functions
from wh_app.config_and_backup import table_headers

functions.info_string(__name__)

PASSWORD = 'password'
POINT_NAME = 'point_name'
POINT_ADDRESS = 'point_address'
POINT_ID = 'point_id'
EQUIP_NAME = 'equip_name'
MODEL = 'model'
SERIAL_NUM = 'serial_num'
PRE_ID = 'pre_id'
EQUIP_ID = 'equip_id'
QUERY = 'query'
WORK = 'work'
WORK_DATETIME = 'work_datetime'
PERFORMER = 'performer'
COMMENT = 'comment'
FIND_REQUEST = 'find_request'
FIND_IN_TABLE = 'find_in_table'
WORKS = 'works'
WORKS_IGNORED_DATE = 'works_ignored_date'
WORKS_POINTS = 'works_points'
EQUIPS = 'equips'
WORK_DATETIME_START = 'work_datetime_start'
WORK_DATETIME_STOP = 'work_datetime_stop'
WORK_ID = 'work_id'
DESCRIPTION = "description"


def link_or_str(elem: str, link_type: bool = False, link: str = '') -> str:
    """Function return simple string or link-string"""
    return '<a href="' + str(link) + '">' + str(elem) + '</a>' if link_type else str(elem)


def style_custom() -> str:
    """Function return string contain sections <style>"""
    result = list()
    result.append('<head><link rel="shortcut icon" href="' + config.full_address +
                  '/favicon.ico" sizes="32x32" type="image/x-icon" title="История произведенных работ">')
    result.append('<title>История произведенных ремонтов</title></head>')
    result.append('<link rel="stylesheet" href="/style.css">')
    result.append('</head>')
    return '\n'.join(result)


def universal_table(name: str, headers: list, data: list, links: bool = False, links_list: list = []) -> str:
    """Function return string contain html-table"""
    result = list()
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
    result.append('<td><input name="' + POINT_NAME + '" placeholder="Обязательно"></td>')
    result.append('<td><input name="' + POINT_ADDRESS + '" placeholder="Обязательно"></td>')
    result.append('<td><input type="password" name="' + PASSWORD + '" placeholder="Обязательно"></td>')
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
    result.append('<td><input name="' + POINT_ID + '" value="' + str(point_id) + '" readonly></td>')
    result.append('<td><input name="' + EQUIP_NAME + '"  placeholder="Обязательно"></td>')
    result.append('<td><input name="' + MODEL + '" placeholder="Если есть"></td>')
    result.append('<td><input name="' + SERIAL_NUM + '" placeholder="Если есть"></td>')
    result.append('<td><input name="' + PRE_ID + '" placeholder="Если есть"></td>')
    result.append('<td><input type="password" name="' + PASSWORD + '"  placeholder="Обязательно"></td>')
    result.append('<td><input type="submit" value="Отправить"></td>')
    result.append('</tr></form></table>')
    return "\n".join(result)


def add_new_work(equip_id: str) -> str:
    """Function return string contain table to add new work"""
    date_to_browser = functions.date_to_browser()

    performers = []
    with Database() as base:
        connection, cursor = base
        performers = select_operations.get_table_current_workers(cursor)

    result = list()
    result.append('<table><caption>Зарегестрировать произведенные работы</caption>')
    result.append('<tr><th>ID оборудования</th><th>Причина ремонта</th><th>описание работ</th><th>Дата и время</th>'
                  '<th>Исполнители</th><th>Пароль доступа</th><th>Отправить</th></tr>')
    result.append('<form action="/add-work" method="post"><tr>')
    result.append('<td><input name="' + EQUIP_ID + '" value="' + str(equip_id) + '" readonly></td>')
    result.append('<td><textarea name="' + QUERY + '" placeholder="Необязательно"></textarea></td>')
    result.append('<td><textarea name="' + WORK + '" placeholder="Обязательно"></textarea></td>')
    result.append('<td><input type="datetime-local" name="' + WORK_DATETIME + '" value="' + date_to_browser + '"></td>')
    result.append('<td><select  name="' + PERFORMER + '">')
    for perfomer in performers:
        result.append('<option value=\'' + str(perfomer[0]) + '\'>' + str(perfomer[2]) + '</option>')
    result.append('</select></td>')
    result.append('<td><input type="password" name="' + PASSWORD + '"  placeholder="Обязательно"></td>')
    result.append('<td><input type="submit" value="Отправить"></td>')
    result.append('</tr></form></table>')
    return "\n".join(result)


def pass_is_not_valid() -> str:
    """Function return string contain message NOT VALID"""
    return '<h1>Неверный пароль!</h1>'


def operation_completed() -> str:
    """Function return string contain message to insert in DB"""
    return '<h1>Добавлена запись в базу данных</h1>'


def data_is_not_valid() -> str:
    """Function return string contain message BAD DATA"""
    return '<h1>Некорректные данные</h1>'


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
    result.append('<td><a href="' + config.full_address + '/system-status' + '">Статус системы</a></td>')
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
    date_to_browser = functions.date_to_browser()

    result = list()
    result.append('<table><caption>Встроенная поисковая система</caption>')
    result.append('<tr><th>Примечание к поиску</th><th>Строка поиска</th><th>Где искать</th>' +
                  '<th>Дата от(Только для работ)</th><th>Дата до(Только для работ)</th><th>Отправить</th></tr>')
    result.append('<form action="/findresult" method="post"><tr>')
    result.append('<td><input name="' + COMMENT +
                  '" value="Введите строку поиска.(Регистр сиволов не важен)" readonly></td>')
    result.append('<td><input name="' + FIND_REQUEST + '"  placeholder="Обязательно"></td>')
    result.append('<td><select name="' + FIND_IN_TABLE + '">')
    result.append('<option selected value="' + WORKS + '">В работах</option>')
    result.append('<option selected value="' + WORKS_IGNORED_DATE + '">В работах не учитывая дату</option>')
    result.append('<option value="' + WORKS_POINTS + '">В предприятиях</option>')
    result.append('<option value="' + EQUIPS + '">В оборудовании</option>')
    result.append('</select></td>')
    result.append('<td><input type="datetime-local" name="' + WORK_DATETIME_START +
                  '" value="' + date_to_browser + '"></td>')
    result.append('<td><input type="datetime-local" name="' + WORK_DATETIME_STOP +
                  '" value="' + date_to_browser + '"></td>')

    result.append('<td><input type="submit" value="Отправить"></td>')
    result.append('</tr></form></table>')
    return "\n".join(result)


def add_performer_in_work(work: list) -> str:
    """Return HTML-table for add new performer to current work"""

    performers = []
    with Database() as base:
        connection, cursor = base
        performers = select_operations.get_table_current_workers(cursor)

    result = list()
    result.append('<table><caption>Добавить исполнителя</caption>')
    result.append('<tr><th>№</th><th>Параметр</th><th>Содержимое</th></tr>')
    for i in range(len(table_headers.works_table)):
        result.append('<tr><td>' + str(i) + '</td><td>' + table_headers.works_table[i] + '</td><td>' + str(work[0][i]) +
                      '</td></tr>')
    result.append('<form action="/add-performer-result" method="post">')
    result.append('<tr><td>' + str(len(table_headers.works_table)) + '</td>')
    result.append('<td>Добавить исполнителя</td><td><select name="' + PERFORMER + '">')
    for worker in performers:
        result.append('<option value="' + str(worker[0]) + '">' + str(worker[2]) + '</option>')
    result.append('</tr><tr></select></td></tr><tr><td><input type="hidden" name="' + WORK_ID + '" value="' +
                  str(work[0][0]) + '"></td>')
    result.append('<td>Пароль</td><td><input type="password" name="' + PASSWORD +
                  '"  placeholder="Обязательно"></td></tr>')
    result.append('<tr><td></td><td>Выполнить</td><td><input type="submit" value="Добавить"></td></tr></form></table>')

    return  "\n".join(result)


def edit_point_information(point: list) -> str:
    """Return editable table about selected point"""

    result = list()
    result.append('<table><caption>Редактировать сведения о предприятии</caption>')
    result.append('<tr><th>№</th><th>Параметр</th><th>Значение</th></tr>')

    result.append('<form action="/upgrade-point-info" method = "post">')
    result.append('<tr><td>1</td><td>ID</td><td>' + point[0] + '</td></tr>')
    result.append('<input type="hidden" name="' + POINT_ID + '" value="' + point[0] + '"></input>')

    result.append('<tr><td>2</td><td>Служебное название</td>')
    result.append('<td><textarea name="' + POINT_NAME + '">' + point[1] + '</textarea></td></tr>')

    result.append('<tr><td>3</td><td>Адрес</td>')
    result.append('<td><textarea rows=2 name="' + POINT_ADDRESS + '">' + point[2] + '</textarea></td></tr>')

    result.append('<tr><td>4</td><td>Статус</td>')
    result.append('<td>' + point[3] + '</td></tr>')

    result.append('<tr><td>5</td><td>Пароль доступа</td>')
    result.append('<td><input type="password" name="' + PASSWORD + '"></input></td></tr>')

    result.append('<tr><td>6</td><td>Применить изменения</td>')
    result.append('<td><input type="submit" value="Отправить"></input></td></tr>')

    result.append('</form></table>')

    return "\n".join(result)


def on_off_point_table(point: list) -> str:
    """Return table, contain dialog ON/OFF selected point"""

    result = list()
    result.append('<table><caption>Изменение статуса предприятия</caption>')
    result.append('<tr><th>№</th><th>Параметр</th><th>Значение</th></tr>')
    result.append('<form action="/invert-point-status" method = "post">')

    result.append('<tr><td>1</td><td>ID</td><td>' + point[0] + '</td></tr>')
    result.append('<input type="hidden" name="' + POINT_ID + '" value="' + point[0] + '"></input>')

    result.append('<tr><td>2</td><td>Служебное название</td>')
    result.append('<td>' + str(point[1]) + '</td></tr>')

    result.append('<tr><td>3</td><td>Адрес</td>')
    result.append('<td>' + str(point[2]) + '</td></tr>')

    result.append('<tr><td>4</td><td>Статус</td>')
    result.append('<td>' + point[3] + '</td></tr>')

    result.append('<tr><td>5</td><td>Пароль доступа</td>')
    result.append('<td><input type="password" name="' + PASSWORD + '"></input></td></tr>')

    result.append('<tr><td>6</td><td>Изменить статус</td>')
    result.append('<td><input type="submit" value="Изменить"></input></td></tr>')

    result.append('</form></table>')
    return "\n".join(result)


def html_page_not_found() -> str:
    """Return html contain PAGE NOT FOUND"""

    return '<h1>Блииннн.. А такой страницы нет...</h1>'


def html_internal_server_error() -> str:
    """Return html contain INTERNAL SERVER ERROR"""

    return '<h1>Произошла ошибка сервера. Обратитесь к администратору сайта или разработчику</h1>'


def info_from_alter_works() -> str:
    """Return information html from use alter_works_days_table"""

    return '<h3>Если у сотрудника, закрепленного за Вашим предприятием выходной день (символы "--" в таблице),' \
           'посмотрите, кто из сотрудников закреплен за Вашим предприятием дополнительно и сегодня на смене.<h3>'


def paging_table(link: str, all_elems: list, current: int) -> str:
    """Return simple table contain paging links"""

    if len(all_elems) == 1:
        result = [""]
    else:
        result = ['<br><table id="pages_table">']
        for tr in range(len(all_elems) // config.max_pages_in_tr + 1):
            result.append('<tr>')
            for td in range(min(config.max_pages_in_tr, len(all_elems) - tr * config.max_pages_in_tr)):
                result.append('<td class="paging_td">')
                elem = all_elems[tr * config.max_pages_in_tr + td]
                result.append(str(elem) if elem == current else '<a href="{0}/{1}">{1}</a>'.format(link, elem))
                result.append('</td>')
            result.append('</tr>')
        result.append('</table>')
    return "\n".join(result)


def new_bug_input_table() -> str:
    """Return form to input new bug in bag tracker"""

    result = list()
    result.append('<table><caption>Зарегистрировать проблему работы с сервером</caption>')
    result.append('<tr><th>Описание проблемы, включая время</th><th>Пароль</th><th>Действие</th></tr>')
    result.append('<form action="/add-bug-result" method="post">')
    result.append('<tr><td><textarea name="' + DESCRIPTION + '" placeholder="Обязательное поле"></textarea></td>')
    result.append('<td><input type="password" name = "' + PASSWORD + '" placeholder="Обязательно"></td>')
    result.append('<td><input type="submit" value="Отправить"></td></tr></form></table>')
    return "\n".join(result)

