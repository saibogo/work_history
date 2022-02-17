"""This module implement window contain statictic from workspoints"""

from PyQt5.QtWidgets import QApplication, QPushButton, QTableWidget, QLayout,\
    QTableWidgetItem
from wh_app.simple_gui.QtGUI.main_window import SimpleGui
from wh_app.postgresql.database import Database
from wh_app.sql_operations.select_operations import get_statistic
from wh_app.config_and_backup.table_headers import statistics_table
from wh_app.simple_gui.QtGUI.support_functions import hide_all_children, show_all_children_in_list


def stat_window(window: SimpleGui, main_layout: QLayout) -> None:
    """This function repaint main window from statistic table"""
    children: list = window.children()
    hide_all_children(window)

    return_button = QPushButton("Вернуться")
    with Database() as base:
        _, cursor = base
        statistic = get_statistic(cursor)
        table = QTableWidget()
        table.setColumnCount(4)
        table.setRowCount(len(statistic))
        minimal_width = 40

        for col in range(len(statistic[0]) - 1):
            table.setHorizontalHeaderItem(col, QTableWidgetItem(statistics_table[col]))
        for row in range(len(statistic)):
            for col in range(1, len(statistic[0])):
                table.setItem(row, col - 1, QTableWidgetItem(str(statistic[row][col])))

        table.resizeColumnsToContents()
        table.verticalHeader().setVisible(False)
        for col in range(len(statistic[0]) - 1):
            minimal_width = minimal_width + table.columnWidth(col)

        window.setFixedWidth(minimal_width)
        window.center()

        main_layout.addWidget(table)

    def return_function() -> None:
        """This function delete all new widgets and repair old"""
        return_button.hide()
        main_layout.removeWidget(return_button)
        table.hide()
        main_layout.removeWidget(table)
        show_all_children_in_list(children)
        return_button.setParent(None)
        table.setParent(None)
        window.set_starting_size()

    return_button.clicked.connect(return_function)
    main_layout.addWidget(return_button)
