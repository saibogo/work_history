"""This module contain all actions from equipment for Flask server.py"""
import flask

from wh_app.web.servers_parts.support_part import *
from wh_app.web.equips_section import equip_to_point_limit,\
    select_equip_to_id_page, add_equip_method, equips_menu, edit_equip_method,\
    upgrade_equip_method, select_point_to_equip_method, move_equip_method,\
    remove_table_page, top_equips_from_maximal_works, get_details_action, details_main_menu, current_subtypes_table,\
    all_exist_details_table, create_equip_subclass_form, create_equip_subtype_method, add_detail_file_form,\
    upload_detail_file_method, attach_detail_method, attach_detail_form, add_manual_file_form, upload_manual_file_method,\
    get_manuals_action, attach_manual_form, attach_manual_method


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


@app.route("/equip/<point_id>/page/<page_num>/<ord_column>")
def equip_point_id_page_order(point_id: int, page_num: int, ord_column: int):
    """Return page №page_num in ALL EQUIP in current point"""
    if is_integer(point_id) and is_integer(page_num):
        page = goto_or_redirect(lambda: equip_to_point_limit(point_id, page_num, stylesheet_number(), ord_column),
                                functions.ROLE_CUSTOMER)
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


@app.route('/get-details/<detail_id>')
def get_details(detail_id: int) -> Response:
    """Return PDF with detail scheme to equip if exist"""

    return goto_or_redirect_from_roles_list(lambda: get_details_action(detail_id), [functions.ROLE_SUPERUSER, functions.ROLE_WORKER])


@app.route('/get-manuals/<manual_id>')
def get_manuals(manual_id: int) -> Response:
    """Return PDF with detail scheme to equip if exist"""

    return goto_or_redirect_from_roles_list(lambda: get_manuals_action(manual_id), [functions.ROLE_SUPERUSER, functions.ROLE_CUSTOMER])


@app.route('/details-and-subclasses')
def details_and_subclasses() -> Response:
    """Go to main menu to work with details and equip subclasses"""

    return goto_or_redirect(lambda: details_main_menu(stylesheet_number()), functions.ROLE_SUPERUSER)


@app.route('/current-subclasses')
def current_subclasses() -> Response:
    """Go to table with all exists equips subtypes"""

    return goto_or_redirect(lambda: current_subtypes_table(stylesheet_number()), functions.ROLE_SUPERUSER)


@app.route('/all-details-from-type/<type_id>')
def all_details_from_type(type_id: int) -> Response:
    """Goto table with all details from this subtype"""

    return goto_or_redirect(lambda: all_exist_details_table(type_id, stylesheet_number()), functions.ROLE_SUPERUSER)


@app.route('/create-subclass')
def create_subclass() -> Response:
    """Goto form to create new subclass"""

    return goto_or_redirect(lambda: create_equip_subclass_form(stylesheet_number()), functions.ROLE_SUPERUSER)


@app.route('/create-subtype-common', methods=['POST'])
def create_subtype_common() -> Response:
    """Go to method to analize and create new subtype if all correct"""

    return goto_or_redirect(lambda: create_equip_subtype_method(functions.form_to_data(request.form),
                                                                request.method, stylesheet_number()),
                            functions.ROLE_SUPERUSER)


@app.route('/add-detail-file/<type_id>')
def add_detail_file(type_id: int) -> Response:
    """Goto form to upload details file to server"""

    return goto_or_redirect(lambda: add_detail_file_form(type_id, stylesheet_number()), functions.ROLE_SUPERUSER)


@app.route('/add-manual-file/<type_id>')
def add_manual_file(type_id: int) -> Response:
    """Goto form to upload details file to server"""

    return goto_or_redirect(lambda: add_manual_file_form(type_id, stylesheet_number()), functions.ROLE_SUPERUSER)


@app.route('/upload-detail-common', methods=['POST'])
def upload_detail_common() -> Response:
    """Goto method upload details file to server"""

    return goto_or_redirect(lambda: upload_detail_file_method(functions.form_to_data(request.form),
                                                              request.method, request.files['filename'],
                                                              stylesheet_number()), functions.ROLE_SUPERUSER)


@app.route('/upload-manual-common', methods=['POST'])
def upload_manual_common() -> Response:
    """Goto's method upload manual file on server"""

    return goto_or_redirect(lambda: upload_manual_file_method(functions.form_to_data(request.form),
                                                              request.method, request.files['filename'],
                                                              stylesheet_number()), functions.ROLE_SUPERUSER)


@app.route('/attach-detail/<equip_id>')
def attach_detail(equip_id: int) -> Response:
    """Goto form select equip detail"""

    return goto_or_redirect(lambda: attach_detail_form(equip_id, stylesheet_number()), functions.ROLE_SUPERUSER)


@app.route('/attach-manual/<equip_id>')
def attach_manual(equip_id: int) -> Response:
    """Goto form select equip detail"""

    return goto_or_redirect(lambda: attach_manual_form(equip_id, stylesheet_number()), functions.ROLE_SUPERUSER)


@app.route('/attach-detail-common', methods=['POST'])
def attach_detail_common() -> Response:
    """Goto's method add detail to equip"""

    return goto_or_redirect(lambda: attach_detail_method(functions.form_to_data(request.form),
                                                         request.method, stylesheet_number()), functions.ROLE_SUPERUSER)

@app.route('/attach-manual-common', methods=['POST'])
def attach_manual_common() -> Response:
    """Goto's method add detail to equip"""

    return goto_or_redirect(lambda: attach_manual_method(functions.form_to_data(request.form),
                                                         request.method, stylesheet_number()), functions.ROLE_SUPERUSER)