import wh_app.web.template as web_template
import wh_app.web.universal_html as uhtml
from wh_app.postgresql.database import Database
from wh_app.sql_operations import insert_operations
from wh_app.sql_operations import select_operations
from wh_app.supporting import functions
from wh_app.config_and_backup import table_headers

functions.info_string(__name__)


def workers_menu():
    name = 'Действия с сотрудниками'
    menu = [(1, 'Все зарегистрированные сотрудники'), (2, 'Базовый график')]
    links_list = ['/all-workers', '/works-days']
    table = uhtml.universal_table(name, ['№', 'Доступное действие'], menu, True, links_list)
    return web_template.result_page(table, '/')


def all_workers_table():
    with Database() as base:
        connection, cursor = base
        all_workers = select_operations.get_all_workers(cursor)
        links = ['/performer/' + str(elem[0]) for elem in all_workers]
        table = uhtml.universal_table(table_headers.all_workers_table_name,
                                      table_headers.workers_table,
                                      all_workers, True, links)
        return web_template.result_page(table, '/workers')


def works_days_page():
    with Database() as base:
        connection, cursor = base
        works_days_list = select_operations.get_works_days_table(cursor)
        alter_works_days = select_operations.get_alter_works_days_table(cursor)
        table = uhtml.universal_table(table_headers.works_days_table_name,
                                      table_headers.works_days_table,
                                      works_days_list)
        table2 = uhtml.universal_table(table_headers.alter_works_days_table_name,
                                       table_headers.alter_works_days_table,
                                       alter_works_days)
        return web_template.result_page(table + uhtml.info_from_alter_works() + table2, '/workers')


def works_from_performers_table(performer_id, pre_adr: str) -> str:
    with Database() as base:
        connection, cursor = base
        full_works = select_operations.get_all_works_from_worker_id(cursor, performer_id)
        full_works = functions.works_table_add_new_performer(full_works)
        table = uhtml.universal_table(table_headers.works_table_name,
                                      table_headers.works_table,
                                      full_works)
        return web_template.result_page(table, pre_adr)


def add_performer_to_work(work_id, pre_adr):
    with Database() as base:
        connection, cursor = base
        full_works = [select_operations.get_full_information_to_work(cursor, work_id)]
        full_works = functions.works_table_add_new_performer(full_works)
        table1 = uhtml.add_performer_in_work(full_works)
        return web_template.result_page(table1, pre_adr)


def add_performer_result_method(data, method):
    if method == 'POST':
        worker_id = data[uhtml.PERFORMER]
        work_id = data[uhtml.WORK_ID]
        password = data[uhtml.PASSWORD]
        pre_addrr = '/'
        if functions.is_valid_password(password):
            with Database() as base:
                connection, cursor = base
                insert_operations.add_new_performer_in_performers_table(cursor, work_id, worker_id)
                connection.commit()
                return web_template.result_page(uhtml.operation_completed(), pre_addrr)
        else:
            return web_template.result_page(uhtml.pass_is_not_valid(), pre_addrr)
    else:
        return web_template.result_page('Method in Add performer not corrected!', '/')