from wh_app.supporting import functions
from wh_app.web.universal_html import list_to_ul, style_custom, navigations_menu
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
            '<a href="https://docs.python.org/3/library/tk.html">tkinter</a>']


def how_many_users_list() -> list:
    """Return const list contain information to multiusers in workhistory"""

    return ['Структура базы данных поддерживает только одного исполнителя',
            'Одновременно над добавлением записей может работать неограниченное количество' +\
            ' пользователей, но все они будут использовать одну учетную запись']


def update_system_in_future_list() -> list:
    """Return const list contain information to update database in future"""

    return ['Планируется изменение структуры базы данных и внедрение многопользовательского режима',
            'В планах внедрение возможности редактирования записей',
            'Планируется  расширение работы с аргументами командной строки для десктопного приложения',
            'Планируется переработка GUI для клиентского приложения с использованием Qt',
            'Также планируется реализация всех возможностей вэб-интерфейса в GUI десктопного приложения']


def faq_state_machine(section: str) -> str:
    """Return ul - element from section FAQ"""

    ls = [];
    if section == 'hardware':
        ls = hardware_needs_list()
    elif section == 'tecnology':
        ls = used_tecnology_list()
    elif section == 'multiuser':
        ls = how_many_users_list()
    elif section == 'update':
        ls = update_system_in_future_list()
    else:
        pass
    return list_to_ul(ls)


def result_page(main_page: str, preview_adr: str="") -> str:
    """Return complete HTML page"""
    return "{0}\n{1}\n{2}\n{3}\n".format(style_custom(),
                                 generate_message_shutdown_server(),
                                 main_page,
                                 navigations_menu(preview_adr) if preview_adr != "" else "")
