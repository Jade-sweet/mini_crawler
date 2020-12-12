# -*- coding: utf-8 -*-

"""推送爬取结果所用到的模型"""

import json
import uuid

from models.base.blog import Blog
from models.base.blogger import Blogger
from models.base.image import Image


class CrawlerResult:
    """CrawlerResult的定义"""

    def __init__(self, state: str, msg, data):
        self.state = state
        self.msg = msg
        self.data = data


class Param:
    """Param的定义"""

    def __init__(self, taskType: str, data: CrawlerResult, task: dict, result: str):
        self.TaskType = taskType  # 任务的大类
        self.Data = data.__dict__  # 抓取的结果，内部为CrawlerResult类型， JSON编码
        self.Uuid = str(uuid.uuid4())  # 任务的uuid
        self.Task = task  # 任务对象的JSON
        self.Result = result  # 任务执行状态


class Data:
    """DATA的定义"""

    def __init__(self):
        self.Params = []

    def add(self, param):
        self.Params.append(param)

    def get(self):
        return self.Params


class Picture:
    """Picture的定义"""

    def __init__(self, image: Image):
        self.pid = image.imageId
        self.mid = image.blogId
        self.uid = image.userId
        self.id = f'{self.mid}_{self.pid}'
        self.url = image.imageUrl


class Post:
    """Posts的定义"""

    def __init__(self, blog: Blog):
        self.id = blog.blogId
        self.tweeted_time = blog.releaseTime
        self.text = blog.detail
        self.like_count = blog.likeCount
        self.reposts_count = blog.relayCount
        self.comment_count = blog.commentCount
        self.pics = json.dumps(blog.pics)


class Profile:
    """Profile的定义"""

    def __init__(self, blogger: Blogger):
        self.uid = blogger.uid
        self.nick_name = blogger.name
        self.avatar = blogger.headPortrait
        self.fans_count = blogger.fansCount
        self.follow_count = blogger.attentionCount
        self.post_count = blogger.postCount
        self.description = blogger.introduction


class Pictures:
    """Pictures的定义"""
    def __init__(self):
        self.pics = []

    def add(self, item: Picture):
        self.pics.append(item.__dict__)

    def get(self):
        return self.pics


class Posts:
    """Pictures的定义"""
    def __init__(self):
        self.posts = []

    def add(self, item: Post):
        self.posts.append(item.__dict__)

    def get(self):
        return self.posts


class Profiles:
    """Profiles的定义"""

    def __init__(self):
        self.profiles = []

    def add(self, item: Profile):
        self.profiles.append(item.__dict__)

    def get(self):
        return self.profiles


class ParamData:
    """Param.Data.data的定义"""

    def __init__(self):
        self.profiles = []
        self.posts = []
        self.pics = []

    def addUsers(self, item):
        self.profiles.extend(item)

    def addPics(self, item):
        self.pics.extend(item)

    def addPosts(self, item):
        self.posts.extend(item)


def handleBaseObjects(items, type_):
    """处理爬取到的基础的对象"""
    # 区分对象
    if type_ == 'blogger':
        res = baseObjects2TaskCenterObjects(Profile, Profiles, items)
    elif type_ == 'blog':
        res = baseObjects2TaskCenterObjects(Post, Posts, items)
    elif type_ == 'image':
        res = baseObjects2TaskCenterObjects(Picture, Pictures, items)
    else:
        res = []
    return res


def baseObjects2TaskCenterObjects(obj, obj_s, items):
    """基础的对象转为任务中心需要的对象格式"""
    res = obj_s()
    for item in items:
        obj_ = obj(item)  # 转化成上传的单个对象
        res.add(obj_)
    # 将转换后的全部对象返回，类型为列表
    return res.get()

