"""This module contain all actions with works for Flask server.py"""

from wh_app.web.servers_parts.support_part import *
from wh_app.web.works_section import works_menu, find_work_to_id_page,\
    select_work_to_id_method, work_to_equip_paging, add_work_method, create_edit_work_form, update_work_method,\
    select_new_point_for_work_form, select_new_equip_for_work_form, move_work_to_new_equip


@app.route("/works")
def works_operations() -> Response:
    """Return main page in WORKS-section"""
    return goto_or_redirect(lambda: works_menu(stylesheet_number()))


@app.route('/find-work-to-id')
def find_work_to_id() -> Response:
    """Return page to FIND WORK"""
    return goto_or_redirect(lambda: find_work_to_id_page(stylesheet_number()))


@app.route("/select-work-to-id", methods=['POST'])
def select_work_to_id() -> Response:
    """Redirect to method, returned full information from selected work"""
    return goto_or_redirect(lambda: select_work_to_id_method(functions.form_to_data(request.form),
                                                             request.method,
                                                             stylesheet_number()))


@app.route("/work/<equip_id>/page/<page_id>")
def work_equip_id_page_page_id(equip_id: int, page_id: int) -> Response:
    """Return page=page_id in ALL work from current EQUIP"""
    if is_integer(equip_id) and is_integer(page_id):
        page = goto_or_redirect(lambda: work_to_equip_paging(equip_id, page_id, stylesheet_number()))
    else:
        page = flask.abort(code=404)
    return page


@app.route("/work-edit/<work_id>")
def work_edit(work_id: int) -> Response:
    """Return form to EDIT some work"""
    if is_integer(work_id):
        page = goto_or_redirect(lambda : create_edit_work_form(work_id, stylesheet_number()))
    else:
        page = flask.abort(code=404)
    return page


@app.route("/update-work-to-id/<work_id>", methods=['POST'])
def update_work_to_id(work_id: int) -> Response:
    """Go to method update work info"""
    if is_integer(work_id):
        page = goto_or_redirect(lambda: update_work_method(work_id,
                                                           functions.form_to_data(request.form),
                                                           request.method,
                                                           stylesheet_number()))
    else:
        page = flask.abort(code=404)
    return page


@app.route("/work/<equip_id>")
def work_to_equip(equip_id: int) -> Response:
    """Redirect to first page in ALL work from EQUIP where EQUIP_ID=equip_id"""
    if is_integer(equip_id):
        page = goto_or_redirect(lambda: redirect('/work/{0}/page/1'.format(equip_id)))
    else:
        page = flask.abort(code=404)
    return page


@app.route("/replace-work-to-point/<work_id>")
def replace_work_to_point(work_id: int) -> Response:
    """Redirect to new form to select new point for work"""
    if is_integer(work_id):
        page = goto_or_redirect(lambda: select_new_point_for_work_form(work_id, stylesheet_number()))
    else:
        page = flask.abort(code=404)
    return page


@app.route("/replace-work-to-point-method", methods=['POST'])
def replace_work_to_point_method() -> Response:
    """Redirect to form select equip to move work"""
    return goto_or_redirect(lambda: select_new_equip_for_work_form(functions.form_to_data(request.form),
                                                                   request.method,
                                                                   stylesheet_number()))


@app.route("/replace-work-to-equip-method", methods=['POST'])
def replace_work_to_new_equip() -> Response:
    """Redirect to method analyze and move work to correct equip"""
    return goto_or_redirect(lambda: move_work_to_new_equip(functions.form_to_data(request.form),
                                                           request.method,
                                                           stylesheet_number()))


@app.route("/all-works")
def all_works() -> Response:
    """Return page contain all works"""
    return goto_or_redirect(lambda: work_to_equip(0))


@app.route("/add-work", methods=['POST'])
def add_work() -> Response:
    """Redirect to method added work to current EQUIP"""
    return goto_or_redirect(lambda: add_work_method(functions.form_to_data(request.form),
                                                    request.method,
                                                    stylesheet_number()))
