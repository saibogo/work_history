"""This module contain all rules WEB-section"""

from flask import Flask, request, redirect, session
from flask import send_from_directory

import wh_app.web.template as web_template
import wh_app.web.universal_html as uhtml
from wh_app.config_and_backup import config
from wh_app.supporting import functions
from wh_app.web.any_section import main_web_menu, faq_page, statistics_page,\
    system_status_page, new_theme_page, viev_changelog
from wh_app.web.equips_section import equip_to_point_limit, find_equip_to_id_page,\
    select_equip_to_id_page, add_equip_method, equips_menu, edit_equip_method,\
    upgrade_equip_method, select_point_to_equip_method, move_equip_method,\
    remove_table_page
from wh_app.web.find_section import find_page, find_method, find_work_paging,\
    find_work_like_date_paging, find_point_page, find_equip_page
from wh_app.web.points_section import points_operations, all_points_table,\
    create_new_point_page, add_point_method, all_works_points_table,\
    edit_point_method, upgrade_point_method, on_off_point_method, \
    invert_point_status_method
from wh_app.web.workers_section import workers_menu, all_workers_table,\
    works_days_page, works_from_performers_table, add_performer_to_work,\
    add_performer_result_method
from wh_app.web.works_section import works_menu, find_work_to_id_page,\
    select_work_to_id_method, work_to_equip_paging, add_work_method
from wh_app.web.bugs_section import bugs_menu, all_bugs_table, all_bugs_in_work_table,\
    add_bugs_result_table
from wh_app.web.orders_section import all_customers_table, orders_main_menu,\
    all_registered_orders_table


app = Flask(__name__, static_folder=config.static_dir)
app.secret_key = 'gleykh secret key'
functions.info_string(__name__)

THEME_NUMBER = 'theme_number'
THEMES_MAXIMAL = 2


def stylesheet_number() -> str:
    """Function return string contains number decors themes"""
    if THEME_NUMBER in session:
        session[THEME_NUMBER] = session.get(THEME_NUMBER)
    else:
        session[THEME_NUMBER] = 0  # default number theme

    return session.get(THEME_NUMBER)


@app.route("/")
def main_page():
    """Return main web-page"""
    return main_web_menu(stylesheet_number())


@app.route('/favicon.ico')
def favicon():
    """Return static favicon-logo to web-page"""
    return send_from_directory(config.static_dir, 'favicon.ico')


@app.route('/style<number>.css')
def styles(number):
    """Return selected CSS-page from static folder"""
    return send_from_directory(config.static_dir, 'style{0}.css'.format(number))


@app.route('/image/background<number>.jpg')
def get_background_image(number):
    """Return selected background from static folder"""
    return send_from_directory(config.static_dir, 'image/background{0}.jpg'.format(number))


@app.route("/equips")
def equips():
    """Return main page EQUIPS-section"""
    return equips_menu(stylesheet_number())


@app.route("/points")
def points():
    """Return main page POINTS-section"""
    return points_operations(stylesheet_number())


@app.route("/all-points")
def all_points():
    """Return page, contain all points in database """
    return all_points_table(stylesheet_number())


@app.route("/create-new-point")
def create_new_point():
    """Return page to create new workspoint"""
    return create_new_point_page(stylesheet_number())


@app.route('/add-point', methods=['POST'])
def add_point():
    """Redirect to method create new workspoint"""
    return add_point_method(functions.form_to_data(request.form),
                            request.method,
                            stylesheet_number())


@app.route("/works-points")
def works_points():
    """Return page, contain all points in database. where status WORK=True"""
    return all_works_points_table(stylesheet_number())


@app.route("/edit-point/<point_id>")
def edit_point(point_id: str):
    """Return page to edit current workspoint"""
    return edit_point_method(point_id, stylesheet_number())


@app.route("/on-off-point/<point_id>")
def on_off_point(point_id:str):
    """Return page invert status WORK"""
    return on_off_point_method(point_id, stylesheet_number())


@app.route("/upgrade-point-info", methods=['POST'])
def upgrade_point_info():
    """Redirect to method upgraded data from point in database"""
    return upgrade_point_method(functions.form_to_data(request.form),
                                request.method,
                                stylesheet_number())


@app.route("/invert-point-status", methods=['POST'])
def invert_point_status():
    """Redirect to method update WORK status in dtabase from current point"""
    return invert_point_status_method(functions.form_to_data(request.form),
                                      request.method,
                                      stylesheet_number())


@app.route("/equip/<point_id>")
def equip_to_point(point_id):
    """Return first page in ALL EQUIP in current Point"""
    return redirect('/equip/{0}/page/1'.format(point_id))


@app.route("/all-equips")
def all_equips_table():
    """Return page, contain ALL EQUIP"""
    return equip_to_point('0')


@app.route("/equip/<point_id>/page/<page_num>")
def equip_point_id_page(point_id, page_num):
    """Retutn page №page_num in ALL EQUIP in current point"""
    return equip_to_point_limit(point_id, page_num, stylesheet_number())


@app.route("/edit-equip/<equip_id>")
def edit_equip_page(equip_id: str) -> str:
    """Return page to EDIT current EQUIP"""
    return edit_equip_method(str(equip_id), stylesheet_number())


@app.route("/upgrade-equip-info", methods=['POST'])
def upgrade_equip_info():
    """Redirect to method UPGRADE EQUIP INFO in database"""
    return upgrade_equip_method(functions.form_to_data(request.form),
                                request.method,
                                stylesheet_number())


@app.route('/find-equip-to-id')
def find_equip_to_id():
    """Return page, contain FIND FORM in EQUIPS List in database"""
    return find_equip_to_id_page(stylesheet_number())


@app.route("/select-equip-to-id", methods=['POST'])
def select_equip_to_id():
    """Redirect to method, returned full information to EQUIP"""
    return select_equip_to_id_page(functions.form_to_data(request.form),
                                   request.method,
                                   stylesheet_number())


@app.route("/change-point/<equip_id>")
def change_point_to_equip(equip_id: str) -> str:
    """Return page, contain FORM to CHANGE new point-location from selected EQUIP"""
    return select_point_to_equip_method(str(equip_id), stylesheet_number())


@app.route("/add-equip", methods=['POST'])
def add_equip():
    """Redirect to method append new equip in current point"""
    return add_equip_method(functions.form_to_data(request.form),
                            request.method,
                            stylesheet_number())


@app.route("/works")
def works_operations():
    """Return main page in WORKS-section"""
    return works_menu(stylesheet_number())


@app.route('/find-work-to-id')
def find_work_to_id():
    """Return page to FIND WORK"""
    return find_work_to_id_page(stylesheet_number())


@app.route("/select-work-to-id", methods=['POST'])
def select_work_to_id():
    """Redirect to method, returned full information from selected work"""
    return select_work_to_id_method(functions.form_to_data(request.form),
                                    request.method,
                                    stylesheet_number())


@app.route("/work/<equip_id>/page/<page_id>")
def work_equip_id_page_page_id(equip_id, page_id):
    """Return page=page_id in ALL work from current EQUIP"""
    return work_to_equip_paging(equip_id, page_id, stylesheet_number())


@app.route("/work/<equip_id>")
def work_to_equip(equip_id):
    """Redirect to first page in ALL work from EQUIP where EQUIP_ID=equip_id"""
    return redirect('/work/{0}/page/1'.format(equip_id))


@app.route("/remove-equip", methods=['POST'])
def remove_equip_method():
    """Redirect to method removed EQUIP to new point"""
    return move_equip_method(functions.form_to_data(request.form),
                             request.method,
                             stylesheet_number())


@app.route("/remove-table/<equip_id>")
def remove_table(equip_id: str):
    """Return page with all move current EQUIP"""
    return remove_table_page(str(equip_id), stylesheet_number())


@app.route("/all-works")
def all_works():
    """Return page contain all works"""
    return work_to_equip('0')


@app.route("/add-work", methods=['POST'])
def add_work():
    """Redirect to method added work to current EQUIP"""
    return add_work_method(functions.form_to_data(request.form),
                           request.method,
                           stylesheet_number())


@app.route("/workers")
def workers():
    """Return main page WORKERS-section"""
    return workers_menu(stylesheet_number())


@app.route("/all-workers")
def all_workers():
    """Return page, contain All WORKERS"""
    return all_workers_table(stylesheet_number())


@app.route("/works-days")
def works_days():
    """Return page current SHEDULE"""
    return works_days_page(stylesheet_number())


@app.route("/performer/<performer_id>", methods=['GET'])
def performer_performer_id(performer_id):
    """Return ALL works where worker == performer_id"""
    return works_from_performers_table(performer_id,
                                       request.args.get('page',
                                                        default=config.full_address,
                                                        type=str),
                                       stylesheet_number())


@app.route("/add-performer-to-work/<work_id>", methods=['GET'])
def add_performer_to_work_work_id(work_id):
    """Redirect to form append performer in current work"""
    return add_performer_to_work(work_id,
                                 request.args.get('page',
                                                  default=config.full_address,
                                                  type=str),
                                 stylesheet_number())


@app.route('/add-performer-result', methods=['POST'])
def add_performer_result():
    """Redirect to method add performer in current work"""
    return add_performer_result_method(functions.form_to_data(request.form),
                                       request.method,
                                       stylesheet_number())


@app.route("/FAQ", methods=['GET'])
def faq():
    """Return FAQ-page"""
    return faq_page(request.args.get('page',
                                     default=config.full_address,
                                     type=str),
                    stylesheet_number())


@app.route('/statistics', methods=['GET'])
def statistics():
    """Return STATISTIC-page"""
    return statistics_page(request.args.get('page',
                                            default=config.full_address,
                                            type=str),
                           stylesheet_number())


@app.route('/system-status', methods=['GET'])
def system_status():
    """Return page, contain status all system components"""
    return system_status_page(request.args.get('page', default=config.full_address, type=str),
                              stylesheet_number())


@app.route('/find', methods=['GET'])
def find():
    """Return main FIND-page"""
    return find_page(request.args.get('page', default=config.full_address, type=str),
                     stylesheet_number())


@app.route('/findresult', methods=['POST'])
def findresult():
    """Redirect to method selected find-type"""
    return find_method(functions.form_to_data(request.form),
                       request.method,
                       stylesheet_number())


@app.route('/find/work/<find_string>/page/<page_num>')
def find_work_find_string_page_page_num(find_string: str, page_num: str) -> str:
    """Return result find work page"""
    return find_work_paging(find_string, page_num, stylesheet_number())


@app.route('/find/work/<find_string>/<data_start>/<data_stop>/page/<page_num>')
def find_work_data_to_data(find_string: str, data_start: str, data_stop: str, page_num: str) -> str:
    """Return page, contain result like WORK_NAME and WORK_DATE"""
    return find_work_like_date_paging(find_string,
                                      data_start,
                                      data_stop,
                                      page_num,
                                      stylesheet_number())


@app.route('/find/point/<find_string>/page/<page_num>')
def find_point(find_string: str, page_num: str) -> str:
    """Return result find point"""
    return find_point_page(find_string, page_num, stylesheet_number())


@app.route('/find/equip/<find_string>/page/<page_num>')
def find_equip(find_string: str, page_num: str) -> str:
    """return result find EQUIP"""
    return find_equip_page(find_string, page_num, stylesheet_number())


@app.route('/bugs')
def bugs():
    """Return main page to BUGS-section"""
    return bugs_menu(stylesheet_number())


@app.route('/all-bugs')
def all_bugs():
    """Return all registered problem"""
    return all_bugs_table(stylesheet_number())


@app.route('/all-bugs-in-work')
def all_bugs_in_work():
    """return all unclosed bugs page"""
    return all_bugs_in_work_table(stylesheet_number())


@app.route('/add-bug')
def add_bug():
    """Return form to create new bug"""
    return web_template.result_page(uhtml.new_bug_input_table(),
                                    '/bugs',
                                    stylesheet_number())


@app.route('/add-bug-result', methods=['POST'])
def add_bug_result():
    """Redirect to method append bug in database"""
    return add_bugs_result_table(functions.form_to_data(request.form),
                                 request.method,
                                 stylesheet_number())


@app.route('/server-ready-to-shutdown')
def server_ready_to_shutdown():
    """Return message from admin"""
    message = ""
    try:
        message_file = open(config.path_to_messages, 'r')
        for line in message_file:
            message += line
    except FileNotFoundError:
        pass
    return message


@app.route('/orders-and-customers')
def orders_and_customers():
    """Return main page ORDERS-sections"""
    return orders_main_menu(stylesheet_number())


@app.route('/all-customers-table')
def all_customers_table_server():
    """Return ALL CUSTOMERS page"""
    return all_customers_table(stylesheet_number())


@app.route('/all-registred-orders')
def all_registred_orders():
    """Return ALL ORDERS page"""
    return all_registered_orders_table(stylesheet_number())


@app.route('/next-themes')
def next_themes() -> str:
    """redirect to new themes methods"""
    if THEME_NUMBER in session:
        session[THEME_NUMBER] = session.get(THEME_NUMBER) + 1
    else:
        session[THEME_NUMBER] = 0  # default number theme
    session[THEME_NUMBER] %= THEMES_MAXIMAL
    session.modified=True
    return new_theme_page(session[THEME_NUMBER])


@app.route('/changelog-page')
def changelog_page() -> str:
    """Return ALL CHANGELOG page"""
    return viev_changelog(stylesheet_number())


@app.errorhandler(404)
def page_not_found(error):
    """Return network error handling page 404"""
    print(error)
    return web_template.result_page(uhtml.html_page_not_found(), '/', stylesheet_number())


@app.errorhandler(405)
def method_not_allowed(error):
    """Return network error handling page 405"""
    print(error)
    return web_template.result_page(uhtml.html_page_not_found(), '/', stylesheet_number())


@app.errorhandler(500)
def page_internal_server_error(error):
    """Return network error handling page 500"""
    print(error)
    return web_template.result_page(uhtml.html_internal_server_error(), '/', stylesheet_number())


@app.route('/not_found')
def not_found():
    """See page_not_found()"""
    return 'Oops!', 404


def start_server():
    """Start development server"""
    app.run(host='0.0.0.0')


if __name__ == "__main__":
    start_server()
