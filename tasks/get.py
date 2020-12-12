# -*- coding: utf-8 -*-
from tasks.models.redis.list import List
from tasks import taskCenter
from conf.taskSettings import TASK_FROM


class Get:

    def __init__(self, listName):
        self.sources = {
            'redisList': GetTaskFromRedisList,
            'taskCenter': GetTaskFromTaskCenter,
        }
        self.listName = listName

    def get(self):
        obj = self.sources[TASK_FROM]()
        return obj.get(self.listName)


class GetTaskFromRedisList:
    """从redis列表中获取任务"""

    @staticmethod
    def get(listName):
        redisList = List(listName)
        task = redisList.get()
        return task


class GetTaskFromTaskCenter:
    """从任务中心获取任务"""

    @staticmethod
    def get(listName):
        task = taskCenter.getTask(listName)
        return task



