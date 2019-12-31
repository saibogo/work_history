from wh_app.supporting import stop_start_web
from wh_app.supporting import backup_operations as bcp_oper


def print_help():
    print('python3 /path/to/main.py [command] [argument]')
    print('-h, --help : View this help')
    print('--startserver : Start WebServer in not running')
    print('--stopserver ; Stop WebServer in running')
    print('--statusserver : View status WebServer')
    print('--savedb path_to_file : Save current database in file path_to_file')
    print('if not arguments - start GUI')


commands = {'--startserver': stop_start_web.start_server,
            '--stopserver': stop_start_web.stop_server,
            '--help': print_help,
            '-h': print_help,
            '--statusserver': stop_start_web.status_server}

commands_ext = {'--savedb': bcp_oper.create_dump}
