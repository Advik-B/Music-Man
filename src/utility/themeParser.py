from qt_material import list_themes as listThemes
from dataclasses import dataclass


class ThemeNotFoundError(Exception):
    pass


@dataclass
class Theme(str):
    """
    (Assuming the theme is dark_cyan.xml)
    current looks like: "Dark Cyan"
    __name looks like: "dark_cyan.xml"

    """

    current: str = None
    __name: str = None

    def __init__(self, theme: str):
        self.__name = theme
        self.current = self.toUI()
        # Perform a check to see if the theme exists
        if self.__name not in listThemes():
            raise ThemeNotFoundError(f"Theme {self.__name} does not exist")

    def __repr__(self):
        return self.current

    __str__ = __repr__

    def toUI(self) -> str:
        return self.__name.replace("_", " ").removesuffix(".xml")

    def toQt(self) -> str:
        return self.current.replace(" ", "_").lower() + ".xml"
