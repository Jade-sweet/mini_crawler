# -*- coding: utf-8 -*-
import json
import os

from utils.decorator import fileSuccessOpen


def searchFileAbsolutePath(path, filename):
    for root, dirs, files in os.walk(path):
        if filename in dirs or filename in files:
            root = str(root)
            return os.path.join(root, filename)
    else:
        return None


def searchRoot(fileRoot):
    curPath = os.path.abspath(os.path.dirname(__file__))
    rootPath = curPath[:curPath.find(fileRoot) + len(fileRoot)]  # 获取项目的根路径
    return rootPath


def findFile(rootName, fileList):
    # 找到目标文件，返回绝对路径
    fileList = [str(i) for i in fileList]
    aimPath = os.path.join(rootName, *fileList)
    re = None
    rootPath = searchRoot(rootName)
    for item in fileList:
        re = searchFileAbsolutePath(rootPath, item)
        if not re:
            raise Exception(f'<{aimPath}> 文件不存在')
        rootPath = re
    return re


@fileSuccessOpen
def readFile(rootName, fileList):
    re = findFile(rootName, fileList)
    with open(re, 'r') as f:
        data = json.loads(f.read())
    return data


def writeFile(rootName, fileList, content):
    re = findFile(rootName, fileList)
    with open(re, 'w') as f:
        f.write(json.dumps(content))


# 写入文档
def write(path_s, text):
    with open(path_s, 'a', encoding='utf-8') as f:
        f.writelines(text)
        f.write('\n')
        f.close()


def truncate_file(path_s):
    """
    清空目标文档
    :param path_s: 文档目录
    :return:
    """
    with open(path_s, 'w', encoding='utf-8') as f:
        f.truncate()


def read(path_s):
    """
    读取文档
    :param path_s: 文档目录
    :return:
    """
    with open(path_s, 'r', encoding='utf-8') as f:
        txt = []
        for s in f.readlines():
            txt.append(s.strip())
    return txt


def deleteFile(filePath):
    """删除文件"""
    os.remove(filePath)
