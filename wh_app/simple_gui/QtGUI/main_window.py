"""This module contain simple GUI to work with database"""

from PyQt5.QtWidgets import QWidget, QMessageBox, QDesktopWidget
from wh_app.supporting import functions
from wh_app.config_and_backup.config import start_width_qt, start_height_qt

functions.info_string(__name__)


class SimpleGui(QWidget):

    def __init__(self):
        """Init main window"""
        super().__init__()

        self.init_ui()

    def init_ui(self) -> None:
        """Init UI in main-window"""
        self.set_starting_size()
        self.setWindowTitle('Запуск приложения')
        print("Главное диалоговое окно создано")
        self.show()

    def set_starting_size(self) -> None:
        """Set fixed size main window"""
        self.setFixedWidth(start_width_qt)
        self.setFixedHeight(start_height_qt)
        self.center()

    def closeEvent(self, event) -> None:
        """close main window. App NOT STOPPED!"""
        reply = QMessageBox.question(self, 'Закрытие Приложения',
                                     "Вы действительно хотите выйти?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def new_window_title(self, name: str) -> None:
        """Rename main window"""
        self.setWindowTitle(name)

    def center(self) -> None:
        """Replace main window in center screen"""
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())