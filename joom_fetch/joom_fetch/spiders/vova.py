# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider
from scrapy.shell import inspect_response
from scrapy_splash import SplashRequest
from scrapy_redis.utils import bytes_to_str


class VovaSpider(RedisSpider):
    name = 'vova'

    # def make_request_from_data(self, data):
    #     url = bytes_to_str(data)
    #     return SplashRequest(url,callback=self.parse,args={'wait':1})

    def parse(self, response):

        inspect_response(response,self)
