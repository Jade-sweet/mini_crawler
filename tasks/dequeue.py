# -*- coding: utf-8 -*-
import tasks.get


def Get(listName: str):
    # 得到一个可执行任务
    task = tasks.get.Get(listName=listName).get()
    return task
