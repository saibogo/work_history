"""This module implement window contain bug-tracker from workspoints"""

from PyQt5.QtWidgets import QPushButton, QTableWidget, QLayout,\
    QTableWidgetItem, QHeaderView
from wh_app.simple_gui.QtGUI.main_window import SimpleGui
from wh_app.postgresql.database import Database
from wh_app.sql_operations.select_operations import get_all_bugz_in_bugzilla
from wh_app.config_and_backup.table_headers import bugs_table
from wh_app.simple_gui.QtGUI.support_functions import hide_all_children, show_all_children_in_list


def bugzilla(window: SimpleGui, main_layout: QLayout) -> None:
    """This function repaint main window to BUG-information window"""

    children: list = window.children()
    hide_all_children(window)

    return_button = QPushButton("Вернуться")
    with Database() as base:
        _, cursor = base
        bugs = get_all_bugz_in_bugzilla(cursor)
        table = QTableWidget()
        table.setWordWrap(True)
        bugs_table_ext = bugs_table + ["Изменить статус"]
        table.setColumnCount(len(bugs_table_ext))
        table.setRowCount(len(bugs))
        minimal_width = 40
        maximal_width = 1200

        for col in range(len(bugs_table_ext)):
            table.setHorizontalHeaderItem(col, QTableWidgetItem(bugs_table_ext[col]))
        for row in range(len(bugs)):
            for col in range(len(bugs[0])):
                table.setItem(row, col, QTableWidgetItem(str(bugs[row][col])))
            table.setCellWidget(row, len(bugs_table_ext) - 1, QPushButton("Изменить статус"))

        table.resizeColumnsToContents()
        table.verticalHeader().setVisible(False)
        for col in range(len(bugs_table)):
            minimal_width = minimal_width + table.columnWidth(col)
        window.setFixedWidth(min(minimal_width, maximal_width))
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