# -*- coding: utf-8 -*-
"""爬取微博主相关信息的Spider"""
import json
import scrapy

import dataClean.image.helper
from conf.otherSettings import SAVE2TASK_CENTER, SAVE2DATABASES
from download.spiders.errBack import errBack

from tasks.models.taskCenter.push import handleBaseObjects
from download.temporaryResult.result import Result
from tasks.taskCenter import parseTaskEnv
from utils.helper import regularMatch


class imageSpider(scrapy.Spider):
    """新浪微博爬虫"""
    name = 'imageSpider'
    allowed_domains = ['m.weibo.cn']

    custom_settings = {
        'DOWNLOAD_DELAY': 2
    }

    def __init__(self, *args, uid=None, startPage=1, endPage=None, taskEnv: str, **kwargs):
        super(imageSpider, self).__init__(*args, **kwargs)
        self.uid = uid
        self.startPage = int(startPage)
        self.endPage = int(endPage) if endPage and endPage != 'None' else self.startPage + 2
        self.beforeText = 107803
        # 创建对象
        self.taskEnv = parseTaskEnv(taskEnv)
        self.temporary = Result(taskJson=self.taskEnv)
        self.pushOnesBloggerTask = False  # 限制每次爬虫只会去推送一次博主任务

    def start_requests(self):
        """爬虫开始"""
        # 返回需要请求的url
        newUrl = dataClean.image.helper.buildUrl(uid=self.uid, startPage=self.startPage, endPage=self.endPage, beforeText=self.beforeText)
        # 开始请求数据
        while True:
            try:
                url = next(newUrl)
                yield dataClean.image.helper.buildRequest(blogId=self.uid, url=url, callBack=self.parse, errBack=self.errBack)
            except StopIteration:
                break

    def errBack(self, failure):
        """错误处理"""
        errBack(failure=failure, logger=self.logger, temporary=self.temporary)

    def parse(self, response):
        """图片"""
        page = regularMatch(r'page=(.*?)/', response.url)
        page = page[0] if page else 1
        # 修改page
        self.temporary.changePage(page)
        images = dataClean.image.helper.parseData2GetImages(json.loads(response.text), self.uid, self.temporary)
        if SAVE2TASK_CENTER:
            res = handleBaseObjects(images, 'image')  # 将取到的结果变成任务中心的提交的爬取结果的结构
            self.temporary.result['Data']['data']['pics'] = res  # 将任务装入上传的数据中
            self.temporary.push()  # 将数据传入外部, 这里在模拟外部追加
        if SAVE2DATABASES:
            for image_ in images:
                # 对象字典转为scrapy 中的item对象
                item = dataClean.image.helper.objectBecomeScrapyItem(image_)
                yield item
