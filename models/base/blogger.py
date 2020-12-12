# -*- coding: utf-8 -*-
class Blogger:

    def __init__(self, uid, name, headPortrait, fansCount, attentionCount, postCount, introduction, storageTime):
        self.uid = uid
        self.name = name
        self.headPortrait = headPortrait
        self.fansCount = fansCount
        self.attentionCount = attentionCount
        self.postCount = postCount
        self.introduction = introduction
        self.storageTime = storageTime

    @staticmethod
    def keys():
        return ('uid', 'name', 'headPortrait', 'fansCount', 'attentionCount', 'postCount', 'introduction', 'storageTime')

    def __getitem__(self, item):
        return getattr(self, item)
