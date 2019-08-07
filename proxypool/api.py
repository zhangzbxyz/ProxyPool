from flask import Flask, g, make_response
from proxypool.setting import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, REDIS_KEY, REDIS_HTTPS, REDIS_HTTP
from .db import RedisClient
__all__ = ['app']

app = Flask(__name__)


def get_conn():
    if not hasattr(g, 'redis'):
        g.redis = RedisClient()
    return g.redis


@app.route('/')
def index():
    return '<h2>Welcome to Proxy Pool System</h2>'


@app.route('/random')
def get_proxy():
    """
    Get a proxy
    :return: 随机代理
    """
    conn = get_conn()
    return conn.random()


@app.route('/https')
def get_https_proxy():
    conn = get_conn()
    return conn.random(mode=REDIS_HTTPS)


@app.route('/http')
def get_http_proxy():
    conn = get_conn()
    return conn.random(mode=REDIS_HTTP)


@app.route('/log')
def get_logger():
    # base_dir = os.path.dirname(__file__)
    # resp = make_response(base_dir)
    logfile = open('/log/proxypool/proxypool.log', 'r')
    logtext = ''
    logtext = logtext.join(logfile.readlines()[-100:])
    # logtext = logfile.read()

    resp = make_response(str(logtext))
    resp.headers["Content-type"] = "text/plan;charset=UTF-8"
    # logfile.close()
    return resp


@app.route('/error')
def get_error():
    logfile = open('/log/proxypool/proxypool_error.log', 'r')
    logtext = logfile.read()
    resp = make_response(str(logtext))
    resp.headers["Content-type"] = "text/plan;charset=UTF-8"
    return resp


@app.route('/count')
def get_counts():
    """
    Get the count of proxies
    :return: 代理池总量
    """
    conn = get_conn()

    string = str(conn.count()) + "个代理，"+str(conn.count(REDIS_HTTP)) + "个http代理，"+str(conn.count(REDIS_HTTPS)) + "个https代理"+"\n" \
        + str(conn.count_good(REDIS_HTTP)) + "个优质http代理，" + \
        str(conn.count_good(REDIS_HTTPS)) + "个https优质代理"
    return string


if __name__ == '__main__':
    app.run()
