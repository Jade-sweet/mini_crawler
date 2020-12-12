# -*- coding: utf-8 -*-
import datetime

from models.base.blog import Blog
from download.scrapys.item.blog import Blog as itemBlog
from utils.helper import regularMatch, timeFormat, getScrapyRequest, removeHtmlTags, removeJumbleChar


def dataToObject(data: str, authority):
    """原始数据转为对可用对象"""
    blogID, commentCount, likeCount, relayCount, detail, storageTime, releaseTime, pics, status = cleanAndGetData(data)
    if not status:
        authority = 1
    # 博文实例
    blog_ = Blog(
        commentCount=commentCount,
        likeCount=likeCount,
        relayCount=relayCount,
        detail=detail,
        blogId=blogID,
        authority=authority,
        releaseTime=releaseTime,
        storageTime=storageTime,
        pics=pics
    )
    return blog_


def cleanAndGetData(data):
    """数据清洗并得到有用数据"""
    blogID = regularMatch('"id": "(.*?)",', data)[-1]
    pics = regularMatch('"pic_ids": \[(.*?)]', data)
    pics = handlePics(pics)
    commentCount = regularMatch('"comments_count": (.*?),', data)
    likeCount = regularMatch('"attitudes_count": (.*?),', data)
    relayCount = regularMatch('"reposts_count": (.*?),', data)
    commentCount, likeCount, relayCount = getNumber(commentCount, likeCount, relayCount)
    detail = regularMatch('"text": (.*?)"source": .*?,', data)
    detail, status = cleanDetailData(detail)
    storageTime = str(datetime.datetime.now())[:-7]
    storageTime = timeFormat(storageTime, '%Y-%m-%d %H:%M:%S', to_format='%Y-%m-%dT%H:%M:%SZ')
    releaseTime = getReleaseTime(data)
    releaseTime = timeFormat(releaseTime, '%a %b %d %H:%M:%S +0800 %Y', to_format='%Y-%m-%dT%H:%M:%SZ')
    return blogID, commentCount, likeCount, relayCount, detail, storageTime, releaseTime, pics, status


def handlePics(data: list):
    if data:
        item = data[0]
        items = item.split(',')
        items = [i.strip('\n').strip().strip('\n').strip().strip('"') for i in items]
        items.remove('') if '' in items else items
        return items
    return data


def getNumber(*args):
    result = []
    for item in args:
         result.append(int(item[-1]) if item else 0)
    return result


def cleanDetailData(detail):
    """清洗博文详情字段的无关内容"""
    if detail:
        status = True
        detail = detail[0].split('"textLength"')
        text = removeHtmlTags(detail[0])
        detail = removeJumbleChar(text)
    else:
        status = False
        detail = '内容暂时无法查看'
    return detail, status


def validStatus(data: str):
    """判断该博文是否可查看"""
    if '<p class="h5-4con">由于作者隐私设置，你没有权限查看此微博</p>' not in data:
        return True


def getReleaseTime(data: str):
    """获取发布时间"""
    timed = regularMatch('"created_at": "(.*?)",', data)
    timed = timed[0] if timed else 'Wed Jun 03 13:29:16 +0800 2020'
    return timed


def objectBecomeScrapyItem(obj):
    if not obj:
        return None
    data = dict(obj)
    item = itemBlog(data)
    return item


def parseData2GetBlog(data, temporary):
    """微博详情"""
    # 判断该微博是否可以查看
    valid = validStatus(data)
    val = None
    if valid:
        blogObject = dataToObject(data, authority=0)
        if blogObject.authority == 1:
            # 表示没有该微博
            temporary.changeResult('not_found')
            return val
        else:
            return blogObject
    else:
        # 博文存在，但是不可见， 被限流
        temporary.changeResult('blocked')
    return val


def buildRequest(blogId, url, callBack, errBack):
    """
    返回请求
    :param blogId: 博文id
    :param url: 请求的url
    :param callBack: 成功回调函数
    :param errBack: 失败回调函数
    :return: 请求结构体
    """
    return getScrapyRequest(uid=blogId, url=url, method='GET', meta={'blogId': blogId}, callback=callBack, errBack=errBack)


def getSinceIDAndPostIDs(data, temporary):
    """获取博文id和since_id"""
    blogIDs = []
    if data['ok']:
        sinceID = data['data']['cardlistInfo']['since_id']  # 获取since_id
        # TODO 改变since_id
        temporary.changeSinceID(sinceID=sinceID)
        items = data['data']['cards']  # 装了博文数据的容器
        for item in items:  # 遍历取到的所有数据
            # if item['card_type'] == 9 and not item['mblog'].get('retweeted_status'):  # 这里抓取所有原创博文
            if item['card_type'] == 9:  # 这里抓取所有原创博文
                blog_ = item['mblog']['id']
                blogIDs.append(blog_)
    return blogIDs


def buildUrl(blogIDs):
    for blogID in blogIDs:
        yield f'https://m.weibo.cn/detail/{blogID}/'
