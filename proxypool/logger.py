import logging
import logging.config
import yaml
import os


class proxypoollogger():
    def __init__(self):
        # 初始化log
        try:

            dirpath = os.path.dirname(__file__)
            log_config_file_path = os.path.join(dirpath, '../log_config.yaml')
            with open(log_config_file_path, 'r') as f:
                log_config = yaml.load(f, Loader=yaml.FullLoader)
                logging.config.dictConfig(log_config)
            spider_log = logging.getLogger('proxypool')
            spider_log.info('Logger初始化成功')
        except Exception as err:
            print('Logger初始化失败' + str(err))
