from PyQt5.QtWidgets import QApplication,QHBoxLayout,QFrame,QLabel,QPushButton,QLineEdit
from PyQt5.QtGui import QPixmap,QIcon

class Player(QFrame):
    def __init__(self, parent=None):
        """头部区域，包括图标/搜索/设置/登陆/最大/小化/关闭。"""
        super().__init__()

        self.setObjectName('Header')
        self.parent = parent

        self.mainLayout = QHBoxLayout(self)
        #self.mainLayout.setSpacing(0)

        self.musicPreButton = QPushButton()
        #self.musicPreButton.setIcon(QIcon("../icons/music_pre.png"))
        self.musicPreButton.setStyleSheet("QPushButton{border-image: url(../icons/music_pre.png)}")
        #self.musicPreButton.setMaximumSize(48,48)
        self.musicPreButton.setMinimumSize(36, 36)
        self.musicPreButton.setObjectName("musicPreButton")
        self.mainLayout.addWidget(self.musicPreButton)

        self.musicPlayButton = QPushButton()
        self.musicPlayButton.setStyleSheet("QPushButton{border-image: url(../icons/music_on.png)}")
        #self.musicPlayButton.setMaximumSize(48, 48)
        self.musicPlayButton.setMinimumSize(36, 36)
        self.musicPlayButton.setObjectName("musicPlayButton")
        self.mainLayout.addWidget(self.musicPlayButton)

        self.musicNextButton = QPushButton()
        self.musicNextButton.setStyleSheet("QPushButton{border-image: url(../icons/music_next.png)}")
        #self.musicNextButton.setMaximumSize(48, 48)
        self.musicNextButton.setMinimumSize(36, 36)
        self.musicNextButton.setObjectName("musicNextButton")
        self.mainLayout.addWidget(self.musicNextButton)
        self.mainLayout.addStretch(1)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    Form = Player()
    Form.resize(900, 40)
    Form.show()
    sys.exit(app.exec_())