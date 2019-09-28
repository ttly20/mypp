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


@app.route('/geiwoyigedaili')
def get_proxy():
    """Get an random enabled proxy"""
    conn = get_conn
    return conn.random()


@app.route('/youduoshaodaili')
def count():
    """Get proxy count"""
    conn = get_conn
    return str(conn.count())


if __name__ == '__main__':
    app.run()

