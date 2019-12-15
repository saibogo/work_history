from wh_app.simple_gui import tkinter_gui as gui
from wh_app.sql_operations import view_operation
from wh_app.postgresql.database import Database

with Database() as base:
    connection, cursor = base
    view_list = view_operation.all_view_list()
    for view in view_list:
        view(cursor)

    connection.commit()

gui.main_window()
