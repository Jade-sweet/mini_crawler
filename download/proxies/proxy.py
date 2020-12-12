# -*- coding: utf-8 -*-
from conf import PROJECT_NAME
from conf.otherSettings import PROXY_FILE_PATH, PROXY_REDIS_NAME, PROXY_SOURCE
from utils.fileHelper import readFile, writeFile
from utils.redisHelper import returnDataLength, addListData


class Proxies:

    def __init__(self, minCount=8, value=None):
        self.sources = {
            'file': FileBasedStorage,
            'redis': RedisBasedStorage
        }
        self.Proxy = self.sources[PROXY_SOURCE]()  #
        self.value = value
        self.minCount = minCount

    def isEnough(self):
        """判断代理是否足够"""
        return self.Proxy.isEnough(self.minCount)

    @staticmethod
    def formatAsDict(proxy):
        return {'http': f'http://{proxy}'}

    def getProxies(self):
        """返回组合之后的代理"""
        proxies = self.formatAsDict(self.value)
        return proxies

    def add(self):
        """添加新的代理"""
        if self.value and isinstance(self.value, str):
            self.Proxy.add(self.value)
        else:
            raise ValueError('proxy object must have an initial value and the value type is string')


class FileBasedStorage:

    @staticmethod
    def isEnough(minCount: int):
        return True if len(readFile(rootName=PROJECT_NAME, fileList=PROXY_FILE_PATH)) >= minCount else False

    @staticmethod
    def add(value: str):
        content = readFile(rootName=PROJECT_NAME, fileList=PROXY_FILE_PATH).append(value)
        writeFile(rootName=PROJECT_NAME, fileList=PROXY_FILE_PATH, content=content)


class RedisBasedStorage:

    @staticmethod
    def isEnough(minCount: int):
        """检测redis列表中的代理数是否足够"""
        trueProxyCount = returnDataLength(PROXY_REDIS_NAME)
        return True if trueProxyCount >= minCount else False

    @staticmethod
    def add(value: str):
        """添加代理到redis列表中"""
        addListData(value, PROXY_REDIS_NAME)
