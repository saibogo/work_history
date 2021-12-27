"""This is main subprogram in project Work History Malachite Company"""

import sys

from wh_app.simple_gui import tkinter_gui as gui
from wh_app.sql_operations import view_operation
from wh_app.postgresql.database import Database
from wh_app.supporting.cli import COMMANDS, COMMANDS_EXT
from wh_app.supporting.auto_save_thread import AutoSaveThread
from wh_app.simple_gui.QtGUI.support_functions import create_window
from wh_app.simple_gui.QtGUI.start_window import start_window


with Database() as base:
    CONNECTION, CURSOR = base
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
    if not AUTO_SAVE_OBJ.is_alive():
        AUTO_SAVE_OBJ.start()
    """
    gui.main_window()
    """
    app, window = create_window()
    start_window(app, window)
    print("Autosave is work" if AutoSaveThread.get_status() else "Autosave not work")
