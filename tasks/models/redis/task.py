# -*- coding: utf-8 -*-

import tasks.models.task
from conf.taskSettings import DEFAULT_TASK_JSON


class Task:

    def __init__(self, text=None):
        self.text = text

    # 取出数据时进行数据校验
    def becomeExecutableTask(self, listName):
        task_ = None
        if listName == 'imageSpiderTask':
            if self.__isLegal():
                data = [i.strip() for i in self.text.split(',')]
                # 这里形成一个picTask
                picTask = tasks.models.task.PicTask(uid=data[0], startPage=data[1], endPage=data[2], taskEnv=DEFAULT_TASK_JSON)
                task_ = self.__task(taskType='image', data=picTask)
        elif listName == 'blogSpiderTask':
            if self.__isBlogLegal():
                data = [i.strip() for i in self.text.split(',')]
                # 这里形成一个picTask
                postTask = tasks.models.task.PostTask(uid=data[0], sinceID=data[1], taskEnv=DEFAULT_TASK_JSON)
                task_ = self.__task(taskType='blog', data=postTask)
        else:
            if self.__isBloggerLegal():
                postTask = tasks.models.task.ProfileTask(uid=self.text, taskEnv=DEFAULT_TASK_JSON)
                task_ = self.__task(taskType='blogger', data=postTask)
        return task_

    # 数据校验---特指image任务类型的任务类型校验
    def __isLegal(self):
        if not isinstance(self.text, str):  # 'b"[xx,xx,xx]"'
            print(f'输入任务的形式必须为字符串')
            return False
        if self.__isContentLegal(num=3) and self.__isTypeLegal():
            return True
        print(f'任务格式错误[{self.text}]，提示：类似于[0123456789,1,1]， 且第2个数小于等于第3个数')
        return False

    def __isBlogLegal(self):
        if not isinstance(self.text, str):  # 'b"[xx ,xx]"'
            print(f'输入任务的形式必须为字符串')
            return False
        if self.__isContentLegal(num=2) and self.__isTypeLegalBlog():
            return True
        print(f'任务格式错误[{self.text}]，提示：类似于[0123456789,1234567890123242]')
        return False

    # 数据校验--特指其他任务类型的任务类型校验
    def __isBloggerLegal(self):
        if not isinstance(self.text, str):
            print(f'输入任务的形式必须为字符串')
            return False
        if self.__isHaveContent(2, -1):
            return True
        print(f'任务格式错误{self.text}')
        return False

    @staticmethod
    def __task(taskType, data):
        # 返回真正的可运行的task
        return tasks.models.task.Task(taskType=taskType, data=data)

    # 校验内容是否合法
    def __isContentLegal(self, num):
        if self.__isHaveContent(3, -2) and self.__lengthIsValid(num):
            return True
        return False

    # 字段类型是否合法
    def __isTypeLegal(self):
        uid, startPage, endPage = self.text.split(',')
        if self.__uidCheck(uid) and self.__pageCheck(startPage, endPage):
            return True
        return False

    def __isTypeLegalBlog(self):
        uid, sinceID = self.text.split(',')
        if self.__uidCheck(uid) and self.__uidCheck(sinceID):
            return True
        return False

    def __isHaveContent(self, num1, num2):
        try:
            self.text = self.text[num1:num2]
            return True
        except IndexError:
            return False

    # 检查长度是否为3
    def __lengthIsValid(self, num):
        dataList = self.text.split(',')
        return True if len(dataList) == num else False

    @staticmethod
    def __uidCheck(uid):
        return True if len(uid) else False

    def __pageCheck(self, startPage, endPage):
        if self.__isInteger(startPage, endPage):
            # 字符型数字转int型数字，用于后面的页面正负以及起始页和终止页的判断
            startPage, endPage = int(startPage.strip().strip('"')), int(endPage.strip().strip('"'))
            if self.__isPositive(startPage, endPage) and self.__isStartLessThanEnd(startPage, endPage):
                return True
        return False

    # 页面大小校验
    @staticmethod
    def __isStartLessThanEnd(startPage, endPage):
        return True if startPage <= endPage else False

    # 页码类型校验
    @staticmethod
    def __isInteger(startPage, endPage):
        try:
            int(startPage.strip().strip('"'))
            int(endPage.strip().strip('"'))
            return True
        except ValueError:
            return False

    # 页码正负校验
    @staticmethod
    def __isPositive(startPage, endPage):
        return True if startPage > 0 and endPage > 0 else False
