"""This module contain all rules WEB-section"""
import flask
from flask import Flask, request, redirect, session, Response
from flask import send_from_directory, send_file
from typing import Callable, Any
import time
from fpdf import FPDF

import wh_app.web.template as web_template
import wh_app.web.universal_html as uhtml
from wh_app.config_and_backup import config
from wh_app.supporting import functions
from wh_app.web.any_section import main_web_menu, faq_page, statistics_page,\
    system_status_page, new_theme_page, viev_changelog, login_input_page
from wh_app.web.equips_section import equip_to_point_limit, find_equip_to_id_page,\
    select_equip_to_id_page, add_equip_method, equips_menu, edit_equip_method,\
    upgrade_equip_method, select_point_to_equip_method, move_equip_method,\
    remove_table_page
from wh_app.web.find_section import find_page, find_method, find_work_paging,\
    find_work_like_date_paging, find_point_page, find_equip_page, find_work_like_performer_and_date_paging
from wh_app.web.points_section import points_operations, all_points_table,\
    create_new_point_page, add_point_method, all_works_points_table,\
    edit_point_method, upgrade_point_method, on_off_point_method, \
    invert_point_status_method, point_tech_info
from wh_app.web.workers_section import workers_menu, all_workers_table,\
    works_days_page, works_from_performers_table, add_performer_to_work,\
    add_performer_result_method, weekly_chart_page
from wh_app.web.works_section import works_menu, find_work_to_id_page,\
    select_work_to_id_method, work_to_equip_paging, add_work_method, create_edit_work_form, update_work_method
from wh_app.web.bugs_section import bugs_menu, all_bugs_table, all_bugs_in_work_table,\
    add_bugs_result_table, create_invert_bug_status_form, invert_bug_status_method, all_bugs_table_limit,\
    all_bugs_in_work_limit
from wh_app.web.orders_section import all_customers_table, orders_main_menu,\
    all_registered_orders_table
from wh_app.web.universal_html import LOGIN, PASSWORD, access_denided, access_allowed, logout_user
from wh_app.web.template import result_page
from wh_app.supporting.pdf_operations.pdf import equips_in_point, works_from_equip,\
    works_from_performer, weekly_charts_pdf, move_equip, point_tech_information


app = Flask(__name__, static_folder=config.static_dir(), template_folder=config.template_folder())
app.secret_key = 'gleykh secret key'
functions.info_string(__name__)

THEME_NUMBER = 'theme_number'
THEMES_MAXIMAL = 2
LOGIN_IS_CORRECT = 'access_is_allowed'
TIME_LOGIN = 'time_login'


def stylesheet_number() -> str:
    """Function return string contains number decors themes"""
    if THEME_NUMBER in session:
        session[THEME_NUMBER] = session.get(THEME_NUMBER)
    else:
        session[THEME_NUMBER] = 0  # default number theme

    return session.get(THEME_NUMBER)


def access_is_allowed() -> bool:
    """Function return if user input correct login and password"""
    if (LOGIN_IS_CORRECT in session) and\
            (TIME_LOGIN in session) and\
            (time.time() - session[TIME_LOGIN] < config.max_session_time()):
        session[LOGIN_IS_CORRECT] = session.get(LOGIN_IS_CORRECT)
        session[TIME_LOGIN] = time.time()
    else:
        session[LOGIN_IS_CORRECT] = False
    session.modified = True
    return session.get(LOGIN_IS_CORRECT)


def goto_or_redirect(function: Callable) -> Any:
    if access_is_allowed():
        return function()
    else:
        return redirect('/login')


@app.route('/login')
def login_page() -> str:
    """Redirect to LOGIN-form"""

    return login_input_page()


@app.route('/logout')
def logout_page() -> str:
    """Function call logout-function for user and redirect to LOGOUT-page"""

    session[LOGIN_IS_CORRECT] = False
    session.modified = True
    return result_page(logout_user(), '/login', stylesheet_number())


@app.route('/login-verification',  methods=['POST'])
def login_verification() -> str:
    """Function compare pair login-password with data in system and redirect to new page"""

    if functions.is_login_and_password_correct(request.form[LOGIN], request.form[PASSWORD]):
        print("Успешная верификация пользователя ", request.form[LOGIN])
        session[LOGIN_IS_CORRECT] = True
        session[TIME_LOGIN] = time.time()
        session.modified = True
        result = access_allowed(request.form[LOGIN])
    else:
        print("Неудачная попытка входа пользователя ", request.form[LOGIN])
        result = access_denided(request.form[LOGIN])
    return result_page(result, '/')


@app.route("/")
def main_page() -> Response:
    """Return main web-page"""
    return goto_or_redirect(lambda:  main_web_menu(stylesheet_number()))


@app.route('/favicon.ico')
def favicon() -> Any:
    """Return static favicon-logo to web-page"""
    return send_from_directory(config.static_dir(), 'favicon.ico')


@app.route('/style<number>.css')
def styles(number: int) -> Response:
    """Return selected CSS-page from static folder"""
    return send_from_directory(config.static_dir(), 'style{0}.css'.format(number))


@app.route('/<folder>/style<number>.css')
def styles_table(folder: str, number: int) -> Response:
    """Return selected CSS-page from static folder"""
    return send_from_directory(config.static_dir(), '{0}/style{1}.css'.format(folder, number))


@app.route('/image/background<number>.jpg')
def get_background_image(number: int) -> Response:
    """Return selected background from static folder"""
    return send_from_directory(config.static_dir(), 'image/background{0}.jpg'.format(number))


@app.route("/equips")
def equips_section() -> Response:
    """Return main page EQUIPS-section"""
    return goto_or_redirect(lambda: equips_menu(stylesheet_number()))


@app.route("/points")
def points() -> Response:
    """Return main page POINTS-section"""
    return goto_or_redirect(lambda: points_operations(stylesheet_number()))


@app.route("/tech-info/<point_num>")
def tech_info(point_num: str) -> Response:
    """Return page. contain all technical information from current point"""

    return Response(point_tech_info(int(point_num), stylesheet_number()))


@app.route("/all-points")
def all_points() -> Response:
    """Return page, contain all points in database """
    return goto_or_redirect(lambda: all_points_table(stylesheet_number()))


@app.route("/create-new-point")
def create_new_point() -> Response:
    """Return page to create new workspoint"""
    return goto_or_redirect(lambda: create_new_point_page(stylesheet_number()))


@app.route('/add-point', methods=['POST'])
def add_point() -> Response:
    """Redirect to method create new workspoint"""
    return goto_or_redirect(lambda: add_point_method(functions.form_to_data(request.form),
                                                     request.method,
                                                     stylesheet_number()))


@app.route("/works-points")
def works_points() -> Response:
    """Return page, contain all points in database. where status WORK=True"""
    return goto_or_redirect(lambda: all_works_points_table(stylesheet_number()))


@app.route("/edit-point/<point_id>")
def edit_point(point_id: int) -> Response:
    """Return page to edit current workspoint"""
    return goto_or_redirect(lambda: edit_point_method(str(point_id), stylesheet_number()))


@app.route("/on-off-point/<point_id>")
def on_off_point(point_id: int) -> Response:
    """Return page invert status WORK"""
    return goto_or_redirect(lambda: on_off_point_method(str(point_id), stylesheet_number()))


@app.route("/upgrade-point-info", methods=['POST'])
def upgrade_point_info() -> Response:
    """Redirect to method upgraded data from point in database"""
    return goto_or_redirect(lambda: upgrade_point_method(functions.form_to_data(request.form),
                                                         request.method,
                                                         stylesheet_number()))


@app.route("/invert-point-status", methods=['POST'])
def invert_point_status() -> Response:
    """Redirect to method update WORK status in database from current point"""
    return goto_or_redirect(lambda: invert_point_status_method(functions.form_to_data(request.form),
                                                               request.method,
                                                               stylesheet_number()))


@app.route("/equip/<point_id>")
def equip_to_point(point_id: int) -> Response:
    """Return first page in ALL EQUIP in current Point"""
    return goto_or_redirect(lambda: redirect('/equip/{0}/page/1'.format(point_id)))


@app.route("/all-equips")
def all_equips_table() -> Response:
    """Return page, contain ALL EQUIP"""
    return goto_or_redirect(lambda: equip_to_point(0))


@app.route("/equip/<point_id>/page/<page_num>")
def equip_point_id_page(point_id: int, page_num: int):
    """Return page №page_num in ALL EQUIP in current point"""
    return goto_or_redirect(lambda: equip_to_point_limit(point_id, page_num, stylesheet_number()))


@app.route("/edit-equip/<equip_id>")
def edit_equip_page(equip_id: str) -> Response:
    """Return page to EDIT current EQUIP"""
    return goto_or_redirect(lambda: edit_equip_method(str(equip_id), stylesheet_number()))


@app.route("/upgrade-equip-info", methods=['POST'])
def upgrade_equip_info() -> Response:
    """Redirect to method UPGRADE EQUIP INFO in database"""
    return goto_or_redirect(lambda: upgrade_equip_method(functions.form_to_data(request.form),
                                                         request.method,
                                                         stylesheet_number()))


@app.route('/find-equip-to-id')
def find_equip_to_id() -> Response:
    """Return page, contain FIND FORM in EQUIPS List in database"""
    return goto_or_redirect(lambda: find_equip_to_id_page(stylesheet_number()))


@app.route("/select-equip-to-id", methods=['POST'])
def select_equip_to_id() -> Response:
    """Redirect to method, returned full information to EQUIP"""
    return goto_or_redirect(lambda: select_equip_to_id_page(functions.form_to_data(request.form),
                                                            request.method,
                                                            stylesheet_number()))


@app.route("/change-point/<equip_id>")
def change_point_to_equip(equip_id: int) -> Response:
    """Return page, contain FORM to CHANGE new point-location from selected EQUIP"""
    return goto_or_redirect(lambda: select_point_to_equip_method(str(equip_id), stylesheet_number()))


@app.route("/add-equip", methods=['POST'])
def add_equip() -> Response:
    """Redirect to method append new equip in current point"""
    return goto_or_redirect(lambda: add_equip_method(functions.form_to_data(request.form),
                                                     request.method,
                                                     stylesheet_number()))


@app.route("/table-to-pdf/<data>")
def html_table_to_pdf(data:str) -> Response:
    """Redirect to method generate pdf-version current main-table
    correct adr /table-to-pdf/<section>=<value>"""

    command_table = {"point": equips_in_point,
                     "equip": works_from_equip,
                     "performer": works_from_performer,
                     "weekly": weekly_charts_pdf,
                     "move-equip-pdf": move_equip,
                     "point-tech": point_tech_information}
    section, value = data.split('=')

    try:
        pdf = command_table[section](value)
    except:
        pdf: FPDF = FPDF()

    pdf.output(config.path_to_pdf)
    return send_file(config.path_to_pdf) \
        if section == "weekly" \
        else goto_or_redirect(lambda : send_file(config.path_to_pdf))


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
    return goto_or_redirect(lambda: work_to_equip_paging(equip_id, page_id, stylesheet_number()))


@app.route("/work-edit/<work_id>")
def work_edit(work_id: int) -> Response:
    """Return form to EDIT some work"""
    return goto_or_redirect(lambda : create_edit_work_form(work_id, stylesheet_number()))


@app.route("/update-work-to-id/<work_id>", methods=['POST'])
def update_work_to_id(work_id: int) -> Response:
    """Go to method update work info"""

    return goto_or_redirect(lambda: update_work_method(work_id,
                                                       functions.form_to_data(request.form),
                                                       request.method,
                                                       stylesheet_number()))



@app.route("/work/<equip_id>")
def work_to_equip(equip_id: int) -> Response:
    """Redirect to first page in ALL work from EQUIP where EQUIP_ID=equip_id"""
    return goto_or_redirect(lambda: redirect('/work/{0}/page/1'.format(equip_id)))


@app.route("/remove-equip", methods=['POST'])
def remove_equip_method() -> Response:
    """Redirect to method removed EQUIP to new point"""
    return goto_or_redirect(lambda: move_equip_method(functions.form_to_data(request.form),
                                                      request.method,
                                                      stylesheet_number()))


@app.route("/remove-table/<equip_id>")
def remove_table(equip_id: int) -> Response:
    """Return page with all move current EQUIP"""
    return goto_or_redirect(lambda: remove_table_page(str(equip_id), stylesheet_number()))


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


@app.route("/workers")
def workers() -> Response:
    """Return main page WORKERS-section"""
    return flask.make_response(workers_menu(stylesheet_number()))


@app.route("/all-workers")
def all_workers() -> Response:
    """Return page, contain All WORKERS"""
    return flask.make_response(all_workers_table(stylesheet_number()))


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
    return goto_or_redirect(lambda: works_from_performers_table(performer_id,
                                                                1,
                                                                request.args.get('page',
                                                                                 default=config.full_address(),
                                                                                 type=str),
                                                                stylesheet_number()))


@app.route("/performer/<performer_id>/page/<page_num>", methods=['GET'])
def performer_id_page(performer_id: int, page_num: int) -> Response:
    """See also performer_performer_id but use paging"""

    return goto_or_redirect(lambda: works_from_performers_table(performer_id,
                                                                page_num,
                                                                request.args.get('page',
                                                                                 default=config.full_address(),
                                                                                 type=str),
                                                                stylesheet_number()))


@app.route('/find/performer/<performer_id>/<data_start>/<data_stop>/page/<page_num>', methods=['GET'])
def find_work_performer_to_data(performer_id: str, data_start: str, data_stop: str, page_num: str) -> Response:
    """Return page, contain result like name or sub_name and in datetime interval [start, stop]"""
    return goto_or_redirect(lambda: find_work_like_performer_and_date_paging(performer_id, data_start,
                                                                             data_stop, page_num,
                                                                             stylesheet_number()))


@app.route("/add-performer-to-work/<work_id>", methods=['GET'])
def add_performer_to_work_work_id(work_id: int) -> Response:
    """Redirect to form append performer in current work"""
    return goto_or_redirect(lambda: add_performer_to_work(work_id,
                                                          request.args.get('page',
                                                                           default=config.full_address(),
                                                                           type=str),
                                                          stylesheet_number()))


@app.route('/add-performer-result', methods=['POST'])
def add_performer_result() -> Response:
    """Redirect to method add performer in current work"""
    return goto_or_redirect(lambda: add_performer_result_method(functions.form_to_data(request.form),
                                                                request.method,
                                                                stylesheet_number()))


@app.route("/FAQ", methods=['GET'])
def faq() -> Response:
    """Return FAQ-page"""
    return goto_or_redirect(lambda: faq_page(request.args.get('page',
                                                              default=config.full_address(),
                                                              type=str),
                                             stylesheet_number()))


@app.route('/statistics', methods=['GET'])
def statistics() -> Response:
    """Return STATISTIC-page"""
    return goto_or_redirect(lambda: statistics_page(request.args.get('page',
                                                                     default=config.full_address(),
                                                                     type=str),
                                                    stylesheet_number()))


@app.route('/system-status', methods=['GET'])
def system_status() -> Response:
    """Return page, contain status all system components"""
    return goto_or_redirect(lambda: system_status_page(request.args.get('page',
                                                                        default=config.full_address(),
                                                                        type=str),
                                                       stylesheet_number()))


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


@app.route('/find/work/<find_string>/page/<page_num>')
def find_work_find_string_page_page_num(find_string: str, page_num: int) -> Response:
    """Return result find work page"""
    return goto_or_redirect(lambda: find_work_paging(find_string,
                                                     str(page_num),
                                                     stylesheet_number()))


@app.route('/find/work/<find_string>/<data_start>/<data_stop>/page/<page_num>')
def find_work_data_to_data(find_string: str, data_start: str, data_stop: str, page_num: int) -> Response:
    """Return page, contain result like WORK_NAME and WORK_DATE"""
    return goto_or_redirect(lambda: find_work_like_date_paging(find_string,
                                                               data_start,
                                                               data_stop,
                                                               str(page_num),
                                                               stylesheet_number()))


@app.route('/find/point/<find_string>/page/<page_num>')
def find_point(find_string: str, page_num: int) -> Response:
    """Return result find point"""
    return goto_or_redirect(lambda: find_point_page(find_string,
                                                    str(page_num),
                                                    stylesheet_number()))


@app.route('/find/equip/<find_string>/page/<page_num>')
def find_equip(find_string: str, page_num: int) -> Response:
    """return result find EQUIP"""
    return goto_or_redirect(lambda: find_equip_page(find_string,
                                                    str(page_num),
                                                    stylesheet_number()))


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
    return goto_or_redirect(lambda: all_bugs_table_limit(page_num ,stylesheet_number()))


@app.route('/all-bugs-in-work')
def all_bugs_in_work() -> Response:
    """return all unclosed bugs page"""
    return goto_or_redirect(lambda: all_bugs_in_work_table(stylesheet_number()))


@app.route('/all-bugs-in-work/<page_num>')
def all_bugs_in_work_paging(page_num: int) -> Response:
    """return all unclosed bugs page with limit records on page"""
    return goto_or_redirect(lambda: all_bugs_in_work_limit(page_num, stylesheet_number()))


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
    return goto_or_redirect(lambda: create_invert_bug_status_form(bug_num, stylesheet_number()))


@app.route('/common-invert-bug-status', methods=['POST'])
def common_invert_bug_status() -> Response:
    """Redirect to method inverted bug-status"""
    return goto_or_redirect(lambda: invert_bug_status_method(functions.form_to_data(request.form),
                                                             request.method,
                                                             stylesheet_number()))


@app.route('/server-ready-to-shutdown')
def server_ready_to_shutdown() -> str:
    """Return message from admin"""
    message = ""
    try:
        message_file = open(config.path_to_messages(), 'r')
        for line in message_file:
            message += line
    except FileNotFoundError:
        pass
    return message


@app.route('/orders-and-customers')
def orders_and_customers() -> Response:
    """Return main page ORDERS-sections"""
    return goto_or_redirect(lambda: orders_main_menu(stylesheet_number()))


@app.route('/all-customers-table')
def all_customers_table_server() -> Response:
    """Return ALL CUSTOMERS page"""
    return goto_or_redirect(lambda: all_customers_table(stylesheet_number()))


@app.route('/all-registred-orders')
def all_registred_orders() -> Response:
    """Return ALL ORDERS page"""
    return goto_or_redirect(lambda: all_registered_orders_table(stylesheet_number()))


@app.route('/next-themes')
def next_themes() -> str:
    """redirect to new themes methods"""
    if THEME_NUMBER in session:
        session[THEME_NUMBER] = session.get(THEME_NUMBER) + 1
    else:
        session[THEME_NUMBER] = 0  # default number theme
    session[THEME_NUMBER] %= THEMES_MAXIMAL
    session.modified = True
    return new_theme_page(session[THEME_NUMBER])


@app.route('/changelog-page')
def changelog_page() -> Response:
    """Return ALL CHANGELOG page"""
    return goto_or_redirect(lambda: viev_changelog(stylesheet_number()))


@app.route("/svu/<point_id>")
def get_svu(point_id: str) -> Response:
    """Return electric scheme if avaliable"""
    try:
        return send_from_directory(config.static_dir(), 'image/svu/svu_{0}.jpg'.format(point_id))
    except:
        return page_not_found(404)


@app.errorhandler(404)
def page_not_found(error: Any) -> Response:
    """Return network error handling page 404"""
    print(error)
    return goto_or_redirect(lambda: web_template.result_page(uhtml.html_page_not_found(),
                                                             '/',
                                                             stylesheet_number()))


@app.errorhandler(405)
def method_not_allowed(error: Any) -> Response:
    """Return network error handling page 405"""
    print(error)
    return goto_or_redirect(lambda: web_template.result_page(uhtml.html_page_not_found(),
                                                             '/',
                                                             stylesheet_number()))


@app.errorhandler(500)
def page_internal_server_error(error: Any) -> Response:
    """Return network error handling page 500"""
    print(error)
    return goto_or_redirect(lambda: web_template.result_page(uhtml.html_internal_server_error(),
                                                             '/',
                                                             stylesheet_number()))


@app.route('/not_found')
def not_found():
    """See page_not_found()"""
    return 'Oops!', 404


def start_server():
    """Start development server"""
    app.run(host='0.0.0.0')


if __name__ == "__main__":
    start_server()
