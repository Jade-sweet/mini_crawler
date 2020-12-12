# -*- coding: utf-8 -*-
from scrapy.exceptions import CloseSpider
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError, TCPTimedOutError

from conf.otherSettings import SAVE2TASK_CENTER


def errBack(failure, logger, temporary):
    """错误处理"""
    if failure.check(HttpError):
        response = failure.value.response
        logger.error('HttpError on %s', response.url)
    elif failure.check(DNSLookupError):
        request = failure.request
        logger.error('DNSLookupError on %s', request.url)
    elif failure.check(TimeoutError, TCPTimedOutError):
        request = failure.request
        logger.error('TimeoutError on %s', request.url)
    # 推送结果
    if SAVE2TASK_CENTER:
        temporary.changeResult('failed')
        temporary.push()
    raise CloseSpider('the crawler exited because there were failed requests')  # 结束当前爬虫
