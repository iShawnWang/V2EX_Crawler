# -*- coding: utf-8 -*-

from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst,Identity
from V2EX_Crawler.items import *


class DefaultItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class TopicLoader(DefaultItemLoader):
    default_item_class = Topic


class TopicContentLoader(DefaultItemLoader):
    default_item_class = TopicContent


class UserLoader(DefaultItemLoader):
    default_item_class = User


class CommentLoader(DefaultItemLoader):
    default_item_class = Comment
