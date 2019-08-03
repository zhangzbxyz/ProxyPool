from proxypool.scheduler import Scheduler
import sys
import io
import logging
import logging.config
from proxypool.logger import proxypoollogger
import yaml

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def main():
    try:
        s = Scheduler()
        s.run()
    except:
        main()


if __name__ == '__main__':
    proxypoollogger()
    main()
