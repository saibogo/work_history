"""This module contain functions to create all orders-pages"""
import datetime

import flask
from flask import render_template, session, redirect
from typing import List, Tuple, Dict

import wh_app.web.template as web_template
import wh_app.web.universal_html as uhtml
from wh_app.config_and_backup.config import max_records_in_page
from wh_app.postgresql.database import Database
from wh_app.sql_operations.select_operations import select_operations
from wh_app.sql_operations import insert_operations, update_operations
from wh_app.supporting import functions
from wh_app.config_and_backup import table_headers
from wh_app.telegram_bot.bot_init import add_new_order_in_loop

functions.info_string(__name__)


def orders_main_menu(stylesheet_number: str) -> str:
    """Function create main page in ORDERS section"""
    menu = ['Все заказчики', 'Добавить заказчика',
            'Все зарегистрированные заявки','Только незакрытые заявки', 'Поиск по ID', 'Зарегистрировать заявку',
            'Только мои заявки']
    links = ['/all-customers-table', '/add-new-customer', '/all-registred-orders', '/all-no-closed-orders',
             '/order-from-id', '/add-order', '/my-orders']
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


def create_new_customer_form(stylesheet_number: str) -> str:
    """Function create page with form to create new customer"""
    pre_adr = '/orders-and-customers'
    form = render_template('add_new_customer.html', password=uhtml.PASSWORD, full_name=uhtml.FULL_NAME,
                           last_name=uhtml.LAST_NAME, first_name=uhtml.FIRST_NAME, password_1=uhtml.PASSWORD1,
                           password_2=uhtml.PASSWORD2)
    return web_template.result_page(form, pre_adr, str(stylesheet_number))


def create_new_customer_method(data: Dict, method, stylesheet_number: str) -> str:
    """Function analyze and if all correct add new customer in database"""
    pre_adr = '/orders-and-customers'
    if method == 'POST':
        password = data[uhtml.PASSWORD]
        full_name = data[uhtml.FULL_NAME]
        first_name = data[uhtml.FIRST_NAME]
        last_name = data[uhtml.LAST_NAME]
        password1 = data[uhtml.PASSWORD1]
        password2 = data[uhtml.PASSWORD2]
        if functions.is_superuser_password(password):
            if password1 == password2:
                with Database() as base:
                    connection, cursor = base
                    user_in_db = select_operations.user_in_customers(cursor, full_name)
                    if user_in_db:
                        page = '<h2>Пользователь {} уже зарегистрирован в системе!</h2>'.format(full_name)
                    else:
                        description = '{} {}'.format(last_name, first_name)
                        new_hash = functions.create_hash(password1)
                        insert_operations.insert_new_customer_in_database(cursor, full_name, description, new_hash)
                        connection.commit()
                        page = uhtml.operation_completed()
            else:
                page = "<h2>Пароль_1 и Пароль_2 не совпадают!</h2>"
        else:
            page = uhtml.pass_is_not_valid()
    else:
        page = '<h2>Method in Add New Customer not corrected!</h2>'
    return web_template.result_page(page, pre_adr, stylesheet_number)


def all_registered_orders_table(stylesheet_number: str) -> str:
    """Function create page, contain list of all registered orders"""
    with Database() as base:
        _, cursor = base
        all_orders = select_operations.get_all_orders(cursor)
        if len(all_orders) > max_records_in_page():
            return all_registered_orders_table_page(page_num=1, stylesheet_number=stylesheet_number)
        correct_orders = _correct_orders_table(all_orders)
        table = uhtml.universal_table(table_headers.orders_table_name,
                                      table_headers.orders_table,
                                      correct_orders)
        return web_template.result_page(table, '/orders-and-customers', str(stylesheet_number), True, 'all-orders=0')


def all_registered_orders_table_page(page_num: int, stylesheet_number: str) -> str:
    """Function create page, contain list of all registered orders with paging"""
    with Database() as base:
        _, cursor = base
        pre_adr = '/orders-and-customers'
        page_orders = select_operations.get_all_orders_limit(cursor, page_num)
        correct_orders = _correct_orders_table(page_orders)
        table = uhtml.universal_table(table_headers.orders_table_name,
                                      table_headers.orders_table,
                                      correct_orders)
        table_paging = uhtml.paging_table("/all-registred-orders/page",
                                          functions.
                                          list_of_pages(select_operations.get_all_orders(cursor)),
                                          int(page_num))
        return web_template.result_page(table + table_paging, pre_adr, stylesheet_number,
                                        True, 'all-orders={}'.format(page_num))


def create_new_order_form(stylesheet_number: str) -> str:
    """Return new page to create new order"""
    with Database() as base:
        _, cursor = base
        user_name = session[uhtml.LOGIN]
        user_role = session[uhtml.SESSION_ROLE]
        if user_role == functions.ROLE_SUPERUSER:
            current_customer = 0
        elif user_role == functions.ROLE_CUSTOMER:
            customers_info = select_operations.get_all_customers(cursor)
            current_customer = 0
            for elem in customers_info:
                if elem[1] == user_name:
                    current_customer = elem[0]
        else:
            return uhtml.access_denided(user_name)

        pre_addr = '/orders-and-customers'
        all_customer = select_operations.get_all_customers(cursor)
        all_points = select_operations.get_all_works_points(cursor)
        form = render_template('create_new_order.html', customer_name=uhtml.CUSTOMER_NAME, all_customers=all_customer,
                               point_name=uhtml.POINT_NAME, all_points=all_points, order_info=uhtml.ORDER_INFO,
                               password=uhtml.PASSWORD, current_customer=current_customer)

        return web_template.result_page(form, pre_addr, str(stylesheet_number))


def create_order_method(data: Dict, method, stylesheet_number: str) -> str:
    """Create new order in database"""
    pre_adr = '/orders-and-customers'
    if method == "POST":
        customer_id = data[uhtml.CUSTOMER_NAME]
        point_id = data[uhtml.POINT_NAME]
        order_info = data[uhtml.ORDER_INFO]
        password = data[uhtml.PASSWORD]
        with Database() as base:
            connection, cursor = base
            customer_info = select_operations.get_full_customer_info(cursor, customer_id)
            if functions.is_valid_customers_password(password, customer_info[1]):
                insert_operations.insert_new_order(cursor, customer_id, point_id, order_info)
                connection.commit()
                page = uhtml.operation_completed()
                new_order_id = select_operations.get_last_order_id_in_work(cursor)
                add_new_order_in_loop(new_order_id)
            else:
                page = uhtml.pass_is_not_valid()
    else:
        page = "Method in add Order not corrected!"
    return web_template.result_page(page, pre_adr, str(stylesheet_number))


def all_no_closed_orders_table(stylesheet_number: str) -> str:
    """Create no-closed orders table"""
    with Database() as base:
        _, cursor = base
        pre_addr = '/orders-and-customers'
        all_orders = select_operations.get_all_no_closed_orders(cursor)
        if len(all_orders) > max_records_in_page():
            return all_no_closed_orders_table_page(1, stylesheet_number)
        correct_orders = _correct_orders_table(all_orders)
        table = uhtml.universal_table(table_headers.orders_table_name,
                                      table_headers.orders_table_no_closed,
                                      correct_orders)
        return web_template.result_page(table, pre_addr, str(stylesheet_number), True, 'no-closed-orders=0')


def all_no_closed_orders_table_page(page_num: int, stylesheet_number: str) -> str:
    """Create no-closed orders table with paging"""
    with Database() as base:
        _, cursor = base
        pre_addr = '/orders-and-customers'
        orders = select_operations.get_all_no_closed_orders_limit(cursor, page_num)
        correct_orders = _correct_orders_table(orders)
        table = uhtml.universal_table(table_headers.orders_table_name,
                                      table_headers.orders_table_no_closed,
                                      correct_orders)
        table_paging = uhtml.paging_table("/all-no-closed-orders/page",
                                          functions.
                                          list_of_pages(select_operations.get_all_no_closed_orders(cursor)),
                                          int(page_num))

        return web_template.result_page(table + table_paging, pre_addr, str(stylesheet_number), True,
                                        'no-closed-orders={}'.format(page_num))


def _correct_orders_table(orders: List[Tuple]) -> List[List]:
    """Reformat orders table from database"""
    correct_orders = list()
    for order in orders:
        correct_orders.append([])
        for i in range(len(order)):
            if isinstance(order[i], datetime.datetime):
                correct_orders[-1].append(order[i].strftime('%Y-%m-%d %H:%M:%S'))
            elif order[i] is None:
                correct_orders[-1].append("")
            else:
                correct_orders[-1].append(order[i])
        link = '<a href="/edit-order/{0}">{1}</a>'.format(correct_orders[-1][0], uhtml.EDIT_CHAR)
        correct_orders[-1].append(link)
    return correct_orders


def create_edit_order_form(order_id: str, stylesheet_number: str) -> str:
    """Create edit order form with id = order_id"""
    with Database() as base:
        _, cursor = base
        user_name = session[uhtml.LOGIN]
        user_role = session[uhtml.SESSION_ROLE]
        if user_role == functions.ROLE_SUPERUSER:
            current_customer = 0
        elif user_role == functions.ROLE_CUSTOMER:
            customers_info = select_operations.get_all_customers(cursor)
            current_customer = 0
            for elem in customers_info:
                if elem[1] == user_name:
                    current_customer = elem[0]
        else:
            return uhtml.access_denided(user_name)

        pre_addr = '/orders-and-customers'
        all_customer = select_operations.get_all_customers(cursor)
        order_info = select_operations.get_order_from_id(cursor, order_id)
        point_name = order_info[1]
        awaliable_statuses = select_operations.get_all_order_status(cursor)
        form = render_template('edit_order_form.html', point_name=point_name, order_info=order_info[5],
                               customer_name=uhtml.CUSTOMER_NAME, all_customers=all_customer, password=uhtml.PASSWORD,
                               order_status_name=uhtml.ORDER_STATUS_NAME, all_status=awaliable_statuses,
                               comment=uhtml.COMMENT, id=uhtml.ORDER_ID, order_id=order_id, current_customer=current_customer)

        return web_template.result_page(form, pre_addr, str(stylesheet_number))


def edit_order_status_method(data: Dict, method, stylesheet_number: str) -> str:
    """Analyze data and/or add record in database"""

    pre_adr = '/orders-and-customers'
    if method == "POST":
        order_id = data[uhtml.ORDER_ID]
        customer_id = data[uhtml.CUSTOMER_NAME]
        order_status = data[uhtml.ORDER_STATUS_NAME]
        comment  = data[uhtml.COMMENT]
        password = data[uhtml.PASSWORD]
        session_user_name = session[uhtml.LOGIN]
        session_user_role = session[uhtml.SESSION_ROLE]
        with Database() as base:
            connection, cursor = base
            customer_name = select_operations.get_full_customer_info(cursor, customer_id)[2]
            if (customer_name == session_user_name or session_user_role == functions.ROLE_SUPERUSER) \
                    and (functions.is_valid_customer(customer_name, password) or
                                                       functions.is_superuser_password(password)):
                if order_status == 'in_work':
                    update_operations.update_order_info_in_work(cursor, order_id, comment)
                else:
                    update_operations.update_order_info_not_work(cursor, order_id,order_status, comment)
                connection.commit()
                page = uhtml.operation_completed()
            else:
                page = uhtml.pass_is_not_valid()
    else:
        page = "Method in add Order not corrected!"
    return web_template.result_page(page, pre_adr, str(stylesheet_number))


def find_order_from_id_form(stylesheet_number: str) -> str:
    """Create form to find order in database"""
    with Database() as base:
        _, cursor = base
        max_id = select_operations.get_maximal_orders_id(cursor)
        page = render_template('find_order_from_id.html', max_order_id=max_id, order_id_name=uhtml.ORDER_ID)
        pre_adr = '/orders-and-customers'
        return web_template.result_page(page, pre_adr, stylesheet_number)


def order_with_id_table(data: Dict, method, stylesheet_number: str) -> str:
    """Create table with ONE record FROM orders table with current_id"""

    pre_adr = '/orders-and-customers'
    if method == "POST":
        order_id = data[uhtml.ORDER_ID]
        with Database() as base:
            _, cursor = base
            try:
                order = select_operations.get_order_from_id(cursor, order_id)
                correct_orders = _correct_orders_table([order])
                page = uhtml.universal_table(table_headers.orders_table_name,
                                             table_headers.orders_table,
                                             correct_orders)
            except IndexError:
                page = uhtml.html_page_not_found()

    else:
        page = "Method in Find Order not corrected!"
    return web_template.result_page(page, pre_adr, stylesheet_number, True, 'order-to-pdf={}'.format(order_id))


def my_orders_table(stylesheet_number: str) -> str:
    """Return table with all customers order or ALL orders if user role = superuser"""
    user_name = session[uhtml.LOGIN]
    user_role = functions.get_user_role(user_name)
    if user_role == functions.ROLE_SUPERUSER:
        return all_registered_orders_table_page(1, stylesheet_number)
    elif user_role == functions.ROLE_CUSTOMER:
        return my_orders_table_page(stylesheet_number, 1)
    else:
        return uhtml.access_denided(session[uhtml.LOGIN])


def my_orders_table_page(stylesheet_number: str, page_num=1) -> str:
    """Return table with all customers order or ALL orders if user role = superuser"""
    user_name = session[uhtml.LOGIN]
    user_role = functions.get_user_role(user_name)
    if user_role == functions.ROLE_SUPERUSER:
        return all_registered_orders_table_page(1, stylesheet_number)
    elif user_role == functions.ROLE_CUSTOMER:
        with Database() as base:
            _, cursor = base
            pre_addr = '/orders-and-customers'
            page_orders = select_operations.get_all_customers_orders_limit(cursor, user_name, page_num)
            correct_orders = _correct_orders_table(page_orders)
            table = uhtml.universal_table(table_headers.orders_table_name,
                                          table_headers.orders_table_no_closed,
                                          correct_orders)
            table_paging = uhtml.paging_table("/my-orders/",
                                              functions.
                                              list_of_pages(select_operations.get_all_customers_orders(cursor, user_name)),
                                              int(page_num))
            return web_template.result_page(table + table_paging, pre_addr, str(stylesheet_number))
    else:
        return uhtml.access_denided(session[uhtml.LOGIN])
