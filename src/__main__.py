from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton
from PyQt6.uic import loadUi
from PyQt6.QtGui import QIcon, QAction
from qt_material import list_themes, apply_stylesheet
from utility import (
    load_settings,
    Logger,
    save_settings,
)
import sys, os

logger = Logger()


class UserInterface(QMainWindow):
    def __init__(self, ChangeWindowFunc):
        super().__init__()
        self.logger = logger
        self.setWindowCaption("Loading...")
        self.settings = load_settings("settings.yml")
        self.changewindow = ChangeWindowFunc
        self.initUI()
        self.logger.info("Application loaded")
        self.setWindowCaption()
        self.show()

    def initUI(self):
        # Load the UI from the .ui file
        loadUi(os.path.abspath("assets/layout.ui"), self)
        # Set the theme
        # FIXME: The theme library doesn't properly work with UI files
        self.setTheme(self.settings["theme"])

    def setWindowCaption(self, caption: str = None):
        if caption is not None:
            self.setWindowTitle("Pulse Player - %s" % caption)
            self.logger.info("Window caption changed to: %s" % caption)
        else:
            self.setWindowTitle("Pulse Player")
            self.logger.info("Window caption changed to: %s" % self.windowTitle())

    def setTheme(self, theme: str):
        EXTRA = dict(
            density_scale=str(self.settings["scale"]),
        )
        try:
            apply_stylesheet(self, theme.replace(" ", "_") + ".xml", extra=EXTRA)
            self.settings["theme"] = theme
            self.logger.info("Theme changed to: %s" % theme)
        except Exception as e:
            # Print the full traceback
            self.logger.error(e.__traceback__)
            self.logger.error("Theme not found: %s" % theme)
            self.logger.error("Using default theme")
            apply_stylesheet(self, "dark_cyan.xml")
            self.settings["theme"] = "Dark Cyan"
            self.logger.info("Theme set to: %s" % self.settings["theme"])

    def saveSettings(self):
        self.logger.info("Saving settings")
        save_settings("settings.yml", self.settings)


def main():
    logger.info("Application starting")
    app = QApplication(sys.argv)
    UI = UserInterface(ChangeWindowFunc=app.setActiveWindow)
    app.setActiveWindow(UI)
    EXIT_CODE = app.exec_()
    if EXIT_CODE == 0:
        logger.info("Application exiting with code: %s" % EXIT_CODE)
    else:
        logger.error("Application exiting with code: %s" % EXIT_CODE)
    logger.quit()
    sys.exit(EXIT_CODE)


if __name__ == "__main__":
    main()
