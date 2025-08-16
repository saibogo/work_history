"""This module contain all actions with orders and customers for Flask server.py"""

from wh_app.web.servers_parts.support_part import *
from wh_app.web.orders_section import all_customers_table, orders_main_menu,\
    all_registered_orders_table, create_new_order_form, create_order_method, all_no_closed_orders_table,\
    create_edit_order_form, edit_order_status_method, all_registered_orders_table_page, all_no_closed_orders_table_page,\
    find_order_from_id_form, order_with_id_table, create_new_customer_form, create_new_customer_method, my_orders_table,\
    my_orders_table_page, change_customer_status_form, change_customer_status_method, change_customer_password_form,\
    change_customer_password_method, add_performer_to_order_form, add_performer_in_order_method,\
    all_registered_orders_table_from_customer, all_registered_orders_table_from_customer_page,\
    no_closed_order_in_point_table


@app.route('/orders-and-customers')
def orders_and_customers() -> Response:
    """Return main page ORDERS-sections"""
    return goto_or_redirect(lambda: orders_main_menu(stylesheet_number()), functions.ROLE_CUSTOMER)


@app.route('/all-customers-table')
def all_customers_table_server() -> Response:
    """Return ALL CUSTOMERS page"""
    return goto_or_redirect(lambda: all_customers_table(stylesheet_number()), functions.ROLE_CUSTOMER)


@app.route('/add-new-customer')
def add_new_customer() -> Response:
    """go to new form to create new customer"""
    return goto_or_redirect(lambda: create_new_customer_form(stylesheet_number()), functions.ROLE_SUPERUSER)


@app.route('/create_new_customer', methods=['POST'])
def create_new_customer() -> Response:
    """Go to analyze and add new customer in database"""
    return goto_or_redirect(lambda: create_new_customer_method(functions.form_to_data(request.form), request.method,
                                                        stylesheet_number()), functions.ROLE_SUPERUSER)


@app.route('/change-customer-status/<customer_id>')
def change_customer_status(customer_id: int) -> Response:
    """Go to form with chane customer status"""

    return goto_or_redirect(lambda: change_customer_status_form(customer_id, stylesheet_number()), functions.ROLE_SUPERUSER)


@app.route('/common-invert-customer-status', methods=['POST'])
def common_invert_customer_status() -> Response:
    """If password is superusers password, then status of customer will invert"""
    return goto_or_redirect(lambda: change_customer_status_method(functions.form_to_data(request.form), request.method,
                                                                  stylesheet_number()), functions.ROLE_SUPERUSER)


@app.route('/change-customer-password/<customer_id>')
def change_customer_password(customer_id: int) -> Response:
    """Go to form change customer's password"""
    return goto_or_redirect_from_roles_list(lambda: change_customer_password_form(customer_id, stylesheet_number()),
                                            [functions.ROLE_SUPERUSER, functions.ROLE_CUSTOMER])


@app.route('/common-change-customer-password', methods=['POST'])
def common_change_customer_password() -> Response:
    """Go to form change customer's password"""
    return goto_or_redirect_from_roles_list(lambda: change_customer_password_method(functions.form_to_data(request.form),
                                                                                    request.method, stylesheet_number()),
                                            [functions.ROLE_SUPERUSER, functions.ROLE_CUSTOMER])


@app.route('/all-registred-orders')
def all_registred_orders() -> Response:
    """Return ALL ORDERS page"""
    return goto_or_redirect(lambda: all_registered_orders_table(stylesheet_number()), functions.ROLE_CUSTOMER)


@app.route('/all-registred-orders/page/<page_num>/<ord_column>')
def all_registred_orders_page(page_num: int, ord_column: int) -> Response:
    """Return ALL ORDERS page"""
    return goto_or_redirect(lambda: all_registered_orders_table_page(page_num, stylesheet_number(), ord_column), functions.ROLE_CUSTOMER)


@app.route('/orders-from-customer/<customer_id>')
def orders_from_customer(customer_id: int) -> Response:
    """Return ALL orders from customer"""

    return goto_or_redirect(lambda: all_registered_orders_table_from_customer(customer_id, stylesheet_number()),
                            functions.ROLE_CUSTOMER)


@app.route('/orders-from-customer/<customer_id>/page/<page_num>')
def orders_from_customer_page(customer_id: int, page_num :int) -> Response:
    """Return ALL orders from customer"""

    return goto_or_redirect(lambda: all_registered_orders_table_from_customer_page(customer_id, page_num,stylesheet_number()),
                            functions.ROLE_CUSTOMER)


@app.route('/add-order')
def add_order() -> Response:
    """Return Form to create new Order"""
    return goto_or_redirect(lambda: create_new_order_form(stylesheet_number()), functions.ROLE_CUSTOMER)


@app.route("/create_new_order", methods=['POST'])
def create_new_order() -> Response:
    """Redirect data to create new order"""

    return goto_or_redirect(lambda: create_order_method(functions.form_to_data(request.form), request.method,
                                                        stylesheet_number()), functions.ROLE_CUSTOMER)


@app.route('/my-orders')
def my_orders() -> Response:
    """Return table with all orders to customer or all orders to superuser"""

    return goto_or_redirect_from_roles_list(lambda: my_orders_table(stylesheet_number()),
                                            [functions.ROLE_CUSTOMER, functions.ROLE_SUPERUSER])


@app.route('/my-orders/<page_num>')
def my_orders_pages(page_num: int) -> Response:
    """Return table with all orders to customer or all orders to superuser"""

    return goto_or_redirect_from_roles_list(lambda: my_orders_table_page(stylesheet_number(), page_num),
                                            [functions.ROLE_CUSTOMER, functions.ROLE_SUPERUSER])


@app.route('/add-performer-to-order/<order_id>')
def add_performer_to_order(order_id: int) -> Response:
    """Go to form to add performer in order with id = order_id"""

    return goto_or_redirect(lambda: add_performer_to_order_form(order_id, stylesheet_number()), functions.ROLE_SUPERUSER)


@app.route('/add-performer-in-order', methods=['POST'])
def add_performer_in_order() -> Response:
    """Go to method set performer in current order"""

    return goto_or_redirect(lambda: add_performer_in_order_method(functions.form_to_data(request.form), request.method,
                                                                  stylesheet_number()), functions.ROLE_SUPERUSER)


@app.route('/all-no-closed-orders')
def all_no_closed_orders() -> Response:
    """Return ALL ORDERS page"""
    return goto_or_redirect(lambda: all_no_closed_orders_table(stylesheet_number()), functions.ROLE_CUSTOMER)


@app.route('/all-no-closed-orders/page/<page_num>/<ord_column>')
def all_no_closed_orders_page(page_num: int, ord_column: int) -> Response:
    """Return ALL ORDERS page with paging"""
    return goto_or_redirect(lambda: all_no_closed_orders_table_page(page_num, stylesheet_number(), ord_column),
                            functions.ROLE_CUSTOMER)


@app.route('/order-from-id')
def order_from_id() -> Response:
    """Redirect to form select order from id"""
    return goto_or_redirect(lambda: find_order_from_id_form(stylesheet_number()), functions.ROLE_CUSTOMER)


@app.route('/edit-order/<order_id>')
def edit_order(order_id: str) -> Response:
    """Go to create order form"""

    return goto_or_redirect(lambda: create_edit_order_form(order_id, stylesheet_number()), functions.ROLE_CUSTOMER)


@app.route('/new-order-status', methods=['POST'])
def new_order_status() -> Response:
    """start method analyze new order status and/or add record in database"""

    return goto_or_redirect(lambda: edit_order_status_method(functions.form_to_data(request.form), request.method,
                                                             stylesheet_number()), functions.ROLE_CUSTOMER)


@app.route('/select-order-from-id', methods=['POST'])
def select_order_from_id() -> Response:
    """Redirect to create table with current ID"""

    return goto_or_redirect(lambda: order_with_id_table(functions.form_to_data(request.form), request.method,
                                                        stylesheet_number()), functions.ROLE_CUSTOMER)


@app.route('/worked-orders-from-point/<point_id>')
def get_no_closed_order_from_point(point_id: int) -> Response:
    """Go to create order form"""

    return goto_or_redirect(lambda: no_closed_order_in_point_table(int(point_id), stylesheet_number()),
                            functions.ROLE_CUSTOMER)