# -*- coding: utf-8 -*-
import json

from utils.redisHelper import addListData, blPopTask
from tasks.models.redis.task import Task


class List:

    def __init__(self, name):
        self.name = name

    def addTasks(self, tasks):
        for task in tasks:
            self.addTask(task)

    def addTask(self, baseTask):
        # 取出任务的值
        val = None
        if baseTask.taskType == 'image':
            val = [baseTask.data.uid, baseTask.data.startPage, baseTask.data.endPage]
        elif baseTask.taskType == 'blog':
            val = [baseTask.data.uid, baseTask.data.sinceID]
        elif baseTask.taskType == 'blogger':
            val = baseTask.data.uid
        if val:
            # 可运行任务转成redisTask
            redisTask = Task(text=val)
            # 序列化成json
            jsonData = json.dumps(redisTask.text)
            # 将json存入到redis
            addListData(jsonData, self.name)

    def get(self):
        # 从redis取值
        val = blPopTask(self.name)
        # 取出的值反序列化
        val = str(val[1])
        # 变成redisTask
        redisTask = Task(text=val)
        # 变成可执行任务
        executableTask = redisTask.becomeExecutableTask(self.name)
        return executableTask
