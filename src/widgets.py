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
        if config is None:
            config = {
                "theme": "Dark Cyan",
                "scale": "0",
            }
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
        self.themeBox.addItems(self.listThemes())
        self.themeBox.currentTextChanged.connect(self.showTheme)
        self.setTheme(config["theme"])

    def setTheme(self, theme: str):
        theme = theme.replace(" ", "_")
        theme = theme.lower()
        theme += ".xml"
        self.showTheme(theme)

    def showTheme(self, theme: str):
        pass

    def listThemes(self):
        ThemeList = []
        for theme in list_themes():
            ThemeList.append(theme.replace("_", " ").removesuffix(".xml"))
        return ThemeList


def main():
    app = QApplication(sys.argv)
    UI = SettingsAppearance(config={"theme": "Dark Cyan", "scale": "5"})
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
