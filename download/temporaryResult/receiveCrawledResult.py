# -*- coding:UTF-8 -*-

"""这个文件包含的是接受从爬虫中传出的参数的类，临时存储之后，满足某个条件，集中向服务器推送"""
import json

from conf.otherSettings import MIN_PUSH_COUNT
from tasks.taskCenter import TaskCenter
from utils.redisHelper import blPopTask


class TemporaryReception:

    def __init__(self):
        self.obj = ReceiveFromRedis()

    def start(self):
        """启动"""
        self.obj.start()  # 启动监听
        while True:  # 循环监听
            self.obj.receive()  # 启动监听接受传回的值
            if self.obj.isEnough():
                self.push()

    def push(self):
        """统一推送任务"""
        self.obj.push()


class ReceiveFromRedis:
    """接受redis中存放的爬取的数据"""

    def __init__(self):
        self.data = []

    @staticmethod
    def start():
        print('redis监听任务启动...')

    def receive(self):
        # 等待从redis中取出存放的爬取数据
        val = blPopTask(name='temporary__result', timeout=3)
        self.data.append(json.loads(val[1]))

    def isEnough(self):
        """是否达到推送条件"""
        return True if len(self.data) >= MIN_PUSH_COUNT else False

    def push(self):
        res = self.data
        self.data = []
        t = TaskCenter(json.dumps(res))
        t.push()
