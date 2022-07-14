from PyQt5.QtWidgets import QApplication, QPushButton, QHBoxLayout, QVBoxLayout
from qframelesswindow import FramelessWindow
from screeninfo import get_monitors
from rich.console import Console
from discord_theme import discord_theme
import sys
import datetime

c = Console(record=True)

class GUI(FramelessWindow):
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
        self.home_button = QPushButton("Home")
        self.search_button = QPushButton("Search")
        self.lib_button = QPushButton("Library")
        self.navbar.addWidget(self.home_button)
        self.navbar.addWidget(self.search_button)
        self.navbar.addWidget(self.lib_button)


def main():
    app = QApplication(sys.argv)
    gui = GUI()
    c.save_html(f"log{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.html", theme=discord_theme)
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()