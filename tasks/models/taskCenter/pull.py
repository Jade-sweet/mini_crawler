# -*- coding: utf-8 -*-

"""拉取任务所涉及的对象"""


class Base:

    def __init__(self, **kwargs):
        self.TaskType = kwargs.get('taskType')
        self.Content = kwargs.get('content')
        self.Sku = kwargs.get('sku')
        self.Data = kwargs.get('data')
        self.taskEnv = kwargs.get('taskEnv')  # 该字段来保存原有的任务的转义之后的字符串


class ImageTask(Base):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.page_num = kwargs.get('page_num')
        self.last_max_page_num = kwargs.get('last_max_page_num')
        self.has_fully_crawled = kwargs.get('has_fully_crawled')


class BlogTask(Base):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.since_id = kwargs.get('since_id')


class BloggerTask(Base):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
