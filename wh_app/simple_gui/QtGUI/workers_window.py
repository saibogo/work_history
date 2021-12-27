"""This module implement window contain workers-data from workspoints"""

from PyQt5.QtWidgets import QPushButton, QTableWidget, QLayout,\
    QTableWidgetItem
from typing import Callable
from wh_app.simple_gui.QtGUI.main_window import SimpleGui
from wh_app.postgresql.database import Database
from wh_app.sql_operations.select_operations import get_all_workers, get_info_from_worker
from wh_app.sql_operations.update_operations import invert_worker_status
from wh_app.config_and_backup.table_headers import workers_table
from wh_app.simple_gui.QtGUI.support_functions import hide_all_children, show_all_children_in_list
from wh_app.simple_gui.QtGUI.edit_worker_window import worker_edit


def workers(window: SimpleGui, main_layout: QLayout) -> None:
    """This function repaint main window to workers-information window"""

    children: list = window.children()
    hide_all_children(window)

    return_button = QPushButton("Вернуться")
    with Database() as base:
        _, cursor = base
        all_workers = get_all_workers(cursor)
        table = QTableWidget()
        columns_count = len(workers_table) + 2
        table.setColumnCount(columns_count)
        table.setRowCount(len(all_workers))
        minimal_width = 40
        invert_button_list = list()
        edit_button_list = list()

        def update_row(id_worker: str, number_row: int) -> None:
            """Function update row in table after update information in database"""

            with Database() as base_local:
                _, cursor_local = base_local
                worker_info = get_info_from_worker(cursor_local, id_worker)
                for col_number in range(len(worker_info)):
                    table.setItem(number_row, col_number, QTableWidgetItem(str(worker_info[col_number])))

        def invert_function(worker_id: str, row_number: int) -> Callable[[str, int], None]:
            """this function create new sub-function from invert worker-status in table"""

            def inner_function() -> None:
                """This function is anonymous function from buttons in table"""

                reverse_status(worker_id, row_number)

            def reverse_status(id_worker: str, number_row: int) -> None:
                """This function reverse status from selected worker"""

                with Database() as base_local:
                    connection, cursor_local = base_local
                    invert_worker_status(cursor_local, id_worker)
                    connection.commit()
                    update_row(id_worker, number_row)

            return inner_function

        def edit_function(worker_id: str, row_number: int) -> Callable[[str, int], None]:
            """this function create new sub-function from edit worker-data in table"""

            def inner_function() -> None:
                """this function is anonymous function from button in table"""

                edit_data(worker_id, row_number)

            def edit_data(id_worker: str, number_row: int) -> None:
                """this function call new window from edit worker-data"""

                worker_edit(window, main_layout, children, id_worker,
                            lambda: update_row(id_worker, number_row))

            return inner_function

        for col in range(len(workers_table)):
            table.setHorizontalHeaderItem(col, QTableWidgetItem(workers_table[col]))
        table.setHorizontalHeaderItem(columns_count - 2, QTableWidgetItem("Изменить статус"))
        table.setHorizontalHeaderItem(columns_count - 1, QTableWidgetItem("Редактировать"))

        for row in range(len(all_workers)):

            invert_button_list.append(list())
            invert_button_list[-1].append(QPushButton("Принять/Уволить"))
            (invert_button_list[-1]).append(invert_function(str(all_workers[row][0]), row))
            (invert_button_list[-1][0]).clicked.connect(invert_button_list[-1][1])

            edit_button_list.append(list())
            edit_button_list[-1].append(QPushButton("Изменить"))
            (edit_button_list[-1]).append(edit_function(str(all_workers[row][0]), row))
            (edit_button_list[-1][0]).clicked.connect(edit_button_list[-1][1])

            for col in range(len(all_workers[0])):
                table.setItem(row, col, QTableWidgetItem(str(all_workers[row][col])))
            table.setCellWidget(row, columns_count - 2, invert_button_list[row][0])
            table.setCellWidget(row, columns_count - 1, edit_button_list[row][0])

        table.resizeColumnsToContents()
        table.verticalHeader().setVisible(False)
        for col in range(columns_count):
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
