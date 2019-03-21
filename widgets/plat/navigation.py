from widgets.base import ScrollArea
from PyQt5.QtWidgets import QApplication,QVBoxLayout,QFrame,QLabel,QPushButton,QListWidget,QListWidgetItem
from PyQt5.QtGui import QIcon

class Navigation(ScrollArea):

    def __init__(self, parent=None):
        """左侧导航栏"""
        super().__init__()

        self.setObjectName('Navigation')
        self.parent = parent
        self.setMaximumWidth(200)
        self.frame.setMaximumWidth(200)

        self.mainLayout = QVBoxLayout(self.frame)
        #self.mainLayout.setSpacing(0)

        self.mainLayout.addSpacing(5)
        self.recommendLabel = QLabel(" 推荐")
        self.recommendLabel.setObjectName("recommendLabel")
        self.recommendLabel.setMaximumHeight(27)
        self.mainLayout.addWidget(self.recommendLabel)

        self.recommendList = QListWidget()
        self.recommendList.setObjectName("recommendList")
        self.recommendList.addItem(QListWidgetItem(QIcon('../icons/music.jpg'), " 发现音乐"))
        self.recommendList.addItem(QListWidgetItem(QIcon('../icons/music.jpg'), " 私人FM"))
        self.recommendList.addItem(QListWidgetItem(QIcon('../icons/music.jpg'), " MV"))
        self.mainLayout.addWidget(self.recommendList)

        self.mainLayout.addSpacing(5)
        self.myMusicLabel = QLabel(" 我的音乐")
        self.myMusicLabel.setObjectName("myMusicLabel")
        self.myMusicLabel.setMaximumHeight(27)
        self.mainLayout.addWidget(self.myMusicLabel)

        self.myMusicList = QListWidget()
        self.myMusicList.setObjectName("myMusicList")
        self.myMusicList.addItem(QListWidgetItem(QIcon('../icons/music.jpg'), " 本地音乐"))
        self.myMusicList.addItem(QListWidgetItem(QIcon('../icons/music.jpg'), " 我的下载"))
        self.mainLayout.addWidget(self.myMusicList)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    Form = Navigation()
    #Form.resize(900, 40)
    Form.show()
    sys.exit(app.exec_())