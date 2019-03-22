from PyQt5.QtCore import QObject,pyqtSignal
from PyQt5.QtGui import QPixmap
from service import headers,addToLoop,session
import aiohttp
import json


class RecommendMusicService(QObject):
    async def loadRecommendImg(self,url,name,data=None):
        try:
            async with self.session.get(url,headers=headers,timeout=60) as response:
                if response.status == 200:
                    image_content = await response.read()
                else:
                    raise aiohttp.ClientError()
        except Exception as e:
            print(e)
            return None
        pic = QPixmap()
        pic.loadFromData(image_content)
        # 缩小到合适的大小会让QT合理的利用内存资源。
        pic = pic.scaled(180, 180)
        pic.save("cache/imgs/{0}".format(name),'jpg')
        return data

class RecommendMusicNetEaseService(RecommendMusicService):
    signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.session = session["session"]

    #@addToLoop
    async def getRecommendPlayList(self, cat='全部歌单', types='all', offset=0, index=1):
        url = 'http://music.163.com/api/playlist/list?cat={0}&type={1}&order={2}&offset={3}&total=true&limit=30&index={4}'.format(
            cat, types, types, offset, index)
        print(url)
        async with self.session.get(url,headers=headers,timeout=3) as response:
            if response.status == 200:
                text =  await response.text()
                return json.loads(text)['playlists']
            else:
                return None


