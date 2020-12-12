# -*- coding: utf-8 -*-
"""爬取单个博文信息的Spider"""
from urllib import request

import dataClean.blog.helper
import download.cookie.get
import download.proxies.get
from download.scrapys.pipelines.saveCrawledResult import Save2DB
from tasks.models.taskCenter.push import handleBaseObjects

from utils.helper import getHeader, timeFormat, regularMatch


class SingleBlogSpider:

    def __init__(self, blogID, temporary):
        self.blogID = blogID
        self.temporary = temporary
        self.url = f'https://m.weibo.cn/detail/{self.blogID}/'

    def getOriginalData(self):
        """获取源数据"""
        cookie = download.cookie.get.Get()
        headers = getHeader(cookie=cookie, uid=self.blogID)
        proxy = download.proxies.get.Get()
        proxy_handler = request.ProxyHandler(proxy.getProxies())
        opener = request.build_opener(proxy_handler)
        request.install_opener(opener)
        res = request.Request(url=self.url, headers=headers)
        response = request.urlopen(res)
        if response.status == 200:
            return response.read().decode('utf-8')
        else:
            self.temporary.changeResult(status='failed')
            return None

    def getTweetedTime(self):
        """获取发布时间"""
        response = self.getOriginalData()
        tweetedTime = dataClean.blog.helper.getReleaseTime(response)
        tweetedTime = timeFormat(tweetedTime, '%a %b %d %H:%M:%S +0800 %Y', to_format='%Y-%m-%dT%H:%M:%SZ')
        return tweetedTime

    def getLongWeibo(self):
        """获取长博文"""
        response = self.getOriginalData()
        detail = regularMatch('"text": (.*?)"source": .*?,', response)
        detail, status = dataClean.blog.helper.cleanDetailData(detail)
        if status:
            print('解析成功')
        else:
            print('解析失败')
        return detail if status else '解析失败'

    def getBlogObject(self):
        response = self.getOriginalData()
        blog_ = dataClean.blog.helper.parseData2GetBlog(data=response, temporary=self.temporary)
        return blog_

    def save2Databases(self):
        """保存到数据库"""
        blog_ = self.getBlogObject()
        item = dataClean.blog.helper.objectBecomeScrapyItem(blog_)
        Save2DB().save(item=item)

    def save2taskCenter(self):
        """保存到任务中心"""
        posts = self.getBlogObject()
        if not posts:
            self.temporary.result['Result'] = 'ok'
        res = handleBaseObjects([posts], 'blog')  # 将取到的结果变成任务中心的提交的爬取结果的结构
        self.temporary.result['Data']['data']['posts'] = res  # 将任务装入上传的数据中
        print(self.temporary.result)
        self.temporary.push()  # 数据传出爬虫外部
