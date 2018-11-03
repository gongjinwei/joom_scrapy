# -*- coding:UTF-8 -*-
import scrapy
import re, json, requests,time,uuid
from urllib.parse import urlsplit
from json.decoder import JSONDecodeError
from redis import StrictRedis
from scrapy_redis.utils import bytes_to_str
from scrapy_redis.spiders import RedisSpider
from fetch.models import WishShop
from joom_fetch.items import WishShopItem

client = StrictRedis('122.226.65.250', 18003)
mac = uuid.uuid1().hex[-12:]


class WishSpider(RedisSpider):
    name = 'wish'

    handle_httpstatus_list = [500,400,504]

    def start_requests(self):
        self.get_authorization()
        return super().start_requests()

    def get_authorization(self,not_valid=False):
        authorization = client.get('wish_authorization:%s' % mac)
        if not authorization or not_valid:
            init_url = 'https://www.wish.com/product/5ad049662293182ed8e8baef'
            s = requests.Session()
            r = s.get(url=init_url,verify=False)
            cookies = r.cookies.get_dict()
            headers = {'X-XSRFToken': cookies['_xsrf']}
            self.headers = headers
            self.cookies = cookies
            client.set('wish_authorization:%s' % mac, json.dumps({'headers': headers, 'cookies': cookies}))
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
            self.get_authorization(not_valid=True)
            meta = {'query': store_id}
            if start:
                meta.update({'start': start})
            return [
                scrapy.FormRequest('https://www.wish.com/api/merchant', callback=self.parse,
                                   formdata=meta, headers=self.headers, cookies=self.cookies,
                                   meta=response.meta, dont_filter=True)]

        if response.status>300:
            WishShop.objects.filter(url='https://www.wish.com/merchant/'+store_id).update(state=response.status)
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
            doc.update({'store_id': store_id,'create_time':int(time.time())})
            item['document'] = doc
            yield item

        if not end_flag:
            formdata = {'query': store_id, 'start': next_offset}
            response.meta.update({'start': next_offset})
            yield scrapy.FormRequest('https://www.wish.com/api/merchant', callback=self.parse,
                                     formdata=formdata, headers=self.headers, meta=response.meta, dont_filter=True)
        else:
            WishShop.objects.filter(url='https://www.wish.com/merchant/' + store_id).update(state=2)
    #
    # def error_header_parse(self, response):
    #     self.get_authorization()
    #     store_id = response.meta.get('query')
    #     formdata = {'query': store_id}
    #     start = response.meta.get('start', '')
    #     if start:
    #         formdata.update({'start': start})
    #     return [scrapy.FormRequest('https://www.wish.com/api/merchant', callback=self.parse,
    #                                formdata=formdata, headers=self.headers, cookies=self.cookies, meta=response.meta,
    #                                dont_filter=True)]
