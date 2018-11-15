# -*- coding: utf-8 -*-
import scrapy, re,json
from scrapy_redis.spiders import RedisSpider
from scrapy.shell import inspect_response
from scrapy_splash import SplashRequest
from scrapy_redis.utils import bytes_to_str
from scrapy_redis.spiders import CrawlSpider
from scrapy.http.cookies import CookieJar

cookie_jar = CookieJar()


class VovaSpider(RedisSpider):
    name = 'vova'

    # def make_request_from_data(self, data):
    #     url = bytes_to_str(data)
    #     return SplashRequest(url, callback=self.parse, args={'wait': 1}, dont_filter=True)

    def parse(self, response):
        # cookie_jar.extract_cookies(response,response.request)
        inspect_response(response, self)
