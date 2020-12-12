# -*- coding: utf-8 -*-
from tasks.receives import addFailedTask, addTasks


def normal(ids: list, name: str):
    """保存正常请求的任务"""
    addTasks(ids=ids, name=name)


def unNormal(url: str):
    """保存失败的链接涉及的任务"""
    addFailedTask(url)
