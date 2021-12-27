"""This module implement start window for application"""
import sys

from PyQt5.QtWidgets import QApplication, QMessageBox, QPushButton, QHBoxLayout, QVBoxLayout
from wh_app.simple_gui.QtGUI.main_window import SimpleGui
from wh_app.supporting.system_status import SystemStatus
from wh_app.supporting.stop_start_web import status_server, start_server, stop_server
from wh_app.supporting import functions
from wh_app.supporting.metadata import CHANGELOG
from wh_app.simple_gui.QtGUI.statistic_window import stat_window
from wh_app.simple_gui.QtGUI.bugz_window import bugzilla
from wh_app.simple_gui.QtGUI.workers_window import workers

functions.info_string(__name__)


def start_window(app: QApplication, window: SimpleGui) -> None:
    """this function create main menu applications"""

    def show_system_status() -> None:
        """This function create dialog window System Status"""
        msgBox = QMessageBox()
        status = SystemStatus.get_status()
        text = "\n".join([elem + ": " + status[elem] for elem in status])
        msgBox.setWindowTitle("Текущий статус системы")
        msgBox.setText(text)
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec_()

    def show_changelog() -> None:
        """This function create dialog window Current Changelog"""
        msgBox = QMessageBox()
        msgBox.setWindowTitle("Актуальный список изменений")
        text = "\n".join([elem[0] + ': ' + elem[1] for elem in CHANGELOG[ : : -1]])
        msgBox.setText(text)
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec_()

    def on_off_web_server() -> None:
        """This function on-off web server"""
        if status_server():
            stop_server()
        else:
            start_server()
        msgBox = QMessageBox()
        msgBox.setWindowTitle("Изменение статуса веб-сервера")
        text = "Произведено изменение статуса веб-сервера"
        msgBox.setText(text)
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec_()

    def new_stat_window() -> None:
        """Repaint window to Statistic Table"""
        stat_window(window, vbox)

    def new_bugz_window() -> None:
        bugzilla(window, vbox)

    def new_workers_window() -> None:
        workers(window, vbox)

    print("Переход на главное окно")
    window.new_window_title("База ремонтов компании Малахит")

    status_button = QPushButton("Статус системы")
    status_button.clicked.connect(show_system_status)

    changelog_button = QPushButton("Список изменений")
    changelog_button.clicked.connect(show_changelog)

    on_off_server_button = QPushButton("Включить/выключить веб-сервер")
    on_off_server_button.clicked.connect(on_off_web_server)

    stat_button = QPushButton("Статистика работ")
    stat_button.clicked.connect(new_stat_window)

    bugz_button = QPushButton("Баг-трекер")
    bugz_button.clicked.connect(new_bugz_window)

    workers_button = QPushButton("сотрудники")
    workers_button.clicked.connect(new_workers_window)

    hbox = QHBoxLayout()
    hbox.addStretch(1)
    hbox.addWidget(changelog_button)
    hbox.addWidget(status_button)

    hbox1 = QHBoxLayout()
    hbox1.addStretch(1)
    hbox1.addWidget(on_off_server_button)
    hbox1.addWidget(stat_button)

    hbox2 = QHBoxLayout()
    hbox2.addStretch(1)
    hbox2.addWidget(bugz_button)
    hbox2.addWidget(workers_button)

    vbox = QVBoxLayout()
    vbox.addStretch(1)
    vbox.addLayout(hbox2)
    vbox.addLayout(hbox1)
    vbox.addLayout(hbox)

    window.setLayout(vbox)

    sys.exit(app.exec_())