import sys
from proxypool.tester import Tester
from proxypool.db import RedisClient
from proxypool.crawler import Crawler
import logging
import traceback
from proxypool.setting import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, REDIS_KEY, REDIS_HTTPS, REDIS_HTTP, LOGGERNAME, TESTLOGGER, GETTERLOGGER, POOL_UPPER_THRESHOLD


class Getter():
    crawler_list = [
        "crawl_ip3366", "crawl_kuaidaili", "crawl_ip3366_new", "crawl_iphai",
        "crawl_data5u"
    ]

    def __init__(self):
        self.spider_log = logging.getLogger(GETTERLOGGER)
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
        self.spider_log.info('获取器定时开始')
        httpflag = 0
        httpsflag = 0
        if not self.is_over_threshold(REDIS_HTTP):
            httpflag = 1
        if not self.is_over_threshold(REDIS_HTTPS):
            httpsflag = 1
        try:
            if httpflag == 1 or httpsflag == 1:
                self.spider_log.info("获取器开始执行,http:" +
                                     str(self.redis.count(REDIS_HTTP)) +
                                     ";https:" +
                                     str(self.redis.count(REDIS_HTTPS)))
                # if True:
                for callback_label in range(self.crawler.__CrawlFuncCount__):
                    callback = self.crawler.__CrawlFunc__[callback_label]
                    # 获取代理
                    if callback not in Getter.crawler_list:
                        continue
                    self.spider_log.info('开始获取：' + callback)
                    proxies = self.crawler.get_proxies(callback)
                    sys.stdout.flush()
                    if httpflag == 1:
                        for proxy in proxies:
                            self.redis.add(proxy, mode=REDIS_HTTP)
                    if httpsflag == 1:
                        for proxy in proxies:
                            self.redis.add(proxy, mode=REDIS_HTTPS)
            else:
                self.spider_log.info("获取器无需执行,http:" +
                                     str(self.redis.count(REDIS_HTTP)) +
                                     ";https:" +
                                     str(self.redis.count(REDIS_HTTPS)))

        except Exception as e:
            self.spider_log.error('获取器发生错误' + str(e.args))
            self.spider_log.error('traceback:' + traceback.format_exc())


if __name__ == '__main__':
    getter = Getter()
    getter.run()
