from PyQt5.QtWidgets import QApplication,QHBoxLayout,QFrame,QLabel,QPushButton,QLineEdit,QSizePolicy,QSpacerItem
from PyQt5.QtGui import QPixmap,QCursor
from PyQt5.QtCore import Qt,pyqtSlot,pyqtSignal
from PyQt5 import QtCore


class SearchLineEdit(QLineEdit):
    searchSignal =  pyqtSignal(str)
    """创建一个可搜索的输入框。"""
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.setMinimumSize(218, 20)

        self.button = QPushButton(self)
        self.button.setMaximumSize(16, 16)
        self.button.setCursor(QCursor(Qt.PointingHandCursor))
        self.button.setStyleSheet("QPushButton{border-image: url(icons/search.png)}")

        self.setTextMargins(3, 0, 19, 0)

        self.spaceItem = QSpacerItem(150, 10, QSizePolicy.Expanding)

        self.mainLayout = QHBoxLayout()
        self.mainLayout.addSpacerItem(self.spaceItem)
        # self.mainLayout.addStretch(1)
        self.mainLayout.addWidget(self.button)
        self.mainLayout.addSpacing(5)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.mainLayout)

        self.button.clicked.connect(self.sendSearchSignal)

    def sendSearchSignal(self):
        self.searchSignal.emit(self.text())

class Header(QFrame):
    def __init__(self, parent=None):
        """头部区域，包括图标/搜索/设置/登陆/最大/小化/关闭。"""
        super().__init__()

        self.setObjectName('Header')
        self.parent = parent

        self.mainLayout = QHBoxLayout(self)
        #self.mainLayout.setSpacing(0)

        self.logoLabel = QLabel()
        self.logoLabel.setMaximumSize(32,32)
        self.logoLabel.setText("")
        self.logoLabel.setPixmap(QPixmap("icons/timg.jpg"))
        self.logoLabel.setScaledContents(True)
        self.logoLabel.setObjectName("logoLabel")
        self.mainLayout.addWidget(self.logoLabel)

        self.titleLabel = QLabel()
        self.titleLabel.setText("<b>Music</b>")
        self.mainLayout.addWidget(self.titleLabel)


        self.preButton = QPushButton('<')
        self.preButton.setObjectName("preButton")
        self.preButton.setMinimumSize(28, 22)
        self.preButton.setMaximumSize(28, 22)
        self.mainLayout.addWidget(self.preButton)

        self.nextButton = QPushButton('>')
        self.nextButton.setObjectName("nextButton")
        self.nextButton.setMinimumSize(28, 22)
        self.nextButton.setMaximumSize(28, 22)
        self.mainLayout.addWidget(self.nextButton)


        self.searchLineEdit = SearchLineEdit()
        self.searchLineEdit.setObjectName("searchLineEdit")
        self.mainLayout.addWidget(self.searchLineEdit)
        self.mainLayout.addStretch(1)

        self.minButton = QPushButton('_')
        self.minButton.setObjectName("minButton")
        self.minButton.setMinimumSize(21, 17)
        self.mainLayout.addWidget(self.minButton)

        self.maxButton = QPushButton("□")
        self.maxButton.setObjectName("maxButton")
        self.maxButton.setMinimumSize(21, 17)
        self.mainLayout.addWidget(self.maxButton)

        self.closeButton = QPushButton("×")
        self.closeButton.setObjectName("closeButton")
        self.closeButton.setMinimumSize(21, 17)
        self.mainLayout.addWidget(self.closeButton)

        QtCore.QMetaObject.connectSlotsByName(self)

    """
    @pyqtSlot()
    def on_closeButton_clicked(self):
        self.parent.close()
    """

    """重写鼠标事件，实现窗口拖动。"""

    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.parent.m_DragPosition = event.globalPos() - self.parent.pos()
            event.accept()

    def mouseMoveEvent(self, event):
        try:
            if event.buttons() and Qt.LeftButton:
                self.parent.move(event.globalPos() - self.parent.m_DragPosition)
                event.accept()
        except AttributeError:
            pass

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    Form = Header()
    Form.resize(900, 40)
    Form.show()
    sys.exit(app.exec_())