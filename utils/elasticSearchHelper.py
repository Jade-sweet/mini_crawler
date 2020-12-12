# -*- coding: utf-8 -*-

from elasticsearch import Elasticsearch

from utils.decorator import esNotFoundError
from conf.elasticSearchSettings import ELASTICSEARCH_SERVER


@esNotFoundError
def delById(index, ids, hosts=ELASTICSEARCH_SERVER):
    """
    根据失败的详情博客id删除对应的图片信息
    :param index: 请求失败的博文index
    :param ids: 请求失败的博文id
    :param hosts: :param hosts: es主机地址
    :return:
    """
    es = Elasticsearch(hosts=hosts)
    query = {'query': {'match': {'_id': ids}}}
    es.delete_by_query(index=index, doc_type='_doc', body=query)


@esNotFoundError
def delAllFields(index, hosts=ELASTICSEARCH_SERVER):
    """删除指定index的所有数据"""
    es = Elasticsearch(hosts=hosts)
    query = {'query': {'match_all': {}}}
    es.delete_by_query(index=index, doc_type='_doc', body=query)


@esNotFoundError
def delIndex(index, hosts=ELASTICSEARCH_SERVER):
    """删除指定的index"""
    es = Elasticsearch(hosts=hosts)
    es.indices.delete(index)


@esNotFoundError
def executeCommand(index, doc_type, m_id, body: dict, hosts=ELASTICSEARCH_SERVER):
    """
    保存到es中
    :param index: 索引名
    :param doc_type: 文档
    :param m_id: 指定id
    :param body: 信息主体
    :param hosts: es主机地址
    :return:
    """
    es = Elasticsearch(hosts=hosts)
    es.index(index=index, doc_type=doc_type, id=m_id, body=body)
