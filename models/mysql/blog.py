# -*- coding: utf-8 -*-
from utils.mysqlHelper import executeSelectCommand, executeCUDCommand
from models.base.blog import Blog as BaseBlog


class Blog(BaseBlog):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

    def isExists(self):
        sql = 'select blogId from blog_info where BlogId=%s'
        val = executeSelectCommand(sql, (self.blogId,))
        return True if val else False

    def saveNewItem(self):
        sql = 'insert into blog_info(blogId, authority, commentCount, likeCount, relayCount, detail, releaseTime, storageTime) values (%s, %s, %s, %s, %s, %s, %s, %s)'
        val = (self.blogId, self.authority, self.commentCount, self.likeCount, self.relayCount, self.detail, self.releaseTime, self.storageTime)
        executeCUDCommand(sql, val)

    def updateItem(self):
        sql = 'update blog_info set commentCount=%s, likeCount=%s, relayCount=%s, storageTime=%s where blogId=%s'
        val = (self.commentCount, self.likeCount, self.relayCount, self.storageTime, self.blogId)
        executeCUDCommand(sql, val)


def saveBlog(item: Blog):
    """将item转为mysql模型后进行保存"""
    # 提取字段
    blogId, authority, commentCount, likeCount, relayCount, detail, releaseTime, storageTime = item.blogId, item.authority, item.commentCount, item.likeCount, item.relayCount, item.detail, item.releaseTime, item.storageTime
    mysqlBlog = Blog(blogId=blogId, authority=authority, commentCount=commentCount,
                     likeCount=likeCount, relayCount=relayCount, detail=detail,
                     releaseTime=releaseTime, storageTime=storageTime, pics=[])
    if not mysqlBlog.isExists():
        mysqlBlog.saveNewItem()
    else:
        mysqlBlog.updateItem()
