# -*- coding: utf-8 -*-
"""程序入口"""
import base64
import os
import signal
import sys
import threading
import time

import download.proxies.proxy
import tasks.dequeue

from download.temporaryResult.localServer import LocalServer
from download.temporaryResult.receiveCrawledResult import TemporaryReception
from tasks.taskCenter import TaskEnv
from utils.fileHelper import readFile
from utils.helper import extendList


def startLocalServer():
    """启动本地服务器， 接受通过HTTP传输的爬取数据"""
    localServer = LocalServer()
    localServer.start()


def startRedisTemporary():
    """启动redis监听，接受通过redis存放的爬取数据"""
    t = TemporaryReception()
    t.start()


def startCrawlers(spiderType, taskListName, proxyName='proxyList', sleepTime=20):
    """爬虫循环函数"""
    while True:
        print(f'{spiderType} loading complete...', threading.get_ident())
        if download.proxies.proxy.Proxies().isEnough():
            startCrawler(spiderType, taskListName)
        else:
            print(f"The {proxyName} proxies are too few")
        time.sleep(sleepTime)


def startCrawler(spiderType, taskListName):
    # 从任务中心取任务
    task_ = tasks.dequeue.Get(taskListName)
    if not task_:
        return
    if task_.taskType == 'image':
        uid, startPage, endPage, taskEnv = task_.data.uid, task_.data.startPage, task_.data.endPage, task_.data.taskEnv
        taskEnv = TaskEnv(taskEnv).base64Encode()
        os.system(f"scrapy crawl {spiderType} -a uid={uid} -a startPage={startPage} -a endPage={endPage} -a taskEnv={taskEnv}")
    elif task_.taskType == 'blog':
        uid, taskEnv, sinceID = task_.data.uid, task_.data.taskEnv, task_.data.sinceID
        taskEnv = TaskEnv(taskEnv).base64Encode()
        os.system(f"scrapy crawl {spiderType} -a uid={uid} -a taskEnv={taskEnv} -a sinceID={sinceID}")
    elif task_.taskType == 'blogger':
        uid, taskEnv = task_.data.uid, task_.data.taskEnv
        taskEnv = TaskEnv(taskEnv).base64Encode()
        os.system(f"scrapy crawl {spiderType} -a uid={uid} -a taskEnv={taskEnv}")
    else:
        return


def exit(sigNum, frame):
    print('All threads closed! Bye-bye')
    sys.exit()


def buildThreads(number, args: tuple, target=startCrawlers):
    threads = []
    for i in range(number):
        threads.append(threading.Thread(target=target, args=args))
    return threads


def setRuntimeEnv():
    signal.signal(signal.SIGINT, exit)
    signal.signal(signal.SIGTERM, exit)
    moduleName = sys.argv[0]
    dirName = os.path.dirname(moduleName)
    absPath = os.path.abspath(dirName)
    os.chdir(absPath)


def readConfig():
    # 读取配置文件
    data = readFile('weibo_spider', ['conf.json'])
    blogSpiderNumber = data['blogSpiderNumber']
    bloggerSpiderNumber = data['bloggerSpiderNumber']
    imageSpiderNumber = data['imageSpiderNumber']
    return blogSpiderNumber, bloggerSpiderNumber, imageSpiderNumber


def start():
    blogSpiderNumber, bloggerSpiderNumber, imageSpiderNumber = readConfig()
    blogSpiderThreads = buildThreads(number=blogSpiderNumber, args=('blogSpider', 'blogSpiderTask'))
    bloggerSpiderThreads = buildThreads(number=bloggerSpiderNumber, args=('bloggerSpider', 'bloggerSpiderTask'))
    imageSpiderThreads = buildThreads(number=imageSpiderNumber, args=('imageSpider', 'imageSpiderTask'))
    localServer = [threading.Thread(target=startLocalServer, args=())]  # 这个线程用来启动本地的HTTP服务，用来接受通过HTTP传来的爬取数据，之后进行集中上传
    redisServer = [threading.Thread(target=startRedisTemporary, args=())]  # 这个线程用来监听是否有爬取结果存入redis，如果有，把它取出来暂存，之后进行集中上传
    threads = extendList(args=(blogSpiderThreads, bloggerSpiderThreads, imageSpiderThreads, localServer, redisServer))
    for thread in threads:
        thread.setDaemon(True)
        thread.start()
    for thread in threads:
        thread.join()


def main():
    """主函数"""
    setRuntimeEnv()
    start()


if __name__ == "__main__":
    """函数入口"""
    main()
