# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo, datetime
import items
from twisted.enterprise import adbapi
from MySQLdb.cursors import DictCursor


class JoomFetchPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, (items.JoomFetchItem, items.WishProductItem)):
            item.save()
        elif isinstance(item, items.XiciItem):
            items.XiciProxy.objects.update_or_create(**item, defaults={'ip': item['ip']})
        return item


class MongoPipeline(object):
    collection_name = datetime.datetime.strftime(datetime.datetime.today(), 'is_new:%Y%m%d')

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item, items.WishShopItem):
            collection = self.db[self.collection_name]
            doc = item['document']
            collection.replace_one({'id': doc['id']}, doc, upsert=True)
        return item


class MySQLPipeline(object):

    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_crawler(cls, crawler):
        dbparams = dict(
            host=crawler.settings['MYSQL_HOST'],
            db=crawler.settings['MYSQL_DB'],
            user=crawler.settings['MYSQL_USER'],
            passwd=crawler.settings['MYSQL_PASSWORD'],
            port=crawler.settings['MYSQL_PORT'],
            charset='utf8mb4',
            cursorclass=DictCursor,
            use_unicode=True)
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbparams)
        return cls(dbpool)

    def do_insert(self, cursor, item):
        insert_sql, params = item.get_insert_sql()
        cursor.execute(insert_sql, params)

    def process_item(self, item, spider):
        """
            runInteraction:It will be passed an L{Transaction} object as an argument (whose interface
            is identical to that of the database cursor for your DB-API module of choice)
        """
        if isinstance(item, (items.XiciDeferItem,items.JoomStoreItem,items.JoomSkuItem,items.JoomProductItem)):
            query = self.dbpool.runInteraction(self.do_insert, item)
            query.addErrback(self.handle_error, item, spider)
        return item

    def handle_error(self, failure, item, spider):
        '''
        处理异步插入数据库错误
        :param failure:
        :return:
        '''
        print(failure)
