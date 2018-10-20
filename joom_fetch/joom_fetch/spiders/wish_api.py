# -*- coding: utf-8 -*-
import scrapy
import re, json, requests
from urllib.parse import urlsplit
from redis import StrictRedis
from json.decoder import JSONDecodeError
from scrapy_redis.utils import bytes_to_str
from scrapy_redis.spiders import RedisSpider
from fetch.models import Shop

client = StrictRedis('122.226.65.250', 18003)
import pymongo

mg = pymongo.MongoClient('122.226.65.250', 18017)
db = mg.wish_api
collection = db.test


class WishApiSpider(RedisSpider):
    name = 'wish_api'
    handle_httpstatus_list = [400]

    def make_request_from_data(self, data):
        merge_data = bytes_to_str(data)
        pk,authorization = merge_data.split('+')
        headers = {
            'Authorization': "Bearer %s" % authorization
        }
        return scrapy.Request('https://merchant.wish.com/api/v2/product/multi-get?start=0&limit=50&show_rejected=true',
                              callback=self.parse,
                              headers=headers, dont_filter=True, meta={'pk':pk})

    def parse(self, response):
        pk = int(response.meta['pk'])
        if response.status > 300:
            Shop.objects.filter(pk=pk).update(already=3)
            return
        try:
            r = json.loads(response.body)
        except JSONDecodeError:
            start=re.match('.*start=(.+?)&',response.url).group(1)
            return [
                scrapy.Request('https://merchant.wish.com/api/v2/product/multi-get?start=%s&limit=25&show_rejected=true' % start,
                               callback=self.parse, headers=response.request.headers, dont_filter=True,
                               meta=response.meta)]
        data = r.get('data')
        if data:
            # 先处理data,判断是否有下一页
            collection.insert_many(data)
            next_page = r['paging'].get('next', '')
            if next_page:
                return [
                    scrapy.Request(next_page, callback=self.parse, headers=response.request.headers, dont_filter=True,
                                   meta=response.meta)]

            else:
                Shop.objects.filter(pk=pk).update(already=2)
