from flask import redirect

import wh_app.web.template as web_template
import wh_app.web.universal_html as uhtml
from wh_app.postgresql.database import Database
from wh_app.sql_operations import select_operations
from wh_app.supporting import functions
from wh_app.config_and_backup import table_headers

functions.info_string(__name__)


def find_page(preview_page):
    return web_template.result_page(uhtml.find_table(), preview_page)


def find_method(data, method):
    if method == "POST":
        find_request = data[uhtml.FIND_REQUEST]
        find_from_table = data[uhtml.FIND_IN_TABLE]
        if find_from_table == uhtml.WORKS_IGNORED_DATE:
            return redirect('/find/work/{0}/page/1'.format(find_request))
        elif find_from_table == uhtml.WORKS:
            return redirect('/find/work/{0}/{1}/{2}/page/1'.format(find_request,
                                                            data[uhtml.WORK_DATETIME_START],
                                                            data[uhtml.WORK_DATETIME_STOP]))
        elif find_from_table == uhtml.WORKS_POINTS:
            return redirect('/find/point/{0}/page/1'.format(find_request))

        elif find_from_table == uhtml.EQUIPS:
            return redirect('/find/equip/{0}/page/1'.format(find_request))
        else:
            return web_template.result_page('Not corrected selected in Find!', '/')

    else:
        return web_template.result_page('Method in Find Page not corrected!', '/')


def find_work_paging(find_string: str, page_num: str) -> str:
    with Database() as base:
        connection, cursor = base
        works = select_operations.get_all_works_like_word_limit(cursor, find_string, int(page_num))
        works = functions.works_table_add_new_performer(works)
        pages_list = functions.list_of_pages(select_operations.get_all_works_like_word(cursor, find_string))
        result = uhtml.universal_table(table_headers.works_table_name,
                                       table_headers.works_table,
                                       [list(work) for work in works])
        pages_table = uhtml.paging_table('/find/work/{0}/page'.format(find_string),
                                         pages_list,
                                         int(page_num))
        return web_template.result_page(result + pages_table, '/find')


def find_work_like_date_paging(find_string: str, data_start: str, data_stop: str, page_num: str) -> str:
    with Database() as base:
        connection, cursor = base
        date_start_correct = data_start.replace('T', ' ')
        date_stop_correct = data_stop.replace('T', ' ')
        pages_list = functions.list_of_pages(select_operations.get_all_works_like_word_and_date(cursor,
                                                                   find_string,
                                                                   date_start_correct,
                                                                   date_stop_correct))
        works = select_operations.get_all_works_like_word_and_date_limit(cursor,
                                                                         find_string,
                                                                         date_start_correct,
                                                                         date_stop_correct,
                                                                         int(page_num))
        works = functions.works_table_add_new_performer(works)
        result = uhtml.universal_table(table_headers.works_table_name,
                                       table_headers.works_table,
                                       [list(work) for work in works])
        pages_table = uhtml.paging_table('/find/work/{0}/{1}/{2}/page'.format(find_string,
                                                                              date_start_correct,
                                                                              date_stop_correct),
                                         pages_list,
                                         int(page_num))
        return web_template.result_page(result + pages_table, '/find')


def find_point_page(find_string: str, page_num: str) -> str:
    with Database() as base:
        connection, cursor = base
        points = select_operations.get_all_points_list_from_like_str_limit(cursor, find_string, int(page_num))
        pages_list = functions.list_of_pages(select_operations.get_all_points_list_from_like_str(cursor, find_string))
        links_list = ['/equip/' + str(elem[0]) for elem in points]
        result = uhtml.universal_table(table_headers.points_table_name,
                                       table_headers.points_table,
                                       [[point[1], point[2]] for point in points],
                                       True,
                                       links_list)
        pages_table = uhtml.paging_table('/find/point/{0}/page'.format(find_string), pages_list, int(page_num))
        return web_template.result_page(result + pages_table, '/find')


def find_equip_page(find_string: str, page_num: str) -> str:
    with Database() as base:
        connection, cursor = base
        equips = select_operations.get_all_equips_list_from_like_str_limit(cursor, find_string, int(page_num))
        pages_list = functions.list_of_pages(select_operations.get_all_equips_list_from_like_str(cursor, find_string))
        links_list = ['/work/' + str(equip[0]) for equip in equips]
        result = uhtml.universal_table(table_headers.equips_table_name,
                                       table_headers.equips_table,
                                       [[equip[i] for i in range(1, len(equip))] for equip in equips],
                                       True,
                                       links_list)
        pages_table = uhtml.paging_table('/find/equip/{0}/page'.format(find_string), pages_list, int(page_num))
        return web_template.result_page(result + pages_table, '/find')
