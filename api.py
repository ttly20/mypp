import json
from flask import Flask, g
from db import RedisClient

__all__ = ['app']
app = Flask(__name__)


def get_conn():
    if not hasattr(g, 'redis'):
        g.redis = RedisClient()
    return g.redis


@app.route('/')
def index():
    return '<h1>你好哇,这里什么都没有噢.</h1>'


@app.route('/geiwoyizudaili/<page>')
def get_proxy(page):
    """Get an random enabled proxy"""
    conn = get_conn()
    if page == 1:
        start = 1 * int(page) - 1
        stop = start + 9
    else:
        start = int(page) * 10 -1
        stop = start + 10
    return json.dumps(conn.random(start, stop))


@app.route('/youduoshaodaili')
def count():
    """Get proxy count"""
    conn = get_conn()
    return str(conn.count())


if __name__ == '__main__':
    app.run()

