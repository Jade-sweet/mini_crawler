# -*- coding: utf-8 -*-
import json
import re
import time
from urllib import parse

import requests
import scrapy
from datetime import datetime
import download.cookie.get
import download.proxies.get

from fake_useragent import UserAgent

from conf.taskSettings import CONTENT_TYPE, CONTENT_ENCODING, USER_AGENT
from utils.decorator import checkNetwork


def regularMatch(role, data):
    """
    给定规则和原始数据，返回匹配数据
    :param role: 规则
    :param data: 原始数据
    :return: 匹配数据
    """
    par = re.compile(role, re.S)
    return re.findall(par, data)


def getHeader(cookie, uid):
    headers = {
        'cookie': cookie.value,
        'user-agent': UserAgent(verify_ssl=False).random,
        'referer': f'https://m.weibo.cn/u/{uid}'
    }
    return headers


def getScrapyRequest(uid, url, method, meta: dict, callback, errBack):
    """
    构建请求函数体，返回该请求结构体
    :param uid: 博主的唯一标识，用于构建header中的referer
    :param url: 请求的地址
    :param method: 请求的方法
    :param meta: 请求的meta
    :param callback: 成功回调函数
    :param errBack: 失败回调函数
    :return: 请求函数体
    """
    cookie = download.cookie.get.Get()
    proxy = download.proxies.get.Get()
    headers = getHeader(cookie=cookie, uid=uid)
    meta.update({'proxies': proxy.getProxies()})
    return scrapy.Request(url=url, headers=headers, method=method, callback=callback, meta=meta, errback=errBack)


def timeFormat(time_string, from_format, to_format='%Y-%m-%d %H:%M:%S', defaultTime='1900-01-01 00:00:00'):
    """
    @note 时间格式转化
    :param time_string: 原数据
    :param from_format: old数据格式
    :param to_format: new数据格式
    :param defaultTime: 默认解析错误返回的时间
    :return:
    """
    times = defaultTime
    try:
        time_struct = time.strptime(time_string, from_format)
        times = time.strftime(to_format, time_struct)
    except ValueError:
        pass
    finally:
        return times


def timeDifference(start_time, end_time, date_format):
    """
    返回两个时间之间的时间差
    :param start_time: spider start time
    :param end_time: spider end time
    :param date_format: time format
    :return: time diff
    """
    val = 0
    try:
        date1 = datetime.strptime(start_time, date_format)
        date2 = datetime.strptime(end_time, date_format)
        val = (date2-date1).seconds
    except ValueError:
        pass
    finally:
        return val


def removeJumbleChar(data: str):
    """去除正文内容两端杂乱字符，保留正文"""
    if isinstance(data, str):
        data = data.strip().strip(',').strip('"').strip()
        data = re.sub(r'\s+', '', data)
    return data


def removeHtmlTags(data: str):
    """去除html标签，保留文字"""
    par = re.compile(r'<[^>]+>', re.S)
    return par.sub('', data).rstrip('')


def getNewProxy():
    """向三方代理请求代理"""
    url = "http://api.wandoudl.com/api/ip?app_key=a9ba52aa5db36e05fbb595bbccf1bd60&pack=0&num=1&xy=1&type=1&lb=\r\n&mr=1&"
    headers = {
        "User-Agent": UserAgent(verify_ssl=False).random
    }
    response = requests.get(url=url, headers=headers)
    if response.status_code == 200:
        return response.text
    return '0.0.0.0'


def extendList(args: tuple):
    List = []
    for item in args:
        List.extend(item)
    return List


@checkNetwork
def sendRequest(url, limit=None, crawler=None, data=None):
    """发起请求，获取数据"""
    header = {
        "Content-Type": CONTENT_TYPE,
        # "Content-Encoding": CONTENT_ENCODING,
        "User-Agent": USER_AGENT,
    }
    data_ = {"black_task": "", "limit": limit, "crawler": crawler, "data": data}
    data_ = parse.urlencode(data_)
    response = requests.post(url=url, data=data_, headers=header)
    if response.status_code == 200:
        print("success", response.content.decode('utf-8'))
        return response.content
    else:
        print("error")
        return None


def handleTime(oldTime):
    """
    将以下时间转为指定格式  --> xxx-xx-xxTxx:xx:xxZ
    刚刚
    xx分钟前
    xx小时前
    昨天 13:16
    07-29
    2019-12-01
    """
    if '刚刚' in oldTime:
        nowTimeStamp = int(time.time())
        timeArray = time.localtime(nowTimeStamp)
        newTime = time.strftime("%Y-%m-%dT%H:%M:%SZ", timeArray)
    elif '分钟前' in oldTime:
        minute = int(regularMatch('(.*?)分钟前', oldTime)[-1])
        nowTimeStamp = int(time.time()) - minute * 60
        timeArray = time.localtime(nowTimeStamp)
        newTime = time.strftime("%Y-%m-%dT%H:%M:%SZ", timeArray)
    elif '小时前' in oldTime:
        hour = int(regularMatch('(.*?)小时前', oldTime)[0])
        nowTimeStamp = int(time.time()) - hour * 60 * 60
        timeArray = time.localtime(nowTimeStamp)
        newTime = time.strftime("%Y-%m-%dT%H:%M:%SZ", timeArray)
    elif '昨天' in oldTime:
        hour, minute = regularMatch('昨天 (.*)', oldTime)[-1].split(':')
        nowTimeStamp = int(time.time()) - 24 * 60 * 60
        timeArray = time.localtime(nowTimeStamp)
        newTime = time.strftime("%Y-%m-%d", timeArray)
        newTime = newTime + f'T{hour}:{minute}:00Z'
    elif len(oldTime) == 5:  # 07-12
        month, day = oldTime.split('-')
        year = datetime.now().year
        newTime = f'{year}-{month}-{day}T00:00:00Z'
    else:
        year, month, day = oldTime.split('-')
        newTime = f'{year}-{month}-{day}T00:00:00Z'
    return newTime
