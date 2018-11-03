# -*- coding:UTF-8 -*-
import os,sys
import redis
import django


sys.path.append(os.path.dirname(os.path.dirname(__file__)))
os.environ['DJANGO_SETTINGS_MODULE']='joom_scrapy.settings'
django.setup()
from fetch.models import ItemUrl,WishShop,Shop,WishNewProduct

client = redis.StrictRedis('122.226.65.250',18003)

#
# ItemUrl.objects.filter(state=0).update(state=1)
# for item in ItemUrl.objects.filter(state=1).values('url_str'):
#     client.lpush('joom:start_urls',item['url_str'])
WishShop.objects.filter(state__lt=3).update(state=1)
for url in WishShop.objects.filter(state=1).values('url'):
    client.lpush('wish_new_list:start_urls',url['url'])
#
# Shop.objects.filter(platform_id=9,status__lt=3).update(status=1)
# for token in Shop.objects.filter(platform_id=9,status=1).values('access_token','id'):
#     client.lpush('wish_api:start_urls', '%s+%s' %(token['id'],token['access_token']))


# for wish_product in WishNewProduct.objects.all():
#     client.lpush('wish_product_info:start_urls',wish_product.product_id)

# y=set([x['shop_id'] for x in WishShop.objects.values('shop_id')])
# print(y)