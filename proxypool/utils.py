import requests
from requests.exceptions import ConnectionError
from .db import RedisClient
from proxypool.setting import REDIS_KEY, REDIS_HTTPS, REDIS_HTTP, START_PROXY, LOGGERNAME
import logging

base_headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate',
    'Accept':
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}


def getnewproxy():
    redisdb = RedisClient()
    newproxy = redisdb.random(mode=REDIS_HTTPS)
    randamproxy = {'http': newproxy, 'https': newproxy}
    return randamproxy


def get_page(url, options={}):
    """
    抓取代理
    :param url:
    :param options:
    :return:
    """
    spider_log = logging.getLogger(LOGGERNAME)
    headers = dict(base_headers, **options)
    spider_log.info('正在抓取:' + url)
    try:
        response = requests.get(url, headers=headers, proxies=START_PROXY)
        if response.status_code == 200:
            spider_log.info('抓取成功' + url + str(response.status_code))
            return response.text
        else:
            spider_log.info('更换ip重试' + url)
            randamproxy = getnewproxy()
            response = requests.get(url, headers=headers, proxies=randamproxy)
            if response.status_code == 200:
                spider_log.info('抓取成功' + url + str(response.status_code))
                return response.text
            else:
                spider_log.warning('抓取失败' + url + str(response.status_code))
                return None
    except ConnectionError:
        spider_log.info('更换ip重试' + url)
        randamproxy = getnewproxy()
        try:
            response = requests.get(url, headers=headers, proxies=randamproxy)
            if response.status_code == 200:
                spider_log.info('抓取成功' + url + str(response.status_code))
                return response.text
            else:
                spider_log.error('抓取失败' + url + str(response.status_code))
                return None
        except ConnectionError:
            spider_log.error('抓取失败' + url)
            return None
