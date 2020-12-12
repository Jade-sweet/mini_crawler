# -*- coding: utf-8 -*-
import datetime
import random
import time

from download.spiders.blog import SingleBlogSpider
from models.base.blog import Blog
from utils.helper import timeFormat, handleTime


def getPosts(data, temporary):
    """获取博文对象"""
    blogs = []
    if data['ok']:
        sinceID = str(data['data']['cardlistInfo']['since_id'])  # 获取since_id
        temporary.changeSinceID(sinceID=sinceID)  # 改变since_id
        items = data['data']['cards']  # 装了博文数据的容器
        for item in items:  # 遍历取到的所有数据
            if item['card_type'] == 9:
                # 处理博文
                blog_ = parseData2GetObject(item['mblog'], temporary)
                blogs.append(blog_)
    return blogs


def parseData2GetObject(item, temporary):
    """解析出单个博文详情"""
    commentCount = item['comments_count']
    likeCount = item['attitudes_count']
    relayCount = item['reposts_count']
    releaseTime = item['created_at']
    # 将时间转为标准格式
    releaseTime = handleTime(releaseTime)
    blogID = item['id']
    authority = 0
    storageTime = timeFormat(str(datetime.datetime.now())[:-7], '%Y-%m-%d %H:%M:%S', to_format='%Y-%m-%dT%H:%M:%SZ')
    if item.get('pics'):
        pics = [pic['pid'] for pic in item['pics']]
    else:
        pics = []
    if item['isLongText']:
        time.sleep(random.randint(3, 6))  # 随机延迟
        detail = SingleBlogSpider(blogID, temporary).getLongWeibo()   # 此API无法显示全文，另外一个爬虫去爬取详情
    else:
        detail = item['raw_text']
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
