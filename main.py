import sys

from wh_app.simple_gui import tkinter_gui as gui
from wh_app.sql_operations import view_operation
from wh_app.postgresql.database import Database
from wh_app.supporting.cli import commands, commands_ext
from wh_app.supporting.auto_save_Thread import AutoSaveThread

with Database() as base:
    connection, cursor = base
    view_list = view_operation.all_view_list()
    for view in view_list:
        view(cursor)

    connection.commit()


if len(sys.argv) > 1:
    command = sys.argv[1]
    if command in commands:
        commands[command]()
    elif command in commands_ext and len(sys.argv) > 2:
        commands_ext[command](sys.argv[2])
    else:
        print('Error command. Use --help for more information')

else:
    auto_save_obj = AutoSaveThread.get_instance()
    if not auto_save_obj.is_alive():
        auto_save_obj.start()
    gui.main_window()
    print("Autosave is work" if AutoSaveThread.get_status() else "Autosave not work")



