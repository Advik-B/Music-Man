# coding:utf-8
import os

from PyQt5.QtCore import QFile, Qt, pyqtSignal
from PyQt5.QtGui import (QBrush, QColor, QFont, QFontMetrics, QMouseEvent,
                         QPainter, QPen, QPixmap)
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
                             QVBoxLayout, QWidget, QPushButton)

from dialog import Dialog
from mask_dialog_base import MaskDialogBase
from scroll_area import ScrollArea


class FolderListDialog(MaskDialogBase):
    """ Folder list dialog box """

    folderChanged = pyqtSignal(list)

    def __init__(self, folderPaths: list, title: str, content: str, parent):
        super().__init__(parent=parent)
        self.title = title
        self.content = content
        self.__originalPaths = folderPaths
        self.folderPaths = folderPaths.copy()

        self.vBoxLayout = QVBoxLayout(self.widget)
        self.titleLabel = QLabel(title, self.widget)
        self.contentLabel = QLabel(content, self.widget)
        self.scrollArea = ScrollArea(self.widget)
        self.scrollWidget = QWidget(self.scrollArea)
        self.completeButton = QPushButton('完成', self.widget)
        self.addFolderCard = AddFolderCard(self.scrollWidget)
        self.folderCards = [FolderCard(i, self.scrollWidget)
                            for i in folderPaths]
        self.__initWidget()

    def __initWidget(self):
        """ initialize widgets """
        self.__setQss()

        w = max(self.titleLabel.width()+60, self.contentLabel.width()+60, 440)
        self.widget.setFixedWidth(w)
        self.scrollArea.resize(368, 90)
        self.scrollWidget.resize(365, 90)
        self.scrollArea.setFixedWidth(368)
        self.scrollWidget.setFixedWidth(365)
        self.scrollArea.setMaximumHeight(500)
        self.scrollArea.setViewportMargins(0, 0, 0, 0)
        self.scrollArea.setWidget(self.scrollWidget)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.__initLayout()

        # connect signal to slot
        self.addFolderCard.clicked.connect(self.__showFileDialog)
        self.completeButton.clicked.connect(self.__onButtonClicked)
        for card in self.folderCards:
            card.clicked.connect(self.__showDeleteFolderCardDialog)

    def __initLayout(self):
        """ initialize layout """
        self.vBoxLayout.setContentsMargins(30, 30, 30, 30)
        self.vBoxLayout.setSizeConstraint(QVBoxLayout.SetFixedSize)
        self.vBoxLayout.setAlignment(Qt.AlignTop)
        self.vBoxLayout.setSpacing(0)

        # labels
        layout_1 = QVBoxLayout()
        layout_1.setContentsMargins(0, 0, 0, 0)
        layout_1.setSpacing(7)
        layout_1.addWidget(self.titleLabel, 0, Qt.AlignTop)
        layout_1.addWidget(self.contentLabel, 0, Qt.AlignTop)
        self.vBoxLayout.addLayout(layout_1, 0)
        self.vBoxLayout.addSpacing(15)

        # cards
        layout_2 = QHBoxLayout()
        layout_2.setAlignment(Qt.AlignCenter)
        layout_2.setContentsMargins(5, 0, 5, 0)
        layout_2.addWidget(self.scrollArea, 0, Qt.AlignCenter)
        self.vBoxLayout.addLayout(layout_2, 1)
        self.vBoxLayout.addSpacing(30)

        self.scrollLayout = QVBoxLayout(self.scrollWidget)
        self.scrollLayout.setAlignment(Qt.AlignTop)
        self.scrollLayout.setContentsMargins(0, 0, 0, 0)
        self.scrollLayout.setSpacing(10)
        self.scrollLayout.addWidget(self.addFolderCard, 0, Qt.AlignTop)
        for card in self.folderCards:
            self.scrollLayout.addWidget(card, 0, Qt.AlignTop)

        # buttons
        layout_3 = QHBoxLayout()
        layout_3.setContentsMargins(0, 0, 0, 0)
        layout_3.addStretch(1)
        layout_3.addWidget(self.completeButton)
        self.vBoxLayout.addLayout(layout_3, 0)

        self.__adjustWidgetSize()

    def __showFileDialog(self):
        """ show file dialog to select folder """
        path = QFileDialog.getExistingDirectory(
            self, self.tr("Choose folder"), "./")

        if not path or path in self.folderPaths:
            return

        # create folder card
        card = FolderCard(path, self.scrollWidget)
        self.scrollLayout.addWidget(card, 0, Qt.AlignTop)
        card.clicked.connect(self.__showDeleteFolderCardDialog)
        card.show()

        self.folderPaths.append(path)
        self.folderCards.append(card)

        self.__adjustWidgetSize()

    def __showDeleteFolderCardDialog(self):
        """ show delete folder card dialog """
        sender = self.sender()
        title = '确认删除文件夹吗？'
        content = f'如果将"{sender.folderName}"文件夹从列表中移除，则该文件夹不会再出现在列表中，但不会被删除。'
        dialog = Dialog(title, content, self.window())
        dialog.yesSignal.connect(lambda: self.__deleteFolderCard(sender))
        dialog.exec_()

    def __deleteFolderCard(self, folderCard):
        """ delete selected folder card """
        self.scrollLayout.removeWidget(folderCard)
        index = self.folderCards.index(folderCard)
        self.folderCards.pop(index)
        self.folderPaths.pop(index)
        folderCard.deleteLater()

        # adjust height
        self.__adjustWidgetSize()

    def __setQss(self):
        """ set style sheet """
        self.titleLabel.setObjectName('titleLabel')
        self.contentLabel.setObjectName('contentLabel')
        self.completeButton.setObjectName('completeButton')
        self.scrollWidget.setObjectName('scrollWidget')

        with open('resource/style/folder_list_dialog.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())

        self.setStyle(QApplication.style())
        self.titleLabel.adjustSize()
        self.contentLabel.adjustSize()
        self.completeButton.adjustSize()

    def __onButtonClicked(self):
        """ done button clicked slot """
        if sorted(self.__originalPaths) != sorted(self.folderPaths):
            self.setEnabled(False)
            QApplication.processEvents()
            self.folderChanged.emit(self.folderPaths)

        self.close()

    def __adjustWidgetSize(self):
        N = len(self.folderCards)
        h = 90*(N+1) + 10*N
        self.scrollArea.setFixedHeight(min(h, 500))
        self.scrollWidget.setFixedHeight(h)


class ClickableWindow(QWidget):
    """ Clickable window """

    clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setFixedSize(365, 90)
        self._isPressed = None
        self._isEnter = False

    def enterEvent(self, e):
        self._isEnter = True
        self.update()

    def leaveEvent(self, e):
        self._isEnter = False
        self.update()

    def mouseReleaseEvent(self, e):
        self._isPressed = False
        self.update()
        if e.button() == Qt.LeftButton:
            self.clicked.emit()

    def mousePressEvent(self, e: QMouseEvent):
        self._isPressed = True
        self.update()

    def paintEvent(self, e):
        """ paint window """
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)
        brush = QBrush(QColor(204, 204, 204))
        painter.setPen(Qt.NoPen)
        if not self._isEnter:
            painter.setBrush(brush)
            painter.drawRoundedRect(self.rect(), 5, 5)
        else:
            painter.setPen(QPen(QColor(204, 204, 204), 2))
            painter.drawRect(1, 1, self.width() - 2, self.height() - 2)
            painter.setPen(Qt.NoPen)
            if not self._isPressed:
                brush.setColor(QColor(230, 230, 230))
                painter.setBrush(brush)
                painter.drawRect(2, 2, self.width() - 4, self.height() - 4)
            else:
                brush.setColor(QColor(153, 153, 153))
                painter.setBrush(brush)
                painter.drawRoundedRect(
                    6, 1, self.width() - 12, self.height() - 2, 3, 3)


class FolderCard(ClickableWindow):
    """ Folder card """

    def __init__(self, folderPath: str, parent=None):
        super().__init__(parent)
        self.folderPath = folderPath
        self.folderName = os.path.basename(folderPath)
        self.__closeIcon = QPixmap("resource/images/黑色叉号.png")

    def paintEvent(self, e):
        """ paint card """
        super().paintEvent(e)
        painter = QPainter(self)
        painter.setRenderHints(
            QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)

        # paint text and icon
        if self._isPressed:
            self.__drawText(painter, 15, 10, 15, 9)
            painter.drawPixmap(self.width() - 33, 23, self.__closeIcon)
        else:
            self.__drawText(painter, 12, 11, 12, 10)
            painter.drawPixmap(self.width() - 30, 25, self.__closeIcon)

    def __drawText(self, painter, x1, fontSize1, x2, fontSize2):
        """ draw text """
        # paint folder name
        font = QFont("Microsoft YaHei", fontSize1, 75)
        painter.setFont(font)
        name = QFontMetrics(font).elidedText(
            self.folderName, Qt.ElideRight, self.width()-60)
        painter.drawText(x1, 37, name)

        # paint folder path
        font = QFont("Microsoft YaHei", fontSize2)
        painter.setFont(font)
        path = QFontMetrics(font).elidedText(
            self.folderPath, Qt.ElideRight, self.width()-30)
        painter.drawText(x2, 46, self.width() - 20, 23, Qt.AlignLeft, path)


class AddFolderCard(ClickableWindow):
    """ Add folder card """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__iconPix = QPixmap("resource/images/黑色加号.png")

    def paintEvent(self, e):
        """ paint card """
        super().paintEvent(e)
        painter = QPainter(self)
        w = self.width()
        h = self.height()
        pw = self.__iconPix.width()
        ph = self.__iconPix.height()
        if not self._isPressed:
            painter.drawPixmap(
                int(w/2 - pw/2), int(h/2 - ph/2), self.__iconPix)
        else:
            painter.drawPixmap(
                int(w/2 - (pw - 4)/2), int(h/2 - (ph - 4)/2), pw - 4, ph - 4, self.__iconPix)
