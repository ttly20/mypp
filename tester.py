VALID_STATUS_CODES = [200, 301]
TEST_URL = 'http://www.zhihu.com'
BATCH_TEST_SIZE = 100

import time
import asyncio
from aiohttp import TCPConnector, ClientSession, ClientError, ClientConnectorError
from db import RedisClient

class Tester(object):


    def __init__(self):
        self.redis = RedisClient()


    async def test_single_proxy(self, proxy):
        """Test single proxy"""
        conn = TCPConnector(verify_ssl=False)
        try:
            async with ClientSession(connector=conn) as session:
                if isinstance(proxy, bytes):
                    proxy = proxy.decode('utf-8')
                real_proxy = 'http://' + proxy
                print('正在测试: ', proxy)
                async with session.get(TEST_URL, proxy=real_proxy, timeout=10) \
                        as response:
                    if response.status in VALID_STATUS_CODES:
                        self.redis.max(proxy)
                        print('代理可用: ', proxy)
                    else:
                        self.redis.derease(proxy)
                        print('请求响应不合法: ', proxy)
            except(ClientError, ClientConnectorError, TimeoutError, \
                    AttributeError):
                self.redis.decrease(proxy)
                print('代理请求失败: ', proxy)


    def run(self):
        """Test function"""
        print('开始测试...')
        try:
            proxies = self.redis.all()
            loop = asyncio.get_event_loop()
            for index in range(0, len(proxies), BATCH_TEST_SIZE):
                test_proxies = proxies[index:index + BATCH_TEST_SIZE]
                tasks = [self.test_single_proxy(proxy) for proxy in test_proxies]
                loop.run_until_complete(asyncio.wait(tasks))
                time.sleep(5)
        except Exception as e:
            print('测试发生错误', e.args)

