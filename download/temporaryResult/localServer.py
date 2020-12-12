# -*- coding:UTF-8 -*-
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import cgi

from conf.otherSettings import MIN_PUSH_COUNT
from conf.taskSettings import LOCAL_SERVER_HOST, LOCAL_SERVER_PORT, LOCAL_SERVER_URL
from tasks.models.taskCenter.push import Data
from tasks.taskCenter import TaskCenter
from utils.decorator import singleton

host = (LOCAL_SERVER_HOST, LOCAL_SERVER_PORT)


@singleton
class DataFromHTTP:
    """用来辅助本地HTTP进行统一的推送管理"""

    def __init__(self):
        self.data = Data()

    def hasEnoughData(self):
        """数据是否满足推送条件"""
        return True if len(self.data.get()) >= MIN_PUSH_COUNT else False

    def push(self):
        """返回数据、列表清空"""
        res = self.data.get()
        self.data.Params = []
        return res


class TodoHandler(BaseHTTPRequestHandler):
    """对本地请求的处理"""

    def __init__(self, *args, **kwargs):
        self.data = DataFromHTTP()
        super(TodoHandler, self).__init__(*args, **kwargs)

    def do_GET(self):
        self.send_error(415, 'Only post is supported')

    def do_POST(self):
        contentType, parseDict = cgi.parse_header(self.headers['content-type'])
        token = self.headers['X-Auth-Token']
        if token == 'token' and contentType == 'application/json':
            path = str(self.path)  # 获取请求的url
            if path == LOCAL_SERVER_URL:
                length = int(self.headers['content-length'])  # 获取除头部后的请求参数的长度
                result = self.rfile.read(length)  # 获取请求参数数据，请求数据为json字符串
                result = json.loads(result.decode())  # 将爬取到的结果缓存起来
                self.data.data.add(result)
                if self.data.hasEnoughData():
                    # 满足推送条件，进行集中推送
                    result = json.dumps(self.data.push())
                    t = TaskCenter(result)
                    t.push()
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps('push success').encode())
            else:
                self.send_error(404, "Not Found")
        else:
            self.send_error(415, "Only json data is supported.")


class LocalServer:
    """本地服务器类"""

    def __init__(self):
        self.server = HTTPServer(host, TodoHandler)

    def start(self):
        print("Starting server, listen at: %s:%s" % host)
        self.server.serve_forever()
