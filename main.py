import tkinter_gui as gui
import view_operation
from database import Database


with Database() as base:
    connection, cursor = base
    view_operation.create_or_replace_second_bindings(cursor)
    view_operation.create_or_replace_firsts_bindings(cursor)
    connection.commit()

gui.main_window()
