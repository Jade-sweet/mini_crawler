# -*- coding: utf-8 -*-
from utils.mysqlHelper import executeSelectCommand, executeCUDCommand
from models.base.blogger import Blogger as BaseBlogger


class Blogger(BaseBlogger):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def isExists(self):
        sql = 'select uid from blogger_info where uid=%s'
        val = executeSelectCommand(sql, (self.uid,))
        return True if val else False

    def saveNewItem(self):
        sql = 'insert into blogger_info(uid, name, headPortrait, fansCount, attentionCount, postCount, introduction, storageTime) values (%s, %s, %s, %s, %s, %s, %s, %s)'
        val = (self.uid, self.name, self.headPortrait, self.fansCount, self.attentionCount, self.postCount, self.introduction, self.storageTime)
        # 执行命令
        executeCUDCommand(sql, val)

    def updateItem(self):
        sql = 'update blogger_info set name=%s, headPortrait=%s, fansCount=%s, attentionCount=%s, postCount=%s, introduction=%s, storageTime=%s where uid=%s'
        val = (self.name, self.headPortrait, self.fansCount, self.attentionCount, self.postCount, self.introduction, self.storageTime, self.uid)
        executeCUDCommand(sql, val)


def saveBlogger(item: Blogger):
    """将item转为mysql模型后进行保存"""
    # 提取相关字段
    uid, name, headPortrait, fansCount, attentionCount, postCount, introduction, storageTime = item.uid, item.name, item.headPortrait, item.fansCount, item.attentionCount, item.postCount, item.introduction, item.storageTime
    mqlBlogger = Blogger(uid=uid, name=name, headPortrait=headPortrait, fansCount=fansCount,
                         attentionCount=attentionCount, postCount=postCount,
                         introduction=introduction, storageTime=storageTime)
    if not mqlBlogger.isExists():
        mqlBlogger.saveNewItem()
    else:
        mqlBlogger.updateItem()
