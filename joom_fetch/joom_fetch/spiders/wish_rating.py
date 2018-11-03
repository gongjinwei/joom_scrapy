# -*- coding: utf-8 -*-
import scrapy
import json
from fetch.models import WishCrawlProduct
from scrapy_redis.spiders import RedisSpider
from scrapy_redis.utils import bytes_to_str


class WishRatingSpider(RedisSpider):
    name = 'wish_rating'
    handle_httpstatus_list = [500]

    def make_request_from_data(self, data):
        source_id = bytes_to_str(data, self.redis_encoding)

        return scrapy.FormRequest('https://www.wish.com/api/product-ratings/get',
                                  formdata={"product_id": source_id, "start": "0", "count": "1"},
                                  headers={"X-XSRFToken": "2|a31a81d1|ecdbaffd4321ee34cec80bea937c1dc4|1539501583"},
                                  cookies={"_xsrf":"2|a31a81d1|ecdbaffd4321ee34cec80bea937c1dc4|1539501583"},
                                  dont_filter=True,meta={'dont_retry':True,"source_id":source_id})

    def parse(self, response):
        res = json.loads(response.body)
        data = res['data']
        if data:
            source_id = response.meta.get('source_id')
            info = data['product_info']
            item=WishCrawlProduct.objects.get(source_id=source_id)
            item.average_score=info["rating"]
            if "rating_spread" in info:
                rating_spread=info["rating_spread"]
                item.score1 = rating_spread.get('star_one_rating_count',0)
                item.score2 = rating_spread.get('star_two_rating_count',0)
                item.score3 = rating_spread.get('star_three_rating_count',0)
                item.score4 = rating_spread.get('star_four_rating_count',0)
                item.score5 = rating_spread.get('star_five_rating_count',0)
            item.save()
