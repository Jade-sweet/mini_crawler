# -*- coding: utf-8 -*-

from functools import wraps
from threading import RLock

import elasticsearch
import pymysql
import redis
import requests


def checkNetwork(func):
    """检查网络的装饰器，用于监听网络状态"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            val = func(*args, **kwargs)
            return val
        except requests.exceptions.ConnectionError:
            print('Network is crash! Try again later')
            return ''
    return wrapper


def fileSuccessOpen(func):
    """检查文件是否存在"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            val = func(*args, **kwargs)
            return val
        except (FileNotFoundError, UnicodeDecodeError, LookupError, IOError):
            raise
    return wrapper


def raiseKeyError(func):
    """检查键错误"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            val = func(*args, **kwargs)
            return val
        except KeyError:
            raise KeyError('非法获取，请检查键的拼写正确性')
    return wrapper


def validDatabase(func):
    """检查数据库层面问题"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            val = func(*args, **kwargs)
            return val
        except (pymysql.err.ProgrammingError, pymysql.err.InternalError):
            return
    return wrapper


def connect2MysqlTimeOut(func):
    """检查数据库连接问题"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            val = func(*args, **kwargs)
            return val
        except pymysql.err.OperationalError:
            return
    return wrapper


def connect2RedisTimeOut(func):
    """检查数据库连接问题"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            val = func(*args, **kwargs)
            return val
        except redis.exceptions.TimeoutError:
            return
    return wrapper


def esNotFoundError(func):
    """检查es运行问题"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            val = func(*args, **kwargs)
            return val
        except elasticsearch.exceptions.NotFoundError:
            return
    return wrapper


# 单例装饰器
def singleton(cls):
    instance = {}
    lock = RLock()

    @wraps(cls)
    def wrapper(*args, **kwargs):
        if cls not in instance:
            with lock:
                if cls not in instance:
                    instance[cls] = cls(*args, **kwargs)
        return instance[cls]
    return wrapper
