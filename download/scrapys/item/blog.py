# -*- coding: utf-8 -*-
import scrapy

from download.scrapys.item.BaseItem import MyItem


class Blog(MyItem):
    """博文字段"""
    blogId = scrapy.Field()
    authority = scrapy.Field()
    commentCount = scrapy.Field()
    likeCount = scrapy.Field()
    relayCount = scrapy.Field()
    detail = scrapy.Field()
    releaseTime = scrapy.Field()
    storageTime = scrapy.Field()
