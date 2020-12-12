# -*- coding: utf-8 -*-
from conf import PROJECT_NAME
from conf.otherSettings import COOKIE_SOURCE, COOKIE_FILE_PATH, COOKIE_REDIS_NAME
from utils.fileHelper import readFile, writeFile
from utils.redisHelper import addListData, returnDataLength


class Cookie:

    def __init__(self, minCount=8, value=None):
        self.sources = {
            'file': FileBasedStorage,
            'redis': RedisBasedStorage
        }
        self.cookie = self.sources[COOKIE_SOURCE]()  #
        self.value = value
        self.minCount = minCount

    def isEnough(self):
        """判断代理是否足够"""
        return self.cookie.isEnough(self.minCount)

    def add(self):
        """添加新的代理"""
        if self.value and isinstance(self.value, str):
            self.cookie.add(self.value)
        else:
            raise ValueError('proxy object must have an initial value and the value type is string')


class FileBasedStorage:

    @staticmethod
    def isEnough(minCount: int):
        return True if len(readFile(rootName=PROJECT_NAME, fileList=COOKIE_FILE_PATH)) >= minCount else False

    @staticmethod
    def add(value: str):
        content = readFile(rootName=PROJECT_NAME, fileList=COOKIE_FILE_PATH).append(value)
        writeFile(rootName=PROJECT_NAME, fileList=COOKIE_FILE_PATH, content=content)


class RedisBasedStorage:

    @staticmethod
    def isEnough(minCount: int):
        """检测redis列表中的代理数是否足够"""
        trueProxyCount = returnDataLength(COOKIE_REDIS_NAME)
        return True if trueProxyCount >= minCount else False

    @staticmethod
    def add(value: str):
        """添加代理到redis列表中"""
        addListData(value, COOKIE_REDIS_NAME)
