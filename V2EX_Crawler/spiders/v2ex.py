# -*- coding: utf-8 -*-

from scrapy.spiders import Spider
from scrapy import Request
from scrapy import FormRequest
from V2EX_Crawler.items import *
from V2EX_Crawler.ItemLoader import *
from urllib.parse import urlparse, parse_qs


class V2EX(Spider):
    name = 'V2EX'
    headers = {
        'Referer': 'https://www.v2ex.com',
    }

    def start_requests(self):
        url = 'https://www.v2ex.com/signin'
        yield Request(url, headers=self.headers, callback=self._parseForm)

    def _parseForm(self, response):
        userNameKey = ''.join(response.xpath('//*[@id="Main"]/div[2]/div[3]/form/table/tr[1]/td[2]/input/@name').extract())
        pwdKey = ''.join(response.xpath('//*[@id="Main"]/div[2]/div[3]/form/table/tr[2]/td[2]/input/@name').extract())
        userName = self.settings.get('V2EX_USERNAME')
        pwd = self.settings.get('V2EX_PASSWORD')
        if not userName or not pwd:
            self.logger.error('\n\n\n在 `settings.py` 配置你的 V2EX 用户名和密码\n\n\n')
            return

        return [FormRequest.from_response(response, url='https://www.v2ex.com/signin', headers=self.headers, formnumber=1, formdata={userNameKey: userName, pwdKey: pwd},callback=self._requestRecent)]

    def _requestRecent(self, response):
        for i in range(1, 2):  # 爬的页数
            url = 'https://www.v2ex.com/recent?p={}'.format(i)
            # priority 高, 请求先执行,
            yield Request(url, headers=self.headers, priority=-i, callback=self._parseTopicTable)

    def _parseTopicTable(self, response):
        url = urlparse(response.request.url)
        numberOfPage = 0

        for k, v in parse_qs(url.query).items():
            if k == "p":
                numberOfPage = v[0] if len(v) > 0 else 0

        table = response.xpath('//*[@id="Main"]/div[2]')
        table = table.xpath('//div[@class="cell item"]')
        idx = 0
        for cell in table:
            indexForTopic = int(numberOfPage) * 10000 + idx
            idx += 1
            topic = self._parseTopic(cell, indexForTopic)
            yield Request(topic['url'], headers=self.headers, priority=-idx, callback=self._parseTopicContent, meta={'topic': topic})

    def _parseTopic(self, cell, idx):
        topicloader = TopicLoader(selector=cell)

        topicloader.add_xpath('title', 'table/tr/td[3]/span[1]/a')
        topicloader.add_xpath('url', 'table/tr/td[3]/span[1]/a/@href')
        topicloader.add_xpath('tag', 'table/tr/td[3]/span[2]/a')
        topicloader.add_xpath('tagHref', 'table/tr/td[3]/span[2]/a/@href')
        topicloader.add_xpath('lastReplayTime', 'table/tr/td[3]/span[2]/text()[2]')
        topicloader.add_xpath('topicID', 'table/tr/td[3]/span[1]/a/@href')

        topicloader.add_value('author', self._parseUser(cell))
        topicloader.add_value('index', idx)
        topicloader.add_value('lastReplayUser', self._parseLastReplayUser(cell))
        item = topicloader.load_item()
        return item

    def _parseTopicContent(self, response):
        topic = response.meta.get('topic')
        topicContentLoader = TopicContentLoader(response=response)
        topicContentLoader.add_xpath('contentHtml', '//*[@id="Main"]/div[2]/div[2]/div')
        topicContentLoader.add_xpath('clickTimes','//*[@id="Main"]/div[2]/div[1]/small')

        if '目前尚无回复' not in response.text and not response.xpath('//*[@id="Main"]/div[4]/div[2]/@id'):
            topicContentLoader.add_value('commentPageCount', len(response.xpath('//*[@id="Main"]/div[4]/div[2]/table/tr/td[1]/a')))

        commentsTable = response.xpath('//*[@id="Main"]/div[4]/div')
        comments = []
        for div in commentsTable:
            if div.xpath('@id'):
                comments.append(self._parseComment(div))

        topicContentLoader.add_value('comments', comments)
        topic['topicContent'] = topicContentLoader.load_item()
        yield topic

    def _parseComment(self, selector):
        commentLoader = CommentLoader(selector=selector)
        commentLoader.add_xpath('content', 'table/tr/td[3]/div[4]')
        commentLoader.add_value('commentUser', self._parseCommentUser(selector))
        commentLoader.add_xpath('floor', 'table/tr/td[3]/div[1]/span')
        comment = commentLoader.load_item()
        return comment

    def _parseCommentUser(self, selector):
        userloader = UserLoader(selector=selector)
        userloader.add_xpath('userHref', 'table/tr/td[3]/strong/a/@href')
        userloader.add_xpath('avatar', 'table/tr/td[1]/img/@src')
        userloader.add_xpath('userName', 'table/tr/td[3]/strong/a')
        return userloader.load_item()

    def _parseUser(self, selector):
        userloader = UserLoader(selector=selector)
        userloader.add_xpath('avatar', 'table/tr/td[1]/a/img/@src')
        userloader.add_xpath('userName', 'table/tr/td[3]/span[2]/strong[1]/a')
        userloader.add_xpath('userHref', 'table/tr/td[3]/span[2]/strong[1]/a/@href')
        item = userloader.load_item()
        return item

    def _parseLastReplayUser(self,selector):
        userloader = UserLoader(selector=selector)
        userloader.add_xpath('userName', 'table/tr/td[3]/span[2]/strong[2]/a')
        userloader.add_xpath('userHref', 'table/tr/td[3]/span[2]/strong[2]/a/@href')
        item = userloader.load_item()
        return item
