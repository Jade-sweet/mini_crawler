# -*- coding: utf-8 -*-
import json
from datetime import datetime

from models.base.blogger import Blogger
from download.scrapys.item.blogger import Blogger as itemBlogger
from utils.decorator import raiseKeyError
from utils.helper import getScrapyRequest, timeFormat


@raiseKeyError
def parseDataReturnObject(data: json, uid: str, storageTime: str):
    """提取博主有关数据"""
    u_data = data['data']['userInfo']
    name = u_data['screen_name'] if u_data['screen_name'] else '@_博主昵称未知_@'
    headPortrait = u_data['profile_image_url']
    fansCount = u_data['followers_count']
    attentionCount = u_data['follow_count']
    postCount = u_data['statuses_count']
    introduction = u_data['description'] if u_data['description'] else '@_博主简介未知_@'
    # 博主实例
    blogger_ = Blogger(
        name=name,
        headPortrait=headPortrait,
        fansCount=fansCount,
        attentionCount=attentionCount,
        postCount=postCount,
        introduction=introduction,
        uid=uid,
        storageTime=timeFormat(storageTime, '%Y-%m-%d %H:%M:%S', to_format='%Y-%m-%dT%H:%M:%SZ')
    )
    return blogger_


def checkForUsefulInformation(data, temporary):
    status, result = toJson(data)
    if status:
        status, result = haveUsefulData(result, temporary)
    return status, result


def toJson(data):
    try:
        html = json.loads(data)
        return True, html
    except (TypeError, json.decoder.JSONDecodeError):
        return False, None


def haveUsefulData(data, temporary):
    try:
        if not data['ok'] and data['msg'] == '这里还没有内容':
            # 表示这个id不存在
            temporary.changeResult('not_found')
            return False, None
        else:
            return True, data
    except (KeyError, TypeError):
        return False, None


def parseData2GetUser(data, uid, temporary):
    """返回博主数据字典"""
    status, result = checkForUsefulInformation(data, temporary)
    if status:
        # 提取数据
        storageTime = str(datetime.now())[:-7]
        bloggerObject = parseDataReturnObject(result, uid, storageTime)
        result = bloggerObject
    return result


def buildRequest(uid, url, callBack, errBack):
    """
    返回博主信息请求
    :param uid: 博主id
    :param url: 请求的url
    :param callBack: 成功回调函数
    :param errBack: 失败回调函数
    :return: 请求结构体
    """
    return getScrapyRequest(uid=uid, url=url, method='GET', meta={'blogger_id': uid}, callback=callBack, errBack=errBack)


def objectBecomeScrapyItem(obj):
    if obj:
        dictData = dict(obj)
        item = itemBlogger(dictData)
    else:
        item = None
    return item
