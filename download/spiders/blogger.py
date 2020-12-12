# -*- coding: utf-8 -*-
"""爬取微博主相关信息的Spider"""
import scrapy

import dataClean.blogger.helper
from conf.otherSettings import SAVE2TASK_CENTER, SAVE2DATABASES
from download.spiders.errBack import errBack

from tasks.models.taskCenter.push import handleBaseObjects
from download.temporaryResult.result import Result
from tasks.taskCenter import parseTaskEnv


class SinaSpiderSpider(scrapy.Spider):
    """新浪微博爬虫"""
    name = 'bloggerSpider'
    allowed_domains = ['m.weibo.cn']

    custom_settings = {
        'DOWNLOAD_DELAY': 1.5
    }

    def __init__(self, *args, uid=None, taskEnv=None, **kwargs):
        super(SinaSpiderSpider, self).__init__(*args, **kwargs)
        self.uid = uid
        self.url = f'https://m.weibo.cn/api/container/getIndex?type=uid&value={self.uid}&/'
        # 创建对象
        self.taskEnv = parseTaskEnv(taskEnv)
        self.temporary = Result(taskJson=self.taskEnv)

    def start_requests(self):
        """爬虫开始"""
        yield dataClean.blogger.helper.buildRequest(uid=self.uid, url=self.url, callBack=self.parse, errBack=self.errBack)

    def errBack(self, failure):
        """错误处理"""
        errBack(failure=failure, logger=self.logger, temporary=self.temporary)

    def parse(self, response):
        """主页"""
        # 返回博主信息item
        user = dataClean.blogger.helper.parseData2GetUser(response.text, self.uid, self.temporary)
        if user and SAVE2TASK_CENTER:
            self.temporary.result['Result'] = 'ok'
            res = handleBaseObjects([user], 'blogger')  # 将取到的结果变成任务中心的提交的爬取结果的结构
            self.temporary.result['Data']['data']['profiles'] = res  # 将任务装入上传的数据中
            self.temporary.push()  # 将数据传入外部, 这里在模拟外部追加
        if user and SAVE2DATABASES:
            yield dataClean.blogger.helper.objectBecomeScrapyItem(user)
