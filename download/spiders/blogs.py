# -*- coding: utf-8 -*-
"""爬取微博主相关信息的Spider"""
import json

import scrapy

import dataClean.blog.helpers
import dataClean.blog.helper
from conf.otherSettings import SAVE2TASK_CENTER, SAVE2DATABASES
from download.spiders.errBack import errBack

from tasks.models.taskCenter.push import handleBaseObjects
from download.temporaryResult.result import Result
from tasks.taskCenter import parseTaskEnv


class blogSpider(scrapy.Spider):
    """新浪微博爬虫"""
    name = 'blogSpider'
    allowed_domains = ['m.weibo.cn']

    custom_settings = {
        'DOWNLOAD_DELAY': 1
    }

    def __init__(self, *args, uid=None, sinceID=None, taskEnv=None, **kwargs):
        super(blogSpider, self).__init__(*args, **kwargs)
        self.uid = uid
        self.sinceID = sinceID
        self.url = f'https://m.weibo.cn/api/container/getIndex?type=uid&value={self.uid}&containerid=107603{self.uid}&since_id={self.sinceID}'
        # 创建对象
        self.taskEnv = parseTaskEnv(taskEnv)
        self.temporary = Result(taskJson=self.taskEnv)

    def start_requests(self):
        """爬虫开始， 获取指定用户的博文列表"""
        yield dataClean.blog.helper.buildRequest(blogId=self.uid, url=self.url, callBack=self.parse, errBack=self.errBack)

    def errBack(self, failure):
        """错误处理"""
        errBack(failure=failure, logger=self.logger, temporary=self.temporary)

    def parse(self, response):
        """解析出一组博文对象"""
        posts = dataClean.blog.helpers.getPosts(json.loads(response.text), self.temporary)
        if posts and SAVE2TASK_CENTER:
            if not posts:
                self.temporary.result['Result'] = 'ok'
            res = handleBaseObjects(posts, 'blog')  # 将取到的结果变成任务中心的提交的爬取结果的结构
            self.temporary.result['Data']['data']['posts'] = res  # 将任务装入上传的数据中
            self.temporary.push()  # 数据传出爬虫外部
        if posts and SAVE2DATABASES:
            for blog in posts:
                item = dataClean.blog.helper.objectBecomeScrapyItem(blog)
                yield item
