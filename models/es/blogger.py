# -*- coding: utf-8 -*-

from elasticsearch_dsl import Document, Keyword, Text, Integer
from elasticsearch_dsl.connections import connections

from conf.elasticSearchSettings import ELASTICSEARCH_SERVER
from utils.elasticSearchHelper import executeCommand

connections.create_connection(hosts=[ELASTICSEARCH_SERVER[0]])


class SinaBloggerType(Document):
    """
    新浪博主信息
    """
    uid = Keyword()
    name = Text()
    headPortrait = Keyword()
    introduction = Text()
    fansCount = Integer()
    attentionCount = Integer()
    postCount = Integer()
    storageTime = Keyword()

    class Index:
        """
        表名sina_blogger_info
        """
        name = 'sina_blogger_info'
        settings = {
            "number_of_shards": 2,
        }

    @staticmethod
    def toSave(item):
        body = dict(item)
        executeCommand('sina_blogger_info', '_doc', item.uid, body)
