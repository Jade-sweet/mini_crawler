# -*- coding: utf-8 -*-
import tasks.models.redis.list
import tasks.models.task
from conf.taskSettings import DEFAULT_TASK_JSON

from tasks.models.redis.list import List
from utils.helper import regularMatch


def addFailedTask(url: str):
    """接受一个失败链接"""
    if 'detail' in url:
        status, iD = getId("blog", url)
        if status and iD:
            taskQueue = List('blogSpiderTask')
            data = iD
            addTask(taskQueue, data)
    elif 'photo' in url:
        status, iD = getId('image', url)
        page = getPage(url)
        if status and iD:
            taskQueue = List('imageSpiderTask')
            data = [iD, page, page]
            addTask(taskQueue, data)
    elif 'uid&value' in url:
        status, iD = getId('blogger', url)
        if status and iD:
            data = iD
            taskQueue = List('bloggerSpiderTask')
            addTask(taskQueue, data)
    else:
        return


def addTasks(ids: list, name: str):
    redisList = List(name)
    # 接受一堆任务进行保存
    runtimeTasks = []
    if name == 'blogSpiderTask':
        # 保存任务
        for item in ids:
            uid = item.get('uid')
            sinceID = item.get('sinceID')
            task_ = tasks.models.task.PostTask(uid=uid, taskEnv={}, sinceID=sinceID)
            runtimeTasks.append(tasks.models.task.Task(taskType='blog', data=task_))
        redisList.addTasks(runtimeTasks)
    elif name == 'bloggerSpiderTask':
        # 保存任务
        for id_ in ids:
            task_ = tasks.models.task.ProfileTask(uid=id_, taskEnv={})
            runtimeTasks.append(tasks.models.task.Task(taskType='blogger', data=task_))
        redisList.addTasks(runtimeTasks)
    else:
        return
    """接受正常的待爬取的列表"""


def getPage(url):
    page = regularMatch(r'page=(.*?)/', url)
    return page[0] if page else 1


def getId(f: str, url: str):
    """提取任务id"""
    iD = None
    if f == 'blog':
        iD = regularMatch(r'detail/(.*?)/', url)
    elif f == 'image':
        iD = regularMatch(r'=107803(.*?)_-_photo', url)
    elif f == 'blogger':
        iD = regularMatch(r'value=(.*?)&', url)
    status = True if iD else False
    if status:
        iD = iD[0]
    return status, iD


def addTask(taskQueue, data):
    # 发布image任务
    if taskQueue.name == 'imageSpiderTask':
        baseTask = tasks.models.task.Task(taskType='image', data=tasks.models.task.PicTask(uid=data[0], startPage=data[1], endPage=data[2], taskEnv=DEFAULT_TASK_JSON))
    else:
        baseTask = tasks.models.task.Task(taskType='', data=tasks.models.task.ProfileTask(uid=data, taskEnv=DEFAULT_TASK_JSON))
    taskQueue.addTask(baseTask)
