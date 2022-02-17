from tkinter import GROOVE


path_to_project = '/home/saibogo/PycharmProjects/work_history/'
path_to_pdf = "/home/saibogo/Документы/report.pdf"
database_name = 'workhistory'
user_name = 'saibogo'
user_password = 'begemot100'
database_host = '127.0.0.1'
database_port = '5432'
static_dir = path_to_project + 'wh_app/web/static/'
str_interrupted = 'Interrupted'
max_size_column = 40
rows_pxls = 25
max_pxls_in_canvas = 600
relief = GROOVE
ip_address = '192.168.6.242'
port = '5000'
full_address = "http://" + ip_address + ":" + port

max_records_in_page = 10
max_pages_in_tr = 40
path_to_dump = path_to_project + 'wh_app/config_and_backup/postgress_backup.db'
path_to_passwords = path_to_project + 'wh_app/config_and_backup/.users_pass'
path_to_messages = path_to_project + 'wh_app/config_and_backup/.message_to_shutdown_server'

max_width_for_date = 7
max_height_for_date = 6
timeout_message = 5 * 60 * 1000 # Use in java script handler. Time in ms.

max_session_time = 6 * 60 * 60 # Max length session in seconds

start_width_qt = 500
start_height_qt = 220
