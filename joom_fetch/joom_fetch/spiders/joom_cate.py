# -*- coding:UTF-8 -*-

import scrapy, json, time, datetime
from joom_fetch.items import JoomCateProductItem, JoomCateSkuItem
from fetch.models import JoomCateInfo
import requests
import redis
from scrapy_redis.utils import bytes_to_str
from scrapy_redis.spiders import RedisSpider
from joom_fetch.spiders.joom import JoomSpider

client = redis.StrictRedis('122.226.65.250', 18003)


class JoomCateSpider(RedisSpider):
    name = "joom_cate"
    handle_httpstatus_list = [404, 400, 401, 429, 500]
    custom_settings = {
        "CONCURRENT_REQUESTS": 8
    }

    def start_requests(self):
        self.get_authorization()
        return super().start_requests()

    def make_request_from_data(self, data):
        cate_id = bytes_to_str(data)
        url = 'https://api.joom.com/1.1/search/products?currency=USD&language=en-US'
        form_data = json.dumps(
            {"filters": [{"id": "categoryId", "value": {"type": "categories", "items": [{"id": cate_id}]}}],
             "count": 25})
        return scrapy.Request(url, headers=self.headers, meta={'cate_id': cate_id, 'download_timeout': 15},
                              body=form_data, method='POST',
                              callback=self.parse, dont_filter=True, errback=self.err_down_handle)

    def get_authorization(self, not_valid=False):
        authorization = client.get('joom_cate_authorization')
        if not authorization or not_valid:

            init_url = "https://www.joom.com/tokens/init"
            r = requests.post(init_url)
            if r.status_code == 200:
                authorization = r.json()["payload"]["accessToken"]
                headers = {
                    'Authorization': "Bearer %s" % authorization,
                    'X-API-Token': 'NsCWe9o88ONiNt4IrMMIGV5JMNuWp8Yv'
                }
                client.set('joom_cate_authorization', json.dumps(headers))
                self.headers = headers
        else:
            self.headers = json.loads(authorization)

    def err_down_handle(self, failure):
        print(failure)
        self.get_authorization(not_valid=True)

    def parse(self, response):
        cate_id = response.meta.get('cate_id')
        req_body = json.loads(response.request.body)
        res = json.loads(response.body)
        if 'payload' not in res:
            self.get_authorization(not_valid=True)
            return response.request
        for item in res['payload']['items']:
            review_url = 'https://api.joom.com/1.1/products/%s/reviews/filters?currency=USD&language=en-US' % item['id']
            meta = {'source_id': item['id']}
            # 查看评价情况，并且过滤重复
            yield scrapy.Request(review_url, headers=self.headers, callback=self.reviews_count,
                                 meta=meta)

        if 'nextPageToken' in res['payload']:
            next_page = res['payload']['nextPageToken']
            req_body.update({'pageToken': next_page})
            yield response.request.replace(body=json.dumps(req_body))
        else:
            # 所有任务正常进行完，更新状态
            JoomCateInfo.objects.filter(cate_id=cate_id).update(state=2)

    def reviews_count(self, response):
        r = json.loads(response.body)
        items = r['payload'].get('items', [])
        # 第一重筛选：评价数大于99
        filter_item = filter(lambda x: x['id'] == 'all' and x['count']['value'] > 99, items)
        for _ in filter_item:
            # 请求产品信息
            source_id = response.meta.get('source_id')
            url = 'https://api.joom.com/1.1/products/%s?currency=USD&language=en-US' % source_id
            return scrapy.Request(url, headers=self.headers, meta={'r': r, 'source_id': source_id},
                                  callback=self.product_filter, dont_filter=True)

    def product_filter(self, response):
        review_data = response.meta.get('r')['payload']
        source_id = response.meta.get('source_id')
        if response.status == 401:
            self.get_authorization(not_valid=True)
            return response.request
        elif response.status > 200:
            return

        r = json.loads(response.body)['payload']
        if r['id'] != source_id:
            self.get_authorization(not_valid=True)
            return response.request
        # 第二重筛选：过滤变体创建时间
        variants = r['variants']
        max_time_variant = max(variants, key=lambda x: ['createdTimeMs'])
        max_time = max_time_variant['createdTimeMs']
        from_time = datetime.datetime.fromtimestamp(max_time / 1000)
        now = datetime.datetime.now()
        if now - from_time <= datetime.timedelta(180):
            return JoomSpider.make_item(r, review_data, JoomCateProductItem, JoomCateSkuItem)
