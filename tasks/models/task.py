# -*- coding: utf-8 -*-


class Task:

    def __init__(self, taskType: str, data):
        self.taskType = taskType
        self.data = data


class PicTask:

    def __init__(self, uid, startPage, endPage, taskEnv: dict):
        self.uid = uid
        self.startPage = startPage
        self.endPage = endPage
        self.taskEnv = taskEnv


class PostTask:

    def __init__(self, uid, taskEnv: dict, sinceID):
        self.uid = uid
        self.taskEnv = taskEnv
        self.sinceID = sinceID


class ProfileTask:

    def __init__(self, uid, taskEnv: dict):
        self.uid = uid
        self.taskEnv = taskEnv

