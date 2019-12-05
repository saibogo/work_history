import tkinter_gui as gui
import view_operation
from database import Database


with Database() as base:
    connection, cursor = base
    view_list = view_operation.all_view_list()
    for view in view_list:
        view(cursor)

    connection.commit()

gui.main_window()
