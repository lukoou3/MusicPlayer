from widgets import ScrollArea,PicLabel
from PyQt5.QtWidgets import (QApplication,QVBoxLayout,QHeaderView,QAbstractItemView,QHBoxLayout,
                             QPushButton,QTabWidget,QLabel,QTextEdit,QTableWidget,QTableWidgetItem,
                             QProgressBar,QMenu,QAction)
from PyQt5.QtGui import QIcon,QCursor
from PyQt5.QtCore import QUrl,Qt
from PyQt5.QtMultimedia import QMediaContent,QMediaPlayer
from service import addToLoop,RecommendMusicDetailNetEaseService,RecommendMusicDetailQQService

class RecommendMusicDetailBase(ScrollArea):
    def __init__(self, parent=None):
        """推荐歌单tabbase"""
        super().__init__()
        self.parent = parent
        self.setObjectName("RecommendMusicDetail")
        self.musicList = []

        self.frame.setContentsMargins(0,0,0,0)

        # 主布局。
        self.mainLayout = QVBoxLayout(self.frame)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)

        self.topLayout = QHBoxLayout()
        self.topLayout.setContentsMargins(0, 0, 0, 0)
        self.picLabel = PicLabel(width=180, height=180)
        self.topLayout.addWidget(self.picLabel)

        self.topRightLayout = QVBoxLayout()
        self.topRightLayout.setContentsMargins(0, 0, 0, 0)
        self.topRightLayout.setSpacing(0)
        self.topLayout.addLayout(self.topRightLayout)

        self.topRightLayoutTitle = QHBoxLayout()
        self.topRightLayoutTitle.setContentsMargins(0, 0, 0, 0)
        self.topRightLayoutTitle.setSpacing(0)
        self.gedanButton = QPushButton("歌单")
        self.gedanButton.setMaximumSize(36, 20)
        self.titleLabel = QLabel()
        self.titleLabel.setWordWrap(True)
        self.titleLabel.setMaximumHeight(40)
        self.topRightLayoutTitle.addWidget(self.gedanButton)
        self.topRightLayoutTitle.addWidget(self.titleLabel)
        self.topRightLayout.addLayout(self.topRightLayoutTitle)

        self.authorLabel = QLabel()
        self.authorLabel.setMaximumHeight(28)
        self.topRightLayout.addWidget(self.authorLabel)

        self.playAllButton = QPushButton("全部播放")
        self.playAllButton.setIcon(QIcon('icons/playAll.png'))
        self.playAllButton.setObjectName('playAllButton')
        self.playAllButton.setMaximumSize(90, 24)
        self.topRightLayout.addWidget(self.playAllButton)

        self.topRightLayoutDesc = QHBoxLayout()
        self.topRightLayoutDesc.setContentsMargins(0, 0, 0, 0)
        self.topRightLayoutDesc.setSpacing(0)
        self.descLabel = QLabel("简介：")
        self.descriptionText = QTextEdit()
        self.descriptionText.setReadOnly(True)
        self.descriptionText.setMinimumWidth(450)
        self.descriptionText.setMinimumHeight(100)
        self.descriptionText.setMaximumHeight(100)
        self.topRightLayoutDesc.addWidget(self.descLabel)
        self.topRightLayoutDesc.addWidget(self.descriptionText)
        self.topRightLayout.addLayout(self.topRightLayoutDesc)

        self.topLayout.addLayout(self.topRightLayout)
        self.mainLayout.addLayout(self.topLayout)

        self.contentsTab = QTabWidget()
        self.singsTable = QTableWidget()
        self.singsTable.verticalHeader().setVisible(False)
        self.singsTable.setAlternatingRowColors(True)
        #self.singsTable.horizontalHeader().setStretchLastSection(True)
        self.singsTable.setColumnCount(4)
        #注意必须在初始化行列之后进行，否则，没有效果
        self.singsTable.setHorizontalHeaderLabels(['序号','音乐标题', '歌手', '时长'])
        self.singsTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.singsTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.Interactive)
        self.singsTable.horizontalHeader().setSectionResizeMode(3, QHeaderView.Interactive)
        self.singsTable.setColumnWidth(0,40)
        self.singsTable.setColumnWidth(3, 100)
        self.singsTable.setObjectName('singsTable')
        """
        self.singsTable.setMinimumWidth(self.width())
        self.singsTable.setColumnWidths({i: j for i, j in zip(range(3),
                  [self.width() / 3 * 1.25, self.width() / 3 * 1.25,
                   self.width() / 3 * 0.5])})
        """
        self.contentsTab.addTab(self.singsTable, "歌曲列表")

        self.mainLayout.addWidget(self.contentsTab)
        self.mainLayout.setStretch(0,3)
        self.mainLayout.setStretch(1,7)

        self.singsTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.singsTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.singsTable.horizontalHeader().setStyleSheet("QHeaderView::section{background:#1C394D;}")

        self.singsTable.itemDoubleClicked.connect(self.musicItemDoubleClick)

        self.singsTable.setContextMenuPolicy(Qt.CustomContextMenu)
        self.singsTable.customContextMenuRequested.connect(self.singsTableContextMenu)

    def musicItemDoubleClick(self,item):
        #print(item)
        currentRow = self.singsTable.currentRow()

        """
        player = self.parent.player
        import os
        import random
        names = [name for name in os.listdir(r"F:\musicdowmload") if ".MP3" in name]
        url = r"F:\musicdowmload\{}".format(random.choice(names))
        player.playMusic(QUrl.fromLocalFile(url))
        """

        self.palyMusic(self.musicList[currentRow])

    def singsTableContextMenu(self,pos):
        currentRow = self.singsTable.currentRow()

        pmenu = QMenu(self)
        downloadAct = QAction("下载", pmenu)
        pmenu.addAction(downloadAct)
        downloadAct.triggered.connect(lambda :self.downloadMusic(currentRow))
        #pmenu.popup(self.singsTable.mapToGlobal(pos))
        pmenu.popup(QCursor.pos())

    async def downloadMusic(self,currentRow):
        pass

    async def palyMusic(self,data):
        pass


class RecommendMusicDetailNetEase(RecommendMusicDetailBase):
    def __init__(self, parent=None):
        """歌单歌曲"""
        super().__init__(parent)
        self.seivice = RecommendMusicDetailNetEaseService()

    def updateInfo(self,data):
        self.picLabel.setSrc(data["imgUrl"])
        self.picLabel.setStyleSheet('''QLabel {padding: 10px;}''')
        self.titleLabel.setText(data["name"])
        self.authorLabel.setText(data['creator']['nickname'])
        self.descriptionText.setText(data.get("description", ""))

        #self.singsTable.clear()
        self.singsTable.clearContents()
        self.updateSingsTable(data)

    @addToLoop
    async def updateSingsTable(self,data):
        # import pprint
        # pprint.pprint(data)
        self.musicList = await self.seivice.getDetailMusicList(data)
        self.singsTable.setRowCount(len(self.musicList))
        for i,data in enumerate(self.musicList):
            item = QTableWidgetItem(str(i+1))
            self.singsTable.setItem(i, 0, item)
            item = QTableWidgetItem(data["name"])
            self.singsTable.setItem(i,1,item)
            item = QTableWidgetItem(data["author"])
            self.singsTable.setItem(i,2,item)
            item = QTableWidgetItem(transSeconds(data["duration"]/1000))
            self.singsTable.setItem(i,3,item)

    @addToLoop
    async def palyMusic(self,data):
        musicList = await self.seivice.getMusicUrlInfo([data["id"]])
        if musicList:
            url = musicList[0]["url"]
        else:
            url = "http://music.163.com/song/media/outer/url?id={}.mp3".format(data["id"])
        player = self.parent.player
        player.playMusic(QUrl(url))

    @addToLoop
    async def downloadMusic(self,currentRow):
        data = self.musicList[currentRow]
        progressBar = QProgressBar()
        self.singsTable.setCellWidget(currentRow, 3, progressBar)
        await self.seivice.downloadMusic("http://music.163.com/song/media/outer/url?id={}.mp3".format(data["id"]),
                                          progressBar)


class RecommendMusicDetailQQ(RecommendMusicDetailBase):
    def __init__(self, parent=None):
        """歌单歌曲"""
        super().__init__(parent)
        self.seivice = RecommendMusicDetailQQService()

    @addToLoop

    async def updateInfo(self,data):
        await self.seivice.getDetailMusicList(data)



def transSeconds(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return "%02d:%02d:%02d" % (h, m, s)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    content = QMediaContent(QUrl("http://m10.music.126.net/20190323193124/9f385ee03ede3f967a9c72152a911a8c/ymusic/46a6/061d/57b9/dca63fbd90a9bcba54084db8b1209593.mp3"))
    #content = QMediaContent(QUrl.fromLocalFile(r"F:\musicdowmload\处处吻__杨千嬅.MP3"))
    play = QMediaPlayer()
    play.setMedia(content)
    play.play()
    sys.exit(app.exec_())

