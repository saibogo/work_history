import wh_app.web.template as web_template
import wh_app.web.universal_html as uhtml
from wh_app.postgresql.database import Database
from wh_app.sql_operations import select_operations
from wh_app.supporting import functions
from wh_app.config_and_backup import table_headers

functions.info_string(__name__)


def orders_main_menu(stylesheet_number: str) -> str:
    menu = [(1, 'Все заказчики'),
            (2, 'Все зарегистрированные заявки')]
    links = ['/all-customers-table',
             '/all-registred-orders']
    table = uhtml.universal_table('Действия с заявками',
                                  ['№', 'Действие'],
                                  menu, True, links)
    preview_page = '/'
    return web_template.result_page(table, preview_page, str(stylesheet_number))


def all_customers_table(stylesheet_number: str) -> str:
    with Database() as base:
        _, cursor = base
        table = uhtml.universal_table(table_headers.customers_table_name,
                                      table_headers.customers_table,
                                      select_operations.get_all_customers(cursor))

        return web_template.result_page(table, '/orders-and-customers', str(stylesheet_number))


def all_registred_orders_table(stylesheet_number: str) -> str:
    with Database() as base:
        _, cursor = base
        table = uhtml.universal_table(table_headers.orders_table_name,
                                      table_headers.orders_table,
                                      select_operations.get_all_orders(cursor))
        return web_template.result_page(table, '/orders-and-customers', str(stylesheet_number))