from PyQt5.QtWidgets import (
    QDialog,
    QApplication,
    QVBoxLayout,
    QComboBox,
    QLabel,
    QSlider,
)
from PyQt5.uic import loadUi
from qt_material import list_themes, apply_stylesheet
import sys

class SettingsAppearance(QDialog):
    def __init__(self, parent=None, config: dict = None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        # self.setFixedSize(400, 200)
        self.initUI(config)
        self.show()

    def initUI(self, config: dict):
        loadUi("assets/settings.appearance.ui", self)
        apply_stylesheet(self, "dark_cyan.xml")
        self.lay = self.findChild(QVBoxLayout, "vl")
        self.setLayout(self.lay)
        self.setWindowTitle("Settings")
        self.themeBox = self.findChild(QComboBox, "themeBox")
        self.themeLabel = self.findChild(QLabel, "themeLabel")
        self.scaleLabel = self.findChild(QLabel, "scaleLabel")
        self.scaleSlider = self.findChild(QSlider, "scaleSlider")

def main():
    app = QApplication(sys.argv)
    ex = SettingsAppearance()
    sys.exit(app.exec_())
