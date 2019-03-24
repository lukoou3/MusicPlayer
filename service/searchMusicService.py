from PyQt5.QtCore import QObject
from service import headers,session,encrypted_request
import json

class SearchMusicService(QObject):
    def __init__(self):
        super().__init__()
        self.session = session["session"]

class SearchMusicNetEaseService(SearchMusicService):

    async def search(self, text, offset=0, limit=100, stype=1):
        """
            type类型: 单曲(1), 专辑(10), 歌手(100), 歌单(1000), 用户(1002)
        """
        url = 'http://music.163.com/weapi/cloudsearch/get/web'
        data = {'s': text,'offset': str(offset),'limit': str(limit),'type': str(stype)}
        data = encrypted_request(data)
        try:
            async with self.session.post(url,data=data,headers=headers,timeout=3) as response:
                if response.status == 200:
                    text =  await response.text()
                    #import asyncio
                    #await asyncio.sleep(5)
                    rst = json.loads(text)
                    if rst["code"] != 200:
                        print(rst)
                        return []
                else:
                    return []
        except:
            return []
        musicList = [
            {"id": item["id"], "name": item["name"], "author": "，".join(artist["name"] for artist in item["ar"]),
             "duration": item["dt"], "lyric": item.get("lyric"),
             "picUrl": item.get("al", {}).get("picUrl")}
            for item in rst["result"]["songs"]]
        return musicList

    async def getMusicUrlInfo(self,ids: list):
        data = {'csrf_token': '', 'ids': ids, 'br': 999000}
        url = "http://music.163.com/weapi/song/enhance/player/url"
        data = encrypted_request(data)
        async with self.session.post(url,data=data,headers=headers,timeout=3) as response:
            if response.status == 200:
                text =  await response.text()
                rst = json.loads(text)
                if rst["code"] == 200:
                    return rst.get("data")
                else:
                    print(rst)
            else:
                return []