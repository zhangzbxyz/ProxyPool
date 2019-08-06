import sys
from proxypool.tester import Tester
from proxypool.db import RedisClient
from proxypool.crawler import Crawler
from proxypool.setting import *
import logging


class Getter():
    def __init__(self):
        self.spider_log = logging.getLogger(LOGGERNAME)
        self.redis = RedisClient()
        self.crawler = Crawler()

    def is_over_threshold(self, mode=None):
        """
        判断是否达到了代理池限制
        """
        if mode is None:
            rediskey = REDIS_KEY
        else:
            rediskey = mode

        if self.redis.count(rediskey) >= POOL_UPPER_THRESHOLD:
            return True
        else:
            return False

    def run(self):

        httpflag = 0
        httpsflag = 0
        if not self.is_over_threshold(REDIS_HTTP):
            httpflag = 1
        if not self.is_over_threshold(REDIS_HTTPS):
            httpsflag = 1

        if httpflag == 1 or httpsflag == 1:
            self.spider_log.info('获取器开始执行,' + str(self.redis.count(REDIS_HTTP)) +
                                 ";" + str(self.redis.count(REDIS_HTTPS)))

            for callback_label in range(self.crawler.__CrawlFuncCount__):
                callback = self.crawler.__CrawlFunc__[callback_label]
                # 获取代理
                self.spider_log.info('开始获取：' + callback)
                proxies = self.crawler.get_proxies(callback)
                sys.stdout.flush()
                if httpflag == 1:
                    for proxy in proxies:
                        self.redis.add(proxy, mode=REDIS_HTTP)
                if httpsflag == 1:
                    for proxy in proxies:
                        self.redis.add(proxy, mode=REDIS_HTTPS)


if __name__ == '__main__':
    getter = Getter()
    getter.run()