# -*- coding:UTF-8 -*-
import pymongo, os, sys, django, datetime

mg = pymongo.MongoClient('122.226.65.250', 18017)
db = mg.wish_api
collection = db.shop3

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
os.environ['DJANGO_SETTINGS_MODULE'] = 'joom_scrapy.settings'
django.setup()

from fetch.models import WishCrawlProduct,WishVariantItem

for post in collection.find({}):
    # 保存产品
    product = WishCrawlProduct()
    product.goods_name = post['name']
    product.sale_num = post['number_sold']
    product.default_img = post.get('main_image', None)
    product.list_img = post.get('extra_images', None)
    product.introduce = post['description']
    product.source_id = post['id']
    product.url = 'https://www.wish.com/product/' + post['id']
    product.date_uploaded = datetime.datetime.strptime(post['date_uploaded'], '%m-%d-%Y')
    product.last_updated = datetime.datetime.strptime(post['last_updated'], '%m-%d-%YT%H:%M:%S')
    product.tags = post['tags']
    product.is_promoted = post['is_promoted']
    product.review_status = post['review_status']
    product.parent_sku = post['parent_sku']
    product.number_saves = post['number_saves']
    product.shop_id = post['shop_id']
    product.save()

    # variants = post['variants']
    # # 保存变体信息
    # for v in variants:
    #     variant=v['Variant']
    #     item = WishVariantItem()
    #     item.source_id=variant['product_id']
    #     item.color =variant.get('color',None)
    #     item.size = variant.get('size',None)
    #     item.price = variant['price']
    #     item.enabled=variant['enabled']
    #     item.all_images=variant['all_images']
    #     item.sku = variant['sku']
    #     item.variantId=variant['id']
    #     item.msrp = variant['msrp']
    #     item.shippingPrice=variant['shipping']
    #     item.shipping_time=variant['shipping_time']
    #     item.save()

mg.close()