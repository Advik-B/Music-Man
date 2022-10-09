from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QHBoxLayout,
    QPushButton,
)
from PyQt6.uic import loadUi
from PyQt6.QtGui import QPalette, QIcon
import qdarktheme
from qt_material import apply_stylesheet
import sys
import os


class MainGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.preStartUp()
        self.show()

    def preStartUp(self):
        self.CURRENT_THEME = "light_teal_500"
        loadUi("design.xml", self)
        self.search_btn = self.findChild(QPushButton, "search_btn")
        self.home_btn = self.findChild(QPushButton, "home_btn")
        self.lib_btn = self.findChild(QPushButton, "lib_btn")
        self.mbar = self.menuBar()
        self.mbar.setNativeMenuBar(False)
        self.navbuttons = [self.search_btn, self.home_btn, self.lib_btn]
        self.setTheme()

    def setTheme(self):
        def apply_to_btns(theme: str):
            for btn in self.navbuttons:
                fname = btn.objectName().removesuffix("_btn")
                btn.setIcon(QIcon(f"svg/{theme}-theme/{fname}.svg"))

        if self.CURRENT_THEME == "light":
            self.setStyleSheet(qdarktheme.load_stylesheet("light"))
            apply_to_btns("light")
            self.setPalette(qdarktheme.load_palette("light"))

        elif self.CURRENT_THEME == "dark":
            self.setStyleSheet(qdarktheme.load_stylesheet("dark"))
            apply_to_btns("dark")
            self.setPalette(qdarktheme.load_palette("dark"))
        elif "_" in self.CURRENT_THEME:
            apply_stylesheet(self, theme=f"{self.CURRENT_THEME}.xml")
            mode = self.CURRENT_THEME.split("_")[0]
            apply_to_btns(mode)
            del mode
        else:
            raise ValueError("Invalid theme name")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = MainGUI()
    app.exec()
