"""This module contain all actions with workers and performers for Flask server.py"""

from wh_app.web.servers_parts.support_part import *
from wh_app.web.workers_section import workers_menu, all_workers_table,\
    works_days_page, works_from_performers_table, add_performer_to_work,\
    add_performer_result_method, weekly_chart_page, create_edit_worker_form, update_worker_information,\
    current_workers_table,  remove_performer_from_work,\
    remove_performer_result_method, top_workers_page, create_new_worker_page, add_new_worker_method, schedule_menu_page,\
    today_schedule_page, week_schedule_page, add_info_in_schedule_form, insert_new_schedule_in_db


@app.route("/workers")
def workers() -> Response:
    """Return main page WORKERS-section"""
    return flask.make_response(workers_menu(stylesheet_number()))


@app.route("/all-workers")
def all_workers() -> Response:
    """Return page, contain All WORKERS"""
    return flask.make_response(all_workers_table(stylesheet_number()))


@app.route("/not-fired-workers")
def not_fired_workers() -> Response:
    """Return page with only NOT-FIRED workers"""
    return flask.make_response(current_workers_table(stylesheet_number()))


@app.route("/edit-worker/<worker_id>")
def edit_worker(worker_id: str) -> Response:
    """Return web-form to edit worker information"""
    if is_integer(worker_id):
        page = goto_or_redirect(lambda: create_edit_worker_form(worker_id, stylesheet_number()), functions.ROLE_SUPERUSER)
    else:
        page = flask.abort(code=404)
    return page


@app.route("/update-worker-to-id/<worker_id>", methods=['POST'])
def update_worker_to_id(worker_id: str) -> Response:
    """Update information in datadase from worker"""
    if is_integer(worker_id):
        page = goto_or_redirect(lambda: update_worker_information(worker_id, functions.form_to_data(request.form),
                                                                  request.method, stylesheet_number()), functions.ROLE_SUPERUSER)
    else:
        page = flask.abort(code=404)
    return page


@app.route("/weekly-chart")
def weekly_chart() -> Response:
    """Return page, contain all works-days to all workers"""

    return flask.make_response(weekly_chart_page(stylesheet_number()))


@app.route("/works-days")
def works_days() -> Response:
    """Return page current SHEDULE"""
    return flask.make_response(works_days_page(stylesheet_number()))


@app.route("/performer/<performer_id>", methods=['GET'])
def performer_performer_id(performer_id: int) -> Response:
    """Return ALL works where worker == performer_id"""
    if is_integer(performer_id):
        page = goto_or_redirect(lambda: works_from_performers_table(performer_id,
                                                                    1,
                                                                    request.args.get('page',
                                                                                     default=config.full_address(),
                                                                                     type=str),
                                                                    stylesheet_number()), functions.NO_ROLE)
    else:
        page = flask.abort(code=404)
    return page


@app.route("/performer/<performer_id>/page/<page_num>", methods=['GET'])
def performer_id_page(performer_id: int, page_num: int) -> Response:
    """See also performer_performer_id but use paging"""
    if is_integer(performer_id) and is_integer(page_num):
        page = goto_or_redirect(lambda: works_from_performers_table(performer_id,
                                                                    page_num,
                                                                    request.args.get('page',
                                                                                     default=config.full_address(),
                                                                                     type=str),
                                                                    stylesheet_number()), functions.NO_ROLE)
    else:
        page = flask.abort(code=404)
    return page


@app.route("/add-performer-to-work/<work_id>", methods=['GET'])
def add_performer_to_work_work_id(work_id: int) -> Response:
    """Redirect to form append performer in current work"""
    if is_integer(work_id):
        page = goto_or_redirect(lambda: add_performer_to_work(work_id,
                                                              request.args.get('page',
                                                                               default=config.full_address(),
                                                                               type=str),
                                                              stylesheet_number()), functions.ROLE_SUPERUSER)
    else:
        page = flask.abort(code=404)
    return page


@app.route("/remove-performer-to-work/<work_id>", methods=['GET'])
def remove_performer_to_work_work_id(work_id: int) -> Response:
    """Redirect to form append performer in current work"""
    if is_integer(work_id):
        page = goto_or_redirect(lambda: remove_performer_from_work(work_id,
                                                                   request.args.get('page',
                                                                                    default=config.full_address(),
                                                                                    type=str),
                                                                   stylesheet_number()), functions.ROLE_SUPERUSER)
    else:
        page = flask.abort(code=404)
    return page


@app.route('/add-performer-result', methods=['POST'])
def add_performer_result() -> Response:
    """Redirect to method add performer in current work"""
    return goto_or_redirect(lambda: add_performer_result_method(functions.form_to_data(request.form),
                                                                request.method,
                                                                stylesheet_number()), functions.ROLE_SUPERUSER)


@app.route('/remove-performer-result', methods=['POST'])
def remove_performer_result() -> Response:
    """Redirect to method add performer in current work"""
    return goto_or_redirect(lambda: remove_performer_result_method(functions.form_to_data(request.form),
                                                                request.method,
                                                                stylesheet_number()), functions.ROLE_SUPERUSER)


@app.route('/top-10-workers')
def top_workers() -> Response:
    """Return to top 10 workers page"""
    return goto_or_redirect(lambda: top_workers_page(stylesheet_number()), functions.NO_ROLE)


@app.route('/add-worker')
def add_worker() -> Response:
    """Return to top 10 workers page"""
    return goto_or_redirect(lambda: create_new_worker_page(stylesheet_number()), functions.ROLE_SUPERUSER)


@app.route('/add-worker-to-db', methods=['POST'])
def add_worker_to_db() -> Response:
    """Redirect to method add performer in current work"""
    return goto_or_redirect(lambda: add_new_worker_method(functions.form_to_data(request.form),
                                                          request.method,
                                                          stylesheet_number()), functions.ROLE_SUPERUSER)


@app.route('/schedule-menu')
def schedule_menu() -> Response:
    """Return menu with current schedule"""
    return goto_or_redirect(lambda: schedule_menu_page(stylesheet_number()), functions.NO_ROLE)


@app.route('/today-schedule')
def today_schedule() -> Response:
    """Return table with all workers work today"""
    return goto_or_redirect(lambda: today_schedule_page(stylesheet_number()), functions.NO_ROLE)


@app.route('/week-schedule')
def week_schedule() -> Response:
    """Return table with all workers work today and +7 days"""
    return goto_or_redirect(lambda: week_schedule_page(stylesheet_number()), functions.NO_ROLE)


@app.route('/add-info-in-schedule')
def add_info_in_schedule() -> Response:
    """Return table with all workers work today and +7 days"""
    return goto_or_redirect(lambda: add_info_in_schedule_form(stylesheet_number()), functions.ROLE_SUPERUSER)


@app.route('/insert-info-in-schedule', methods=['POST'])
def insert_info_in_schedule() -> Response:
    """Redirect to method add performer in current work"""
    return goto_or_redirect(lambda: insert_new_schedule_in_db(functions.form_to_data(request.form),
                                                              request.method,
                                                              stylesheet_number()), functions.ROLE_SUPERUSER)