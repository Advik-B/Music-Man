from PyQt6.QtWidgets import QApplication, QMainWindow, QHBoxLayout
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
        # self.layout_ = self.findChild(QHBoxLayout, "mainLayout")
        # self.setLayout(self.layout_)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = MainGUI()
    app.exec()
