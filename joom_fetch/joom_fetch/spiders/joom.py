# -*- coding:UTF-8 -*-

import scrapy, json, time
from urllib.parse import urlsplit
from decimal import Decimal
from fetch.models import ItemUrl
from joom_fetch.items import JoomProductItem,JoomSkuItem,JoomStoreItem
import requests
import redis
from scrapy_redis.utils import bytes_to_str
from scrapy_redis.spiders import RedisSpider
from django.utils.crypto import get_random_string

client = redis.StrictRedis('122.226.65.250',18003)


class JoomSpider(RedisSpider):
    name = "joom"
    handle_httpstatus_list = [404, 400, 401, 429, 500]

    def start_requests(self):
        self.get_authorization()
        return super().start_requests()

    def make_request_from_data(self, data):
        item_url = bytes_to_str(data)
        source_id = urlsplit(item_url).path.split('/')[-1]
        url = 'https://api.joom.com/1.1/products/%s?currency=USD&language=en-US' % source_id
        return scrapy.Request(url, headers=self.headers, meta={'item_url': item_url, 'source_id': source_id},
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
        item_url = response.meta.get('item_url')
        source_id = response.meta.get('source_id')
        # 处理非200返回

        if response.status == 401:
            self.get_authorization(not_valid=True)
            return [response.request]
        elif response.status > 200:
            # 处理url状态
            ItemUrl.objects.filter(url_str=item_url).update(state=3)
            return

        r = json.loads(response.body)['payload']
        if r['id'] != source_id:
            self.get_authorization(not_valid=True)
            return [response.request]

        review_url = 'https://api.joom.com/1.1/products/%s/reviews/filters?currency=USD&language=en-US' % source_id

        return scrapy.Request(review_url, headers=self.headers, callback=self.item_handle,
                             meta={'r': r, 'item_url': item_url},dont_filter=True)

    def item_handle(self, response):
        item_url = response.meta.get('item_url')
        # r是产品信息返回的json
        r = response.meta.get('r')
        reviews_data=json.loads(response.body)['payload']
        return self.make_item(r,reviews_data,JoomProductItem,JoomSkuItem,state_change_class=ItemUrl,state_change_arg='url_str',state_change_value=item_url)


    @classmethod
    def make_item(cls,r,reviews_data,ProductItemClass,SkuItemClass,state_change_class=None,state_change_arg=None,state_change_value=None):
        """
        :param r: 产品信息返回的json数据
        :param reviews_data: 评价信息返回的json数据
        """
        item = ProductItemClass()

        item['goods_name'] = r['name']
        item['price'] = Decimal(r['lite']['price']).quantize(Decimal('.01'))
        item['msrp'] = Decimal(r['lite'].get('msrPrice', 0)).quantize(Decimal('.01'))
        item['default_img'] = r['mainImage']['images'][-1]['url']
        item['list_img'] = '|'.join(
            [gallery['payload']['images'][-1]['url'] if 'images' in gallery['payload'] else '' for gallery in
             r['gallery']])
        item['introduce'] = r['description']
        item['average_score'] = Decimal(r['lite'].get("rating", 0)).quantize(Decimal('.1'))
        item['cate'] = r['category']['name'] if 'category' in r else 'Catalog'
        item['source_id'] = r['id']
        item['url'] = 'https://www.joom.com/en/products/' + r['id']
        item['create_time'] = int(time.time())
        item['storeId'] = r.get('storeId', None)
        item['tags'] ='|'.join([tag['nameEng'] for tag in (r['nameExt']['tags'] if "nameExt" in r and "tags" in r['nameExt'] else [])])
        item['categoryId']=r.get('categoryId','')
        item['dangerousKind']=r.get('dangerousKind','')
        variants = r['variants']
        min_time_variant = min(variants, key=lambda x: ['createdTimeMs'])
        item['date_uploaded']= int(min_time_variant['createdTimeMs']/1000)

        # 处理与保存sku 信息
        for variant in r['variants']:
            sku_log = SkuItemClass()
            if "colors" in variant:
                sku_log['color'] = variant['colors'][0]['name']
            sku_log['size'] = variant.get('size', '')
            # sku_log['price']= Decimal(variant['price']).quantize(Decimal('.01'))
            sku_log['price']= Decimal(variant['price']).quantize(Decimal('.01'))
            sku_log['msrp'] = Decimal(variant.get('msrPrice',0)).quantize(Decimal('.01'))
            if 'mainImage' in variant:
                sku_log['main_image'] = variant['mainImage']['images'][-1]['url']
            sku_log['source_id'] = variant['productId']
            sku_log['variantId'] = variant['id']
            sku_log['inStock'] = variant['inStock']
            sku_log['createdTimeMs'] = variant['createdTimeMs']
            sku_log['publishedTimeMs'] = variant['publishedTimeMs']
            sku_log['shippingPrice'] = Decimal(variant['shipping'].get('price', 0)).quantize(Decimal('.01'))
            sku_log['shippingWeight'] =Decimal(variant.get('shippingWeight', 0)).quantize(Decimal('.01'))
            sku_log['create_time'] = int(time.time())
            sku_log['status']=1
            yield sku_log

        # 暂停采集店铺信息
        '''
        store_data = r['store']
        store = JoomStoreItem()
        store['storeId'] = store_data.get('id')
        store['updatedTimeMerchantMs'] = store_data.get('updatedTimeMerchantMs', None)
        store['enabled'] = store_data.get('enabled', None)
        store['rating'] = store_data.get('rating', None)
        store['name'] = store_data.get('name', None)
        positiveReviewsCount = store_data.get('positiveReviewsCount', None)
        favoritesCount = store_data.get('favoritesCount', None)
        productsCount = store_data.get('productsCount', None)
        reviewsCount = store_data.get('reviewsCount', None)
        store['positiveReviewsCount'] = positiveReviewsCount['value'] if positiveReviewsCount else None
        store['favoritesCount'] = favoritesCount['value'] if favoritesCount else None
        store['productsCount'] = productsCount['value'] if productsCount else None
        store['reviewsCount'] = reviewsCount['value'] if reviewsCount else None
        yield store
        '''

        # 处理星数
        if 'items' in reviews_data:
            review_items = reviews_data['items']
            star_match = {
                "fiveStars": 5,
                "fourStars": 4,
                "threeStars": 3,
                "twoStars": 2,
                "oneStar": 1
            }
            # 求得所有星数和所有人数
            for review_item in review_items:
                if review_item['id'] in star_match:
                    star_int = star_match[review_item['id']]
                    index = 'score%s' % star_int
                    item[index] = review_item['count']['value']
        if state_change_class:
            # 处理url_状态
            state_change_class.objects.filter(**{state_change_arg:state_change_value}).update(state=2)
        yield item

