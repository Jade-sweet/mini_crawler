# -*- coding: utf-8 -*-
from utils.mysqlHelper import executeSelectCommand, executeCUDCommand
from models.base.image import Image as BaseImage


class Image(BaseImage):

    def __init__(self, **kwargs):
        super(Image, self).__init__(**kwargs)

    def isExists(self):
        sql = 'select imageId from img_info where imageId=%s and blogId=%s'
        val = executeSelectCommand(sql, (self.imageId, self.blogId))
        return True if val else False

    def saveNewItem(self):
        sql = 'insert into img_info(imageId, userId, blogId, storageTime, imageUrl) values (%s, %s, %s, %s, %s)'
        val = (self.imageId, self.userId, self.blogId, self.storageTime, self.imageUrl)
        executeCUDCommand(sql, val)

    def updateItem(self):
        sql = 'update img_info set storageTime=%s where imageId=%s'
        val = (self.storageTime, self.imageId)
        executeCUDCommand(sql, val)


def saveImage(item: Image):
    """将item转为mysql模型后进行保存"""
    imageId, userId, blogId, storageTime, imageUrl = item.imageId, item.userId, item.blogId, item.storageTime, item.imageUrl
    mysqlImage = Image(imageId=imageId, userId=userId, blogId=blogId,  storageTime=storageTime, imageUrl=imageUrl)
    if not mysqlImage.isExists():
        mysqlImage.saveNewItem()
    else:
        mysqlImage.updateItem()
