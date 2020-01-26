import wh_app.web.template as web_template
import wh_app.web.universal_html as uhtml
from wh_app.config_and_backup import config
from wh_app.postgresql.database import Database
from wh_app.sql_operations import select_operations
from wh_app.supporting import functions
from wh_app.config_and_backup import table_headers

functions.info_string(__name__)


def bugs_menu() -> str:
    menu = [(1, 'Отобразить все'),
            (2, 'Отобразить незакрытые')]
    headers = ['№', 'Выполнить']
    links_list = ['/all-bugs', '/all-bugs-in-work']
    table = uhtml.universal_table('Возможные действия', headers, menu, True, links_list)
    return web_template.result_page(table, '/bugs')


def all_bugs_table() -> str:
    with Database() as base:
        _, cursor = base
        bugs_list = select_operations.get_all_bugz_in_bugzilla(cursor)
        table = uhtml.universal_table(table_headers.bugs_table_name,
                                      table_headers.bugs_table,
                                      bugs_list)
        return web_template.result_page(table, '/bugs')


def all_bugs_in_work_table() -> str:
    with Database() as base:
        _, cursor = base
        bugs_list = select_operations.get_all_bugz_in_work_in_bugzilla(cursor)
        table = uhtml.universal_table(table_headers.bugs_table_name,
                                      table_headers.bugs_table,
                                      bugs_list)
        return web_template.result_page(table, '/bugs')