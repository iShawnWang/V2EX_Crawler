# -*- coding: utf-8 -*-

from scrapy.item import Item, Field
from scrapy.loader.processors import MapCompose
from urllib.parse import urljoin
from scrapy.loader.processors import Identity
from w3lib.html import remove_tags
from V2EX_Crawler.constants import V2EX_URL


"""模型类"""


def _urlContact(url):
    """拼接 url"""

    u = urljoin(V2EX_URL, url)
    u = u.split('#')[0]
    return u


def _parseTopicID(url):
    """话题 id"""

    u = url
    tmpU = u.split('/')
    u = tmpU[2] if len(tmpU) > 0 else ""
    tmpU = u.split('#')
    u = tmpU[0] if len(tmpU) else ""
    return u


def _parseLastReplayTime(string):
    """最近一次回复时间"""

    if not len(string) > 0:
        return ""
    splited = string.split('•')
    lastReplayTime = splited[1] if len(splited) >= 1 else ""
    return lastReplayTime


def _parseClickTimes(string):
    """多少人点击"""

    splited = string.split('·')
    return splited[len(splited)-1]


class User(Item):
    userHref = Field(input_processor=MapCompose(_urlContact))
    avatar = Field(input_processor=MapCompose(_urlContact))
    userName = Field(input_processor=MapCompose(remove_tags))


class Comment(Item):
    commentUser = Field(serializer=User)
    content = Field()
    commentDate = Field()
    floor = Field(input_processor=MapCompose(remove_tags))  # 几楼


class TopicContent(Item):
    contentHtml = Field()
    clickTimes = Field(input_processor=MapCompose(remove_tags, _parseClickTimes))
    comments = Field(output_processor=Identity())
    commentPageCount = Field()
    pass


class Topic(Item):

    topicID = Field(input_processor=MapCompose(_parseTopicID))
    index = Field()

    title = Field(input_processor=MapCompose(remove_tags))
    url = Field(input_processor=MapCompose(_urlContact))
    tag = Field(input_processor=MapCompose(remove_tags))
    tagHref = Field(input_processor=MapCompose(_urlContact))
    lastReplayTime = Field(input_processor=MapCompose(_parseLastReplayTime))
    author = Field(serializer=User)
    lastReplayUser = Field(serializer=User)
    topicContent = Field(serializer=TopicContent)
