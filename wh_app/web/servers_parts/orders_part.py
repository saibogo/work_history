"""This module contain all actions with orders and customers for Flask server.py"""

from wh_app.web.servers_parts.support_part import *
from wh_app.web.orders_section import all_customers_table, orders_main_menu,\
    all_registered_orders_table


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
