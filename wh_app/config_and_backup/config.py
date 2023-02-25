"""Contain all configuration variables"""

import xml.etree.cElementTree as ET
import os


path_to_project: str
path_to_pdf: str
path_to_telegram_token: str
static_dir: str
template_folder: str
path_to_dump: str
path_to_passwords: str
path_to_messages: str

database_name: str
user_name: str
user_password: str
database_host: str
database_port: str

ip_address: str
port: str
full_address: str

max_records_in_page: int
max_pages_in_tr: int
timeout_message: int
max_session_time: int

start_width_qt: int
start_height_qt: int
max_width_for_date: int
max_height_for_date: int


def telegram_delete_message_pause():
    return globals()['telegram_delete_message_pause_var']


str_interrupted: str
max_size_column: int
rows_pxls: int
max_pxls_in_canvas: int

path_to_config_xml = str(os.path.abspath(__file__)).replace('config.py', 'config.xml')


def load_config():
    """Load parameters from config.xml"""
    global path_to_config_xml
    try:
        tree = ET.parse(path_to_config_xml)

        # path_sections
        globals()['path_to_project'] = tree.find('pathes/path_to_project').text
        globals()['path_to_pdf'] = tree.find('pathes/path_to_pdf').text
        globals()['path_to_telegram_token'] = tree.find('pathes/path_to_telegram_token').text
        globals()['static_dir'] = globals()['path_to_project'] + 'wh_app/web/static/'
        globals()['template_folder'] = globals()['path_to_project'] + 'wh_app/web/templates'
        globals()['path_to_dump'] = globals()['path_to_project'] + 'wh_app/config_and_backup/postgress_backup.db'
        globals()['path_to_passwords'] = globals()['path_to_project'] + 'wh_app/config_and_backup/.users_pass'
        globals()['path_to_messages'] = globals()['path_to_project'] + 'wh_app/config_and_backup/.message_to_shutdown_server'

        # Database section
        globals()['database_name'] = tree.find('database/database_name').text
        globals()['user_name'] = tree.find('database/user_name').text
        globals()['user_password'] = tree.find('database/user_password').text
        globals()['database_host'] = tree.find('database/database_host').text
        globals()['database_port'] = tree.find('database/database_port').text

        # IP section
        globals()['ip_address'] = tree.find('web/ip_address').text
        globals()['port'] = tree.find('web/port').text
        globals()['full_address'] = "http://" + globals()['ip_address'] + ':' + globals()['port']

        # Web-interface section
        globals()['max_records_in_page'] = int(tree.find('web-interface/max_records_in_page').text)
        globals()['max_pages_in_tr'] = int(tree.find('web-interface/max_pages_in_tr').text)
        globals()['timeout_message'] = int(tree.find('web-interface/timeout_message').text)
        globals()['max_session_time'] = int(tree.find('web-interface/max_session_time').text)

        # Qt section
        globals()['start_width_qt'] = int(tree.find('Qt/start_width_qt').text)
        globals()['start_height_qt'] = int(tree.find('Qt/start_height_qt').text)
        globals()['max_width_for_date'] = int(tree.find('Qt/max_width_for_date').text)
        globals()['max_height_for_date'] = int(tree.find('Qt/max_height_for_date').text)

        # Telegram section
        globals()['telegram_delete_message_pause_var'] = int(tree.find('telegram/telegram_delete_message_pause').text)

        # Any section
        globals()['str_interrupted'] = tree.find('any/str_interrupted').text
        globals()['max_size_column'] = int(tree.find('any/max_size_column').text)
        globals()['rows_pxls'] = int(tree.find('any/rows_pxls').text)
        globals()['max_pxls_in_canvas'] = int(tree.find('any/max_pxls_in_canvas').text)
    except FileNotFoundError:
        print('Конфигурационный файл по пути {}, недоступен!'.format(path_to_config_xml))
        exit(1)
    except AttributeError:
        print('Конфигурационный файл {} поврежден!'.format(path_to_config_xml))
        exit(1)


load_config()
