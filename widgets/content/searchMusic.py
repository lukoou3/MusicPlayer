from widgets import ScrollArea
from PyQt5.QtWidgets import QVBoxLayout,QAbstractItemView,QTableWidget,QHeaderView,QTableWidgetItem,QTabWidget,QLabel
from service import addToLoop,SearchMusicNetEaseService

class SearchMusicTab(ScrollArea):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.setObjectName("SearchMusicTab")
        self.musicList = []

        self.frame.setContentsMargins(0,0,0,0)

        # 主布局。
        self.mainLayout = QVBoxLayout(self.frame)
        self.mainLayout.setSpacing(0)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

        self.noSingsContentsLabel = QLabel()
        self.noSingsContentsLabel.setMaximumHeight(60)
        self.noSingsContentsLabel.hide()
        self.mainLayout.addWidget(self.noSingsContentsLabel)

        self.singsTable = QTableWidget()
        self.singsTable.verticalHeader().setVisible(False)
        self.singsTable.setAlternatingRowColors(True)
        # self.singsTable.horizontalHeader().setStretchLastSection(True)
        self.singsTable.setColumnCount(4)
        # 注意必须在初始化行列之后进行，否则，没有效果
        self.singsTable.setHorizontalHeaderLabels(['序号', '音乐标题', '歌手', '时长'])
        self.singsTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.singsTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.Interactive)
        self.singsTable.horizontalHeader().setSectionResizeMode(3, QHeaderView.Interactive)
        self.singsTable.setColumnWidth(0, 40)
        self.singsTable.setColumnWidth(3, 100)
        self.singsTable.setObjectName('singsTable')
        self.mainLayout.addWidget(self.singsTable)

        self.singsTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.singsTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.singsTable.horizontalHeader().setStyleSheet("QHeaderView::section{background:#1C394D;}")

        self.singsTable.itemDoubleClicked.connect(self.musicItemDoubleClick)

    def search(self, text):
        pass

    def musicItemDoubleClick(self,item):
        #print(item)
        currentRow = self.singsTable.currentRow()
        player = self.parent.player
        import os
        import random
        names = [name for name in os.listdir(r"F:\musicdowmload") if ".MP3" in name]
        url = r"F:\musicdowmload\{}".format(random.choice(names))
        player.playMusic(url)
        #self.palyMusic(self.musicList[currentRow])

class SearchMusic(ScrollArea):
    def __init__(self, parent=None):
        super().__init__(self)
        self.parent = parent
        self.setObjectName("SearchMusic")
        self.searchText = ""

        self.frame.setContentsMargins(0, 0, 0, 0)

        self.tabWidget = QTabWidget()
        self.tabWidget.setObjectName("tabWidget")

        self.mainLayout = QVBoxLayout()
        # self.mainLayout.setSpacing(0)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.titleLabel = QLabel()
        self.mainLayout.addWidget(self.titleLabel)
        self.mainLayout.addWidget(self.tabWidget)

        self.frame.setLayout(self.mainLayout)

        self.addSearchMusicTabs()

    def addSearchMusicTabs(self):
        tab = SearchMusicNetEase(self.parent)
        self.addTab(tab,"网易云")

    def addTab(self, widget, name=''):
        self.tabWidget.addTab(widget, name)

    def search(self,text):
        self.searchText = text
        self.titleLabel.setText("搜索<font color='#23518F'>“{0}”</font><br>".format(self.searchText))
        tab = self.tabWidget.currentWidget()
        tab.search(self.searchText)


class SearchMusicNetEase(SearchMusicTab):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.seivice = SearchMusicNetEaseService()

    @addToLoop
    async def search(self, text):
        self.singsTable.clearContents()
        self.musicList = await self.seivice.search(text)
        self.singsTable.setRowCount(len(self.musicList))
        for i, data in enumerate(self.musicList):
            item = QTableWidgetItem(str(i + 1))
            self.singsTable.setItem(i, 0, item)
            item = QTableWidgetItem(data["name"])
            self.singsTable.setItem(i, 1, item)
            item = QTableWidgetItem(data["author"])
            self.singsTable.setItem(i, 2, item)
            item = QTableWidgetItem(transSeconds(data["duration"] / 1000))
            self.singsTable.setItem(i, 3, item)



def transSeconds(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return "%02d:%02d:%02d" % (h, m, s)