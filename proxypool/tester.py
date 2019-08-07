import asyncio
import aiohttp
import time
import sys
try:
    from aiohttp import ClientError
except:
    from aiohttp import ClientProxyConnectionError as ProxyConnectionError
from proxypool.db import RedisClient
from proxypool.setting import *
import logging


class Tester(object):
    def __init__(self):
        self.redis = RedisClient()
        self.spider_log = logging.getLogger(LOGGERNAME)

    async def test_single_proxy(self, proxy, mode=None):
        """
        测试单个代理
        :param proxy:
        :return:
        """
        if isinstance(proxy, bytes):
            proxy = proxy.decode('utf-8')

        if mode is None:
            rediskey = REDIS_KEY
            url = TEST_URL
            proxy_prefix = 'http'

        elif mode == REDIS_HTTP:
            rediskey = REDIS_HTTP
            url = TEST_URL
            proxy_prefix = 'http'

        elif mode == REDIS_HTTPS:
            rediskey = REDIS_HTTPS
            url = HTTPSTEST_URL
            proxy_prefix = 'https'
        test_proxy = 'http://' + proxy

        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                # self.spider_log.info('正在测试' + test_proxy)

                async with session.get(url,
                                       proxy=test_proxy,
                                       timeout=15,
                                       allow_redirects=False) as response:
                    if response.status in VALID_STATUS_CODES:
                        self.redis.max(proxy, mode)
                        # self.spider_log.info(proxy_prefix + '代理可用' + proxy)
                    else:
                        self.redis.decrease(proxy, mode)
                        self.spider_log.warn('请求响应码不合法 ' +
                                             str(response.status) + 'IP' +
                                             proxy_prefix + ":" + proxy)
            except (ClientError,
                    aiohttp.client_exceptions.ClientConnectorError,
                    asyncio.TimeoutError, AttributeError):
                self.redis.decrease(proxy, mode)
                # self.spider_log.warn(proxy_prefix + '代理请求失败' + proxy)

    def run(self, mode=None):
        """
        测试主函数
        :return:
        """
        if mode is None:
            rediskey = REDIS_KEY
        else:
            rediskey = mode
        try:
            count = self.redis.count(mode)
            self.spider_log.info('测试器开始运行' + rediskey + '当前剩余' + str(count) +
                                 '个代理')

            for i in range(0, count, BATCH_TEST_SIZE):
                start = i
                stop = min(i + BATCH_TEST_SIZE, count)
                self.spider_log.info('正在测试第' + str(start + 1) + '-' +
                                     str(stop) + '个' + rediskey + '代理')
                test_proxies = self.redis.batch(start, stop, mode=mode)
                loop = asyncio.get_event_loop()
                tasks = [
                    self.test_single_proxy(proxy, mode=mode)
                    for proxy in test_proxies
                ]
                loop.run_until_complete(asyncio.wait(tasks))
                sys.stdout.flush()
                time.sleep(5)
        except Exception as e:
            self.spider_log.error('测试器发生错误' + str(e.args))
