# Redis数据库地址
REDIS_HOST = '127.0.0.1'

# Redis端口
REDIS_PORT = 6379

# Redis密码，如无填None
REDIS_PASSWORD = 'password'
#REDIS_PASSWORD = None

REDIS_KEY = 'proxies'
REDIS_HTTP = 'http_proxy'
REDIS_HTTPS = 'https_proxy'

# 代理分数
MAX_SCORE = 100
MIN_SCORE = 80
INITIAL_SCORE = 90

VALID_STATUS_CODES = [200, 302]

# 代理池数量界限
POOL_UPPER_THRESHOLD = 100

# 检查周期
TESTER_CYCLE = 5
# 获取周期
GETTER_CYCLE = 60

# 测试API，建议抓哪个网站测哪个
TEST_URL = 'https://www.baidu.com'
HTTPSTEST_URL = 'https://www.baidu.com'

# API配置
API_HOST = '0.0.0.0'
API_PORT = 8989

# 开关
TESTER_ENABLED = True
GETTER_ENABLED = True
API_ENABLED = True

# 最大批测试量
BATCH_TEST_SIZE = 3

START_PROXY = None

LOGGERNAME = 'proxypool'
