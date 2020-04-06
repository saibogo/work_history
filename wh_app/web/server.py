from flask import Flask, request, redirect, abort
from flask import send_from_directory

import wh_app.web.template as web_template
import wh_app.web.universal_html as uhtml
from wh_app.config_and_backup import config
from wh_app.supporting import functions
from wh_app.web.any_section import main_web_menu, faq_page, statistics_page, system_status_page
from wh_app.web.equips_section import equip_to_point_limit, find_equip_to_id_page, select_equip_to_id_page, \
    add_equip_method, equips_menu
from wh_app.web.find_section import find_page, find_method, find_work_paging, find_work_like_date_paging, \
    find_point_page, find_equip_page
from wh_app.web.points_section import points_operations, all_points_table, create_new_point_page, \
    add_point_method, all_works_points_table
from wh_app.web.workers_section import workers_menu, all_workers_table, works_days_page, works_from_performers_table, \
    add_performer_to_work, add_performer_result_method
from wh_app.web.works_section import works_menu, find_work_to_id_page, select_work_to_id_method, \
    work_to_equip_paging, add_work_method
from wh_app.web.bugs_section import bugs_menu, all_bugs_table, all_bugs_in_work_table, add_bugs_result_table
from wh_app.web.orders_section import all_customers_table, orders_main_menu, all_registred_orders_table


app = Flask(__name__, static_folder=config.static_dir)
functions.info_string(__name__)


@app.route("/")
def main_page():
    return main_web_menu()


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(config.static_dir, 'favicon.ico')


@app.route("/equips")
def equips():
    return equips_menu()


@app.route("/points")
def points():
    return points_operations()


@app.route("/all-points")
def all_points():
    return all_points_table()


@app.route("/create-new-point")
def create_new_point():
    return create_new_point_page()


@app.route('/add-point', methods=['POST'])
def add_point():
    return add_point_method(functions.form_to_data(request.form), request.method)


@app.route("/works-points")
def works_points():
    return all_works_points_table()


@app.route("/equip/<point_id>")
def equip_to_point(point_id):
    return redirect('/equip/{0}/page/1'.format(point_id))


@app.route("/all-equips")
def all_equips_table():
    return equip_to_point('0')


@app.route("/equip/<point_id>/page/<page_num>")
def equip_point_id_page(point_id, page_num):
    return equip_to_point_limit(point_id, page_num)


@app.route('/find-equip-to-id')
def find_equip_to_id():
    return find_equip_to_id_page()


@app.route("/select-equip-to-id", methods=['POST'])
def select_equip_to_id():
    return select_equip_to_id_page(functions.form_to_data(request.form), request.method)


@app.route("/add-equip", methods=['POST'])
def add_equip():
    return add_equip_method(functions.form_to_data(request.form), request.method)


@app.route("/works")
def works_operations():
    return works_menu()


@app.route('/find-work-to-id')
def find_work_to_id():
    return find_work_to_id_page()


@app.route("/select-work-to-id", methods=['POST'])
def select_work_to_id():
    return select_work_to_id_method(functions.form_to_data(request.form), request.method)


@app.route("/work/<equip_id>/page/<page_id>")
def work_equip_id_page_page_id(equip_id, page_id):
    return work_to_equip_paging(equip_id, page_id)


@app.route("/work/<equip_id>")
def work_to_equip(equip_id):
    return redirect('/work/{0}/page/1'.format(equip_id))


@app.route("/all-works")
def all_works():
    return work_to_equip('0')


@app.route("/add-work", methods=['POST'])
def add_work():
    return add_work_method(functions.form_to_data(request.form), request.method)


@app.route("/workers")
def workers():
    return workers_menu()


@app.route("/all-workers")
def all_workers():
    return all_workers_table()


@app.route("/works-days")
def works_days():
    return works_days_page()


@app.route("/performer/<performer_id>", methods=['GET'])
def performer_performer_id(performer_id):
    return works_from_performers_table(performer_id, request.args.get('page', default=config.full_address, type=str))


@app.route("/add-performer-to-work/<work_id>", methods=['GET'])
def add_performer_to_work_work_id(work_id):
    return add_performer_to_work(work_id, request.args.get('page', default=config.full_address, type=str))


@app.route('/add-performer-result', methods=['POST'])
def add_performer_result():
    return add_performer_result_method(functions.form_to_data(request.form), request.method)


@app.route("/FAQ", methods=['GET'])
def faq():
    return faq_page(request.args.get('page', default=config.full_address, type=str))


@app.route('/statistics', methods=['GET'])
def statistics():
    return statistics_page(request.args.get('page', default=config.full_address, type=str))


@app.route('/system-status', methods=['GET'])
def system_status():
    return system_status_page(request.args.get('page', default=config.full_address, type=str))


@app.route('/find', methods=['GET'])
def find():
    return find_page(request.args.get('page', default=config.full_address, type=str))


@app.route('/findresult', methods=['POST'])
def findresult():
    return find_method(functions.form_to_data(request.form), request.method)


@app.route('/find/work/<find_string>/page/<page_num>')
def find_work_find_string_page_page_num(find_string: str, page_num: str) -> str:
    return find_work_paging(find_string, page_num)


@app.route('/find/work/<find_string>/<data_start>/<data_stop>/page/<page_num>')
def find_work_data_to_data(find_string: str, data_start: str, data_stop: str, page_num: str) -> str:
    return find_work_like_date_paging(find_string, data_start, data_stop, page_num)


@app.route('/find/point/<find_string>/page/<page_num>')
def find_point(find_string: str, page_num: str) -> str:
    return find_point_page(find_string, page_num)


@app.route('/find/equip/<find_string>/page/<page_num>')
def find_equip(find_string: str, page_num: str) -> str:
    return find_equip_page(find_string, page_num)


@app.route('/bugs')
def bugs():
    return bugs_menu()


@app.route('/all-bugs')
def all_bugs():
    return all_bugs_table()


@app.route('/all-bugs-in-work')
def all_bugs_in_work():
    return all_bugs_in_work_table()


@app.route('/add-bug')
def add_bug():
    return web_template.result_page(uhtml.new_bug_input_table(), '/bugs')


@app.route('/add-bug-result', methods=['POST'])
def add_bug_result():
    return add_bugs_result_table(functions.form_to_data(request.form), request.method)


@app.route('/server-ready-to-shutdown')
def server_ready_to_shutdown():
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
    return orders_main_menu()


@app.route('/all-customers-table')
def all_customers_table_server():
    return all_customers_table()


@app.route('/all-registred-orders')
def all_registred_orders():
    return all_registred_orders_table()


@app.errorhandler(404)
def page_not_found(error):
    return web_template.result_page(uhtml.html_page_not_found(), '/')


@app.errorhandler(405)
def method_not_allowed(error):
    return web_template.result_page(uhtml.html_page_not_found(), '/')


@app.errorhandler(500)
def page_internal_server_error(error):
    return web_template.result_page(uhtml.html_internal_server_error(), '/')


@app.route('/not_found')
def not_found():
    return 'Oops!', 404


def start_server():
    app.run(host='0.0.0.0')


if __name__ == "__main__":
    start_server()