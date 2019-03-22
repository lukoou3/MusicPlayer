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