"""This module implements the command line interface"""

from wh_app.supporting import stop_start_web
from wh_app.supporting import backup_operations as bcp_oper
from wh_app.supporting import functions
from wh_app.supporting import delete_views_and_tables as cleardb
from wh_app.supporting import users_operation
from wh_app.supporting import backup_operations


functions.info_string(__name__)


def print_help() -> None:
    """Implement --help argument in command line interface"""
    print('python3 /path/to/main.py [command] [argument]')
    print('-h, --help : View this help')
    print('--startserver : Start WebServer in not running')
    print('--stopserver ; Stop WebServer in running')
    print('--allstart : Start server and autosave procedure')
    print('--statusserver : View status WebServer')
    print('--cleardb: Create dump database and delete ALL DATA in workhistory database')
    print('--createdump : Create statndart backup database')
    print('--createscheme', 'Create empty database dump')
    print('--savedb path_to_file : Save current database in file path_to_file')
    print("--adduser: Create new user if not exist")
    print("--updatepassword username : Update password from user if username exist")
    print("--saystop message: Send message all user 'Server ready to shutdown'")
    print('if not arguments - Break Program and print HELP section')


COMMANDS = {'--startserver': stop_start_web.start_server,
            '--stopserver': stop_start_web.stop_server,
            '--help': print_help,
            '-h': print_help,
            '--statusserver': lambda: print("Веб-сервер работает" if stop_start_web.status_server()
                                            else "Веб-сервер не запущен"),
            '--cleardb': cleardb.drop_all_data,
            '--adduser': users_operation.create_new_user,
            '--createdump': backup_operations.create_dump,
            '--createscheme' : backup_operations.create_empty,
            '--allstart': stop_start_web.all_start}

COMMANDS_EXT = {'--savedb': bcp_oper.create_dump,
                '--updatepassword': users_operation.update_password,
                '--saystop': stop_start_web.say_stop}
