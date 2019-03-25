# event loop
# https://github.com/harvimt/quamash
# an asyncio eventloop for PyQt.
from quamash import QEventLoop
import asyncio
from PyQt5.QtWidgets import QApplication,QTabWidget,QHBoxLayout,QVBoxLayout,QFrame,QLabel,QPushButton,QLineEdit
from PyQt5.QtCore import Qt
from widgets.plat import Header,Navigation,Player
from widgets.content import RecommendMusic,RecommendMusicDetailNetEase,RecommendMusicDetailQQ,SearchMusic
import sip
import aiohttp
from service import addToLoop
from service.util import open_session,close_session

class Main(QFrame):
    def __init__(self, parent=None):
        """"""
        super().__init__()

        self.setObjectName('Main')
        self.parent = parent

    def initUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint)  # 隐藏边框

        self.mainLayout = QVBoxLayout(self)
        # self.mainLayout.setSpacing(0)

        self.header = Header(self)
        self.mainLayout.addWidget(self.header, 20)

        self.contentLayout = QHBoxLayout()
        self.contentLayout.setContentsMargins(0,0,0,0)
        self.contentLayout.setSpacing(0)
        self.navigation = Navigation(self)
        self.contentLayout.addWidget(self.navigation)
        self.contents = QTabWidget()
        self.contents.setContentsMargins(0,0,0,0)
        self.contents.tabBar().hide()
        self.recommendMusic = RecommendMusic(self)
        self.musicDetailNetEase = RecommendMusicDetailNetEase(self)
        self.musicDetailQQ = RecommendMusicDetailQQ(self)
        self.searchMusic = SearchMusic(self)
        self.contents.addTab(self.recommendMusic, "")
        self.contents.addTab(self.musicDetailNetEase, "")
        self.contents.addTab(self.musicDetailQQ, "")
        self.contents.addTab(self.searchMusic, "")
        self.content = self.recommendMusic
        self.contents.setCurrentWidget(self.content)
        self.contentLayout.addWidget(self.contents)
        self.mainLayout.addLayout(self.contentLayout, 400)

        self.player = Player(self)
        self.mainLayout.addWidget(self.player, 20)


        self.registerSignalConnect()

    def registerSignalConnect(self):
        # 注册最小化事件
        self.header.minButton.clicked.connect(self.showMinimized)
        # 注册最大化事件
        self.header.maxButton.clicked.connect(self.showMaxiOrRevert)
        #注册关闭事件
        self.header.closeButton.clicked.connect(self.close)
        # 注册导航栏事件
        self.navigation.recommendList.currentRowChanged.connect(self.navigationRecommendChanged)
        self.navigation.recommendList.itemPressed.connect(self.navigationRecommendItemClick)
        self.navigation.myMusicList.currentRowChanged.connect(self.navigationmyMusicChanged)

        self.header.searchLineEdit.searchSignal.connect(self.showSearchMusic)

    def showMaxiOrRevert(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def navigationRecommendChanged(self,index):
        #print(index)
        self.navigation.myMusicList.setCurrentRow(-1)

        self.changeContentWidget(self.recommendMusic)

    def navigationRecommendItemClick(self,widgetItem):
        pass
        print(self.navigation.recommendList.currentRow())
        #print(widgetItem)

    def navigationmyMusicChanged(self,index):
        self.navigation.recommendList.setCurrentRow(-1)

    def changeContentWidget(self,content):
        #self.contentLayout.replaceWidget(self.content, content)
        #sip.delete(self.content)
        #del self.content
        self.content = content
        self.contents.setCurrentWidget(self.content)

    def showSearchMusic(self,text):
        text = text.strip()
        if text:
            self.changeContentWidget(self.searchMusic)
            self.searchMusic.search(text)
            #self.changeContentWidget(self.searchMusic)

"""
@addToLoop
async def open_session():
    session = aiohttp.ClientSession()
    Form.session = session

@addToLoop
async def close_session():
    if Form.session:
        await Form.session.close()
        print("session close")
"""

if __name__ == "__main__":
    """
    在PyQt5中,如果在Python 代码中抛出了异常,没有进行捕获,异常只要进入事件循环,程序就崩溃,而没有任何提示,给程序调试带来不少麻烦,通过在程序运行前加入以下代码,则能避免程序崩溃.
    import cgitb 
    cgitb.enable( format = ‘text’)
    """
    """
    import sys
    import qdarkstyle
    import cgitb
    cgitb.enable(format='text')#
    app = QApplication(sys.argv)
    # 将Qt事件循环写到asyncio事件循环里。
    # QEventLoop不是Qt原生事件循环，
    # 是被asyncio重写的事件循环。
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    with loop:
        Form = Main()
        loop.run_until_complete(open_session())
        app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        Form.initUI()
        #Form.resize(1022, 700)
        Form.resize(600, 400)
        Form.show()
        #sys.exit(app.exec_())
        loop.run_forever()
        loop.run_until_complete(close_session())
        print("close")
    """

