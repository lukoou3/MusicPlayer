import asyncio
import aiohttp
import hashlib

def makeMd5(raw):
    """计算出一个字符串的MD5值"""
    md5 = hashlib.md5()
    md5.update(raw.encode())
    return md5.hexdigest()

def addToLoop(func):
    """将异步函数添加到事件循环中，返回future"""
    def addToTask(*args, **kwargs):
        eventLoop = asyncio.get_event_loop()
        future = eventLoop.create_task(func(*args, **kwargs))
        return future
    return addToTask

headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Accept-Encoding': 'gzip,deflate,sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'
    }

#全局变量session，一个应用一个session
session = {"session":None}#

@addToLoop
async def open_session():
    global session
    session["session"] = aiohttp.ClientSession()

@addToLoop
async def close_session():
    if session["session"]:
        await session["session"].close()
        #print("session close")

if __name__ == '__main__':
    async def test():
        length = 0
        async with aiohttp.ClientSession() as session:
            async with session.get("http://m10.music.126.net/20190324223917/0991994d69a07d9539b09e3563bf336d/ymusic/2f43/79c5/bd3c/7fe89e927098b086e99223a996189cba.mp3"
                                   ,headers=headers) as response:
                content = response.content
                print(response.content_length)
                print(response.content_type)
                while True:
                    chunk = await content.read(1024)
                    length = length + len(chunk)
                    if not chunk:
                        break
        print(length)



    loop = asyncio.get_event_loop()
    loop.run_until_complete(test())
    loop.close()