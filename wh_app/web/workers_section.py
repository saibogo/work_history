"""this module contain all pages implements from workers sections"""

from flask import render_template

import wh_app.web.template as web_template
import wh_app.web.universal_html as uhtml
from wh_app.postgresql.database import Database
from wh_app.sql_operations import insert_operations
from wh_app.sql_operations import select_operations
from wh_app.sql_operations import update_operations
from wh_app.sql_operations import delete_operations
from wh_app.supporting import functions
from wh_app.config_and_backup import table_headers
from wh_app.config_and_backup.config import max_records_in_page

functions.info_string(__name__)


def create_edit_link_to_worker(worker_id: str) -> str:
    """Create EDIT-char (link)"""
    return '<a href="/edit-worker/{0}">{1}</a>'.format(worker_id, uhtml.EDIT_CHAR)


def workers_menu(stylesheet_number: str) -> str:
    """Return main page from WORKERS section"""
    name = 'Действия с сотрудниками'
    menu = [(1, 'Все зарегистрированные сотрудники'), (3, 'Только работающие'), (2, 'Привязки по предприятиям'),
            (3, 'Рабочие дни')]
    links_list = ['/all-workers', '/not-fired-workers', '/works-days', 'weekly-chart']
    table = uhtml.universal_table(name, ['№', 'Доступное действие'], menu, True, links_list)
    return web_template.result_page(table, '/', str(stylesheet_number))


def all_workers_table(stylesheet_number: str) -> str:
    """Return page, contain all workers"""
    with Database() as base:
        _, cursor = base
        all_workers = select_operations.get_all_workers(cursor)
        workers = [[elem for elem in worker] + [create_edit_link_to_worker(worker[0])] for worker in all_workers]
        links = ['/performer/' + str(elem[0]) for elem in all_workers]
        table = uhtml.universal_table(table_headers.all_workers_table_name,
                                      table_headers.workers_table,
                                      workers, True, links)
        return web_template.result_page(table,
                                        '/workers',
                                        str(stylesheet_number))


def current_workers_table(stylesheet_number: str) -> str:
    """Return only NOT FIRED workers"""
    with Database() as base:
        _, cursor = base
        current_workers_list = select_operations.get_table_current_workers(cursor)
        workers = [[elem for elem in worker] + [create_edit_link_to_worker(worker[0])] for worker in current_workers_list]
        links = ['/performer/' + str(elem[0]) for elem in current_workers_list]
        table = uhtml.universal_table(table_headers.current_workers_table_name,
                                      table_headers.workers_table,
                                      workers, True, links)
        return web_template.result_page(table,
                                        '/workers',
                                        str(stylesheet_number))


def create_edit_worker_form(worker_id: str, stylesheet_number: str) -> str:
    """Return new form to edit worker information"""

    with Database() as base:
        _, cursor = base
        try:
            description = select_operations.get_all_desriptions_workers_status(cursor)
            all_workers_status = {elem[1]: elem[0] for elem in description}
            all_workers_posts = select_operations.get_all_posts(cursor)
            current_post = 0
            avaliable_posts = []
            worker_info = select_operations.get_info_from_worker(cursor, worker_id)
            for elem in all_workers_posts:
                if elem[1] == worker_info[5]:
                    current_post = elem[0]
                else:
                    avaliable_posts.append(elem)
            possible_statuses = []
            for key in all_workers_status:
                if key != worker_info[4]:
                    possible_statuses.append([all_workers_status[key], key])
            table = render_template('edit_worker.html', worker_info=worker_info, worker_subname=uhtml.WORKER_SUBNAME,
                                    worker_name=uhtml.WORKER_NAME, phone_number=uhtml.PHONE_NUMBER,
                                    password=uhtml.PASSWORD, status=uhtml.STATUS,
                                    status_in_sql=all_workers_status[worker_info[4]], all_statuses=possible_statuses,
                                    post=uhtml.POST, current_post=current_post, all_posts=avaliable_posts)
        except IndexError:
            table = uhtml.data_is_not_valid()
    return web_template.result_page(table,
                                    '/workers',
                                    str(stylesheet_number))


def update_worker_information(worker_id: str, data, method, stylesheet_number: str) -> str:
    """Exam and update information from worker in database"""
    if method == 'POST':
        pre_adr = '/all-workers'
        subname = data[uhtml.WORKER_SUBNAME]
        name = data[uhtml.WORKER_NAME]
        phone_number = data[uhtml.PHONE_NUMBER]
        status = data[uhtml.STATUS]
        post = data[uhtml.POST]
        password = data[uhtml.PASSWORD]
        if functions.is_superuser_password(password):
            with Database() as base:
                connection, cursor = base
                update_operations.update_worker_info(cursor, worker_id, name, subname, phone_number, post, status)
                connection.commit()
                return web_template.result_page(uhtml.operation_completed(),
                                                pre_adr,
                                                str(stylesheet_number))
        else:
            return web_template.result_page(uhtml.pass_is_not_valid(),
                                            pre_adr,
                                            str(stylesheet_number))
    else:
        return web_template.result_page('Method in Add New Bug not corrected!',
                                        '/bugs',
                                        str(stylesheet_number))


def create_new_binding_method(data, method, stylesheet_number: str) -> str:
    """Examine data and add new binding if data correct"""
    if method == 'POST':
        pre_adr = '/works-points'
        point_id = data[uhtml.POINT_ID]
        worker_id = data[uhtml.WORKER_ID]
        is_main = data[uhtml.TYPE_BINDINGS]
        password = data[uhtml.PASSWORD]
        if functions.is_superuser_password(password):
            with Database() as base:
                connection, cursor = base
                insert_operations.insert_new_binding(cursor, point_id, worker_id, is_main)
                connection.commit()
                return web_template.result_page(uhtml.operation_completed(),
                                                pre_adr,
                                                str(stylesheet_number))
        else:
            return web_template.result_page(uhtml.pass_is_not_valid(),
                                            pre_adr,
                                            str(stylesheet_number))
    else:
        return web_template.result_page('Method in Add New Bug not corrected!',
                                        '/works-points',
                                        str(stylesheet_number))


def delete_binding_method(data, method, stylesheet_number: str) -> str:
    """Examine data and if OK delete selected binding in database"""
    if method == 'POST':
        pre_adr = '/works-points'
        password = data[uhtml.PASSWORD]
        binding_id = data[uhtml.BINDING_ID]
        if functions.is_superuser_password(password):
            with Database() as base:
                connection, cursor = base
                delete_operations.delete_binding(cursor, binding_id)
                connection.commit()
                return web_template.result_page(uhtml.operation_completed(),
                                                pre_adr,
                                                str(stylesheet_number))
        else:
            return web_template.result_page(uhtml.pass_is_not_valid(),
                                            pre_adr,
                                            str(stylesheet_number))
    else:
        return web_template.result_page('Method in Add New Bug not corrected!',
                                        '/works-points',
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
        full_works = [work + ['<a href="/work-edit/{1}">{0}</a>'.format(uhtml.EDIT_CHAR, work[0])] for work in full_works]
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
