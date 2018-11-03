# -*- coding: utf-8 -*-
import datetime
import scrapy
from scrapy_redis.spiders import RedisSpider
from items import XiciDeferItem,XiciLoader
from scrapy_redis.utils import bytes_to_str


class XiciSpider(RedisSpider):
    name = 'xici'
    allowed_domains = ['ww.xicidali.com']
    handle_httpstatus_list=[503]

    def make_request_from_data(self, data):
        url = bytes_to_str(data, self.redis_encoding)
        return scrapy.Request(url,dont_filter=True,meta={'dont_retry':True})

    def parse(self, response):
        if response.status==200:
            for i in range(len(response.xpath('//table/tr'))-1):

                loader =XiciLoader(item=XiciDeferItem(),response=response)
                loader.add_xpath('ip','//table/tr[{0}]/td[2]/text()'.format(i+2))
                loader.add_xpath('port','//table/tr[{0}]/td[3]/text()'.format(i+2))
                loader.add_xpath('address','//table/tr[{0}]/td[4]/a/text()'.format(i+2))
                loader.add_xpath('protocol','//table/tr[{0}]/td[6]/text()'.format(i+2))
                loader.add_value('create_time',datetime.datetime.now())
                item =loader.load_item()
                yield item
            next_url = response.xpath('//*[@class="next_page"]/@href').extract_first()
            if next_url:
                yield response.follow(next_url,dont_filter=True,meta={'dont_retry':True})

