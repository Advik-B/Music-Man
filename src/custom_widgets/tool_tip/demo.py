# coding:utf-8
import sys
from PyQt5.QtCore import QEvent, QPoint
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout

from tool_tip import ToolTip


class Demo(QWidget):

    def __init__(self):
        super().__init__()
        self.hBox = QHBoxLayout(self)
        self.button1 = QPushButton('キラキラ', self)
        self.button2 = QPushButton('食べた愛', self)
        self._toolTip = ToolTip(parent=self)
        # self._tooltip.setDarkTheme(True)

        self.button1.setToolTip('aiko - キラキラ ✨')
        self.button2.setToolTip('aiko - 食べた愛 🥰')
        self.button1.setToolTipDuration(1000)
        self.button2.setToolTipDuration(5000)

        self.button1.installEventFilter(self)
        self.button2.installEventFilter(self)

        self.hBox.setContentsMargins(30, 30, 30, 30)
        self.hBox.setSpacing(20)
        self.hBox.addWidget(self.button1)
        self.hBox.addWidget(self.button2)

        self.resize(600, 300)
        self._toolTip.hide()

        with open('resource/demo.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())

    def eventFilter(self, obj, e: QEvent):
        if obj is self:
            return super().eventFilter(obj, e)

        tip = self._toolTip
        if e.type() == QEvent.Enter:
            tip.setText(obj.toolTip())
            tip.setDuration(obj.toolTipDuration())

            pos = obj.mapTo(self, QPoint(0, 0))
            x = pos.x() + obj.width()//2 - tip.width()//2
            y = pos.y() - 5 - tip.height()

            # adjust postion to prevent tooltips from appearing outside the window
            x = min(max(5, x), self.width() - tip.width() - 5)
            y = min(max(5, y), self.height() - tip.height() - 5)

            tip.move(x, y)
            tip.show()
        elif e.type() == QEvent.Leave:
            tip.hide()
        elif e.type() == QEvent.ToolTip:
            return True

        return super().eventFilter(obj, e)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec_()
