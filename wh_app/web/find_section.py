"""This module implement web-pages to find operations"""

from flask import redirect

import wh_app.web.template as web_template
import wh_app.web.universal_html as uhtml
from wh_app.postgresql.database import Database
from wh_app.sql_operations.select_operations import select_operations
from wh_app.supporting import functions
from wh_app.config_and_backup import table_headers
from wh_app.web.points_section import create_edit_links, create_tech_links

functions.info_string(__name__)


def find_page(preview_page, stylesheet_number: str) -> str:
    """Create main find table for all operations"""
    return web_template.result_page(uhtml.find_table(),
                                    preview_page,
                                    str(stylesheet_number))


def find_method(data, method, stylesheet_number: str) -> str:
    """Switch for different find methods"""
    if method == "POST":
        find_request = data[uhtml.FIND_REQUEST]
        find_from_table = data[uhtml.FIND_IN_TABLE]
        if find_from_table == uhtml.WORKS_IGNORED_DATE:
            page = redirect('/find/work/{0}/page/1'.format(find_request))
        elif find_from_table == uhtml.WORKS:
            page = redirect('/find/work/{0}/{1}/{2}/page/1'.format(find_request,
                                                            data[uhtml.WORK_DATETIME_START],
                                                            data[uhtml.WORK_DATETIME_STOP]))
        elif find_from_table == uhtml.WORKS_POINTS:
            page = redirect('/find/point/{0}/page/1'.format(find_request))

        elif find_from_table == uhtml.EQUIPS:
            page = redirect('/find/equip/{0}/page/1'.format(find_request))
        elif find_from_table == uhtml.PERFORMER or find_from_table == uhtml.PERFORMER_WITH_DATE:
            with Database() as base:
                _, cursor = base
                try:
                    worker_id = select_operations.get_worker_id_from_name(cursor, find_request)
                    if find_from_table == uhtml.PERFORMER:
                        page = redirect('/performer/{0}/page/1'.format(worker_id))
                    else:
                        page = redirect('/find/performer/{0}/{1}/{2}/page/1'.format(worker_id,
                                                                                    data[uhtml.WORK_DATETIME_START],
                                                                                    data[uhtml.WORK_DATETIME_STOP]))
                except IndexError:
                    page = web_template.result_page('<h1>Данных не найдено!</h1>', '/find', str(stylesheet_number))
                    return page
        else:
            page = web_template.result_page('Not corrected selected in Find!',
                                            '/',
                                            str(stylesheet_number))
    else:
        page = web_template.result_page('Method in Find Page not corrected!',
                                        '/',
                                        str(stylesheet_number))
    return page


def find_work_paging(find_string: str, page_num: str, stylesheet_number: str, ord_column=1) -> str:
    """Create table contain result find from only works"""
    with Database() as base:
        _, cursor = base
        works = select_operations.get_all_works_like_word_limit(cursor, find_string, int(page_num), True, ord_column)
        works = functions.works_table_add_new_performer(works)
        works = functions.works_table_add_edit(works)
        pages_list = functions.list_of_pages(select_operations.
                                             get_all_works_like_word(cursor, find_string, True, ord_column))
        headers = []
        for elem in table_headers.works_table_ext:
            headers.append(elem.format('/find/work/{0}/page/{1}'.format(find_string, page_num)))
        result = uhtml.universal_table(table_headers.works_table_name,
                                       headers,
                                       [list(work)  for work in works])
        pages_table = uhtml.paging_table('/find/work/{0}/page'.format(find_string),
                                         pages_list,
                                         int(page_num), True, ord_column)
        return web_template.result_page(result + pages_table, '/find', str(stylesheet_number), True,
                                        'find-work-not-date={}={}'.format(find_string, page_num))


def find_work_like_date_paging(find_string: str, data_start: str,
                               data_stop: str, page_num: str, stylesheet_number: str) -> str:
    """Create table contain result find from works and data"""

    with Database() as base:
        _, cursor = base
        date_start_correct = data_start.replace('T', ' ')
        date_stop_correct = data_stop.replace('T', ' ')
        pages_list = functions.list_of_pages(select_operations.
                                             get_all_works_like_word_and_date(cursor,
                                                                              find_string,
                                                                              date_start_correct,
                                                                              date_stop_correct))
        works = select_operations.get_all_works_like_word_and_date_limit(cursor,
                                                                         find_string,
                                                                         date_start_correct,
                                                                         date_stop_correct,
                                                                         int(page_num))
        works = functions.works_table_add_new_performer(works)
        works = functions.works_table_add_edit(works)
        result = uhtml.universal_table(table_headers.works_table_name,
                                       table_headers.works_table,
                                       [list(work) for work in works])
        pages_table = uhtml.paging_table('/find/work/{0}/{1}/{2}/page'.format(find_string,
                                                                              date_start_correct,
                                                                              date_stop_correct),
                                         pages_list,
                                         int(page_num))
        return web_template.result_page(result + pages_table, '/find', str(stylesheet_number), True,
                                        'find-work-with-date={}={}={}={}'.format(find_string, date_start_correct,
                                                                                 date_stop_correct, page_num))


def find_work_like_performer_and_date_paging(performer_id: str, data_start: str,
                                             data_stop: str, page_num: str, stylesheet_number: str, ord_column=1) -> str:
    """Create table contain result find from works and data"""

    with Database() as base:
        _, cursor = base
        date_start_correct = data_start.replace('T', ' ')
        date_stop_correct = data_stop.replace('T', ' ')
        pages_list = functions.list_of_pages(select_operations.
                                             get_works_from_performer_and_date(cursor,
                                                                              performer_id,
                                                                              date_start_correct,
                                                                              date_stop_correct, 0, True, ord_column))
        works = select_operations.get_works_from_performer_and_date(cursor, performer_id,
                                                                    date_start_correct,
                                                                    date_stop_correct,
                                                                    int(page_num), True, ord_column)
        works = functions.works_table_add_new_performer(works)
        works = functions.works_table_add_edit(works)
        headers = []
        for elem in table_headers.works_table_ext:
            headers.append(elem.format('/find/performer/{0}/{1}/{2}/page/{3}'.format(performer_id, date_start_correct,
                                                                                     date_stop_correct, page_num)))

        result = uhtml.universal_table(table_headers.works_table_name,
                                       headers,
                                       [list(work) for work in works])
        pages_table = uhtml.paging_table('/find/performer/{0}/{1}/{2}/page'.format(performer_id,
                                                                                   date_start_correct,
                                                                                   date_stop_correct),
                                         pages_list,
                                         int(page_num), True, ord_column)
        return web_template.result_page(result + pages_table, '/find', str(stylesheet_number),
                                        True, 'performer-with-date={}={}={}={}'.format(performer_id, date_start_correct,
                                                                                       date_stop_correct, page_num))


def find_point_page(find_string: str, page_num: str, stylesheet_number: str) -> str:
    """Create table contain result find from only works points"""
    with Database() as base:
        _, cursor = base
        points = select_operations.get_all_points_list_from_like_str_limit(cursor,
                                                                           find_string,
                                                                           int(page_num))
        pages_list = functions.list_of_pages(select_operations.
                                             get_all_points_list_from_like_str(cursor,
                                                                               find_string))
        links_list = ['/equip/' + str(elem[0]) for elem in points]
        full_points = [[point[1], point[2], point[3], create_edit_links(point[0]), create_tech_links(point[0])] for point in points]
        result = uhtml.universal_table(table_headers.points_table_name,
                                       table_headers.points_table,
                                       full_points,
                                       True,
                                       links_list)
        pages_table = uhtml.paging_table('/find/point/{0}/page'.format(find_string),
                                         pages_list,
                                         int(page_num))
        return web_template.result_page(result + pages_table, '/find',
                                        str(stylesheet_number), True, 'point={}={}'.format(find_string, page_num))


def find_equip_page(find_string: str, page_num: str, stylesheet_number: str, ord_column=2) -> str:
    """Create table contains result find from equips only"""
    with Database() as base:
        _, cursor = base
        equips = select_operations.get_all_equips_list_from_like_str_limit(cursor,
                                                                           find_string,
                                                                           int(page_num), True, ord_column)
        pages_list = functions.list_of_pages(select_operations.
                                             get_all_equips_list_from_like_str(cursor, find_string, True, ord_column))
        links_list = ['/work/' + str(equip[0]) for equip in equips]
        headers = []
        for elem in table_headers.equips_table_ext[: len(table_headers.equips_table) - 1]:
            headers.append(elem.format('/find/equip/{0}/page/{1}'.format(find_string, page_num)))
        result = uhtml.universal_table(table_headers.equips_table_name,
                                       headers,
                                       [[equip[i] for i in range(1, len(equip))]
                                        for equip in equips],
                                       True,
                                       links_list)
        pages_table = uhtml.paging_table('/find/equip/{0}/page'.format(find_string),
                                         pages_list,
                                         int(page_num), True, ord_column)
        return web_template.result_page(result + pages_table, '/find', str(stylesheet_number), True,
                                        'find-equip={}={}'.format(find_string, page_num))
