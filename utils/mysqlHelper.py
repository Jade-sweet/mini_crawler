# -*- coding: utf-8 -*-
import pymysql

from conf.mysqlSettings import MYSQL_HOST, MYSQL_PORT, MYSQL_USERNAME, MYSQL_PASSWORD, MYSQL_DATABASE
from utils.decorator import validDatabase, connect2MysqlTimeOut


@validDatabase
def deleteById(db, ids, val):
    """删除记录"""
    sql = 'delete from %s where %s=%s'
    executeCUDCommand(sql, (db, ids, val))


@connect2MysqlTimeOut
def connect2DB():
    """
    连接数据库
    :return:
    """
    config = dict(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USERNAME, password=MYSQL_PASSWORD, db=MYSQL_DATABASE, charset='utf8')
    conn = pymysql.connect(**config)
    return conn


def executeCUDCommand(sql, val):
    """
    插入、更新、删除数据
    :param sql: sql语句
    :param val: 值
    :return: None
    """
    db = connect2DB()
    cursor = db.cursor()
    try:
        cursor.execute(sql, val)
        db.commit()
    except Exception:
        db.rollback()
    finally:
        cursor.close()
        db.close()


@validDatabase
def executeSelectCommand(sql, val):
    """
    查询语句，看数据是否存在
    :param sql:
    :param val:
    :return:
    """
    db = connect2DB()
    cursor = db.cursor()
    cursor.execute(sql, val)
    val = cursor.fetchall()
    cursor.close()
    db.close()
    return val

