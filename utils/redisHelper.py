# -*- coding: utf-8 -*-
import json
import random
import redis

from conf.redisSettings import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD
from utils.decorator import connect2RedisTimeOut


def connect(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
    """
    连接redis数据库
    :return: 连接对象
    """
    redis_conn = redis.StrictRedis(host=host, port=port, password=password, socket_connect_timeout=10)
    return redis_conn


@connect2RedisTimeOut
def addListData(data, name):
    """添加数据到指定的表"""
    conn = connect()
    conn.rpush(name, data)
    conn.close()


@connect2RedisTimeOut
def setResult(name, value):
    """为一个字符添加数据"""
    conn = connect()
    conn.set(name, value)
    conn.close()


@connect2RedisTimeOut
def getRandomData(name):
    """从redis随机取回数据"""
    conn = connect()
    lens = conn.llen(name)
    if lens < 1:
        return None
    val = conn.lindex(name, random.randint(0, lens-1))
    conn.close()
    return val


@connect2RedisTimeOut
def returnDataLength(name):
    conn = connect()
    lens = conn.llen(name)
    conn.close()
    return lens


@connect2RedisTimeOut
def getResult(name):
    """从redis里面取回数据"""
    conn = connect()
    val = conn.get(name)
    conn.close()
    return val


@connect2RedisTimeOut
def clearAllData():
    """清除所有数据"""
    conn = connect()
    conn.flushall()
    conn.close()


@connect2RedisTimeOut
def blPopTask(name, timeout=60):
    """阻塞式获得列表数据"""
    while True:
        conn = connect()
        val = conn.blpop(name, timeout=timeout)
        if val:
            conn.close()
            return val
        else:
            continue


@connect2RedisTimeOut
def lPopAllData(name):
    """弹出所有列表数据"""
    conn = connect()
    dataList = []
    while True:
        val = conn.lpop(name)
        if not val:
            break
        dataList.extend(json.loads(val))
    conn.close()
    return dataList


@connect2RedisTimeOut
def incrData(name, num=1):
    """加操作，默认为1"""
    conn = connect()
    conn.incr(name, num)
    conn.close()
