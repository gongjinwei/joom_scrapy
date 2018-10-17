# -*- coding:UTF-8 -*-
import scrapy
import re, json
from json.decoder import JSONDecodeError
from redis import StrictRedis


client = StrictRedis()


class WishSpider(scrapy.Spider):
    name = 'wish'
    start_urls = ['https://www.wish.com']
    urls = [
        'https://www.wish.com/merchant/5a0e81bd448a522a1e19ccee',
        'https://www.wish.com/merchant/555302688889150e60b5023b',
        'https://www.wish.com/merchant/556ec9326faa881d1260e28f',
        'https://www.wish.com/merchant/58db754cfe9cae6d16fe6d3f',
        'https://www.wish.com/merchant/59ed48d4ef7b896652383000',
        'https://www.wish.com/merchant/5534bdb73b6cc80c1bafdcd3',
        'https://www.wish.com/merchant/5533976e1a8a2217256ed50a',
        'https://www.wish.com/merchant/540f08f61d2d431f274b61d2',
        'https://www.wish.com/merchant/585cb92239d9d1526ad44261',
        'https://www.wish.com/merchant/54281bb7f8abc81aad40160b',
    ]
    handle_httpstatus_list = [500]
    headers={}

    def parse(self, response):
        self.get_headers(response)
        for url in self.urls:
            store_id = url.split('/')[-1]
            yield scrapy.FormRequest('https://www.wish.com/api/merchant', callback=self.offset_parse,
                                     formdata={'query': store_id}, headers=self.headers,
                                     meta={'query': store_id})

    def get_headers(self, response):
        cookie_str = response.headers.to_unicode_dict().get('set-cookie', '')
        match = re.match('.*_xsrf=(.+?);', cookie_str)
        if match:
            self.headers={'X-XSRFToken': match.group(1)}

    def error_header_parse(self, response):
        self.get_headers(response)
        store_id = response.meta.get('query')
        formdata={'query': store_id}
        start = response.get('start','')
        if start:
            formdata.update({'start':start})
        yield scrapy.FormRequest('https://www.wish.com/api/merchant', callback=self.offset_parse,
                                 formdata=formdata, headers=self.headers,meta=formdata)

    def offset_parse(self, response):
        store_id = response.meta.get('query')
        start = response.meta.get('start', '')
        try:
            r = json.loads(response.body)
        except JSONDecodeError:
            # 如果json解析错误则重新请求
            query={'query':store_id}
            if start:
                query.update({'start':start})
            return scrapy.FormRequest(response.url,callback=self.offset_parse,formdata=query,meta=query,headers=response.request.headers)

        if response.status == 500:
            meta = {'query': store_id}
            if start:
                meta.update({'start': start})
            return scrapy.Request('https://www.wish.com', callback=self.error_header_parse, meta=meta)
        next_offset = str(r['data']['next_offset'])
        end_flag = r['data']['feed_ended']
        results = r['data']['results']
        print(len(results), next_offset)
        for result in results:
            client.sadd('wish','%s:%s' %(store_id, result['id']))

        if not end_flag:
            formdata={'query': store_id, 'start': next_offset}
            yield scrapy.FormRequest('https://www.wish.com/api/merchant', callback=self.offset_parse,
                                     formdata=formdata, headers=self.headers,meta=formdata)
