"""This module contain simple GUI to work with database"""

from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QDesktopWidget,\
    QPushButton, QHBoxLayout, QVBoxLayout
from wh_app.supporting import functions

functions.info_string(__name__)


class SimpleGui(QWidget):

    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self) -> None:
        self.set_starting_size()
        self.setWindowTitle('Запуск приложения')
        print("Главное диалоговое окно создано")
        self.show()

    def set_starting_size(self) -> None:
        self.setFixedWidth(500)
        self.setFixedHeight(220)
        self.center()

    def closeEvent(self, event) -> None:
        reply = QMessageBox.question(self, 'Закрытие Приложения',
                                     "Вы действительно хотите выйти?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def new_window_title(self, name: str) -> None:
        self.setWindowTitle(name)

    def center(self) -> None:
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())