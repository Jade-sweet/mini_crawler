# -*- coding: utf-8 -*-
import base64
import hashlib
import json
import queue
import threading
import time

from conf.taskSettings import ACCESSKEY, ACCESSSEC, HOST, GET_URL, CRAWLER, LIMIT, SAVE_URL
from tasks.models.task import Task, PicTask, PostTask, ProfileTask
from tasks.models.taskCenter.pull import ImageTask, BlogTask, BloggerTask
from tasks.models.taskCenter.push import CrawlerResult, ParamData, Param, Data
from download.temporaryResult.result import Result
from utils import helper
from utils.decorator import singleton
from utils.fileHelper import readFile


STATUS = False  # 标准是否有线程正在发起网络请求获取任务


@singleton
class TaskQueue:
    """单例队列"""
    def __init__(self):
        self.lock = threading.RLock()
        self.queues = {
            "bloggerSpiderTask": queue.Queue(),
            "blogSpiderTask": queue.Queue(),
            "imageSpiderTask": queue.Queue(),
        }


class TaskCenter:  # <---- 任务中心
    """只提供两个外部方法 push用来提交任务结果， get用来获取任务"""

    def __init__(self, data=None):
        self.jsonContent = data  # 这个数据是json化的字节串
        self.queue = TaskQueue()  # 用到了单例的队列
        self.lock = threading.RLock()

    def __queueSize(self):
        print(f'博主任务数剩余---{self.queue.queues.get("bloggerSpiderTask").qsize()}  博文任务数剩余---{self.queue.queues.get("blogSpiderTask").qsize()}  图片任务数剩余---{self.queue.queues.get("imageSpiderTask").qsize()}')

    def __queueIsNone(self, queueName: str) -> bool:
        # 返回任务管道的任务剩余量
        return False if self.queue.queues.get(queueName).qsize() else True

    def __allQueueIsNone(self) -> bool:
        # 所有任务管道有没有任务
        return True if self.queue.queues.get("bloggerSpiderTask").empty() and self.queue.queues.get("blogSpiderTask").empty() and self.queue.queues.get("imageSpiderTask").empty() else False

    @staticmethod
    def __buildAuthkey(accessKey: str, accessSec: str, timeString=u'\ufffd') -> str:
        """建立authKey"""
        authKey = f'{accessKey}__{timeString}__{accessSec}'
        authKey = authKey.encode('utf-8')
        h = hashlib.md5()
        h.update(authKey)
        val = h.hexdigest()
        return val

    def __buildPullUrl(self) -> str:
        authKey = self.__buildAuthkey(ACCESSKEY, ACCESSSEC)
        url = f'{HOST}{GET_URL}{authKey}'
        return url

    def __buildPushUrl(self) -> str:
        authKey = self.__buildAuthkey(ACCESSKEY, ACCESSSEC)
        url = f'{HOST}{SAVE_URL}{authKey}'
        return url

    def __getNew(self):
        """任务数消耗完毕，请求新的任务json,也就是更新self.jsonContent字段的值"""
        # 1. 发起请求、得到数据
        url = self.__buildPullUrl()
        limit = LIMIT
        crawler = CRAWLER
        # result = helper.sendRequest(url, limit, crawler)
        # 这里可读取本地json文件中的任务，取消下面一行注释，然后注释掉上面4行代码即可
        result = readFile(rootName='weibo_spider', fileList=['content.json']); result = json.dumps(result)
        # 2. 更新数据
        self.jsonContent = result
        # 3. 把字节串变成一堆中间任务
        tasks_ = self.__toMiddleTask()
        # 4. 把中间任务变成可执行任务、将任务存入到对应的管道中
        self.__toTasksAndSaveToQueue(tasks_)

    @staticmethod
    def __parseImage(item):
        try:
            data_ = item["Data"]
            data_ = json.loads(data_)
            page_num = data_["page_num"]
        except (TypeError, KeyError):
            page_num = 1
        try:
            has_fully_crawled = item["Data"]["has_fully_crawled"]
        except (TypeError, KeyError):
            has_fully_crawled = False
        try:
            last_max_page_num = item["Data"]["last_max_page_num"]
        except (TypeError, KeyError):
            last_max_page_num = 1
        return page_num, has_fully_crawled, last_max_page_num

    def __toMiddleTask(self) -> list:
        """这里是解析的方法，将从数据中心得到的json数据变成中间的任务"""
        tasks = []
        try:
            items = json.loads(self.jsonContent)
        except json.decoder.JSONDecodeError:
            return tasks
        # 解析任务
        for item in items:
            taskType = item["TaskType"]
            uid = item["Sku"]
            content = item["Content"]
            if content == 'pic_list':
                page_num, has_fully_crawled, last_max_page_num = self.__parseImage(item)
                task = ImageTask(
                    taskType=taskType,
                    content=content,
                    sku=uid,
                    page_num=page_num,
                    last_max_page_num=last_max_page_num,
                    has_fully_crawled=has_fully_crawled,
                    taskEnv=item)
                tasks.append(task)
            # 其他的类型
            elif content == 'post_list':
                try:
                    data_ = item["Data"]
                    data_ = json.loads(data_)
                    since_id = data_["since_id"]
                except (TypeError, KeyError):
                    since_id = 0
                task = BlogTask(
                    taskType=taskType,
                    content=content,
                    sku=uid,
                    taskEnv=item,
                    since_id=since_id)
                tasks.append(task)
            elif content == 'blogger':
                task = BloggerTask(
                    taskType=taskType,
                    content=content,
                    sku=uid,
                    taskEnv=item)
                tasks.append(task)
        return tasks

    def __toTasksAndSaveToQueue(self, middleTasks):
        # 转变成可执行的任务 middleTasks ---> tasks
        for middleTask in middleTasks:
            if middleTask.Content == 'pic_list':
                task = Task(taskType='image', data=PicTask(uid=middleTask.Sku, startPage=middleTask.page_num, endPage=None, taskEnv=middleTask.taskEnv))
                self.queue.queues.get('imageSpiderTask').put(task)
            elif middleTask.Content == 'post_list':
                task = Task(taskType='blog', data=PostTask(uid=middleTask.Sku, taskEnv=middleTask.taskEnv, sinceID=middleTask.since_id))
                self.queue.queues.get('blogSpiderTask').put(task)
            else:
                task = Task(taskType='blogger', data=ProfileTask(uid=middleTask.Sku, taskEnv=middleTask.taskEnv))
                self.queue.queues.get('bloggerSpiderTask').put(task)

    def get(self, queueName):
        """返回一个可执行的任务"""
        task = None
        global STATUS
        while True:
            if task:
                return task
            if self.__queueIsNone(queueName):
                # 请求新的任务 -- > 这里做一个锁
                with self.lock:
                    if self.__allQueueIsNone() and not STATUS:
                        STATUS = True
                        print('请求新任务', threading.get_ident())
                        self.__getNew()
                        time.sleep(3)
                    else:
                        print('等待,所有任务执行完毕才会重新请求', end='  ')
                        self.__queueSize()
                        time.sleep(5)
                STATUS = False
            else:
                task = self.queue.queues.get(queueName).get()

    def push(self):
        # 推送结果
        self.__saveCrawledResult()

    def __saveCrawledResult(self):
        url = self.__buildPushUrl()
        limit = None
        crawler = None
        print(self.jsonContent)
        helper.sendRequest(url, limit, crawler, data=self.jsonContent)


def getTask(name) -> Task:
    """获取任务的接口，调用的时taskCenter类中的get方法"""
    t = TaskCenter()
    task = t.get(name)
    return task


class TaskEnv:
    """提供任务环境变量的编码"""

    def __init__(self, taskEnv=None):
        self.taskEnv = taskEnv

    def base64Encode(self):
        taskEnv = str(base64.b64encode(str(self.taskEnv).encode()))[2:-1]
        return taskEnv


def parseTaskEnv(data):
    """解码"""
    taskEnv = eval((base64.b64decode(data.encode())).decode())
    return taskEnv
