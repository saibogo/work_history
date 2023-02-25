"""This is main subprogram in project Work History Malachite Company"""

import sys

from wh_app.sql_operations import view_operation
from wh_app.sql_operations.select_operations import get_database_version as dbversion
from wh_app.postgresql.database import Database
from wh_app.supporting.cli import COMMANDS, COMMANDS_EXT
from wh_app.supporting.auto_save_thread import AutoSaveThread
from wh_app.supporting.auto_load_config import AutoLoadConfig
from wh_app.simple_gui.QtGUI.support_functions import create_window
from wh_app.simple_gui.QtGUI.start_window import start_window


with Database() as base:
    CONNECTION, CURSOR = base
    print("Connect to Database {0}".format(dbversion(CURSOR)[0][0]))
    VIEW_LIST = view_operation.all_view_list()
    for view in VIEW_LIST:
        view(CURSOR)

    CONNECTION.commit()


if len(sys.argv) > 1:
    COMMAND = sys.argv[1]
    if COMMAND in COMMANDS:
        COMMANDS[COMMAND]()
    elif COMMAND in COMMANDS_EXT and len(sys.argv) > 2:
        COMMANDS_EXT[COMMAND](sys.argv[2])
    else:
        print('Error command. Use --help for more information')

else:
    AUTO_SAVE_OBJ = AutoSaveThread.get_instance()
    if not AutoSaveThread.get_status():
        AUTO_SAVE_OBJ.start()
    print("Autosave is work" if AutoSaveThread.get_status() else "Autosave not work")

    AUTO_LOAD_OBJ = AutoLoadConfig.get_instance()
    if not AutoLoadConfig.get_status():
        AUTO_LOAD_OBJ.start()
    print("Auto load config is work" if AutoLoadConfig.get_status() else "Auto Load Config not work")

    app, window = create_window()
    start_window(app, window)

