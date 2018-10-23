# -*- coding: utf-8 -*-
import scrapy
import re, json, requests, datetime,time
from redis import StrictRedis
from json.decoder import JSONDecodeError
from scrapy_redis.utils import bytes_to_str
from scrapy_redis.spiders import RedisSpider
from fetch.models import Shop
from items import WishProductItem, WishSkuItem

client = StrictRedis('122.226.65.250', 18003)
import pymongo

mg = pymongo.MongoClient('122.226.65.250', 18017)
db = mg.wish_api
collection = db.shop3


class WishApiSpider(RedisSpider):
    name = 'wish_api'
    handle_httpstatus_list = [400]

    def make_request_from_data(self, data):
        merge_data = bytes_to_str(data)
        pk, authorization = merge_data.split('+')
        headers = {
            'Authorization': "Bearer %s" % authorization
        }
        return scrapy.Request('https://merchant.wish.com/api/v2/product/multi-get?start=0&limit=50&show_rejected=true',
                              callback=self.parse,
                              headers=headers, dont_filter=True, meta={'pk': pk})

    def parse(self, response):
        pk = int(response.meta['pk'])
        if response.status > 300:
            Shop.objects.filter(pk=pk).update(status=3)
            return
        try:
            r = json.loads(response.body)
        except JSONDecodeError:
            start = re.match('.*start=(.+?)&', response.url).group(1)
            return [
                scrapy.Request(
                    'https://merchant.wish.com/api/v2/product/multi-get?start=%s&limit=25&show_rejected=true' % start,
                    callback=self.parse, headers=response.request.headers, dont_filter=True,
                    meta=response.meta)]
        data = r.get('data')

        for product in data:
            info = product['Product']
            yield self.handle_product(info, pk)

            # if info['number_sold']:
            #     yield scrapy.FormRequest('https://www.wish.com/api/product-ratings/get',callback=self.item_handle,
            #                              formdata={"product_id": info['id'], "start": "0", "count": "1"},
            #                              headers={"X-XSRFToken": "2|a31a81d1|ecdbaffd4321ee34cec80bea937c1dc4|1539501583"},
            #                              cookies={"_xsrf": "2|a31a81d1|ecdbaffd4321ee34cec80bea937c1dc4|1539501583"},
            #                              dont_filter=True, meta={'dont_retry': True, 'info': info,'pk':pk})
            # else:

        next_page = r['paging'].get('next', '')
        if next_page:
            url = re.sub('(?<=limit=)\d+', '50', next_page)
            yield scrapy.Request(url, callback=self.parse, headers=response.request.headers, dont_filter=True,meta=response.meta)

        else:
            Shop.objects.filter(pk=pk).update(status=2)

    def item_handle(self, response):
        info = response.meta['info']
        pk = response.meta['pk']
        res = json.loads(response.body)
        data = res['data']
        item_p = self.handle_product(info,pk)
        if data:
            rate_data=data['product_info']
            item_p['average_score'] = rate_data['rating']
            if "rating_spread" in rate_data:
                rating_spread=rate_data["rating_spread"]
                item_p['score1'] = rating_spread.get('star_one_rating_count',0)
                item_p['score2'] = rating_spread.get('star_two_rating_count',0)
                item_p['score3'] = rating_spread.get('star_three_rating_count',0)
                item_p['score4'] = rating_spread.get('star_four_rating_count',0)
                item_p['score5'] = rating_spread.get('star_five_rating_count',0)

        return item_p

    def handle_product(self,info,pk):
        item_p = WishProductItem()
        item_p['goods_name'] = info['name']
        item_p['sale_num'] = info['number_sold']
        item_p['default_img'] = info.get('main_image', None)
        item_p['list_img'] = info.get('extra_images', None)
        item_p['introduce'] = info['description']
        item_p['source_id'] = info['id']
        item_p['url'] = 'https://www.wish.com/product/' + info['id']
        item_p['date_uploaded'] = datetime.datetime.strptime(info['date_uploaded'], '%m-%d-%Y')
        item_p['last_updated'] = datetime.datetime.strptime(info['last_updated'], '%m-%d-%YT%H:%M:%S')
        item_p['tags'] = info['tags']
        item_p['parent_sku'] = info['parent_sku']
        item_p['is_promoted'] = info['is_promoted']
        item_p['review_status'] = info['review_status']
        item_p['number_saves'] = info['number_saves']
        item_p['shop_id'] = pk
        item_p['create_time'] = int(time.time())
        variants = info['variants']

        for v in variants:
            variant = v['Variant']
            sku = WishSkuItem()
            sku['source_id'] = info['id']
            sku['color'] = variant.get('color', None)
            sku['size'] = variant.get('size', None)
            sku['price'] = variant['price']
            sku['enabled'] = variant['enabled']
            sku['all_images'] = variant['all_images']
            sku['sku'] = variant['sku']
            sku['variantId'] = variant['id']
            sku['msrp'] = variant['msrp']
            sku['shippingPrice'] = variant.get('shipping',0)
            sku['shipping_time'] = variant['shipping_time']
            sku['create_time'] = int(time.time())
            sku.save()
        min_variant = min(variants, key=lambda x: float(x['Variant']['price']))
        item_p['price'] = min_variant['Variant']['price']
        item_p['msrp'] = min_variant['Variant'].get('msrp', 0)
        return item_p
