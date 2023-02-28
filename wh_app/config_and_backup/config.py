"""Contain all configuration variables"""

import xml.etree.cElementTree as ET
import os

path_to_project = lambda: str(globals()['path_to_project_var'])
path_to_pdf = lambda: str(globals()['path_to_pdf_var'])
path_to_telegram_token = lambda: str(globals()['path_to_telegram_token_var'])
static_dir = lambda: str(globals()['static_dir_var'])
template_folder = lambda: str(globals()['template_folder_var'])
path_to_dump = lambda: str(globals()['path_to_dump_var'])
path_to_passwords = lambda: str(globals()['path_to_passwords_var'])
path_to_messages = lambda: str(globals()['path_to_messages_var'])

database_name = lambda: str(globals()['database_name_var'])
user_name = lambda: str(globals()['user_name_var'])
user_password = lambda: str(globals()['user_password_var'])
database_host = lambda: str(globals()['database_host_var'])
database_port = lambda: str(globals()['database_port_var'])

ip_address = lambda: str(globals()['ip_address_var'])
port = lambda: str(globals()['port_var'])
full_address = lambda: str(globals()['full_address_var'])


def max_records_in_page() -> int:
    return globals()['max_records_in_page_var']


max_pages_in_tr = lambda: int(globals()['max_pages_in_tr_var'])
timeout_message = lambda: int(globals()['timeout_message_var'])
max_session_time = lambda: int(globals()['max_session_time_var'])

start_width_qt = lambda: int(globals()['start_width_qt_var'])
start_height_qt = lambda: int(globals()['start_height_qt_var'])
max_width_for_date = lambda: int(globals()['max_width_for_date_var'])
max_height_for_date = lambda: int(globals()['max_height_for_date_var'])


def telegram_delete_message_pause():
    return globals()['telegram_delete_message_pause_var']


path_to_config_xml = str(os.path.abspath(__file__)).replace('config.py', 'config.xml')


def load_config():
    """Load parameters from config.xml"""
    global path_to_config_xml
    try:
        tree = ET.parse(path_to_config_xml)

        # path_sections
        globals()['path_to_project_var'] = tree.find('pathes/path_to_project').text
        globals()['path_to_pdf_var'] = tree.find('pathes/path_to_pdf').text
        globals()['path_to_telegram_token_var'] = tree.find('pathes/path_to_telegram_token').text
        globals()['static_dir_var'] = path_to_project() + 'wh_app/web/static/'
        globals()['template_folder_var'] = path_to_project() + 'wh_app/web/templates'
        globals()['path_to_dump_var'] = path_to_project() + 'wh_app/config_and_backup/postgress_backup.db'
        globals()['path_to_passwords_var'] = path_to_project() + 'wh_app/config_and_backup/.users_pass'
        globals()['path_to_messages_var'] = path_to_project() + 'wh_app/config_and_backup/.message_to_shutdown_server'

        # Database section
        globals()['database_name_var'] = tree.find('database/database_name').text
        globals()['user_name_var'] = tree.find('database/user_name').text
        globals()['user_password_var'] = tree.find('database/user_password').text
        globals()['database_host_var'] = tree.find('database/database_host').text
        globals()['database_port_var'] = tree.find('database/database_port').text

        # IP section
        globals()['ip_address_var'] = tree.find('web/ip_address').text
        globals()['port_var'] = tree.find('web/port').text
        globals()['full_address_var'] = "http://" + globals()['ip_address_var'] + ':' + globals()['port_var']

        # Web-interface section
        globals()['max_records_in_page_var'] = int(tree.find('web-interface/max_records_in_page').text)
        globals()['max_pages_in_tr_var'] = int(tree.find('web-interface/max_pages_in_tr').text)
        globals()['timeout_message_var'] = int(tree.find('web-interface/timeout_message').text)
        globals()['max_session_time_var'] = int(tree.find('web-interface/max_session_time').text)

        # Qt section
        globals()['start_width_qt_var'] = int(tree.find('Qt/start_width_qt').text)
        globals()['start_height_qt_var'] = int(tree.find('Qt/start_height_qt').text)
        globals()['max_width_for_date_var'] = int(tree.find('Qt/max_width_for_date').text)
        globals()['max_height_for_date_var'] = int(tree.find('Qt/max_height_for_date').text)

        # Telegram section
        globals()['telegram_delete_message_pause_var'] = int(tree.find('telegram/telegram_delete_message_pause').text)

    except FileNotFoundError:
        print('Конфигурационный файл по пути {}, недоступен!'.format(path_to_config_xml))
        exit(1)
    except AttributeError:
        print('Конфигурационный файл {} поврежден!'.format(path_to_config_xml))
        exit(1)


load_config()
