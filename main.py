"""This is main subprogram in project Work History Malachite Company"""

import sys

from wh_app.sql_operations import view_operation, sql_functions_operations, sql_procedures_operations
from wh_app.sql_operations.select_operations.select_operations import get_database_version as dbversion
from wh_app.postgresql.database import Database
from wh_app.sql_operations.call_operations import find_all_table_to_vacuum
from wh_app.supporting.cli import COMMANDS, COMMANDS_EXT

with Database() as base:
    CONNECTION, CURSOR = base
    print("Connect to Database {0}".format(dbversion(CURSOR)[0][0]))
    VIEW_LIST = view_operation.all_view_list()
    for view in VIEW_LIST:
        view(CURSOR)

    SQL_FUNCTIONS_LIST = sql_functions_operations.all_sql_functions_list()
    for sql_funct in SQL_FUNCTIONS_LIST:
        sql_funct(CURSOR)

    SQL_PROCEDURES_LIST = sql_procedures_operations.all_sql_procedures_list()
    for sql_proc in SQL_PROCEDURES_LIST:
        sql_proc(CURSOR)

    CONNECTION.commit()

    with Database() as base:
        connection, cursor = base
        find_all_table_to_vacuum(cursor)
        for elem in connection.notices:
            print(elem)


if len(sys.argv) > 1:
    COMMAND = sys.argv[1]
    if COMMAND in COMMANDS:
        COMMANDS[COMMAND]()
    elif COMMAND in COMMANDS_EXT and len(sys.argv) > 2:
        COMMANDS_EXT[COMMAND](sys.argv[2])
    else:
        print('Error command. Use --help for more information')

else:
    print('Error command. Use --help for more information')

