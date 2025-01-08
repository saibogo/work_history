"""this module contain all pages implements from workers sections"""
import datetime

from flask import render_template

import wh_app.web.template as web_template
import wh_app.web.universal_html as uhtml
from wh_app.postgresql.database import Database
from wh_app.sql_operations import insert_operations
from wh_app.sql_operations.select_operations import select_operations
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
    menu = ['Все зарегистрированные сотрудники', 'Только работающие',  'Привязки по предприятиям',
            'Рабочие дни', 'TOP-10 по зарегистрированным работам', "Добавить сотрудника", "Сотрудники на смене"]
    links_list = ['/all-workers', '/not-fired-workers', '/works-days', '/weekly-chart', '/top-10-workers',
                  '/add-worker', '/schedule-menu']
    table = uhtml.universal_table(name, ['№', 'Доступное действие'], functions.list_to_numer_list(menu), True, links_list)
    return web_template.result_page(table, '/', str(stylesheet_number))


def schedule_menu_page(stylesheet_number: str) -> str:
    """Return submenu with all current shedulle section"""
    name = 'Текущие графики'
    menu = ['График на сегодня', 'График на неделю', 'Добавить рабочую смену']
    links_list = ['/today-schedule', '/week-schedule', '/add-info-in-schedule']
    table = uhtml.universal_table(name, ['№', 'Период'], functions.list_to_numer_list(menu), True, links_list)
    return web_template.result_page(table, '/workers-menu', str(stylesheet_number))


def today_schedule_page(stylesheet_number: str) -> str:
    """Return all worker who work today"""
    with Database() as base:
        _, cursor = base
        today_date = datetime.date.today()
        schedule_list = select_operations.get_schedule_to_date(cursor, str(today_date))
        table = render_template('universal_table.html', table_name=table_headers.schedule_table_name,
                                num_columns=len(table_headers.schedule_table), headers=table_headers.schedule_table,
                                data=schedule_list)
        return web_template.result_page(table, '/schedule-menu', stylesheet_number, True, 'schedule-td')


def week_schedule_page(stylesheet_number: str) -> str:
    """Return all worker work today and +7 days include"""
    with Database() as base:
        _, cursor = base
        tables = []
        for i in range(7):
            result = []
            today_date = datetime.date.today() + datetime.timedelta(days=i)
            schedule_list = select_operations.get_schedule_to_date(cursor, str(today_date))
            for elem in schedule_list:
                result.append(elem)
            table = render_template('universal_table.html', table_name=str(today_date),
                                    num_columns=len(table_headers.schedule_table), headers=table_headers.schedule_table, data=result)
            tables.append(table)
        return web_template.result_page('\n'.join(tables), '/schedule-menu', stylesheet_number, True, 'schedule-wk')


def add_info_in_schedule_form(stylesheet_number: str) -> str:
    """Create form to add new information in shedule"""
    with Database() as base:
        _, cursor = base
        cd = functions.date_to_browser()
        performers = select_operations.get_all_workers_real(cursor)
        days_types = select_operations.get_all_work_days_types(cursor)
        table = render_template('add_work_day_in_schedule.html', current_date=cd, performers=performers,
                                performer_name=uhtml.PERFORMER, days_types=days_types, work_day_type=uhtml.WORK_DAY_TYPE,
                                password=uhtml.PASSWORD)
        return web_template.result_page(table, '/schedule-menu', stylesheet_number)


def all_workers_table(stylesheet_number: str) -> str:
    """Return page, contain all workers"""
    with Database() as base:
        _, cursor = base
        all_workers = select_operations.get_all_workers(cursor)
        all_workers = [list(map(lambda e: str(e) if e is not None else "", row)) for row in all_workers]
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
        current_workers_list = [list(map(lambda e: str(e) if e is not None else "", row)) for row in current_workers_list]
        workers = [[elem for elem in worker] + [create_edit_link_to_worker(worker[0])] for worker in current_workers_list]
        links = ['/performer/' + str(elem[0]) for elem in current_workers_list]
        table = uhtml.universal_table(table_headers.current_workers_table_name,
                                      table_headers.only_works_workers,
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
            correct_info = []
            for elem in worker_info:
                if isinstance(elem, datetime.date):
                    correct_info.append(datetime.datetime.strptime(elem.strftime('%Y%m%d'), '%Y%m%d'))
                else:
                    correct_info.append(elem)
            worker_info = correct_info
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
                                    post=uhtml.POST, current_post=current_post, all_posts=avaliable_posts,
                                    employee_date=uhtml.EMPLOYEE_DATE)
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
        employee_date = datetime.datetime.strptime(data[uhtml.EMPLOYEE_DATE].replace("T", ' ').split()[0], '%Y-%m-%d')\
            .date()
        password = data[uhtml.PASSWORD]
        if functions.is_superuser_password(password):
            with Database() as base:
                connection, cursor = base
                update_operations.update_worker_info(cursor, worker_id, name, subname, phone_number, post,
                                                     status, employee_date)
                connection.commit()
                if status == 'fired':
                    update_operations.set_worker_dismissal_date(cursor, worker_id)
                    connection.commit()
                else:
                    update_operations.set_worker_dismissal_date_in_null(cursor, worker_id)
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
                                        'performer={0}={1}'.format(performer_id, page_num))


def add_performer_to_work(work_id, pre_adr: str, stylesheet_number: str) -> str:
    """Return page, contain form to add new performer in current work"""
    with Database() as base:
        _, cursor = base
        full_works = [select_operations.get_full_information_to_work(cursor, work_id)]
        full_works = functions.works_table_add_new_performer(full_works)
        table1 = uhtml.add_performer_in_work(full_works)
        return web_template.result_page(table1, pre_adr, str(stylesheet_number))


def remove_performer_from_work(work_id, pre_adr: str, stylesheet_number: str) -> str:
    """Create form select performer to delete in current work-report"""
    with Database() as base:
        _, cursor = base
        work = select_operations.get_full_information_to_work(cursor, work_id)
        performers = select_operations.get_workers_in_work(cursor, work_id)
        table =  render_template('remove_performer_from_work.html', work_id_name=uhtml.WORK_ID, work_id=work[0],
                                 point_name=work[1], equip_name=work[2], work_time=work[5], order=work[6],
                                 resume=work[7], performer=uhtml.PERFORMER, performers=performers,
                                 password=uhtml.PASSWORD)
        return web_template.result_page(table, pre_adr, str(stylesheet_number))


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
        page = '<h2>Method in Add performer not corrected!</h2>'
    return web_template.result_page(page, pre_adr, str(stylesheet_number))


def remove_performer_result_method(data, method, stylesheet_number: str) -> str:
    """analyze and remove performer if data correct"""
    pre_adr = '/'
    if method == 'POST':
        work_id = data[uhtml.WORK_ID]
        performer = data[uhtml.PERFORMER]
        password = data[uhtml.PASSWORD]
        with Database() as base:
            connection, cursor = base
            performers = select_operations.get_workers_in_work(cursor, work_id)
            if len(performers) < 2:
                page = '<h2>Невозможно удалить единственного исполнителя!</h2>'
            elif functions.is_superuser_password(password):
                delete_operations.delete_performer_from_work(cursor, work_id, performer)
                connection.commit()
                page = uhtml.operation_completed()
            else:
                page = uhtml.pass_is_not_valid()
    else:
        page = '<h2>Method in Remove performer not corrected!</h2>'
    return web_template.result_page(page, pre_adr, str(stylesheet_number))


def top_workers_page(stylesheet_number: str) -> str:
    """Create top 10 workers page"""

    pre_adr = '/workers'
    with Database() as base:
        _, cursor = base
        workers = select_operations.get_top_10_workers(cursor)
        links = ['/performer/' + str(elem[0]) for elem in workers]
        page = uhtml.universal_table(table_headers.top_10_workers_table_name,
                                     table_headers.top_10_workers_table,
                                     workers, True, links)
        return web_template.result_page(page, pre_adr, stylesheet_number, True, 'top10workers')


def create_new_worker_page(stylesheet_number: str) -> str:
    """Create page to Add New Worker"""

    pre_addr = '/workers'
    with Database() as base:
        _, cursor = base
        posts = select_operations.get_all_posts(cursor)
        table = render_template('add_new_worker.html', all_posts=posts, worker_subname=uhtml.WORKER_SUBNAME,
                                worker_name=uhtml.WORKER_NAME, phone_number=uhtml.PHONE_NUMBER, post=uhtml.POST,
                                password=uhtml.PASSWORD)
        return web_template.result_page(table, pre_addr, stylesheet_number)


def add_new_worker_method(data, method, stylesheet_number: str) -> str:
    """Add new worker in DataBase"""
    pre_adr = '/'
    if method == 'POST':
        subname = data[uhtml.WORKER_SUBNAME]
        name = data[uhtml.WORKER_NAME]
        phone_number = data[uhtml.PHONE_NUMBER]
        post = data[uhtml.POST]
        password = data[uhtml.PASSWORD]
        if functions.is_superuser_password(password):
            if subname == '' or name == '':
                page = uhtml.data_is_not_valid()
            else:
                with Database() as base:
                    connection, cursor = base
                    insert_operations.insert_new_worker(cursor, name, subname, phone_number, post)
                    connection.commit()
                    page = uhtml.operation_completed()
        else:
            page = uhtml.pass_is_not_valid()
    else:
        page = '<h2>Method in Remove performer not corrected!</h2>'
    return web_template.result_page(page, pre_adr, str(stylesheet_number))


def insert_new_schedule_in_db(data, method, stylesheet_number: str) -> str:
    """Add new info in schedule"""
    pre_adr = 'schedule-menu'
    if method == 'POST':
        performer = data[uhtml.PERFORMER]
        day_datetype = data['day_datetime']
        correct_date = day_datetype[:day_datetype.index('T')]
        work_day_type = data[uhtml.WORK_DAY_TYPE]
        password = data[uhtml.PASSWORD]
        if functions.is_superuser_password(password):
            with Database() as base:
                connection, cursor = base
                insert_operations.insert_new_day_in_schedule(cursor, correct_date, performer, work_day_type)
                connection.commit()
                page = uhtml.operation_completed()
        else:
            page = uhtml.pass_is_not_valid()
    else:
        page = '<h2>Method in Add new data in Shedule not corrected!</h2>'
    return web_template.result_page(page, pre_adr, str(stylesheet_number))