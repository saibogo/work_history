"""this module contain all pages implements from workers sections"""

import wh_app.web.template as web_template
import wh_app.web.universal_html as uhtml
from wh_app.postgresql.database import Database
from wh_app.sql_operations import insert_operations
from wh_app.sql_operations import select_operations
from wh_app.supporting import functions
from wh_app.config_and_backup import table_headers
from wh_app.config_and_backup.config import max_records_in_page
from wh_app.web.equips_section import EDIT_CHAR

functions.info_string(__name__)


def workers_menu(stylesheet_number: str) -> str:
    """Return main page from WORKERS section"""
    name = 'Действия с сотрудниками'
    menu = [(1, 'Все зарегистрированные сотрудники'), (2, 'Привязки по предприятиям'), (3, 'Рабочие дни')]
    links_list = ['/all-workers', '/works-days', 'weekly-chart']
    table = uhtml.universal_table(name, ['№', 'Доступное действие'], menu, True, links_list)
    return web_template.result_page(table, '/', str(stylesheet_number))


def all_workers_table(stylesheet_number: str) -> str:
    """Return page, contain all workers"""
    with Database() as base:
        _, cursor = base
        all_workers = select_operations.get_all_workers(cursor)
        links = ['/performer/' + str(elem[0]) for elem in all_workers]
        table = uhtml.universal_table(table_headers.all_workers_table_name,
                                      table_headers.workers_table,
                                      all_workers, True, links)
        return web_template.result_page(table,
                                        '/workers',
                                        str(stylesheet_number))


def weekly_chart_page(stylesheet_number: str) -> str:
    """Return page, contain all works days from all workers"""
    with Database() as base:
        _, cursor = base
        days = select_operations.get_weekly_chart(cursor)
        days_human_view = list()
        for human in days:
            days_human_view.append(list())
            days_human_view[-1].append(human[0])
            for i in range(1, len(human)):
                days_human_view[-1].append("Работает" if human[i] else "Выходной")
        table = uhtml.universal_table(table_headers.workers_days_table_name,
                                      table_headers.workers_days_table,
                                      days_human_view)
        return web_template.result_page(table,
                                        '/workers',
                                        str(stylesheet_number),
                                        True, "weekly=all")


def works_days_page(stylesheet_number: str) -> str:
    """Return page, contain current shedulle"""
    with Database() as base:
        _, cursor = base
        works_days_list = select_operations.get_works_days_table(cursor)
        alter_works_days = select_operations.get_alter_works_days_table(cursor)
        table = uhtml.universal_table(table_headers.works_days_table_name,
                                      table_headers.works_days_table,
                                      works_days_list)
        table2 = uhtml.universal_table(table_headers.alter_works_days_table_name,
                                       table_headers.alter_works_days_table,
                                       alter_works_days)
        return web_template.result_page(table + uhtml.info_from_alter_works() + table2,
                                        '/workers',
                                        str(stylesheet_number))


def works_from_performers_table(performer_id: int,
                                page_num: int,
                                pre_adr: str,
                                stylesheet_number: str) -> str:
    """Return all works from current performer"""
    with Database() as base:
        _, cursor = base
        full_works_count = select_operations.get_count_all_works_from_worker_id(cursor, str(performer_id))
        create_paging = False
        if full_works_count > max_records_in_page():
            create_paging = True
            full_works = select_operations.get_all_works_from_worker_id_limit(cursor, str(performer_id), page_num)
        else:
            full_works = select_operations.get_all_works_from_worker_id(cursor, str(performer_id))
        full_works = functions.works_table_add_new_performer(full_works)
        full_works = [work + ['<a href="/work-edit/{1}">{0}</a>'.format(EDIT_CHAR, work[0])] for work in full_works]
        table = uhtml.universal_table(table_headers.works_table_name,
                                      table_headers.works_table,
                                      full_works)
        if create_paging:
            page = uhtml.paging_table("/performer/{0}/page".format(performer_id),
                                      functions.list_of_pages(select_operations.
                                                              get_all_works_from_worker_id(cursor,
                                                                                           str(performer_id))),
                                      int(page_num))
        else:
            page = ""

        return web_template.result_page(table + page, pre_adr,
                                        str(stylesheet_number),
                                        True,
                                        'performer={0}'.format(performer_id))


def add_performer_to_work(work_id, pre_adr: str, stylesheet_number: str) -> str:
    """Return page, contain form to add new performer in current work"""
    with Database() as base:
        _, cursor = base
        full_works = [select_operations.get_full_information_to_work(cursor, work_id)]
        full_works = functions.works_table_add_new_performer(full_works)
        table1 = uhtml.add_performer_in_work(full_works)
        return web_template.result_page(table1, pre_adr, str(stylesheet_number))


def add_performer_result_method(data, method, stylesheet_number: str) -> str:
    """Method append performer in current work"""
    pre_adr = '/'
    if method == 'POST':
        worker_id = data[uhtml.PERFORMER]
        work_id = data[uhtml.WORK_ID]
        password = data[uhtml.PASSWORD]
        if functions.is_valid_password(password):
            with Database() as base:
                connection, cursor = base
                insert_operations.add_new_performer_in_performers_table(cursor,
                                                                        work_id,
                                                                        worker_id)
                connection.commit()
                page = uhtml.operation_completed()
        else:
            page = uhtml.pass_is_not_valid()
    else:
        page = 'Method in Add performer not corrected!'
    return web_template.result_page(page, pre_adr, str(stylesheet_number))
