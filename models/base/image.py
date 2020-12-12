# -*- coding: utf-8 -*-
class Image:

    def __init__(self, imageId, imageUrl, userId, blogId, storageTime):
        self.imageId = imageId
        self.imageUrl = imageUrl
        self.userId = userId
        self.blogId = blogId
        self.storageTime = storageTime

    @staticmethod
    def keys():
        return ('imageId', 'imageUrl','userId', 'blogId', 'storageTime')

    def __getitem__(self, item):
        return getattr(self, item)
