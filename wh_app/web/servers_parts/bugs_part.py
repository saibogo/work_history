"""This module contain all actions with bugs for Flask server.py"""

from wh_app.web.servers_parts.support_part import *
from wh_app.web.bugs_section import bugs_menu, all_bugs_table, all_bugs_in_work_table,\
    add_bugs_result_table, create_invert_bug_status_form, invert_bug_status_method, all_bugs_table_limit,\
    all_bugs_in_work_limit


@app.route('/bugs')
def bugs() -> Response:
    """Return main page to BUGS-section"""
    return goto_or_redirect(lambda: bugs_menu(stylesheet_number()))


@app.route('/all-bugs')
def all_bugs() -> Response:
    """Return all registered problem"""
    return goto_or_redirect(lambda: all_bugs_table(stylesheet_number()))


@app.route('/all-bugs/<page_num>')
def all_bugs_paging(page_num: int) -> Response:
    """Return all registered problem use limit records on page"""
    if is_integer(page_num):
        page = goto_or_redirect(lambda: all_bugs_table_limit(page_num ,stylesheet_number()))
    else:
        page = flask.abort(code=404)
    return page


@app.route('/all-bugs-in-work')
def all_bugs_in_work() -> Response:
    """return all unclosed bugs page"""
    return goto_or_redirect(lambda: all_bugs_in_work_table(stylesheet_number()))


@app.route('/all-bugs-in-work/<page_num>')
def all_bugs_in_work_paging(page_num: int) -> Response:
    """return all unclosed bugs page with limit records on page"""
    if is_integer(page_num):
        page = goto_or_redirect(lambda: all_bugs_in_work_limit(page_num, stylesheet_number()))
    else:
        page = flask.abort(code=404)
    return page


@app.route('/add-bug')
def add_bug() -> Response:
    """Return form to create new bug"""
    return goto_or_redirect(lambda: web_template.result_page(uhtml.new_bug_input_table(),
                                                             '/bugs',
                                                             stylesheet_number()))


@app.route('/add-bug-result', methods=['POST'])
def add_bug_result() -> Response:
    """Redirect to method append bug in database"""
    return goto_or_redirect(lambda: add_bugs_result_table(functions.form_to_data(request.form),
                                                          request.method,
                                                          stylesheet_number()))


@app.route('/invert-bug-status/<bug_num>')
def invert_bug_status(bug_num: str) -> Response:
    """Redirect to form inverting bug status"""
    if is_integer(bug_num):
        page = goto_or_redirect(lambda: create_invert_bug_status_form(bug_num, stylesheet_number()))
    else:
        page = flask.abort(code=404)
    return page


@app.route('/common-invert-bug-status', methods=['POST'])
def common_invert_bug_status() -> Response:
    """Redirect to method inverted bug-status"""
    return goto_or_redirect(lambda: invert_bug_status_method(functions.form_to_data(request.form),
                                                             request.method,
                                                             stylesheet_number()))

