"""This module contain all universal HTML-section for pages"""

import datetime
from flask import request, render_template
from typing import Callable, Any
import re

from wh_app.config_and_backup import config
from wh_app.postgresql.database import Database
from wh_app.sql_operations.select_operations import select_operations
from wh_app.supporting import functions
from wh_app.config_and_backup import table_headers


functions.info_string(__name__)

ON_OFF_CHAR = '&#9211'
PAPERS_CHAR = '&#128441;'
SVU_CHAR = '&#9889;'
METER_CHAR = '&#9099;'
EDIT_CHAR = '&#9998'
BINDING_CHAR = '🔨'
REMOVE_CHAR = 'A&#8646;B'
TABLE_REMOVE_CHAR = '&#8694'
SPACE_CHAR = '&nbsp;'

PASSWORD = 'password'
LOGIN = 'login'
SESSION_ROLE = 'role'
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
WORK_DAY_TYPE = 'work_day_type'
PERFORMER = 'performer'
PERFORMER_WITH_DATE = 'performer_with_date'
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
BUG_ID = "bug_id"
RESUME = "resume"
DOGOVOR = "dogovor"
WORKER_ID = "worker_id"
WORKER_NAME = "name"
WORKER_SUBNAME = "subname"
TYPE_BINDINGS = "is_main"
PHONE_NUMBER = "phone_number"
STATUS = "status"
POST = "post"
BINDING_ID = "id"
EMPLOYEE_DATE = "employee_date"
CUSTOMER_NAME = "customer"
CUSTOMER_ID = 'customer_id'
ORDER_STATUS_NAME = "order_status"
ORDER_ID = "order_id"
DEVICE_ID = "device_id"
READING_NAME = "reading"
FULL_NAME = "full_name"
LAST_NAME = "last_name"
FIRST_NAME = "first_name"
PASSWORD1 = "password_1"
PASSWORD2 = "password_2"


def link_or_str(elem: str, link_type: bool = False, link: str = '') -> str:
    """Function return simple string or link-string"""
    flag = False
    for char in [ON_OFF_CHAR, PAPERS_CHAR, SVU_CHAR, EDIT_CHAR, REMOVE_CHAR]:
        if char in str(elem):
            flag = True
            break
    tmp = '<a href="' + str(link) + '">' + str(elem) + '</a>' if link_type and not flag else str(elem)
    return tmp


def replace_decor(func: Callable) -> Callable:
    """Replaces all invalid characters"""
    empty_link_pattern = r'<a *></a>'

    def wrap(*args: Any) -> str:
        tmp = func(*args)
        tmp = tmp.replace('&lt;', '<').\
            replace('&gt;', '>').\
            replace('&#34;', '"').\
            replace('&amp;', '&').\
            replace('&#39;', '')

        return tmp
    return wrap


def list_to_ul(data_list: list) -> str:
    """Function return html-string contain notnumeric html-list"""
    return render_template('list.html', list=data_list)


def style_custom(stylesheet_number=0) -> str:
    """Function return string contain sections <style>"""
    return render_template('style_template.html',
                           ico_addres=config.full_address() + '/favicon.ico',
                           stylesheet_name="/style{0}.css".format(stylesheet_number))


@replace_decor
def universal_table(name: str, headers: list, data: list, links: bool = False,
                    links_list: list = None) -> str:
    """Function return string contain html-table"""
    if links_list is None:
        links_list = []
    new_data = list()
    num_columns = len(headers)
    for i in range(len(data)):
        new_data.append(list())
        for elem in data[i]:
            new_data[-1].append(link_or_str(elem, links, links_list[i] if links else ''))
    tmp = render_template('universal_table.html', table_name=str(name), headers=headers, data=new_data,
                          num_columns=num_columns)
    return tmp


def add_new_point() -> str:
    """Function return string contain form to add new point"""
    return render_template('add_new_point.html', point_name=POINT_NAME, point_address=POINT_ADDRESS, password=PASSWORD)


def add_new_reading(device_id: int) -> str:
    """Function return string contain form to add new reading to meter device"""
    date_to_browser = functions.date_to_browser()
    tmp = render_template('add_new_reading.html', device_id_name=DEVICE_ID, device_id=device_id,
                          reading_name=READING_NAME, work_datetime=WORK_DATETIME, date_to_browser=date_to_browser,
                          password=PASSWORD)
    return tmp


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
    return '<h2>Неверный пароль!</h2>'


def operation_completed() -> str:
    """Function return string contain message to insert in DB"""
    return '<h2>Добавлена запись в базу данных</h2>'


def data_is_not_valid() -> str:
    """Function return string contain message BAD DATA"""
    return '<h2>Некорректные данные</h2>'


def selected_new_theme() -> str:
    """ Function return string contain message NEW THEME"""
    return '<h2>Произведена смена темы оформления</h2>'


def navigations_menu(pre_html: str, save_to_pdf: bool=False, current_adr: str="") -> str:
    """Function return string contain navigations bar
    save_to_pdf=True create button "Save" in navigation menu
    """
    return render_template('navigation_template.html', pre_html=pre_html, address=config.full_address(),
                           request_url=request.url, to_pdf=True if save_to_pdf and current_adr != "" else None,
                           current_adress=current_adr)


def find_table() -> str:
    """Function return table to select find-string"""
    date_to_browser = functions.date_to_browser()
    return render_template('find_template.html', comment=COMMENT, find_request=FIND_REQUEST,
                           find_in_table=FIND_IN_TABLE, works=WORKS, works_ignored_date=WORKS_IGNORED_DATE,
                           works_points=WORKS_POINTS, equips=EQUIPS, work_datetime_start=WORK_DATETIME_START,
                           work_datetime_stop=WORK_DATETIME_STOP, date_to_browser=date_to_browser,
                           performer=PERFORMER, performer_with_date=PERFORMER_WITH_DATE)


def add_performer_in_work(work: list) -> str:
    """Return HTML-table for add new performer to current work"""

    performers = []
    with Database() as base:
        _, cursor = base
        all_performers = select_operations.get_table_current_workers(cursor)
        current_performers = select_operations.get_list_performers_in_work(cursor, work[0][0])
        performers = [elem for elem in all_performers if elem not in current_performers]
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

    return render_template('add_equip_information.html', equip_id_name=EQUIP_ID, equip=equip, equip_name=EQUIP_NAME,
                           model=MODEL, serial_num=SERIAL_NUM, pre_id=PRE_ID, password=PASSWORD)


def select_point_form(equip: list, point_id: str) -> str:
    """Create form to generate html-page to remove equip in new point"""
    new_points = []
    with Database() as base:
        _, cursor = base
        new_points  = select_operations.get_all_point_except_id(cursor, str(point_id))

    return render_template('redirect_equip.html', equip_id=EQUIP_ID, equip=equip, point_id_name=POINT_ID,
                           point_id=point_id, equip_name=EQUIP_NAME, model=MODEL, serial_num=SERIAL_NUM,
                           pre_id=PRE_ID, new_point_id=NEW_POINT_ID, points=new_points, password=PASSWORD)


def on_off_point_table(point: list) -> str:
    """Return table, contain dialog ON/OFF selected point"""
    return render_template('on_off_point.html', point_id=POINT_ID, point=point, password=PASSWORD)


def html_page_not_found() -> str:
    """Return html contain PAGE NOT FOUND"""
    return '<h2>Простите, но страницы с таким адресом не существует!</h2>'


def html_internal_server_error() -> str:
    """Return html contain INTERNAL SERVER ERROR"""
    message = '<h2>Произошла ошибка сервера. ' +\
              ' Обратитесь к администратору сайта или разработчику</h2>' +\
              '<h2>Время возникновения ошибки: {}</h2>'.format(
                  datetime.datetime.now().strftime("%d-%m-%Y %H:%M"))
    return message


def info_from_alter_works() -> str:
    """Return information html from use alter_works_days_table"""

    return '<h3>Если у сотрудника, закрепленного за Вашим' +\
           ' предприятием выходной день (символы "--" в таблице),' \
           'посмотрите, кто из сотрудников закреплен за Вашим' +\
           ' предприятием дополнительно и сегодня на смене.<h3>'


@replace_decor
@replace_decor
def paging_table(link: str, all_elems: list, current: int) -> str:
    """Return simple table contain paging links"""

    if len(all_elems) == 1:
        tmp = ""
    else:
        if len(all_elems) < 2 * config.max_pages_in_tr():
            rows = []
            for row in range(len(all_elems) // config.max_pages_in_tr() + 1):
                cells = []
                for cell in range(min(config.max_pages_in_tr(), len(all_elems) - row * config.max_pages_in_tr())):
                    elem = all_elems[row * config.max_pages_in_tr() + cell]
                    cells.append('<p>{}</p>'.format(elem) if elem == current else '<a href="{0}/{1}">{1}</a>'.format(link, elem))
                rows.append(render_template('paging/paging_string_v1.html', cells=cells))
            tmp = render_template('paging/paging_table_v1.html', rows=rows)
        else:
            down_page_number = max(1, current - 10)
            list_of_intervals = [[], [], []]
            len_of_interval = config.max_pages_in_tr() // 4

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

            up_page_number = min(len(all_elems), current + 10)
            tmp = render_template('paging/paging_table_v2.html', link=link, first_page=all_elems[0],
                                  down_page=down_page_number,
                                  interval1=create_td_in_paging_table(all_elems, link, list_of_intervals[0], current),
                                  interval2=create_td_in_paging_table(all_elems, link, list_of_intervals[1], current),
                                  interval3=create_td_in_paging_table(all_elems, link, list_of_intervals[2], current),
                                  up_page=up_page_number, last_page=all_elems[-1])
    return tmp


@replace_decor
def create_td_in_paging_table(all_elems: list, link: str,
                              list_of_interval: list, current: int) -> str:
    """Support function for paging_table()"""
    tmp = list(map(lambda i: '<p>{}</p>'.format(i + 1) if i == current - 1 else '<a href="{0}/{1}">{1}</a>'.
                   format(link, all_elems[i]), list_of_interval))
    return render_template('paging/td_in_paging_table.html', interval=tmp)


def new_bug_input_table() -> str:
    """Return form to input new bug in bag tracker"""
    return render_template('bug_input_table.html', description=DESCRIPTION, password=PASSWORD)


def logpass_table() -> str:
    """Return new form to input login and password"""
    return render_template('logpass.html', login=LOGIN, password=PASSWORD)


def access_denided(name: str) -> str:
    """Function return page from not correct login or password"""

    return "<h2>Ошибка доступа для пользователя {0}. Попробуйте еще раз!</h2>".format(name)


def access_allowed(name: str) -> str:
    """Function return page from correct login and password"""

    return "<h2>С возвращением, {0}!</h2>".format(name)


def logout_user() -> str:
    """Function return BYE-page"""

    return "<h2>Осуществлен выход из системы</h2>"