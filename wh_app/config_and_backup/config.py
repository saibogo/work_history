"""Contain all configuration variables"""

import xml.etree.cElementTree as ET
import os

path_to_project = lambda: str(globals()['path_to_project_var'])
path_to_pdf = lambda: str(globals()['path_to_pdf_var'])
path_to_telegram_token = lambda: str(globals()['path_to_telegram_token_var'])
static_dir = lambda: str(globals()['static_dir_var'])
power_profiles = lambda: str(globals()['power_profiles_var'])
template_folder = lambda: str(globals()['template_folder_var'])
path_to_dump = lambda: str(globals()['path_to_dump_var'])
path_to_structure_dump = lambda: str(globals()['path_to_structure_dump_var'])
path_to_passwords = lambda: str(globals()['path_to_passwords_var'])
path_to_messages = lambda: str(globals()['path_to_messages_var'])
path_to_sql_log = lambda: str(globals()['path_to_sql_log_var'])
path_to_login_log = lambda: str(globals()['path_to_login_log_var'])
path_to_fonts = lambda: str(globals()['path_to_fonts_var'])
path_to_certificate = lambda: str(globals()['certificate_var'])
path_to_private_key = lambda: str(globals()['privateKey_var'])

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
        globals()['power_profiles_var'] = path_to_project() + 'wh_app/web/static/power_profiles'
        globals()['template_folder_var'] = path_to_project() + 'wh_app/web/templates'
        globals()['path_to_dump_var'] = path_to_project() + 'wh_app/config_and_backup/backups/postgress_backup.{}.db'
        globals()['path_to_structure_dump_var'] = path_to_project() + 'wh_app/config_and_backup/backups/postgress_backup_empty.{}.db'

        globals()['path_to_passwords_var'] = path_to_project() + 'wh_app/config_and_backup/.users_pass'
        globals()['path_to_messages_var'] = path_to_project() + 'wh_app/config_and_backup/.message_to_shutdown_server'
        globals()['path_to_sql_log_var'] = tree.find('pathes/path_to_sql_log').text
        globals()['path_to_login_log_var'] = tree.find('pathes/path_to_login_log').text
        globals()['path_to_fonts_var'] = path_to_project() + 'wh_app/supporting/pdf_operations/'
        globals()['certificate_var'] = path_to_project() + 'wh_app/cert/certificate.crt'
        globals()['privateKey_var'] = path_to_project() + 'wh_app/cert/privateKey.key'

        # Database section
        globals()['database_name_var'] = tree.find('database/database_name').text
        globals()['user_name_var'] = tree.find('database/user_name').text
        globals()['user_password_var'] = tree.find('database/user_password').text
        globals()['database_host_var'] = tree.find('database/database_host').text
        globals()['database_port_var'] = tree.find('database/database_port').text

        # IP section
        globals()['ip_address_var'] = tree.find('web/ip_address').text
        globals()['port_var'] = tree.find('web/port').text
        globals()['full_address_var'] = "https://" + globals()['ip_address_var'] + ':' + globals()['port_var']

        # Web-interface section
        globals()['max_records_in_page_var'] = int(tree.find('web-interface/max_records_in_page').text)
        globals()['max_pages_in_tr_var'] = int(tree.find('web-interface/max_pages_in_tr').text)
        globals()['timeout_message_var'] = int(tree.find('web-interface/timeout_message').text)
        globals()['max_session_time_var'] = int(tree.find('web-interface/max_session_time').text)

        # Telegram section
        globals()['telegram_delete_message_pause_var'] = int(tree.find('telegram/telegram_delete_message_pause').text)

    except FileNotFoundError:
        print('Конфигурационный файл по пути {}, недоступен!'.format(path_to_config_xml))
        exit(1)
    except AttributeError:
        print('Конфигурационный файл {} поврежден!'.format(path_to_config_xml))
        exit(1)


load_config()
