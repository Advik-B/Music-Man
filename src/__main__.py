from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi
from qt_material import list_themes, apply_stylesheet
from utility import (
    load_settings,
    Logger,
)
import sys, os


class UserInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.logger = Logger()
        self.logger.log("Application started")
        self.settings = load_settings("settings.yml")
        self.show()

    def initUI(self):
        # Load the UI from the .ui file
        loadUi(os.path.abspath("assets/layout.ui"), self)
        # Set the theme
        self.setTheme(self.settings["theme"])
        # Set the window title
        self.setWindowTitle("Qt Material")
        # Show the window
        self.show()

    def setTheme(self, theme: str):
        apply_stylesheet(self, theme.replace(" ", "_") + ".xml")


def main():
    app = QApplication(sys.argv)
    UI = UserInterface()
    app.setActiveWindow(UI)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
