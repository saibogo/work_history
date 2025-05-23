"""This module implements the command line interface"""


def print_version() -> None:
    """Print program`s version"""
    from wh_app.supporting.metadata import __version__ as vers
    print(vers)


def print_help() -> None:
    """Implement --help argument in command line interface"""
    print('python3 /path/to/main.py [command] [argument]')
    print('-h, --help : View this help')
    print('-v, --version: Print current program version')
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


def no_sql_commands() -> dict:
    """Return all commands without SQL"""
    return {'--help': print_help, '-h': print_help, '-v': print_version, '--version': print_version}


def db_commands() -> dict:
    """Return all commands to work with PosgreSQL"""
    from wh_app.supporting import delete_views_and_tables as cleardb
    from wh_app.supporting import backup_operations

    return {'--cleardb': cleardb.drop_all_data,
            '--createdump': backup_operations.create_dump,
            '--createscheme' : backup_operations.create_empty,}


def commands_with_sql() -> dict:
    """Return all single commands with using SQL"""
    from wh_app.supporting import stop_start_web
    from wh_app.supporting import users_operation

    return {'--startserver': stop_start_web.start_server,
            '--stopserver': stop_start_web.stop_server,
            '--statusserver': lambda: print("Веб-сервер работает" if stop_start_web.status_server()
                                            else "Веб-сервер не запущен"),
            '--adduser': users_operation.create_new_user,
            '--allstart': stop_start_web.all_start}


def commands_ext() -> dict:
    """Return all command with arguments and using SQL"""
    from wh_app.supporting import stop_start_web
    from wh_app.supporting import backup_operations as bcp_oper
    from wh_app.supporting import users_operation

    return {'--savedb': bcp_oper.create_dump,
            '--updatepassword': users_operation.update_password,
            '--saystop': stop_start_web.say_stop}
