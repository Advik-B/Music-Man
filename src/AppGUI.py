from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QHBoxLayout,
    QPushButton,
)
from PyQt6.uic import loadUi
from PyQt6.QtGui import QPalette, QIcon
import sys


class MainGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.preStartUp()
        self.show()

    def preStartUp(self):
        loadUi("design.xml", self)
        self.search_btn = self.findChild(QPushButton, "search_btn")
        self.home_btn = self.findChild(QPushButton, "home_btn")
        self.lib_btn = self.findChild(QPushButton, "lib_btn")
        self.mbar = self.menuBar()
        # self.home_btn.setIcon(QIcon("svg/home.svg"))
        # self.search_btn.setIcon(QIcon("svg/search.svg"))
        # self.lib_btn.setIcon(QIcon("svg/library.svg"))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = MainGUI()
    app.exec()
