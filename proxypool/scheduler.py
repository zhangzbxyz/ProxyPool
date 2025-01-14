import sys
import time
from multiprocessing import Process
from proxypool.api import app
from proxypool.getter import Getter
from proxypool.tester import Tester
from proxypool.db import RedisClient
from proxypool.setting import *
import logging


class Scheduler():
    # def __init__(self):
    # self.spider_log = logging.getLogger(LOGGERNAME)

    def schedule_tester(self, cycle=TESTER_CYCLE, mode=None):
        """
        定时测试代理
        """
        tester = Tester()
        while True:
            tester.run(mode)
            time.sleep(cycle)

    def schedule_getter(self, cycle=GETTER_CYCLE):
        """
        定时获取代理
        """
        getter = Getter()
        while True:
            getter.run()
            time.sleep(cycle)

    def schedule_api(self):
        """
        开启API
        """
        # self.spider_log.info('代理API启动')
        app.run(API_HOST, API_PORT)

    def run(self):
        # self.spider_log.info('代理池开始运行')

        if TESTER_ENABLED:
            tester_process = Process(target=self.schedule_tester,
                                     kwargs={'mode': REDIS_HTTPS})
            tester_process.start()

        if TESTER_ENABLED:
            tester_process = Process(target=self.schedule_tester,
                                     kwargs={'mode': REDIS_HTTP})
            tester_process.start()

        if GETTER_ENABLED:
            getter_process = Process(target=self.schedule_getter)
            getter_process.start()

        if API_ENABLED:
            api_process = Process(target=self.schedule_api)
            api_process.start()


if __name__ == '__main__':
    getter = Scheduler()
    getter.run()
