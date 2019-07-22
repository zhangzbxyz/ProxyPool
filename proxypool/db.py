import redis
from proxypool.error import PoolEmptyError
from proxypool.setting import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, REDIS_KEY, REDIS_HTTPS, REDIS_HTTP
from proxypool.setting import MAX_SCORE, MIN_SCORE, INITIAL_SCORE
from random import choice
import re


class RedisClient(object):
    def __init__(self,
                 host=REDIS_HOST,
                 port=REDIS_PORT,
                 password=REDIS_PASSWORD):
        """
        初始化
        :param host: Redis 地址
        :param port: Redis 端口
        :param password: Redis密码
        """
        self.db = redis.StrictRedis(host=host,
                                    port=port,
                                    password=password,
                                    decode_responses=True)

    def add(self, proxy, score=INITIAL_SCORE, mode=None):
        """
        添加代理，设置分数为最高
        :param proxy: 代理
        :param score: 分数
        :return: 添加结果
        """
        if not re.match('\d+\.\d+\.\d+\.\d+\:\d+', proxy):
            print('代理不符合规范', proxy, '丢弃')
            return

        if mode is None:
            rediskey = REDIS_KEY
        else:
            rediskey = mode

        if not self.db.zscore(rediskey, proxy):
            return self.db.zadd(rediskey, {proxy: score})

    def random(self, mode=None):
        """
        随机获取有效代理，首先尝试获取最高分数代理，如果不存在，按照排名获取，否则异常
        :return: 随机代理
        """
        if mode is None:
            rediskey = REDIS_KEY
        else:
            rediskey = mode

        result = self.db.zrangebyscore(rediskey, MAX_SCORE, MAX_SCORE)
        if len(result):
            return choice(result)
        else:
            result = self.db.zrevrange(rediskey, 0, 100)
            if len(result):
                return choice(result)
            else:
                raise PoolEmptyError

    def decrease(self, proxy, mode=None):
        """
        代理值减一分，小于最小值则删除
        :param proxy: 代理
        :return: 修改后的代理分数
        """
        if mode is None:
            rediskey = REDIS_KEY
        else:
            rediskey = mode

        score = self.db.zscore(rediskey, proxy)
        if score and score > MIN_SCORE:
            print(rediskey, '代理', proxy, '当前分数', score, '减1')
            return self.db.zincrby(rediskey, -1, proxy)
        else:
            print(rediskey, '代理', proxy, '当前分数', score, '移除')
            return self.db.zrem(rediskey, proxy)

    def exists(self, proxy, mode=None):
        """
        判断是否存在
        :param proxy: 代理
        :return: 是否存在
        """
        if mode is None:
            rediskey = REDIS_KEY
        else:
            rediskey = mode

        return not self.db.zscore(rediskey, proxy) == None

    def max(self, proxy, mode=None):
        """
        将代理设置为MAX_SCORE
        :param proxy: 代理
        :return: 设置结果
        """

        if mode == REDIS_HTTP:
            print('代理', proxy, '可用，设置为', MAX_SCORE)
            return self.db.zadd(REDIS_HTTP, {proxy: MAX_SCORE})
        elif mode == REDIS_HTTPS:
            print('代理', proxy, '可用，设置为', MAX_SCORE)
            return self.db.zadd(REDIS_HTTPS, {proxy: MAX_SCORE})
        else:
            return self.db.zadd(REDIS_KEY, {proxy: MAX_SCORE})

    def count(self, mode=None):
        """
        获取数量
        :return: 数量
        """
        if mode is None:
            rediskey = REDIS_KEY
        else:
            rediskey = mode

        return self.db.zcard(rediskey)

    def count_good(self, mode=None):
        """
        获取数量
        :return: 数量
        """
        if mode is None:
            rediskey = REDIS_KEY
        else:
            rediskey = mode

        return self.db.zcount(rediskey, MAX_SCORE, MAX_SCORE)

    def all(self, mode=None):
        """
        获取全部代理
        :return: 全部代理列表
        """
        if mode is None:
            rediskey = REDIS_KEY
        else:
            rediskey = mode

        return self.db.zrangebyscore(rediskey, MIN_SCORE, MAX_SCORE)

    def batch(self, start, stop, mode=None):
        """
        批量获取
        :param start: 开始索引
        :param stop: 结束索引
        :return: 代理列表
        """
        if mode is None:
            rediskey = REDIS_KEY
        else:
            rediskey = mode
        return self.db.zrevrange(rediskey, start, stop - 1)


if __name__ == '__main__':
    conn = RedisClient()
    result = conn.batch(680, 688)
    print(result)
