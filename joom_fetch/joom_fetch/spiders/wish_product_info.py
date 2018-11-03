# -*- coding:UTF-8 -*-
import scrapy
from decimal import Decimal
import re, json, requests, time, uuid,datetime
from json.decoder import JSONDecodeError
from redis import StrictRedis
from scrapy_redis.utils import bytes_to_str
from scrapy_redis.spiders import RedisSpider
from joom_fetch.items import WishProductInfoItem,WishSkuNewItem

client = StrictRedis('122.226.65.250', 18003)
mac = uuid.uuid1().hex[-12:]


class WishSpider(RedisSpider):
    name = 'wish_product_info'

    handle_httpstatus_list = [500, 400, 504]

    def start_requests(self):
        self.get_authorization()
        return super().start_requests()

    def get_authorization(self, not_valid=False):
        authorization = client.get('wish_authorization:%s' % mac)
        if not authorization or not_valid:
            init_url = 'https://www.wish.com/product/5ad049662293182ed8e8baef'
            s = requests.Session()
            r = s.get(url=init_url, verify=False)
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
        cid = bytes_to_str(data)
        return scrapy.FormRequest('https://www.wish.com/api/product/get', callback=self.parse,
                                  formdata={'cid': cid,'request_sizing_chart_info':'true','do_not_track':'true'}, headers=self.headers, cookies=self.cookies, dont_filter=True)

    def parse(self, response):

        if response.status > 300:
            print(response.request.formdata)
            return

        try:
            r = json.loads(response.body)
        except JSONDecodeError:
            # 如果json解析错误则重新请求
            return [response.request]
        info = r['data']['contest']
        item_p = WishProductInfoItem()
        item_p['goods_name'] = info['name'][:255]
        item_p['sale_num'] = info['num_bought']
        item_p['default_img'] = info.get('contest_page_picture', None)
        extra_photo_urls =info.get('extra_photo_urls',{})
        item_p['list_img'] = '|'.join(extra_photo_urls.values())
        item_p['introduce'] = info['description']
        item_p['source_id'] = info['id']
        item_p['url'] = 'https://www.wish.com/product/' + info['id']
        item_p['tags'] = json.dumps(info['true_tag_ids'])
        item_p['keywords']=info['keywords']
        item_p['num_wishes']=info['num_wishes']
        if 'rating_size_summary' in item_p:
            item_p['rating_size_num']=info['rating_size_summary']['num_ratings']
            item_p['rating_size_summary']=json.dumps(info['rating_size_summary']['size_bars'])
        item_p['average_score']=Decimal(info['product_rating']["rating"]).quantize(Decimal('.01'))
        item_p['rating_count']=info['product_rating']["rating_count"]
        message = info['currently_viewing'].get('message','')
        match = re.match('(\d+?) viewing now',message)
        if match:
            item_p['currently_viewing_nums'] =int(match.group(1))
        item_p['create_time'] = info['generation_time']
        default_v = info['commerce_product_info']['default_variation_experiment']['no-init-max']
        item_p['enabled'] = default_v['enabled']
        item_p['price'] = Decimal(default_v['price']).quantize(Decimal('.01'))
        item_p['msrp'] = Decimal(default_v.get('retail_price', 0)).quantize(Decimal('.1'))
        item_p['shipping']=Decimal(default_v.get('shipping', 0)).quantize(Decimal('.1'))
        item_p['variation_id']=default_v['variation_id']
        item_p['merchant_id']=default_v['merchant_id']
        item_p['merchant_name']=default_v['merchant_name']
        item_p['size_id']=default_v['size_id']
        item_p['color_id']=default_v['color_id']
        item_p['extra_photo_sequence_id']=default_v.get('extra_photo_sequence_id',None)

        yield item_p
        variants = info['commerce_product_info']['variations']
        for variant in variants:
            sku = WishSkuNewItem()
            sku['source_id'] = info['id']
            sku['color'] = variant.get('color', None)
            sku['size'] = variant.get('size', None)
            sku['enabled'] = variant['enabled']
            sku['variantId'] = variant['variation_id']
            sku['price'] = Decimal(variant['price']).quantize(Decimal('.01'))
            sku['msrp'] = Decimal(variant.get('retail_price', 0)).quantize(Decimal('.01'))
            sku['shippingPrice'] = Decimal(variant.get('shipping', 0)).quantize(Decimal('.01'))
            extra_photo_sequence_id=variant.get('extra_photo_sequence_id',0)
            sku['extra_photo_sequence_id']=extra_photo_sequence_id
            sku['main_image'] = extra_photo_urls.get(str(extra_photo_sequence_id),None)
            sku['create_time'] = info['generation_time']
            yield sku
