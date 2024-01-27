"""This module contain functions to create all orders-pages"""
import datetime

import wh_app.web.template as web_template
import wh_app.web.universal_html as uhtml
from wh_app.postgresql.database import Database
from wh_app.sql_operations import select_operations
from wh_app.supporting import functions
from wh_app.config_and_backup import table_headers

functions.info_string(__name__)


def orders_main_menu(stylesheet_number: str) -> str:
    """Function create main page in ORDERS section"""
    menu = ['Все заказчики', 'Все зарегистрированные заявки']
    links = ['/all-customers-table',
             '/all-registred-orders']
    table = uhtml.universal_table('Действия с заявками',
                                  ['№', 'Действие'],
                                  functions.list_to_numer_list(menu), True, links)
    preview_page = '/'
    return web_template.result_page(table, preview_page, str(stylesheet_number))


def all_customers_table(stylesheet_number: str) -> str:
    """Functions create page, contain list of all customer in system"""
    with Database() as base:
        _, cursor = base
        table = uhtml.universal_table(table_headers.customers_table_name,
                                      table_headers.customers_table,
                                      select_operations.get_all_customers(cursor))

        return web_template.result_page(table, '/orders-and-customers', str(stylesheet_number))


def all_registered_orders_table(stylesheet_number: str) -> str:
    """Function create page. contain list of all registered orders"""
    with Database() as base:
        _, cursor = base
        all_orders = select_operations.get_all_orders(cursor)
        correct_orders = []
        for order in all_orders:
            correct_orders.append([])
            for i in range(len(order)):
                if isinstance(order[i], datetime.datetime):
                    correct_orders[-1].append(order[i].strftime('%Y-%m-%d %H:%M:%S'))
                elif order[i] is None:
                    correct_orders[-1].append("")
                else:
                    correct_orders[-1].append(order[i])
        table = uhtml.universal_table(table_headers.orders_table_name,
                                      table_headers.orders_table,
                                      correct_orders)
        return web_template.result_page(table, '/orders-and-customers', str(stylesheet_number))
