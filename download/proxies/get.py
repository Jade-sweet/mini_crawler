# -*- coding: utf-8 -*-
import random

from conf import PROJECT_NAME
from conf.otherSettings import PROXY_SOURCE, PROXY_FILE_PATH, PROXY_REDIS_NAME
from download.proxies import proxy
from utils.fileHelper import readFile
from utils.redisHelper import getRandomData


def Get():
    sources = {
        'file': getProxyFromFile,
        'redis': getProxyFromRedis
    }
    val = sources[PROXY_SOURCE]()
    proxy_ = proxy.Proxies(value=val)
    return proxy_


def getProxyFromFile():
    val = random.choice(readFile(rootName=PROJECT_NAME, fileList=PROXY_FILE_PATH))
    if not val:
        raise ValueError(f'待选proxy值不足1，请补充！')
    return val


def getProxyFromRedis():
    val = getRandomData(PROXY_REDIS_NAME)
    if not val:
        raise ValueError(f'待选proxy值不足1，请补充！')
    return val
