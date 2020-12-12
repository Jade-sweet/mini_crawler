# -*- coding: utf-8 -*-
import random

from conf import PROJECT_NAME
from conf.otherSettings import COOKIE_SOURCE, COOKIE_FILE_PATH, COOKIE_REDIS_NAME
from download.cookie import cookie
from utils.fileHelper import readFile
from utils.redisHelper import getRandomData


def Get():
    sources = {
        'file': getCookieFromFile,
        'redis': getCookieFromRedis
    }
    val = sources[COOKIE_SOURCE]()
    # 创建一个实例
    cookie_ = cookie.Cookie(value=val)
    return cookie_


def getCookieFromFile():
    val = random.choice(readFile(rootName=PROJECT_NAME, fileList=COOKIE_FILE_PATH))
    if not val:
        raise ValueError(f'待选cookie值不足1，请补充！')
    return val


def getCookieFromRedis():
    val = getRandomData(COOKIE_REDIS_NAME)
    if not val:
        raise ValueError(f'待选cookie值不足1，请补充！')
    return val
