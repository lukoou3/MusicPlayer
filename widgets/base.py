from PyQt5.QtWidgets import QScrollArea,QFrame,QGridLayout,QHBoxLayout,QPushButton,QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal,Qt
from service import makeMd5,addToLoop,session,headers
import aiohttp
import os

# 一个用于继承的类，方便多次调用。
class ScrollArea(QScrollArea):
    """包括一个ScrollArea做主体承载一个QFrame的基础类。"""
    scrollDown = pyqtSignal()

    def __init__(self, parent=None):
        super(ScrollArea, self).__init__()
        self.parent = parent
        self.frame = QFrame()
        self.frame.setObjectName('frame')

        # 用于发出scroll滑到最底部的信号。
        self.verticalScrollBar().valueChanged.connect(self.sliderPostionEvent)

        self.setWidgetResizable(True)

        self.setWidget(self.frame)#必须设置Widget

    def noInternet(self):
        # 设置没有网络的提示。
        self.noInternetLayout = QGridLayout()
        self.setLayout(self.mainLayout)

        self.Tip = QLabel("您已进入没有网络的异次元，打破次元壁 →", self)
        self.TipButton = QPushButton("打破次元壁", self)
        self.TipButton.setObjectName("TipButton")

        self.TipLayout = QHBoxLayout()
        self.TipLayout.addWidget(self.Tip)
        self.TipLayout.addWidget(self.TipButton)

        # self.indexAllSings.setLayout(self.TipLayout)

        self.noInternetLayout.addLayout(self.TipLayout, 0, 0, Qt.AlignCenter|Qt.AlignTop)

        self.frame.setLayout(self.noInternetLayout)

    def sliderPostionEvent(self):
        if self.verticalScrollBar().value() == self.verticalScrollBar().maximum():
            self.scrollDown.emit()

    def maximumValue(self):
        return self.verticalScrollBar().maximum()

cacheFolder = "cache/imgs"
def checkOneFolder(folderName:str):
    if not os.path.exists(folderName):
        os.makedirs(folderName)
    def _check(func):
        def _exec(*args):
            try:
                func(*args)
            except Exception as e:
                print(e)
        return _exec
    return _check
## 对<img src=1.jpg>的初步探索。
# 暂只接受http(s)和本地目录。
class PicLabel(QLabel):

    def __init__(self,parent=None,src=None, width=200, height=200, pixMask=None):
        super().__init__(parent)

        self.src = None
        self.width = width
        self.height = height

        self.pixMask = None
        if pixMask:
            self.pixMask = pixMask
        if src:
            self.setSrc(src)

        if self.width:
            self.setMaximumSize(self.width, self.height)
            self.setMinimumSize(self.width, self.height)

    @checkOneFolder(cacheFolder)
    def setSrc(self, src):
        src = str(src)
        if 'http' in src or 'https' in src:
            cacheList = os.listdir(cacheFolder)

            name = makeMd5(src)
            localSrc = cacheFolder+'/'+name
            if name in cacheList:
                self.setSrc(localSrc)
                self.src = localSrc
                return

            self.loadImg(src,name)
        else:
            self.src = src
            pix = QPixmap(src)
            pix.load(src)
            pix = pix.scaled(self.width, self.height)
            # mask需要与pix是相同大小。
            if self.pixMask:
                mask = QPixmap(self.pixMask)
                mask = mask.scaled(self.width, self.height)
                pix.setMask(mask.createHeuristicMask())

            self.setPixmap(pix)

    def getSrc(self):
        """返回该图片的地址。"""
        return self.src

    @addToLoop
    async def loadImg(self,src,name):
        try:
            async with session["session"].get(src,headers=headers,timeout=60) as response:
                if response.status == 200:
                    image_content = await response.read()
                else:
                    raise aiohttp.ClientError()
        except Exception as e:
            print(e)
            return

        width = self.width
        height = self.height

        pic = QPixmap()
        pic.loadFromData(image_content)
        localSrc = cacheFolder + '/' + name
        pic.save(localSrc, 'jpg')
        pic = pic.scaled(width, height)

        self.src = localSrc

        # 上遮罩。
        if self.pixMask:
            mask = QPixmap()
            mask.load(self.pixMask)
            mask = mask.scaled(width, height)

            pic.setMask(mask.createHeuristicMask())

        self.setPixmap(pic)