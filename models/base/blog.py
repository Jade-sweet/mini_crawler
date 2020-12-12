# -*- coding: utf-8 -*-
class Blog:

    def __init__(self, blogId, authority, commentCount, likeCount, relayCount, detail, releaseTime, storageTime, pics):
        self.blogId = blogId
        self.authority = authority
        self.commentCount = commentCount
        self.likeCount = likeCount
        self.relayCount = relayCount
        self.detail = detail
        self.releaseTime = releaseTime
        self.storageTime = storageTime
        self.pics = pics

    @staticmethod
    def keys():
        return ('blogId', 'authority', 'commentCount', 'likeCount', 'relayCount', 'detail', 'releaseTime', 'storageTime', 'pics')

    def __getitem__(self, item):
        return getattr(self, item)
