# -*- coding:UTF-8 -*-

import scrapy, json, time, datetime
from joom_fetch.items import JoomTmpProductItem, JoomTmpSkuItem
import requests
import redis
from scrapy_redis.utils import bytes_to_str
from scrapy_redis.spiders import RedisSpider
from joom_fetch.spiders.joom import JoomSpider

client = redis.StrictRedis('122.226.65.250', 18003)


class JoomTempSpider(RedisSpider):
    name = "joom_tmp"
    handle_httpstatus_list = [404, 400, 401, 429, 500]

    def start_requests(self):
        self.get_authorization()
        return super().start_requests()

    def make_request_from_data(self, data):
        source_id = bytes_to_str(data)
        url = 'https://api.joom.com/1.1/products/%s?currency=USD&language=en-US' % source_id
        return scrapy.Request(url, headers=self.headers, meta={'source_id': source_id},
                             callback=self.parse,dont_filter=True)

    def get_authorization(self,not_valid=False):
        authorization = client.get('joom_authorization')
        if not authorization or not_valid:

            init_url = "https://www.joom.com/tokens/init"
            r = requests.post(init_url, verify=False)
            if r.status_code == 200:
                authorization = r.json()["payload"]["accessToken"]
                headers = {
                    'Authorization': "Bearer %s" % authorization,
                    'X-API-Token': 'qMprb1boKjfwMWXbkZQx7y5I9cztn9oc'
                }
                client.set('joom_authorization', json.dumps(headers))
                self.headers = headers
        else:
            self.headers = json.loads(authorization)

    def parse(self, response):
        source_id = response.meta.get('source_id')
        # 处理非200返回

        if response.status == 401:
            self.get_authorization(not_valid=True)
            return [response.request]
        elif response.status > 200:
            # 处理url状态
            return

        r = json.loads(response.body)['payload']
        if r['id'] != source_id:
            self.get_authorization(not_valid=True)
            return [response.request]

        review_url = 'https://api.joom.com/1.1/products/%s/reviews/filters?currency=USD&language=en-US' % source_id

        return scrapy.Request(review_url, headers=self.headers, callback=self.item_handle,
                             meta={'r': r},dont_filter=True)

    def item_handle(self, response):
        item_url = response.meta.get('item_url')
        # r是产品信息返回的json
        r = response.meta.get('r')
        reviews_data=json.loads(response.body)['payload']
        return JoomSpider.make_item(r,reviews_data,JoomTmpProductItem,JoomTmpSkuItem)

