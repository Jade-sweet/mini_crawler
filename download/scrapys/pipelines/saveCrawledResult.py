# -*-coding:utf-8 -*-
from download.scrapys.item.blog import Blog
from download.scrapys.item.blogger import Blogger
from download.scrapys.item.image import Image
from models.mysql.blog import saveBlog
from models.mysql.blogger import saveBlogger
from models.mysql.image import saveImage
from models.es.blog import SinaBlogType
from models.es.blogger import SinaBloggerType
from models.es.image import SinaImgType


class Save2DB:
    """保存到指定的数据库中"""

    def __init__(self):
        self.objects = [Save2ElasticSearch(), Save2Mysql()]

    def process_item(self, item, spider):
        self.save(item=item)
        return item

    def save(self, item):
        if isinstance(item, Image):
            for obj in self.objects:
                obj.saveImage(item)  # 图片保存
        if isinstance(item, Blogger):
            for obj in self.objects:
                obj.saveUser(item)  # 用户保存
        if isinstance(item, Blog):
            for obj in self.objects:
                obj.saveBlog(item)  # 博文保存


class Save2Mysql:
    """保存到mysql"""

    @staticmethod
    def saveBlog(item):
        saveBlog(item)

    @staticmethod
    def saveUser(item):
        saveBlogger(item)

    @staticmethod
    def saveImage(item):
        saveImage(item)


class Save2ElasticSearch:
    """保存到es"""

    @staticmethod
    def saveBlog(item):
        SinaBlogType.toSave(item)

    @staticmethod
    def saveUser(item):
        SinaBloggerType.toSave(item)

    @staticmethod
    def saveImage(item):
        SinaImgType.toSave(item)
