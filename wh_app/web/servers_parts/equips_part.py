"""This module contain all actions from equipment for Flask server.py"""
import flask

from wh_app.web.servers_parts.support_part import *
from wh_app.web.equips_section import equip_to_point_limit,\
    select_equip_to_id_page, add_equip_method, equips_menu, edit_equip_method,\
    upgrade_equip_method, select_point_to_equip_method, move_equip_method,\
    remove_table_page, top_equips_from_maximal_works


@app.route("/equips")
def equips_section() -> Response:
    """Return main page EQUIPS-section"""
    return goto_or_redirect(lambda: equips_menu(stylesheet_number()), functions.ROLE_CUSTOMER)


@app.route("/equip/<point_id>")
def equip_to_point(point_id: int) -> Response:
    """Return first page in ALL EQUIP in current Point"""
    if is_integer(point_id):
        page = goto_or_redirect(lambda: redirect('/equip/{0}/page/1'.format(point_id)), functions.ROLE_CUSTOMER)
    else:
        page = flask.abort(code=404)
    return page


@app.route("/all-equips")
def all_equips_table() -> Response:
    """Return page, contain ALL EQUIP"""
    return goto_or_redirect(lambda: equip_to_point(0), functions.ROLE_CUSTOMER)


@app.route("/equip/<point_id>/page/<page_num>")
def equip_point_id_page(point_id: int, page_num: int):
    """Return page №page_num in ALL EQUIP in current point"""
    if is_integer(point_id) and is_integer(page_num):
        page = goto_or_redirect(lambda: equip_to_point_limit(point_id, page_num, stylesheet_number()), functions.ROLE_CUSTOMER)
    else:
        page = flask.abort(code=404)
    return page


@app.route("/edit-equip/<equip_id>")
def edit_equip_page(equip_id: str) -> Response:
    """Return page to EDIT current EQUIP"""
    if is_integer(equip_id):
        page = goto_or_redirect(lambda: edit_equip_method(str(equip_id), stylesheet_number()), functions.ROLE_WORKER)
    else:
        page = flask.abort(code=404)
    return page


@app.route("/upgrade-equip-info", methods=['POST'])
def upgrade_equip_info() -> Response:
    """Redirect to method UPGRADE EQUIP INFO in database"""
    return goto_or_redirect(lambda: upgrade_equip_method(functions.form_to_data(request.form),
                                                         request.method,
                                                         stylesheet_number()), functions.ROLE_WORKER)


@app.route("/select-equip-to-id", methods=['POST'])
def select_equip_to_id() -> Response:
    """Redirect to method, returned full information to EQUIP"""
    return goto_or_redirect(lambda: select_equip_to_id_page(functions.form_to_data(request.form),
                                                            request.method,
                                                            stylesheet_number()), functions.ROLE_CUSTOMER)


@app.route("/change-point/<equip_id>")
def change_point_to_equip(equip_id: int) -> Response:
    """Return page, contain FORM to CHANGE new point-location from selected EQUIP"""
    if is_integer(equip_id):
        page = goto_or_redirect(lambda: select_point_to_equip_method(str(equip_id), stylesheet_number()), functions.ROLE_SUPERUSER)
    else:
        page = flask.abort(code=404)
    return page


@app.route("/add-equip", methods=['POST'])
def add_equip() -> Response:
    """Redirect to method append new equip in current point"""
    return goto_or_redirect(lambda: add_equip_method(functions.form_to_data(request.form),
                                                     request.method,
                                                     stylesheet_number()), functions.ROLE_WORKER)


@app.route("/remove-equip", methods=['POST'])
def remove_equip_method() -> Response:
    """Redirect to method removed EQUIP to new point"""
    return goto_or_redirect(lambda: move_equip_method(functions.form_to_data(request.form),
                                                      request.method,
                                                      stylesheet_number()), functions.ROLE_SUPERUSER)


@app.route("/remove-table/<equip_id>")
def remove_table(equip_id: int) -> Response:
    """Return page with all move current EQUIP"""
    if is_integer(equip_id):
        page = goto_or_redirect(lambda: remove_table_page(str(equip_id), stylesheet_number()), functions.ROLE_CUSTOMER)
    else:
        page = flask.abort(code=404)
    return page


@app.route("/top-10-from-works")
def top_10_equips_from_work() -> Response:
    """Return page with top-10 equip with maximal count of works"""
    return goto_or_redirect(lambda: top_equips_from_maximal_works(stylesheet_number()), functions.NO_ROLE)