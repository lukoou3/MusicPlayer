from PyQt5.QtCore import QObject
from service import headers,session,encrypted_request
import json

class RecommendMusicDetailNetEaseService(QObject):
    def __init__(self):
        super().__init__()
        self.session = session["session"]

    async def getDetailMusicList(self,data):
        url = 'http://music.163.com/api/playlist/detail?id={0}'.format(data["id"])
        print(url)
        async with self.session.get(url,headers=headers,timeout=3) as response:
            if response.status == 200:
                text =  await response.text()
                result = json.loads(text).get("result")
            else:
                return []
        if not result:
            return
        musicList = [{"id":item["id"],"name":item["name"],"author":"，".join(artist["name"] for artist in item["artists"] ),
                      "duration": item["duration"], "lyric": item.get("lyric"),"picUrl":item.get("album",{}).get("blurPicUrl")}
                     for item in result["tracks"]]
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

    async def downloadMusic(self,url,progressBar):
        length = 0
        async with self.session.get(url,headers=headers) as response:
            content = response.content
            progressBar.setMaximum(response.content_length)
            print(response.content_length)
            print(response.content_type)
            while True:
                chunk = await content.read(1024*100)
                length = length + len(chunk)
                progressBar.setValue(length)
                if not chunk:
                    break

if __name__ == '__main__':
    import requests

    data = {'csrf_token': '', 'ids': [435289323], 'br': 999000}
    url = "http://music.163.com/weapi/song/enhance/player/url"
    data = encrypted_request(data)
    r = requests.post(url,data,headers=headers)
    print(r.text)

    myheaders = headers.copy()
    myheaders.update({"Origin":"http://music.ifkdy.com",
                      "Referer": "http://music.ifkdy.com",
                      "X-Requested-With":"XMLHttpRequest"})
    data = {"input":"http://music.163.com/#/song?id=435289323",
            "filter":"url","type":"_","page":1}
    r = requests.post("http://music.ifkdy.com/",data, headers=myheaders)
    rst = json.loads(r.text)
    print(rst)
    """
    r = requests.get(rst["data"][0]["url"],headers=headers)
    with open("text.mp3","wb") as f:
        f.write(r.content)
    print(r.content)
    """
