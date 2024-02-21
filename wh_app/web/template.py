"""This module contain templates to web pages"""

from flask import render_template

from wh_app.supporting import functions
from wh_app.web.universal_html import list_to_ul, style_custom, navigations_menu, replace_decor
from wh_app.web.java_script_generate.shutdown_handler import generate_message_shutdown_server

functions.info_string(__name__)


def hardware_needs_list() -> list:
    """Return const list"""

    return ['Компьютер во внутренней сети компании Малахит',
            'Браузер с поддержкой технологии ' +
            '<a href="https://www.w3.org/Style/CSS/Overview.en.html">CSS</a>']


def used_tecnology_list() -> list:
    """Return const list tecnology used in this application"""

    return ['Используется база данных <a href="https://www.postgresql.org/"> PostgreSQL</a>',
            'Используется веб-сервер ' +
            '<a href="https://flask.palletsprojects.com/en/1.0.x/changelog/">Flask</a>',
            'Используется язык программирования ' +
            '<a href="https://www.python.org/">Python3</a>',
            'Также для создания сообщений пользователям использован язык' +
            '<a href="https://www.javascript.com/">JavaScript</a>',
            'Для клиентского приложения использована связка ' +
            '<a href="https://www.python.org/">Python3</a> + ' +
            '<a href="https://www.qt.io/qt-for-python">PyQt</a>']


def how_many_users_list() -> list:
    """Return const list contain information to multiusers in workhistory"""

    return ['Структура базы данных поддерживает только одного исполнителя',
            'Одновременно над добавлением записей может работать неограниченное количество' +\
            ' пользователей, но все они будут использовать одну учетную запись']


def update_system_in_future_list() -> list:
    """Return const list contain information to update database in future"""

    return ['Планируется изменение структуры базы данных и внедрение многопользовательского режима',
            'Планируется  расширение работы с аргументами командной строки',
            'В связи с редким использованием, планируется полный отказ от десктоп-версии приложения',
            ]


def faq_state_machine(section: str) -> str:
    """Return ul - element from section FAQ"""

    result_list = []
    if section == 'hardware':
        result_list = hardware_needs_list()
    elif section == 'tecnology':
        result_list = used_tecnology_list()
    elif section == 'multiuser':
        result_list = how_many_users_list()
    elif section == 'update':
        result_list = update_system_in_future_list()
    else:
        pass
    return list_to_ul(result_list)


@replace_decor
@replace_decor
def result_page(main_page: str, preview_adr: str="", stylesheet_number: str="0", to_pdf: bool=False,
                current_adr: str="") -> str:
    """Return complete HTML page"""
    tmp = render_template('universal_page.html', style_section=style_custom(stylesheet_number),
                          scrypt_section=generate_message_shutdown_server(),
                          main_section=main_page,
                          navigation_section=navigations_menu(preview_adr,
                                                              to_pdf,
                                                              current_adr) if preview_adr != "" else "")
    return tmp
