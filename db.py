import redis

# Constant setting

## Max score
MAX_SCORE = 100

## Min score
MIN_SCORE = 0

## Init score
INIT_SCORE =10

## Connection information
REDIS_HOST = 'localhost' 
REDIS_PORT = 6379
REDIS_PASSWORD = None
REDIS_COLLECTIONS = 'ProxyPool'

# Redis maximum save number
POOL_UPPER_THRESHLD = 10000

class RedisClient:


    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, passwd=REDIS_PASSWORD):
        """Init Redis Object"""
        self.db = redis.Redis(host=host, port=port, password=passwd)


    def add(self, proxy, score=INIT_SCORE):
        """Add a proxy and set init score"""
        if not self.db.zscore(REDIS_COLLECTIONS, proxy):
            return self.db.zadd(REDIS_COLLECTIONS, { proxy: score })


    def random(self, start, stop):
        """
        Return all proxies from start to stop.
        """
        result = []
        items = self.db.zrevrange(REDIS_COLLECTIONS, start, stop)
        if len(items):
            for item in items:
                if isinstance(item, bytes):
                    result.append(str(item, encoding='utf-8'))
                else:
                    result.append(item)
            return result
        else:
            Exception('无可用代理')


    def decrease(self, proxy):
        """Score minus,if less than or equal to 0,delete."""
        score = self.db.zscore(REDIS_COLLECTIONS, proxy)
        if score and score > MIN_SCORE:
            print('代理 ', proxy, '当前分数 ', score, '减1')
            return self.db.zincrby(REDIS_COLLECTIONS, -1, proxy)
        else:
            print('代理 ', proxy, '当前分数 ', score, '移除')
            return self.db.zrem(REDIS_COLLECTIONS, proxy)


    def max(self, proxy):
        """Update the agent score to the maximum score."""
        print(proxy, MAX_SCORE)
        return self.db.zadd(REDIS_COLLECTIONS, MAX_SCORE, proxy)


    def count(self):
        """Get proxy count"""
        return self.db.zcard(REDIS_COLLECTIONS)


    def all(self):
        """Get all proxy"""
        return self.db.zrangebyscore(REDIS_COLLECTIONS, MIN_SCORE, MAX_SCORE)

