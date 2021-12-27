"""This module implement sheduller for main Qt window"""

import sys
from typing import List, Tuple
from PyQt5.QtWidgets import QApplication, QWidget
from wh_app.simple_gui.QtGUI.main_window import SimpleGui


def create_window() -> Tuple[QApplication, SimpleGui]:
    app = QApplication(sys.argv)
    ex = SimpleGui()

    return app, ex


def hide_all_children(window: SimpleGui) -> None:
    """This function hide all children to parent-window"""

    children: list = window.children()
    for child in children:
        if isinstance(child, QWidget):
            child.hide()


def show_all_children_in_list(children: List[QWidget]) -> None:
    """this function show all widget contains in children-list"""

    for child in children:
        if isinstance(child, QWidget):
            child.show()


def show_selected_children_in_list(children: List[QWidget], not_show_children_list: List[QWidget]) -> None:
    """This function show children in children-list and not in not_show-list"""

    for child in children:
        if isinstance(child, QWidget) and not (child in not_show_children_list):
            child.show()

