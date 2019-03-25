from PyQt5.QtCore import QObject
from service import headers,session,encrypted_request
import json

class SearchMusicService(QObject):
    pass

class SearchMusicNetEaseService(SearchMusicService):
    def __init__(self):
        super().__init__()
        self.session = session["session"]

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

    async def getMusicUrlInfo(self,id):
        data = {'csrf_token': '', 'ids': [id], 'br': 999000}
        url = "http://music.163.com/weapi/song/enhance/player/url"
        data = encrypted_request(data)
        async with self.session.post(url, data=data, headers=headers, timeout=3) as response:
            if response.status == 200:
                text = await response.text()
                rst = json.loads(text)
                if rst["code"] == 200:
                    return rst.get("data")[0]["url"]
                else:
                    print(rst)
            else:
                return None

class SearchMusicQQService(SearchMusicService):
    def __init__(self):
        super().__init__()
        self.session = session["session_qq"]
        self.guid = 3768717388
        # self.guid = 5150825362

    async def search(self, text):
        url = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp?ct=24&qqmusic_ver=1298&' + \
              'new_json=1&remoteplace=txt.yqq.center&searchid=43541888870417375&t=0&aggr=1' + \
              '&cr=1&catZhida=1&lossless=0&flag_qc=0&p=1&n=50&' + \
              'w={0}'.format(text) + \
              '&g_tk=5381&jsonpCallback=searchCallbacksong6064&loginUin=0&hostUin=0&' + \
              'format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0'
        try:
            async with self.session.post(url,headers=headers,timeout=3) as response:
                if response.status == 200:
                    text =  await response.text()
                    result = json.loads(text[len('searchCallbacksong6064('):-1])
                else:
                    return []
        except:
            return []
        musicList = [
            {"id": item["mid"], "name": item["name"], "author": "，".join(artist["name"] for artist in item["singer"]),
             "duration": item["interval"] * 1000, "lyric": item.get("lyric"),
             "picUrl": 'https://y.gtimg.cn/music/photo_new/T002R300x300M000{0}.jpg'.format(item['album']['mid'])}
            for item in result['data']['song']['list']]
        return musicList

    async def getMusicUrlInfo(self,id):
        vkey = await self._getSongUrlVkey(id)
        if not vkey:
            vkey = '000'
        sip = 'http://dl.stream.qqmusic.qq.com/'
        return '{0}M500{1}.mp3?vkey={2}&guid={3}&fromtag=1'.format(sip, id, vkey, self.guid)
        #return '{0}C400{1}.m4a?vkey={2}&guid={3}&uin=0&fromtag=66'.format(sip, id, vkey,self.guid)

    async def _getSongUrlVkey(self, mid):
        # 获取得到QQ音乐歌曲地址所需的vkey。
        # 返回的是vkey。
        vkey_url = 'https://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg'
        params = {
            'g_tk': '5381',
            'jsonpCallback': 'MusicJsonCallback8571665793949388',
            'loginUin': '0',
            'hostUin': '0',
            'format': 'json',
            'inCharset': 'utf8',
            'outCharset': 'utf-8',
            'notice': '0',
            'platform': 'yqq',
            'needNewCode': '0',
            'cid': '205361747',
            'callback': 'MusicJsonCallback8571665793949388',
            'uin': '0',
            'songmid': mid,
            #'filename': 'C400' + mid + '.m4a',
            'filename': 'M500' + mid + '.mp3',
            'guid': '{}'.format(self.guid)
        }
        myheaders = headers.copy()
        myheaders.update({"Host": "c.y.qq.com", "Referer": "https://y.qq.com/portal/playlist.html"})

        async with self.session.get(vkey_url,params=params,headers=myheaders,timeout=3) as response:
            if response.status == 200:
                text =  await response.text()
                result = json.loads(text[text.find("{"):-1])
            else:
                return []
        return  result['data']['items'][0]['vkey']