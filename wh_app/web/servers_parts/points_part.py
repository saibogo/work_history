"""This module contain all actions from workspoints for Flask server.py"""
import flask

from wh_app.web.servers_parts.support_part import *
from wh_app.web.servers_parts.errors_part import page_not_found
from wh_app.web.workers_section import create_new_binding_method, delete_binding_method
from wh_app.web.points_section import points_operations, all_points_table,\
    create_new_point_page, add_point_method, all_works_points_table,\
    edit_point_method, upgrade_point_method, on_off_point_method, \
    invert_point_status_method, point_tech_info, edit_tech_section, edit_point_tech_method, create_bindings_form,\
    top_10_points_page


@app.route("/points")
def points() -> Response:
    """Return main page POINTS-section"""
    return goto_or_redirect(lambda: points_operations(stylesheet_number()), functions.NO_ROLE)


@app.route("/tech-info/<point_num>")
def tech_info(point_num: str) -> Response:
    """Return page. contain all technical information from current point"""
    if is_integer(point_num):
        page = Response(point_tech_info(int(point_num), stylesheet_number()), functions.ROLE_CUSTOMER)
    else:
        page = flask.abort(code=404)
    return page


@app.route("/all-points")
def all_points() -> Response:
    """Return page, contain all points in database """
    return goto_or_redirect(lambda: all_points_table(stylesheet_number()), functions.NO_ROLE)


@app.route("/create-new-point")
def create_new_point() -> Response:
    """Return page to create new workspoint"""
    return goto_or_redirect(lambda: create_new_point_page(stylesheet_number()), functions.ROLE_SUPERUSER)


@app.route('/add-point', methods=['POST'])
def add_point() -> Response:
    """Redirect to method create new workspoint"""
    return goto_or_redirect(lambda: add_point_method(functions.form_to_data(request.form),
                                                     request.method,
                                                     stylesheet_number()), functions.ROLE_SUPERUSER)


@app.route("/works-points")
def works_points() -> Response:
    """Return page, contain all points in database. where status WORK=True"""
    return goto_or_redirect(lambda: all_works_points_table(stylesheet_number()), functions.NO_ROLE)


@app.route("/edit-point/<point_id>")
def edit_point(point_id: int) -> Response:
    """Return page to edit current workspoint"""
    if is_integer(point_id):
        page = goto_or_redirect(lambda: edit_point_method(str(point_id), stylesheet_number()), functions.ROLE_SUPERUSER)
    else:
        page = flask.abort(code=404)
    return page


@app.route("/on-off-point/<point_id>")
def on_off_point(point_id: int) -> Response:
    """Return page invert status WORK"""
    if is_integer(point_id):
        page = goto_or_redirect(lambda: on_off_point_method(str(point_id), stylesheet_number()), functions.ROLE_SUPERUSER)
    else:
        page = flask.abort(code=404)
    return page


@app.route("/upgrade-point-info", methods=['POST'])
def upgrade_point_info() -> Response:
    """Redirect to method upgraded data from point in database"""
    return goto_or_redirect(lambda: upgrade_point_method(functions.form_to_data(request.form),
                                                         request.method,
                                                         stylesheet_number()), functions.ROLE_SUPERUSER)


@app.route("/invert-point-status", methods=['POST'])
def invert_point_status() -> Response:
    """Redirect to method update WORK status in database from current point"""
    return goto_or_redirect(lambda: invert_point_status_method(functions.form_to_data(request.form),
                                                               request.method,
                                                               stylesheet_number()), functions.ROLE_SUPERUSER)


@app.route("/edit-bindings/<point_id>")
def edit_bindings_in_point(point_id: str) -> Response:
    """Go to page with edit bindings forms"""
    if is_integer(point_id):
        page = goto_or_redirect(lambda: create_bindings_form(point_id, stylesheet_number()), functions.ROLE_SUPERUSER)
    else:
        page = flask.abort(code=404)
    return page


@app.route("/add-new-binding", methods=['POST'])
def add_new_binding() -> Response:
    """Redirect to method analyze data for new binding"""
    return goto_or_redirect(lambda: create_new_binding_method(functions.form_to_data(request.form),
                                                              request.method,
                                                              stylesheet_number()), functions.ROLE_SUPERUSER)


@app.route("/remove-binding", methods=['POST'])
def remove_binding() -> Response:
    """Redirect to method. delete current binding"""
    return goto_or_redirect(lambda: delete_binding_method(functions.form_to_data(request.form),
                                                          request.method,
                                                          stylesheet_number()), functions.ROLE_SUPERUSER)


@app.route("/edit-electric/<point_num>")
def edit_electric(point_num: int) -> Response:
    """Create form to edit electric partition technical information to workspoint"""
    if is_integer(point_num):
        page = goto_or_redirect(lambda: edit_tech_section(point_num, 'electric', stylesheet_number()), functions.ROLE_SUPERUSER)
    else:
        page = flask.abort(code=404)
    return page


@app.route("/edit-cold-water/<point_num>")
def edit_cold_water(point_num: int) -> Response:
    """Create form to edit cold-water partition technical information to workspoint"""
    if is_integer(point_num):
        page = goto_or_redirect(lambda: edit_tech_section(point_num, 'cold-water', stylesheet_number()), functions.ROLE_SUPERUSER)
    else:
        page = flask.abort(code=404)
    return page


@app.route("/edit-hot-water/<point_num>")
def edit_hot_water(point_num: int) -> Response:
    """Create form to edit hot-water partition technical information to workspoint"""
    if is_integer(point_num):
        page = goto_or_redirect(lambda: edit_tech_section(point_num, 'hot-water', stylesheet_number()), functions.ROLE_SUPERUSER)
    else:
        page = flask.abort(code=404)
    return page


@app.route("/edit-heating/<point_num>")
def edit_heating(point_num: int) -> Response:
    """Create form to edit heating partition technical information to workspoint"""
    if is_integer(point_num):
        page = goto_or_redirect(lambda: edit_tech_section(point_num, 'heating', stylesheet_number()), functions.ROLE_SUPERUSER)
    else:
        page = flask.abort(code=404)
    return page


@app.route("/edit-sewerage/<point_num>")
def edit_sewerage(point_num: int) -> Response:
    """Create form to edit sewerage partition technical information to workspoint"""
    if is_integer(point_num):
        page = goto_or_redirect(lambda: edit_tech_section(point_num, 'sewerage', stylesheet_number()), functions.ROLE_SUPERUSER)
    else:
        page = flask.abort(code=404)
    return page


@app.route("/edit-section-method/<section_name>", methods=['POST'])
def edit_section_method(section_name: str) -> Response:
    """Create form to edit sewerage partition technical information to workspoint"""
    return goto_or_redirect(lambda: edit_point_tech_method(section_name,
                                                           functions.form_to_data(request.form),
                                                           request.method,
                                                           stylesheet_number()), functions.ROLE_SUPERUSER)


@app.route("/svu/<point_id>")
def get_svu(point_id: str) -> Response:
    """Return electric scheme if avaliable"""
    try:
        return send_from_directory(config.static_dir(), 'image/svu/svu_{0}.jpg'.format(point_id))
    except:
        return page_not_found(404)


@app.route("/top-10-points")
def top_10_points() -> Response:
    """Return HTML with table points with mawimal works"""

    return goto_or_redirect(lambda: top_10_points_page(stylesheet_number()), functions.NO_ROLE)



