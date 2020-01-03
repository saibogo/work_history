from wh_app.supporting import stop_start_web
from wh_app.supporting import backup_operations as bcp_oper
from wh_app.supporting import functions
from wh_app.supporting import delete_views_and_tables as cleardb

functions.info_string(__name__)


def print_help():
    print('python3 /path/to/main.py [command] [argument]')
    print('-h, --help : View this help')
    print('--startserver : Start WebServer in not running')
    print('--stopserver ; Stop WebServer in running')
    print('--statusserver : View status WebServer')
    print('--cleardb: Create dump database and delete ALL DATA in workhistory database')
    print('--savedb path_to_file : Save current database in file path_to_file')
    print('if not arguments - start GUI')


commands = {'--startserver': stop_start_web.start_server,
            '--stopserver': stop_start_web.stop_server,
            '--help': print_help,
            '-h': print_help,
            '--statusserver': lambda : print("Веб-сервер работает" if stop_start_web.status_server()
            else "Веб-сервер не запущен"),
            '--cleardb': cleardb.drop_all_data}

commands_ext = {'--savedb': bcp_oper.create_dump}
