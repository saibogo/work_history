import wh_app.web.template as web_template
import wh_app.web.universal_html as uhtml
from wh_app.postgresql.database import Database
from wh_app.sql_operations import select_operations
from wh_app.supporting import functions
from wh_app.config_and_backup import table_headers
from wh_app.sql_operations import insert_operations

functions.info_string(__name__)


def bugs_menu(stylesheet_number: str) -> str:
    menu = [(1, 'Отобразить все'),
            (2, 'Отобразить незакрытые'),
            (3, 'Зарегистрировать проблемму')]
    headers = ['№', 'Выполнить']
    links_list = ['/all-bugs', '/all-bugs-in-work', '/add-bug']
    table = uhtml.universal_table('Возможные действия', headers, menu, True, links_list)
    return web_template.result_page(table, '/bugs', str(stylesheet_number))


def all_bugs_table(stylesheet_number: str) -> str:
    with Database() as base:
        _, cursor = base
        bugs_list = select_operations.get_all_bugz_in_bugzilla(cursor)
        table = uhtml.universal_table(table_headers.bugs_table_name,
                                      table_headers.bugs_table,
                                      bugs_list)
        return web_template.result_page(table, '/bugs', str(stylesheet_number))


def all_bugs_in_work_table(stylesheet_number: str) -> str:
    with Database() as base:
        _, cursor = base
        bugs_list = select_operations.get_all_bugz_in_work_in_bugzilla(cursor)
        table = uhtml.universal_table(table_headers.bugs_table_name,
                                      table_headers.bugs_table,
                                      bugs_list)
        return web_template.result_page(table, '/bugs', str(stylesheet_number))


def add_bugs_result_table(data, method, stylesheet_number: str) -> str:
    """Add new bug in bug tracker after use input form to add bug"""

    if method == 'POST':
        bug_description = data[uhtml.DESCRIPTION]
        password = data[uhtml.PASSWORD];
        pre_adr = '/bugs'
        if functions.is_valid_password(password):
            with Database() as base:
                connection, cursor = base
                insert_operations.add_new_bug_in_bugzilla(cursor, bug_description)
                connection.commit()
                return web_template.result_page(uhtml.operation_completed(), pre_adr, str(stylesheet_number))
        else:
            return web_template.result_page(uhtml.pass_is_not_valid(), pre_adr, str(stylesheet_number))
    else:
        return web_template.result_page('Method in Add New Bug not corrected!', '/bugs', str(stylesheet_number))
