import datetime
import sys

from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QStatusBar,
    QSizePolicy,
    QWidget,
)
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon

# from pyqt_svg_button.svgButton import SvgButton as QPushButton
from qframelesswindow import FramelessWindow
from rich.console import Console
from screeninfo import get_monitors

from discord_theme import discord_theme

c = Console(record=True)
with open("dark-style.css", "rb") as f:
    dark_theme = f.read().decode("utf-8")


class GUI(QWidget):
    def __init__(self):
        super().__init__()
        self.basetitile = "Music Man"
        self.setWindowTitle(self.basetitile)
        self.loadUI()
        self.show()

    def loadUI(self):
        moniter = get_monitors()[0]
        self.resize(moniter.width // 2, moniter.height // 2 + moniter.height % 2)
        c.log(f"Window Size {self.size()}")
        self.layout_ = QHBoxLayout()
        self.setLayout(self.layout_)
        self.navbar = QVBoxLayout()
        self.layout_.addLayout(self.navbar)
        self.setWindowIcon(QIcon("icons/icon.png"))

        self.home_button = QPushButton()
        self.home_button.setText("Home")
        self.search_button = QPushButton()
        self.search_button.setText("Search")
        self.lib_button = QPushButton()
        self.lib_button.setText("Library")

        self.navbar.addWidget(self.home_button)
        self.navbar.addWidget(self.search_button)
        self.navbar.addWidget(self.lib_button)

        self.search_button.setIcon(QIcon("svg/search.svg"))
        self.lib_button.setIcon(QIcon("svg/library.svg"))
        self.home_button.setIcon(QIcon("svg/home.svg"))
        self.apply_styles(self.home_button, self.search_button, self.lib_button)
        # When the window is resized, the home button should be resized to fit the window
        self.apply_size_policies(
            self.home_button,
            self.search_button,
            self.lib_button,
            h=QSizePolicy.Expanding,
            v=QSizePolicy.Expanding,
        )

        self.setMinimumSizes(
            self.home_button, self.search_button, self.lib_button, size=QSize(150, 50)
        )
        self.setMaximumSizes(
            self.home_button, self.search_button, self.lib_button, size=QSize(200, 100)
        )

        self.statusBar = QStatusBar()
        self.status_layout = QVBoxLayout()
        # self.statusBar.setSizeGripEnabled(True)
        self.status_layout.addWidget(self.statusBar)
        self.layout_.addLayout(self.status_layout)

    def apply_styles(self, *widgets):
        for widget in widgets:
            widget.setStyleSheet(dark_theme)

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
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
