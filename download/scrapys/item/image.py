# -*- coding: utf-8 -*-
import scrapy

from download.scrapys.item.BaseItem import MyItem


class Image(MyItem):
    """图片字段"""
    imageId = scrapy.Field()
    imageUrl = scrapy.Field()
    blogId = scrapy.Field()
    userId = scrapy.Field()
    storageTime = scrapy.Field()
