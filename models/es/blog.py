# -*- coding: utf-8 -*-

from elasticsearch_dsl import Document, Keyword, Text, Integer
from elasticsearch_dsl.connections import connections

from conf.elasticSearchSettings import ELASTICSEARCH_SERVER
from utils.elasticSearchHelper import executeCommand

connections.create_connection(hosts=[ELASTICSEARCH_SERVER[0]])


class SinaBlogType(Document):
    """
    新浪博文信息
    """
    blogId = Keyword()
    commentCount = Integer()
    likeCount = Integer()
    relayCount = Integer()
    detail = Text()
    releaseTime = Keyword()
    storageTime = Keyword()
    authority = Keyword()

    class Index:
        """
        表名sina_blog_info
        """
        name = 'sina_blog_info'
        settings = {
            "number_of_shards": 2,
        }

    @staticmethod
    def toSave(item):
        body = dict(item)
        executeCommand('sina_blog_info', '_doc', item.blogId, body)
