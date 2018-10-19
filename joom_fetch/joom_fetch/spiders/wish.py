# -*- coding:UTF-8 -*-
import scrapy
import re, json, requests
from urllib.parse import urlsplit
from json.decoder import JSONDecodeError
from redis import StrictRedis
from scrapy_redis.utils import bytes_to_str
from scrapy_redis.spiders import RedisSpider
from fetch.models import WishShop
from items import WishShopItem

client = StrictRedis('122.226.65.250', 18003)


class WishSpider(RedisSpider):
    name = 'wish'

    handle_httpstatus_list = [500,400,504]

    def start_requests(self):
        self.get_authorization()
        return super().start_requests()

    def get_authorization(self):
        authorization = client.get('wish_authorization')
        if not authorization:
            init_url = 'https://www.wish.com'

            r = requests.get(init_url)
            cookies = r.cookies.get_dict()
            headers = {'X-XSRFToken': cookies['_xsrf']}
            self.headers = headers
            self.cookies = cookies
            client.set('wish_authorization', json.dumps({'headers': headers, 'cookies': cookies}),3600*4)

        else:
            _auth = json.loads(authorization)
            self.cookies = _auth['cookies']
            self.headers = _auth['headers']

    def make_request_from_data(self, data):
        item_url = bytes_to_str(data)
        source_id = urlsplit(item_url).path.split('/')[-1]
        return scrapy.FormRequest('https://www.wish.com/api/merchant', callback=self.parse,
                                  formdata={'query': source_id}, headers=self.headers, cookies=self.cookies,
                                  meta={'query': source_id,'dont_retry':True}, dont_filter=True)

    def parse(self, response):
        store_id = response.meta.get('query')
        start = response.meta.get('start', '')

        if response.status == 500:
            client.delete('wish_authorization')
            self.get_authorization()
            meta = {'query': store_id}
            if start:
                meta.update({'start': start})
            return [
                scrapy.FormRequest('https://www.wish.com/api/merchant', callback=self.parse,
                                   formdata=meta, headers=self.headers, cookies=self.cookies,
                                   meta=response.meta, dont_filter=True)]

        elif response.status>300:
            WishShop.objects.filter(url='https://www.wish.com/merchant/'+store_id).update(state=3)
            return

        try:
            r = json.loads(response.body)
        except JSONDecodeError:
            # 如果json解析错误则重新请求

            query = {'query': store_id}
            if start:
                query.update({'start': start})
            return [scrapy.FormRequest(response.url, callback=self.parse, formdata=query, meta=response.meta,
                                       headers=response.request.headers, dont_filter=True)]

        next_offset = str(r['data']['next_offset'])
        end_flag = r['data']['feed_ended']
        results = r['data']['results']

        for doc in filter(lambda x: x.get('is_new', False), results):
        # for doc in results:
            item = WishShopItem()
            doc.update({'store_id': store_id})
            item['document'] = doc
            yield item

        if not end_flag:
            formdata = {'query': store_id, 'start': next_offset}
            response.meta.update({'start': next_offset})
            yield scrapy.FormRequest('https://www.wish.com/api/merchant', callback=self.parse,
                                     formdata=formdata, headers=self.headers, meta=response.meta, dont_filter=True)
        else:
            WishShop.objects.filter(url='https://www.wish.com/merchant/' + store_id).update(state=2)

    def error_header_parse(self, response):
        self.get_authorization()
        store_id = response.meta.get('query')
        formdata = {'query': store_id}
        start = response.meta.get('start', '')
        if start:
            formdata.update({'start': start})
        return [scrapy.FormRequest('https://www.wish.com/api/merchant', callback=self.parse,
                                   formdata=formdata, headers=self.headers, cookies=self.cookies, meta=response.meta,
                                   dont_filter=True)]
