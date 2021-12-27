"""This module implement window contain edit window to worker"""

from PyQt5.QtWidgets import QPushButton, QLayout, QWidget, QLineEdit, QComboBox, QLabel, QMessageBox
from typing import List, Callable
from wh_app.simple_gui.QtGUI.main_window import SimpleGui
from wh_app.postgresql.database import Database
from wh_app.sql_operations.select_operations import get_info_from_worker, get_all_posts
from wh_app.sql_operations.update_operations import update_worker_info
from wh_app.simple_gui.QtGUI.support_functions import hide_all_children, show_selected_children_in_list
from wh_app.supporting.functions import is_superuser_password


def worker_edit(window: SimpleGui, main_layout: QLayout, no_show_children: List[QWidget],
                worker_id: str, callback_funct: Callable) -> None:
    """This function repaint main window to BUG-information window"""

    children: list = window.children()
    hide_all_children(window)
    old_size = window.size()
    new_widget = list()
    return_button = QPushButton("Вернуться")
    edit_button = QPushButton("Применить изменения")

    with Database() as base:
        _, cursor = base
        worker_info = get_info_from_worker(cursor, worker_id)
        minimal_width = 200

        family_area = QLineEdit(worker_info[1])
        new_widget.append(family_area)

        name_area = QLineEdit(worker_info[2])
        new_widget.append(name_area)

        phone_area = QLineEdit(worker_info[3])
        new_widget.append(phone_area)

        grade_box = QComboBox()
        posts = get_all_posts(cursor)
        current_index = 0
        for post in posts:
            grade_box.addItem(post[1], post[0])
            if post[1] == worker_info[5]:
                grade_box.setCurrentIndex(current_index)
            else:
                current_index += 1
        new_widget.append(grade_box)

        label = QLabel("Пароль администратора")
        new_widget.append(label)

        pw = QLineEdit()
        pw.setEchoMode(QLineEdit.Password)
        new_widget.append(pw)

        window.setFixedWidth(minimal_width)
        window.center()

    def done_edit() -> None:
        """This function update new worker-data elements"""

        result_ok: bool = True
        if is_superuser_password(pw.text()):
            result_ok = result_ok and (False not in [elem.isalpha() for elem in family_area.text()])
            result_ok = result_ok and (family_area.text() != "")
            result_ok = result_ok and (False not in [elem.isalpha() for elem in name_area.text()])
            result_ok = result_ok and (name_area.text() != "")
            result_ok = result_ok and (False not in
                                       [elem.isdigit() or elem == ' ' or elem == '-' or elem == '+'
                                        for elem in phone_area.text()])
            result_ok = result_ok and (phone_area.text() != "")
            if not result_ok:
                err_message_box("Некорректные данные!")
            else:
                result_ok = family_area.text() != worker_info[1] or\
                            name_area.text() != worker_info[2] or\
                            phone_area.text() != worker_info[3] or\
                            grade_box.currentText() != worker_info[5]
                if not result_ok:
                    err_message_box("Данные не изменены!")
                else:
                    with Database() as base:
                        connection, local_cursor = base
                        update_worker_info(local_cursor, worker_id, name_area.text(), family_area.text(),
                                           phone_area.text(), str(posts[grade_box.currentIndex()][0]))
                        connection.commit()
        else:
            err_message_box("Неверный пароль администратора!")
            result_ok = False
        if result_ok:
            return_function()
        else:
            return

    def err_message_box(msg: str) -> None:
        """Create universal error message box"""

        msgbox = QMessageBox()
        msgbox.setText(msg)
        msgbox.setWindowTitle("Ошибка")
        msgbox.setStandardButtons(QMessageBox.Ok)
        msgbox.exec_()

    def return_function() -> None:
        """This function delete all new widgets and repair old"""
        for elem in new_widget:
            elem.hide()
            main_layout.removeWidget(elem)
            elem.setParent(None)
        show_selected_children_in_list(children, no_show_children)
        window.setFixedWidth(old_size.width())
        window.setFixedHeight(old_size.height())
        callback_funct()

    return_button.clicked.connect(return_function)
    edit_button.clicked.connect(done_edit)

    new_widget.append(edit_button)
    new_widget.append(return_button)

    for widget in new_widget:
        main_layout.addWidget(widget)