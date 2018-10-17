# -*- coding:UTF-8 -*-

import scrapy, json, time
from urllib.parse import urlsplit
from decimal import Decimal
from fetch.models import ItemSkuLog, JoomStore,ItemUrl
from items import JoomFetchItem
import requests
import redis, pickle
from scrapy_redis.spiders import RedisSpider

client = redis.StrictRedis('122.226.65.250',18003)


class JoomSpider(RedisSpider):
    name = "joom"
    handle_httpstatus_list = [404, 400, 401, 429, 500]


    def start_requests(self):
        self.get_authorization()
        return super().start_requests()

    def make_request_from_data(self, data):
        item_url = pickle.loads(data)
        source_id = urlsplit(item_url).path.split('/')[-1]
        url = 'https://api.joom.com/1.1/products/%s?currency=USD&language=en-US' % source_id
        return scrapy.Request(url, headers=self.headers, meta={'item_url': item_url, 'source_id': source_id},
                             callback=self.parse,dont_filter=True)

    def get_authorization(self):
        authorization = client.get('joom_authorization')
        if not authorization:

            init_url = "https://www.joom.com/tokens/init"
            r = requests.post(init_url, verify=False)
            if r.status_code == 200:
                authorization = r.json()["payload"]["accessToken"]
                headers = {
                    'Authorization': "Bearer %s" % authorization,
                    'X-API-Token': '0NQPzyCD1fALL4IjrNyvR84C9ewCcUkk'
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
            client.delete('joom_authorization')
            self.get_authorization()
            ItemUrl.objects.filter(url_str=item_url).update(state=3)
            return
        elif response.status > 200:
            # 处理url状态
            ItemUrl.objects.filter(url_str=item_url).update(state=3)
            return

        r = json.loads(response.body)['payload']

        review_url = 'https://api.joom.com/1.1/products/%s/reviews/filters?currency=USD&language=en-US' % source_id

        yield scrapy.Request(review_url, headers=self.headers, callback=self.item_handle,
                             meta={'r': r, 'item_url': item_url},dont_filter=True)

    def item_handle(self, response):
        item_url = response.meta.get('item_url')
        r = response.meta.get('r')
        item = JoomFetchItem()
        item['storeId'] = r.get('storeId', None)
        item['tags'] = r.get('tags', None)
        item['goods_name'] = r['name']
        item['price'] = r['lite']['price']
        item['msrp'] = r['lite'].get('msrPrice', 0)
        item['default_img'] = r['mainImage']['images'][-1]['url']
        item['list_img'] = '|'.join(
            [gallery['payload']['images'][-1]['url'] if 'images' in gallery['payload'] else '' for gallery in
             r['gallery']])
        item['introduce'] = r['description']
        item['cate'] = r['category']['name'] if 'category' in r else 'Catalog'
        item['source_id'] = r['id']
        item['url'] = 'https://www.joom.com/en/products/' + item['source_id']
        item['create_time'] = int(time.time())
        item['average_score'] = r['lite'].get("rating", 0)

        # 处理与保存sku 信息
        if r.get('variants', ''):
            for variant in r['variants']:
                sku_log = ItemSkuLog()
                if "colors" in variant:
                    sku_log.color = variant['colors'][0]['name']
                sku_log.size = variant.get('size', '')
                sku_log.price = variant['price']
                sku_log.msrp = variant.get('msrPrice', Decimal(0.00))
                if 'mainImage' in variant:
                    sku_log.main_image = variant['mainImage']['images'][-1]['url']
                sku_log.source_id = variant['productId']
                sku_log.variantId = variant['id']
                sku_log.inStock = variant['inStock']
                sku_log.createdTimeMs = variant['createdTimeMs']
                sku_log.publishedTimeMs = variant['publishedTimeMs']
                sku_log.shippingPrice = variant['shipping'].get('price', None)
                sku_log.shippingWeight = variant.get('shippingWeight', None)
                sku_log.create_time = int(time.time())
                sku_log.save()

        if r.get('store', None):
            store_data = r['store']
            storeId = store_data.get('id')
            if not JoomStore.objects.filter(storeId=storeId).exists():
                store = JoomStore()
                store.storeId = store_data.get('id')
                store.updatedTimeMerchantMs = store_data.get('updatedTimeMerchantMs', None)
                store.enabled = store_data.get('enabled', None)
                store.rating = store_data.get('rating', None)
                store.name = store_data.get('name', None)
                positiveReviewsCount = store_data.get('positiveReviewsCount', None)
                favoritesCount = store_data.get('favoritesCount', None)
                productsCount = store_data.get('productsCount', None)
                reviewsCount = store_data.get('reviewsCount', None)
                store.positiveReviewsCount = positiveReviewsCount['value'] if positiveReviewsCount else None
                store.favoritesCount = favoritesCount['value'] if favoritesCount else None
                store.productsCount = productsCount['value'] if productsCount else None
                store.reviewsCount = reviewsCount['value'] if reviewsCount else None
                store.save()

        # 处理星数
        reviews = json.loads(response.text)['payload']
        if 'items' in reviews:
            review_items = reviews['items']
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

        # 处理url状态
        ItemUrl.objects.filter(url_str=item_url).update(state=2)

        yield item
