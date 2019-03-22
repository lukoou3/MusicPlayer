from widgets import ScrollArea
from PyQt5.QtWidgets import QVBoxLayout,QGridLayout,QFrame,QTabWidget,QLabel
from PyQt5.QtCore import Qt,pyqtSignal
from service import addToLoop,RecommendMusicNetEaseService,makeMd5
import asyncio
import os

@addToLoop
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
        tab = RecommendMusicNetEase(self)
        tab.getRecommendPlayList()
        self.addTab(tab,"网易云")

    def addTab(self, widget, name=''):
        self.tabWidget.addTab(widget, name)


class RecommendMusicNetEase(RecommendMusicTabBase):
    def __init__(self, parent=None):
        """推荐歌单tabbase"""
        super().__init__(parent)
        self.seivice = RecommendMusicNetEaseService()

    @addToLoop
    async def getRecommendPlayList(self, cat='全部歌单', types='all', offset=0, index=1):
        playlists = await self.seivice.getRecommendPlayList(cat,types,offset,index)

        if playlists:
            if not os.path.exists('cache/imgs'):
                os.makedirs('cache/imgs')
            cacheSet = set(os.listdir('cache/imgs'))

            length = 0
            do_list = list()
            for data in playlists:
                picName = makeMd5(data["coverImgUrl"])
                data["imgUrl"] = 'cache/imgs/{}'.format(picName)
                if picName in cacheSet:
                    row = int(length/4)
                    column = length % 4
                    length += 1
                    imgLabel = OneSingSeriesLabel(data["id"],data["imgUrl"],data["name"])
                    self.mainLayout.addWidget(imgLabel, row, column, Qt.AlignCenter)
                else:
                    do_list.append(self.seivice.loadRecommendImg(data["coverImgUrl"],picName,data))

            if do_list:
                to_do_iter = asyncio.as_completed(do_list)
                for future in to_do_iter:
                    data = await future
                    if data:
                        row = int(length / 4)
                        column = length % 4
                        length += 1
                        imgLabel = OneSingSeriesLabel(data["id"],data["imgUrl"], data["name"])
                        self.mainLayout.addWidget(imgLabel, row, column, Qt.AlignCenter)


class OneSingSeriesLabel(QFrame):
    clicked = pyqtSignal()
    def __init__(self,id,imgUrl,name):
        super().__init__()
        self.id = id

        self.setMinimumSize(160, 200)

        imgLabel = QLabel()
        imgLabel.setObjectName("imgLabel")
        imgLabel.setStyleSheet("#imgLabel{border-image: url(%s)}" % imgUrl)
        imgLabel.setMinimumSize(160, 160)
        imgLabel.setMaximumSize(160, 160)

        nameLabel = QLabel(name)
        nameLabel.setMaximumWidth(160)
        nameLabel.setWordWrap(True)

        self.mainLayout = QVBoxLayout(self)
        #self.mainLayout.setAlignment(Qt.AlignCenter)#设了无用
        self.mainLayout.addWidget(imgLabel,alignment=Qt.AlignCenter)
        self.mainLayout.addWidget(nameLabel,alignment=Qt.AlignLeft)


