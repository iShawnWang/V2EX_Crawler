# -*- coding: utf-8 -*-

from fake_useragent import UserAgent


class RandomUserAgentMiddleware(object):
    """随机 User Agent"""

    def __init__(self, crawler):
        super(RandomUserAgentMiddleware, self).__init__()
        self.ua = UserAgent()
        self.ua_type = crawler.settings.get('RANDOM_UA_TYPE', 'random')

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):
        def get_ua():
            return getattr(self.ua, self.ua_type)

        request.headers.setdefault('User-Agent', get_ua())
        # request.meta["proxy"] = 'https://171.39.115.221:8123'  # 测试时出现访问次数过多, 一直 404 的情况, 某宝购买代理 ip 解决