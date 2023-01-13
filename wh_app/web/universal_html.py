"""This module contain all universal HTML-section for pages"""

import datetime
from flask import request, render_template
import re

from wh_app.config_and_backup import config
from wh_app.postgresql.database import Database
from wh_app.sql_operations import select_operations
from wh_app.supporting import functions
from wh_app.config_and_backup import table_headers

functions.info_string(__name__)

PASSWORD = 'password'
LOGIN = 'login'
POINT_NAME = 'point_name'
POINT_ADDRESS = 'point_address'
POINT_ID = 'point_id'
NEW_POINT_ID = 'new_point_id'
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
ORDER_INFO = "order_info"


def link_or_str(elem: str, link_type: bool = False, link: str = '') -> str:
    """Function return simple string or link-string"""
    return '<a href="' + str(link) + '">' + str(elem) + '</a>' if link_type else str(elem)


def remove_extended_chars(html: str) -> str:
    """Remove all extended chars in html-string"""
    return html.replace('&lt;', '<').\
        replace('&gt;', '>').\
        replace('&#34;', '"').\
        replace('&amp;', '&').\
        replace('&#39;', '')


def list_to_ul(data_list: list) -> str:
    """Function return html-string contain notnumeric html-list"""
    result = list()
    result.append('<ul>')
    for elem in data_list:
        result.append('<li>' + str(elem) + '</li>')
    result.append('</ul>')
    return '\n'.join(result)


def style_custom(stylesheet_number=0) -> str:
    """Function return string contain sections <style>"""
    return render_template('style_template.html',
                           ico_addres=config.full_address + '/favicon.ico',
                           stylesheet_name="/style{0}.css".format(stylesheet_number))


def universal_table(name: str, headers: list, data: list, links: bool = False,
                    links_list: list = None) -> str:
    """Function return string contain html-table"""
    if links_list is None:
        links_list = []
    new_data = list()
    for i in range(len(data)):
        new_data.append(list())
        for elem in data[i]:
            new_data[-1].append(link_or_str(elem, links, links_list[i] if links else ''))
    tmp = render_template('universal_table.html', table_name=str(name), headers=headers, data=new_data)
    return remove_extended_chars(tmp)


def add_new_point() -> str:
    """Function return string contain form to add new point"""
    return render_template('add_new_point.html', point_name=POINT_NAME, point_address=POINT_ADDRESS, password=PASSWORD)


def add_new_equip(point_id: str) -> str:
    """Function return string contain form to add new equipment"""
    return render_template('add_new_equip.html', point_id_name=POINT_ID, point_id=str(point_id),
                           equip_name=EQUIP_NAME, model=MODEL, serial_num=SERIAL_NUM, pre_id=PRE_ID,
                           password=PASSWORD)


def add_new_work(equip_id: str) -> str:
    """Function return string contain table to add new work"""
    date_to_browser = functions.date_to_browser()

    performers = []
    with Database() as base:
        _, cursor = base
        performers = select_operations.get_table_current_workers(cursor)

    return render_template('add_new_work.html', equip_id_name=EQUIP_ID, equip_id=str(equip_id), query=QUERY,
                           work=WORK, work_datetime=WORK_DATETIME, date_to_browser=date_to_browser,
                           performer_name=PERFORMER, performers=performers, password=PASSWORD)


def pass_is_not_valid() -> str:
    """Function return string contain message NOT VALID"""
    return '<h1>Неверный пароль!</h1>'


def operation_completed() -> str:
    """Function return string contain message to insert in DB"""
    return '<h1>Добавлена запись в базу данных</h1>'


def data_is_not_valid() -> str:
    """Function return string contain message BAD DATA"""
    return '<h1>Некорректные данные</h1>'


def selected_new_theme() -> str:
    """ Function return string contain message NEW THEME"""
    return '<h1>Произведена смена темы оформления</h1>'


def navigations_menu(pre_html: str, save_to_pdf: bool=False, current_adr: str="") -> str:
    """Function return string contain navigations bar
    save_to_pdf=True create button "Save" in navigation menu
    """
    return render_template('navigation_template.html', pre_html=pre_html, address=config.full_address,
                           request_url=request.url, to_pdf=True if save_to_pdf and current_adr != "" else None,
                           current_adress=current_adr)


def find_table() -> str:
    """Function return table to select find-string"""
    date_to_browser = functions.date_to_browser()
    return render_template('find_template.html', comment=COMMENT, find_request=FIND_REQUEST,
                           find_in_table=FIND_IN_TABLE, works=WORKS, works_ignored_date=WORKS_IGNORED_DATE,
                           works_points=WORKS_POINTS, equips=EQUIPS, work_datetime_start=WORK_DATETIME_START,
                           work_datetime_stop=WORK_DATETIME_STOP, date_to_browser=date_to_browser)


def add_performer_in_work(work: list) -> str:
    """Return HTML-table for add new performer to current work"""

    performers = []
    with Database() as base:
        _, cursor = base
        performers = select_operations.get_table_current_workers(cursor)
    table = [(i + 1, table_headers.works_table[i], re.sub(r"<a href.*a>", '', str(work[0][i])))
             for i in range(len(work[0]))]

    return render_template('add_performer_in_work.html', table=table, string_num=str(len(work[0])),
                           performer=PERFORMER, performers=performers, work_id_name=WORK_ID, work_id=str(work[0][0]),
                           password=PASSWORD)


def edit_point_information(point: list) -> str:
    """Return editable table about selected point"""
    return render_template('edit_point_information.html', point_id=POINT_ID, point=point, point_name=POINT_NAME,
                           point_address=POINT_ADDRESS, password=PASSWORD)


def edit_equip_information(equip: list) -> str:
    """Return editable table about selected point"""

    result = list()
    result.append('<table><caption>Редактировать сведения об оборудовании</caption>')
    result.append('<tr><th>№</th><th>Параметр</th><th>Значение</th></tr>')

    result.append('<form action="/upgrade-equip-info" method = "post">')
    result.append('<tr><td>1</td><td>ID</td><td>' + equip[0] + '</td></tr>')
    result.append('<input type="hidden" name="' + EQUIP_ID + '" value="' + equip[0] + '"></input>')
    result.append('<tr><td>2</td><td>Предприятие</td><td>' + equip[1] + '</td></tr>')

    result.append('<tr><td>3</td><td>Наименование</td>')
    result.append('<td><textarea name="' + EQUIP_NAME + '">' + equip[2] + '</textarea></td></tr>')

    result.append('<tr><td>4</td><td>Модель</td>')
    result.append('<td><textarea rows=2 name="' + MODEL + '">' + equip[3] + '</textarea></td></tr>')

    result.append('<tr><td>5</td><td>Серийный номер</td>')
    result.append('<td><textarea rows=2 name="' +
                  SERIAL_NUM + '">' + equip[4] +
                  '</textarea></td></tr>')

    result.append('<tr><td>6</td><td>Предыдущий ID</td>')
    result.append('<td><textarea rows=1 name="' + PRE_ID +
                  '">' + str(equip[5]) + '</textarea></td></tr>')

    result.append('<tr><td>7</td><td>Пароль доступа</td>')
    result.append('<td><input type="password" name="' + PASSWORD + '"></input></td></tr>')

    result.append('<tr><td>8</td><td>Применить изменения</td>')
    result.append('<td><input type="submit" value="Отправить"></input></td></tr>')

    result.append('</form></table>')

    return "\n".join(result)


def select_point_form(equip: list, point_id: str) -> str:
    """Create form to generate html-page to remove equip in new point"""

    result = list()
    result.append('<table><caption>Перемещение оборудования</caption>')
    result.append('<tr><th>№</th><th>Параметр</th><th>Значение</th></tr>')

    result.append('<form action="/remove-equip" method = "post">')
    result.append('<tr><td>1</td><td>ID</td><td>' + equip[0] + '</td></tr>')
    result.append('<input type="hidden" name="' + EQUIP_ID + '" value="' + equip[0] + '"></input>')

    result.append('<tr><td>2</td><td>Текущее предприятие</td><td>' + equip[1] + '</td></tr>')
    result.append('<input type="hidden" name="' + POINT_ID + '" value="' + point_id + '"></input>')

    result.append('<tr><td>3</td><td>Наименование</td><td>' + equip[2] + '</td></tr>')
    result.append('<input type="hidden" name="' + EQUIP_NAME +
                  '" value="' + equip[2] + '"></input>')

    result.append('<tr><td>4</td><td>Модель</td><td>' + equip[3] + '</td></tr>')
    result.append('<input type="hidden" name="' + MODEL + '" value="' + equip[3] + '"></input>')

    result.append('<tr><td>5</td><td>Серийный номер</td><td>' + equip[4] + '</td></tr>')
    result.append('<input type="hidden" name="' +
                  SERIAL_NUM +
                  '" value="' + equip[4] + '"></input>')

    result.append('<tr><td>6</td><td>Предыдущий ID</td><td>' + str(equip[5]) + '</td></tr>')
    result.append('<input type="hidden" name="' +
                  PRE_ID +
                  '" value="' + str(equip[5]) + '"></input>')

    result.append('<tr><td>7</td><td>Точка перемещения</td><td><select name="' +
                  NEW_POINT_ID + '">')
    new_points = []
    with Database() as base:
        _, cursor = base
        new_points  = select_operations.get_all_point_except_id(cursor, str(point_id))
        for point in new_points:
            result.append('<option value="' + str(point[0]) + '">' + str(point[1]) + '</option>')

    result.append('</select></td></tr>')

    result.append('<tr><td>7</td><td>Пароль доступа</td>')
    result.append('<td><input type="password" name="' + PASSWORD + '"></input></td></tr>')

    result.append('<tr><td>8</td><td>Применить изменения</td>')
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
    result.append('<input type="hidden" name="' +
                  POINT_ID +
                  '" value="' + point[0] + '"></input>')

    result.append('<tr><td>2</td><td>Служебное название</td>')
    result.append('<td>' + str(point[1]) + '</td></tr>')

    result.append('<tr><td>3</td><td>Адрес</td>')
    result.append('<td>' + str(point[2]) + '</td></tr>')

    result.append('<tr><td>4</td><td>Статус</td>')
    result.append('<td>' + point[3] + '</td></tr>')

    result.append('<tr><td>5</td><td>Пароль доступа</td>')
    result.append('<td><input type="password" name="' +
                  PASSWORD +
                  '"></input></td></tr>')

    result.append('<tr><td>6</td><td>Изменить статус</td>')
    result.append('<td><input type="submit" value="Изменить"></input></td></tr>')

    result.append('</form></table>')
    return "\n".join(result)


def html_page_not_found() -> str:
    """Return html contain PAGE NOT FOUND"""

    return '<h1>Блииннн.. А такой страницы нет...</h1>'


def html_internal_server_error() -> str:
    """Return html contain INTERNAL SERVER ERROR"""

    message = '<h1>Произошла ошибка сервера. ' +\
              ' Обратитесь к администратору сайта или разработчику</h1>' +\
              '<h2>Время возникновения ошибки: {}</h2>'.format(
                  datetime.datetime.now().strftime("%d-%m-%Y %H:%M"))
    return message


def info_from_alter_works() -> str:
    """Return information html from use alter_works_days_table"""

    return '<h3>Если у сотрудника, закрепленного за Вашим' +\
           ' предприятием выходной день (символы "--" в таблице),' \
           'посмотрите, кто из сотрудников закреплен за Вашим' +\
           ' предприятием дополнительно и сегодня на смене.<h3>'


def paging_table(link: str, all_elems: list, current: int) -> str:
    """Return simple table contain paging links"""

    if len(all_elems) == 1:
        result = [""]
    else:
        result = ['<br><table id="pages_table">']
        if len(all_elems) < 2 * config.max_pages_in_tr:
            for row in range(len(all_elems) // config.max_pages_in_tr + 1):
                result.append('<tr>')
                for cell in range(min(config.max_pages_in_tr,
                                    len(all_elems) - row * config.max_pages_in_tr)):
                    result.append('<td class="paging_td">')
                    elem = all_elems[row * config.max_pages_in_tr + cell]
                    result.append(str(elem)
                                  if elem == current
                                  else '<a href="{0}/{1}">{1}</a>'.format(link, elem))
                    result.append('</td>')
                result.append('</tr>')
        else:
            result.append('<tr>')
            result.append('<td class="paging_td"><a href="{0}/{1}">&laquo;</a>'.format(
                link, all_elems[0]))
            result.append('</td>')
            down_page_number = max(1, current - 10)
            result.append('<td class="paging_td" title="page {1}"><a href="{0}/{1}">&lt</a>'.
                          format(link, down_page_number))
            result.append('</td>')
            list_of_intervals = [[], [], []]
            len_of_interval = config.max_pages_in_tr // 4

            if 0 < current < len_of_interval:
                start_index = max(0, current - 3)
                list_of_intervals[0] = list(range(start_index, start_index + 6))

                start_index = len(all_elems) // 2 - 3
                list_of_intervals[1] = list(range(start_index, start_index + 6))

                list_of_intervals[2] = list(range(len(all_elems) - 6, len(all_elems)))
            elif len(all_elems) - len_of_interval < current <= len(all_elems):
                list_of_intervals[0] = list(range(0, 6))

                start_index = len(all_elems) // 2 - 3
                list_of_intervals[1] = list(range(start_index, start_index + 6))

                stop_index = min(len(all_elems), current + 3)
                list_of_intervals[2] = list(range(stop_index - 6, stop_index))

            else:
                list_of_intervals[0] = list(range(0, 6))

                start_index = current - 3
                list_of_intervals[1] = list(range(start_index, start_index + 6))

                list_of_intervals[2] = list(range(len(all_elems) - 6, len(all_elems)))

            result.append(create_td_in_paging_table(all_elems, link, list_of_intervals[0], current))
            result.append('<td class="paging_td">...</td>')

            result.append(create_td_in_paging_table(all_elems, link, list_of_intervals[1], current))
            result.append('<td class="paging_td">...</td>')

            result.append(create_td_in_paging_table(all_elems, link, list_of_intervals[2], current))

            up_page_number = min(len(all_elems), current + 10)
            result.append('<td class="paging_td" title="page {1}"><a href="{0}/{1}">&gt</a>'.
                          format(link, up_page_number))
            result.append('</td>')

            result.append('<td class="paging_td"><a href="{0}/{1}">&raquo;</a>'.format(
                link, all_elems[-1]))
            result.append('</td>')

            result.append('</tr>')
        result.append('</table>')
    return "\n".join(result)


def create_td_in_paging_table(all_elems: list, link: str,
                              list_of_interval: list, current: int) -> str:
    """Support function for paging_table()"""
    result = []
    for i in list_of_interval:
        result.append('<td class="paging_td">')
        result.append(str(i + 1) if i == current - 1
                      else '<a href="{0}/{1}">{1}</a></td>'.format(link, all_elems[i]))
    return "\n".join(result)


def new_bug_input_table() -> str:
    """Return form to input new bug in bag tracker"""

    result = list()
    result.append('<table><caption>Зарегистрировать проблему работы с сервером</caption>')
    result.append('<tr><th>Описание проблемы, включая время</th>' +
                  '<th>Пароль</th><th>Действие</th></tr>')
    result.append('<form action="/add-bug-result" method="post">')
    result.append('<tr><td><textarea name="' +
                  DESCRIPTION +
                  '" placeholder="Обязательное поле"></textarea></td>')
    result.append('<td><input type="password" name = "' +
                  PASSWORD +
                  '" placeholder="Обязательно"></td>')
    result.append('<td><input type="submit" value="Отправить"></td></tr></form></table>')
    return "\n".join(result)


def logpass_table() -> str:
    """Return new form to input login and password"""

    result = list()
    result.append('<table><caption>Получение доступа к системе</caption>')
    result.append('<tr><th>Логин</th><th>Пароль</th><th>Действие</th></tr>')
    result.append('<form action="/login-verification" method="post">')
    result.append('<tr><td><textarea name="' + LOGIN + '" placeholder="Обязательное поле"></textarea></td>')
    result.append('<td><input type="password" name = "' +
                  PASSWORD +
                  '" placeholder="Обязательно"></td>')
    result.append('<td><input type="submit" value="Отправить"></td></tr></form></table>')
    return "\n".join(result)


def access_denided(name: str) -> str:
    """Function return page from not correct login or password"""

    return "<h1>Ошибка доступа для пользователя {0}. Попробуйте еще раз!</h1>".format(name)


def access_allowed(name: str) -> str:
    """Function return page from correct login and password"""

    return "<h1>С возвращением, {0}!</h1>".format(name)


def logout_user() -> str:
    """Function return BYE-page"""

    return "<h1>Осуществлен выход из системы</h1>"