import datetime
import sys

from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QStatusBar,
    QSizePolicy,
    QWidget,
    QGridLayout,
)
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon
from PyQt6.uic import loadUi

# from pyqt_svg_button.svgButton import SvgButton as QPushButton
from rich.console import Console
from screeninfo import get_monitors
from qt_material import apply_stylesheet

from discord_theme import discord_theme
c = Console(record=True)


class GUI(QWidget):
    def __init__(self):
        super().__init__()
        self.basetitile = "Music Man"
        self.loadUI()
        self.show()

    def loadUI(self):
        moniter = get_monitors()[0]
        c.log(f"Window Size {self.size()}")
        loadUi("design.xml", self)
        self.resize(moniter.width // 2, moniter.height // 2 + ( moniter.height % 2))
        self.setWindowTitle(self.basetitile)
        self.lay = self.findChild(QGridLayout, "layout")
        self.setLayout(self.lay)
        apply_stylesheet(self, "dark_cyan.xml")


    def apply_styles(self, *widgets):
        for widget in widgets:
            apply_stylesheet(widget, "dark_cyan.xml")

    def apply_size_policies(self, *widgets, h, v):
        for widget in widgets:
            widget.setSizePolicy(h, v)

    def setMinimumSizes(self, *widgets, size: QSize):
        for widget in widgets:
            widget.setMinimumSize(size)

    def setMaximumSizes(self, *widgets, size: QSize):
        for widget in widgets:
            widget.setMaximumSize(size)

def main():
    app = QApplication(sys.argv)
    gui = GUI()
    # c.save_html(f"log{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.html", theme=discord_theme)
    # ^^ Enable this is production
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
