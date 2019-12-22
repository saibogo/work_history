from wh_app.simple_gui import tkinter_gui as gui
from wh_app.sql_operations import view_operation
from wh_app.postgresql.database import Database
import sys
from wh_app.supporting import stop_start_web

with Database() as base:
    connection, cursor = base
    view_list = view_operation.all_view_list()
    for view in view_list:
        view(cursor)

    connection.commit()

if len(sys.argv) > 1:
    command = sys.argv[1]
    if command == '--startserver':
        stop_start_web.start_server()
    elif command == '--stopserver':
        stop_start_web.stop_server()
    elif command == '--help':
        print('--help, --startserver, --stopserver')
    else:
        print('Error command. Use --help for more information')

else:
    gui.main_window()
