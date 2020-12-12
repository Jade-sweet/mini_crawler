# -*- coding: utf-8 -*-
import copy
import json
import requests

from tasks.models.taskCenter.push import ParamData, CrawlerResult, Param
from utils.redisHelper import addListData
from conf.taskSettings import LOCAL_SERVER_HOST, LOCAL_SERVER_PORT, LOCAL_SERVER_URL


class Result:
    """控制存放中间值方式的类"""

    def __init__(self, taskJson=None):
        self.obj = TemporaryHTTPService(taskJson)
        self.result = self.obj.initResult()  # 创建初始化数据

    def push(self):
        """把爬取的数据传到爬虫之外"""
        result = copy.deepcopy(self.result)
        self.obj.push(result)

    def changeResult(self, status):
        """改变Result的值"""
        self.result['Result'] = status

    def changeFully(self, status):
        """改变fully的值"""
        self.result['Task']['Data']['has_fully_crawled'] = status

    def changePage(self, page):
        """改变页面的值"""
        self.result['Task']['Data']['page_num'] = page

    def changeSinceID(self, sinceID):
        """改变since_id的值"""
        self.result['Task']['Data']['since_id'] = sinceID


class TemporaryHTTPService:
    """利用HTTP本地通信，实现进程间通信"""

    def __init__(self, taskEnv=None):
        self.taskEnv = taskEnv  # 原始的taskJson

    def initResult(self):
        """
        初始化数据， 这个初始化数据就是需要上传的原始数据Param，格式如下
        {
            "TaskType": xx,
            "Data": {
                "state": "ok",
                "msg": "ok",
                "data": {
                    "pics": [],
                    "posts": [],
                    "profiles":[]
                }
            },
            "Uuid": "xx",
            "Task": {taskEnv},
            "Result": "uncomplete"
        }
        """
        self.taskEnv['Data'] = json.loads(self.taskEnv['Data'])
        paramData = ParamData()  # 单个的param
        result, taskJson = "uncomplete", self.taskEnv
        obj = paramData.__dict__  # Data - data 数据组装完成
        # 准备数据 这个数据是CrawlerResult
        data = CrawlerResult(state='ok', msg='test', data=obj)
        # 构建最终数据
        pushResult = Param(taskType='weibo', result=result, data=data, task=taskJson)
        # 给self.result赋值
        param = pushResult.__dict__
        return param

    @staticmethod
    def push(result):
        # 发送本地的http请求 将数据传入外部
        headers = {
            'Content-Type': 'application/json',
            'X-Auth-Token': 'token'
        }
        result['Task']['Data'] = json.dumps(result['Task']['Data'])
        result['Task'] = json.dumps(result['Task'])
        result['Data'] = json.dumps(result['Data'])
        response = requests.post(url=f'http://{LOCAL_SERVER_HOST}:{LOCAL_SERVER_PORT}{LOCAL_SERVER_URL}', data=json.dumps(result), headers=headers)
        print(response.content.decode())


class TemporaryRedis:
    """利用HTTP本地通信，实现进程间通信"""

    def __init__(self, taskEnv=None):
        self.taskEnv = taskEnv  # 原始的taskJson

    def initResult(self):
        """
        初始化数据， 这个初始化数据就是需要上传的原始数据Param，格式大致如下
        {
            "TaskType": xx,
            "Data": {
                "state": "ok",
                "msg": "ok",
                "data": {
                    "pics": [],
                    "posts": [],
                    "profiles":[]
                }
            },
            "Uuid": "xx",
            "Task": "taskEnv",
            "Result": "uncomplete"
        }
        """
        self.taskEnv['Data'] = json.loads(self.taskEnv['Data'])
        paramData = ParamData()  # 单个的param
        result, taskJson = "uncomplete", self.taskEnv
        obj = paramData.__dict__  # Data - data 数据组装完成
        # 准备数据 这个数据是CrawlerResult
        data = CrawlerResult(state='ok', msg='test', data=obj)
        # 构建最终数据
        pushResult = Param(taskType='weibo', result=result, data=data, task=taskJson)
        # 给self.result赋值
        param = pushResult.__dict__
        return param

    @staticmethod
    def push(result):
        # 向redis中添加元素 将数据传入外部
        result['Task']['Data'] = json.dumps(result['Task']['Data'])
        result['Task'] = json.dumps(result['Task'])
        result['Data'] = json.dumps(result['Data'])
        addListData(name='temporary__result', data=json.dumps(result))
