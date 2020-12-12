# -*- coding: utf-8 -*-

from elasticsearch_dsl import Document, Keyword
from elasticsearch_dsl.connections import connections
from conf.elasticSearchSettings import ELASTICSEARCH_SERVER
from utils.elasticSearchHelper import executeCommand

connections.create_connection(hosts=[ELASTICSEARCH_SERVER[0]])


class SinaImgType(Document):
    """
    新浪博主图片信息
    """
    imageId = Keyword()
    imageUrl = Keyword()
    userId = Keyword()
    blogId = Keyword()
    storageTime = Keyword()

    class Index:
        """
        表名sina_img_info
        """
        name = 'sina_img_info'
        settings = {
            "number_of_shards": 2,
        }

    @staticmethod
    def toSave(item):
        body = dict(item)
        executeCommand('sina_img_info', '_doc', item.imageId, body)