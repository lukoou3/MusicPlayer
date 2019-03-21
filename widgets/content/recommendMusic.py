from widgets import ScrollArea
from PyQt5.QtWidgets import QApplication,QVBoxLayout,QGridLayout,QFrame,QTabWidget,QLabel,QPushButton,QLineEdit
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt,pyqtSignal
import requests
import asyncio

async def test():
    await asyncio.sleep(0.1)
    print('timeout expired')
    await asyncio.sleep(2)
    print('second timeout expired')

class RecommendMusicTabBase(ScrollArea):
    def __init__(self, parent=None):
        """推荐歌单tabbase"""
        super().__init__()
        self.parent = parent
        self.setObjectName("RecommendMusicTab")

        self.frame.setContentsMargins(0,0,0,0)

        # 主布局。
        self.mainLayout = QGridLayout(self.frame)
        self.mainLayout.setSpacing(0)
        self.mainLayout.setHorizontalSpacing(10)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

    def addImgs(self):
        for i in range(4):
            for j in range(4):
                imgLabel = OneSingSeriesLabel()
                self.mainLayout.addWidget(imgLabel,i,j,Qt.AlignCenter)

class RecommendMusic(ScrollArea):
    def __init__(self, parent=None):
        """主内容区，包括推荐歌单等。"""
        super().__init__()
        self.parent = parent
        self.setObjectName("RecommendMusic")

        self.frame.setContentsMargins(0, 0, 0, 0)

        self.tabWidget = QTabWidget()
        self.tabWidget.setObjectName("tabWidget")

        self.mainLayout = QVBoxLayout()
        #self.mainLayout.setSpacing(0)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.addWidget(self.tabWidget)

        self.frame.setLayout(self.mainLayout)

        self.addRecommendMusicTabs()

    def addRecommendMusicTabs(self):
        tab = RecommendMusicNetEase()
        tab.addImgs()
        loop = asyncio.get_event_loop()
        loop.create_task(test())
        loop.create_task(test())
        loop.create_task(test())
        loop.create_task(test())
        #tab.getRecommendPlayList()
        self.addTab(tab,"网易云")

    def addTab(self, widget, name=''):
        self.tabWidget.addTab(widget, name)


class RecommendMusicNetEase(RecommendMusicTabBase):

    def getRecommendPlayList(self, cat='全部歌单', types='all', offset=0, index=1):
        url = 'http://music.163.com/api/playlist/list?cat=%s&type=%s&order=%s&offset=%d&total=true&limit=30&index=%d' \
              % (cat, types, types, offset, index)
        response = requests.get(url,headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Accept-Encoding': 'gzip,deflate,sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'
    })
        print(response.text)

    def addImgs(self):
        for i in range(4):
            for j in range(4):
                imgLabel = OneSingSeriesLabel()
                self.mainLayout.addWidget(imgLabel,i,j,Qt.AlignCenter)


class OneSingSeriesLabel(QFrame):
    clicked = pyqtSignal()
    def __init__(self):
        super().__init__()

        self.setMinimumSize(160, 210)

        imgLabel = QLabel()
        imgLabel.setPixmap(QPixmap("../icons/0a7e0e9c945d8049f4a6a2c461147917"))
        imgLabel.setScaledContents(True)
        imgLabel.setMinimumSize(160, 180)
        imgLabel.setMaximumSize(160, 180)

        nameLabel = QLabel("福欧艾斯")
        nameLabel.setMaximumWidth(160)
        nameLabel.setWordWrap(True)

        self.mainLayout = QVBoxLayout(self)
        #self.mainLayout.setAlignment(Qt.AlignCenter)#设了无用
        self.mainLayout.addWidget(imgLabel,alignment=Qt.AlignCenter)
        self.mainLayout.addWidget(nameLabel,alignment=Qt.AlignLeft)


