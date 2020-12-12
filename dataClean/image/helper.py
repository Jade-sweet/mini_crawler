# -*- coding: utf-8 -*-
import datetime

import tasks.enqueue
from download.scrapys.item.image import Image as itemImage
from models.base.image import Image

from utils.decorator import raiseKeyError
from utils.helper import getScrapyRequest, timeFormat


def objectBecomeScrapyItem(obj):
    data = dict(obj)
    item = itemImage(data)
    return item


@raiseKeyError
def parseData2GetImages(json_data, uid, temporary):
    """
    提取图片数据相关字段列表并返回
    :param json_data: 原始的json数据
    :param uid: 此次爬取的博主id
    :param temporary 临时对象
    :return: 图片数据相关字段列表
    """
    images = []
    data = json_data['data']['cards']
    counts = len(data)
    if not counts:
        # 证明这里已经没有数据，那么从开始页到这里就已经爬取完了，修改fully的值为True
        temporary.changeResult('ok')
        temporary.changeFully(True)
        return images

    for idx in range(counts):
        row = len(data[idx]['pics'])
        for i in range(row):
            # 图片的id号
            image_id = data[idx]['pics'][i]['pic_id']
            # 处理id号
            image_id = image_id.strip('"')
            imageUrl = 'https://wx1.sinaimg.cn/wap720/%s.jpg' % image_id
            # 对应的单条微博id
            blogId = data[idx]['pics'][i]['mblog']['mid']
            # 图片实例
            image_ = Image(
                imageId=image_id,
                imageUrl=imageUrl,
                userId=uid,
                blogId=blogId,
                storageTime=timeFormat(str(datetime.datetime.now())[:-7], '%Y-%m-%d %H:%M:%S', to_format='%Y-%m-%dT%H:%M:%SZ')
            )
            images.append(image_)
    return images


def buildUrl(uid, startPage: int, endPage: int, beforeText):
    for page in range(startPage, endPage + 1):
        yield f'https://m.weibo.cn/api/container/getSecond?containerid={beforeText}{uid}_-_photoall&count=24&page={page}/'


def buildRequest(blogId, url, callBack, errBack):
    """
    返回请求
    :param blogId: 博文id
    :param url: 请求的url
    :param callBack: 成功回调函数
    :param errBack: 失败回调函数
    :return: 请求结构体
    """
    return getScrapyRequest(uid=blogId, url=url, method='GET', meta={}, callback=callBack, errBack=errBack)


def addTaskToTaskQueue(blogs, users):
    """保存新的任务"""
    tasks.enqueue.normal(blogs, 'blogSpiderTask')
    tasks.enqueue.normal(users, 'bloggerSpiderTask')
