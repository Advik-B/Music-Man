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
from utility import Theme, ThemeNotFoundError
import sys


class SettingsAppearance(QDialog):
    def __init__(self, parent=None, config: dict = None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.themes = []
        if config is None:
            config = {
                "theme": "Dark Cyan",
                "scale": "0",
            }
        self.config = config
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
        self.beforeStartUp()
        self.themeBox.currentTextChanged.connect(self.setTheme)
        self.scaleSlider.valueChanged.connect(self.setScale)

    def beforeStartUp(self):
        self.setThemes()
        self.themeBox.setCurrentText(self.config["theme"])
        self.themeLabel.setText("Theme: %s" % self.themeBox.currentText())
        self.scaleLabel.setText("Scale: %s" % str(self.scaleSlider.value()))
        self.setTheme()
        self.setScale()

    def setTheme(self):
        self.themeLabel.setText("Theme: %s" % self.themeBox.currentText())
        self.showTheme()

    def setScale(self):
        self.scaleLabel.setText("Scale: %s" % str(self.scaleSlider.value()))
        EXTRA = dict(
            density_scale=str(self.scaleSlider.value()),
        )

    def showTheme(self):
        theme = Theme(self.themeBox.currentText())
        apply_stylesheet(self, theme.toQt())

    def setThemes(self):
        for theme in list_themes():
            self.themes.append(Theme(theme))
        tl = []
        for theme in self.themes:
            tl.append(theme.toUI())
        self.themeBox.addItems(tl)


def main():
    app = QApplication(sys.argv)
    UI = SettingsAppearance(config={"theme": "Dark Cyan", "scale": "5"})
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
