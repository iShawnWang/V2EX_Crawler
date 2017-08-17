# -*- coding: utf-8 -*-


import pymongo

Topics = "Topics"
Author = "Author"


class DefaultValuePipeline(object):
    """为 item 设置默认值"""

    def process_item(self, item, spider):
        item.setdefault('lastReplayTime', None)
        item['topicContent'].setdefault('commentPageCount', 0)

        return item


class V2ExCrawlerPipeline(object):

    Topics = "Topics"

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

        self.db.drop_collection(Topics)  # drop collection

        self.topics = self.db[Topics]
        self.authors = self.db[Author]

    def close_spider(self, spider):
        # 测试查询 ~
        # for t in self.topics.find():
        #     t['author'] = self.authors.find_one({'_id': t['author']})
        #     t['lastReplayUser'] = self.authors.find_one({'_id': t['lastReplayUser']})
        #     print(t)

        self.client.close()

    def process_item(self, item, spider):
        """保存数据到 mongodb"""

        if not item:
            return None
        lastReplayUser = item.get('lastReplayUser')
        author = item.get('author')

        lastReplayUserID = None
        authorID = None

        # 保存最近一次回复的用户
        if lastReplayUser.get('userName'):  # 可能没有回复, 所以要判断一下
            self.authors.update_one({'userName': lastReplayUser['userName']}, {'$set': lastReplayUser}, upsert=True)
            lastReplayUserID = self.authors.find_one({'userName': lastReplayUser['userName']}).get('_id')

        # 保存话题作者
        authorID = self.authors.update_one({'userName': author['userName']}, {'$set': author}, upsert=True)
        if authorID.modified_count <= 0:
            authorID = self.authors.find_one({'userName': author['userName']}).get('_id')

        item['lastReplayUser'] = lastReplayUserID
        item['author'] = authorID

        # 再保存话题
        self.topics.update_one({'topicID': item['topicID']}, {'$set': dict(item)}, upsert=True)
        return item
