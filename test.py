from proxypool.scheduler import Scheduler
import sys
import io
import logging
import logging.config
from proxypool.logger import proxypoollogger
import yaml
from proxypool.getter import Getter

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def test():
    getter = Getter()
    getter.run()


if __name__ == '__main__':
    test()
