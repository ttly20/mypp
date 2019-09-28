import re
from aiohttp import ClientSession
from lxml import etree
from db import RedisClient, POOL_UPPER_THRESHLD


class ProxyMetaClass(type):
    """
    Meta class, get all methods staring with crawl_
    when initializing the class
    """
    def __new__(mcs, name, bases, attrs):
        count = 0
        attrs['CrawlFunc'] = []
        for k, v in attrs.items():
            if 'crawl_'in k:
                attrs['CrawlFunc'].append(k)
                count += 1
        attrs['CrawlFuncCount'] = count
        return type.__new__(mcs, name, bases, attrs)


class Crawler(object, metaclass=ProxyMetaClass):


    async def get(self, url):
        headers = {
            #'User-Agent': 'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  Safari/535.19'
            'User-Agent': 'Mozilla/5.0 (Linux; U; Android 4.0.4; en-gb; GT-I9300 Build/IMM76D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'
        }
        async with ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                return await response.text()


    async def get_proxy(self, crawl_func):
        proxies = []
        for proxy in await eval('self.{}()'.format(crawl_func)):
            proxies.append(proxy)
        return proxies


    async def crawl_xicidaili(self, page_count=10):
        """Get xicidaili free proxy website source."""
        print('获取西刺代理')
        start_url = 'https://www.xicidaili.com/nn/{page}'
        urls = [start_url.format(page=page) for page in range(1, page_count + 1)]
        proxy = []
        for url in urls:
            html = etree.HTML(await self.get(url))
            result = html.xpath('//div/div/table/tr[@class]')
            for item in result:
                data = item.xpath('td/text()')
                proxy.append(':'.join([data[0], data[1]]))
        return proxy


    # async def crawl_mipu(self):
    #     """Get Mi Pu free proxy"""
    #     print('获取米扑代理')
    #     # html = etree.HTML(await self.get('https://proxy.mimvp.com/free.php'))
    #     # print(html.xpath('//body/div/div[@class="free-content"]/'))
    #     return [1,2,3]


    async def crawl_kuaidaili(self, page_count=10):
        print('获取快代理')
        start_url = 'https://www.kuaidaili.com/free/inha/{}/'
        urls = [start_url.format(page) for page in range(1, page_count + 1)]
        proxy = []
        for url in urls:
            html = etree.HTML(await self.get(url))
            result = html.xpath('//div/div/div/div/div/table/tbody/tr')
            for item in result:
                data = item.xpath('td/text()')
                proxy.append(':'.join([data[0], data[1]]))
        return proxy


    # async def crawl_quanwangdaili(self, page_count=10):
    #     print('获取全区代理')
    #     return [1,2,3]


class Getter:


    def __init__(self):
        """Initializing databases class and spider class"""
        self.redis = RedisClient()
        self.crawler = Crawler()


    def is_over_threshold(self):
        """Determine if the database if full"""
        if self.redis.count() >= POOL_UPPER_THRESHLD:
            return True
        return False

    async def run(self):
        print('开始获取代理...')
        if not self.is_over_threshold():
            for i in range(self.crawler.CrawlFuncCount):
                crawl_func = self.crawler.CrawlFunc[i]
                proxies = await self.crawler.get_proxy(crawl_func)
                for proxy in proxies:
                    print(proxy)
                    self.redis.add(proxy)

