# -*- coding: utf-8 -*-
import scrapy

from download.scrapys.item.BaseItem import MyItem


class Blogger(MyItem):
    """博主字段"""
    uid = scrapy.Field()
    name = scrapy.Field()
    headPortrait = scrapy.Field()
    fansCount = scrapy.Field()
    attentionCount = scrapy.Field()
    postCount = scrapy.Field()
    introduction = scrapy.Field()
    storageTime = scrapy.Field()