"""This module contain all find-actions for Flas server.py"""
import flask

from wh_app.web.servers_parts.support_part import *
from wh_app.web.equips_section import  find_equip_to_id_page
from wh_app.web.find_section import find_page, find_method, find_work_paging,\
    find_work_like_date_paging, find_point_page, find_equip_page, find_work_like_performer_and_date_paging


@app.route('/find-equip-to-id')
def find_equip_to_id() -> Response:
    """Return page, contain FIND FORM in EQUIPS List in database"""
    return goto_or_redirect(lambda: find_equip_to_id_page(stylesheet_number()))


@app.route('/find', methods=['GET'])
def find() -> Response:
    """Return main FIND-page"""
    return goto_or_redirect(lambda: find_page(request.args.get('page',
                                                               default=config.full_address(),
                                                               type=str),
                                              stylesheet_number()))


@app.route('/findresult', methods=['POST'])
def findresult() -> Response:
    """Redirect to method selected find-type"""
    return goto_or_redirect(lambda: find_method(functions.form_to_data(request.form),
                                                request.method,
                                                stylesheet_number()))


@app.route('/find/performer/<performer_id>/<data_start>/<data_stop>/page/<page_num>', methods=['GET'])
def find_work_performer_to_data(performer_id: str, data_start: str, data_stop: str, page_num: str) -> Response:
    """Return page, contain result like name or sub_name and in datetime interval [start, stop]"""
    if is_integer(page_num):
        page = goto_or_redirect(lambda: find_work_like_performer_and_date_paging(performer_id, data_start,
                                                                                data_stop, page_num,
                                                                                stylesheet_number()))
    else:
        page = flask.abort(code=404)
    return page


@app.route('/find/work/<find_string>/page/<page_num>')
def find_work_find_string_page_page_num(find_string: str, page_num: int) -> Response:
    """Return result find work page"""
    if is_integer(page_num):
        page = goto_or_redirect(lambda: find_work_paging(find_string,
                                                        str(page_num),
                                                        stylesheet_number()))
    else:
        page = flask.abort(code=404)
    return page


@app.route('/find/work/<find_string>/<data_start>/<data_stop>/page/<page_num>')
def find_work_data_to_data(find_string: str, data_start: str, data_stop: str, page_num: int) -> Response:
    """Return page, contain result like WORK_NAME and WORK_DATE"""
    if is_integer(page_num):
        page = goto_or_redirect(lambda: find_work_like_date_paging(find_string,
                                                                data_start,
                                                                data_stop,
                                                                str(page_num),
                                                                stylesheet_number()))
    else:
        page = flask.abort(code=404)
    return page


@app.route('/find/point/<find_string>/page/<page_num>')
def find_point(find_string: str, page_num: int) -> Response:
    """Return result find point"""
    if is_integer(page_num):
        page = goto_or_redirect(lambda: find_point_page(find_string,
                                                        str(page_num),
                                                        stylesheet_number()))
    else:
        page = flask.abort(code=404)
    return page


@app.route('/find/equip/<find_string>/page/<page_num>')
def find_equip(find_string: str, page_num: int) -> Response:
    """return result find EQUIP"""
    if is_integer(page_num):
        page = goto_or_redirect(lambda: find_equip_page(find_string,
                                                        str(page_num),
                                                        stylesheet_number()))
    else:
        page = flask.abort(code=404)
    return page


